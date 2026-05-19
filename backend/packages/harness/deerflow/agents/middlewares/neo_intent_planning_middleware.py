import json
import logging
import re
from typing import Any, NotRequired, override

from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langgraph.runtime import Runtime
from pydantic import BaseModel, Field

from deerflow.models import create_chat_model

logger = logging.getLogger(__name__)

_INTENT_CONTEXT_MESSAGE_NAME = "intent_planning_context"


class IntentCardSchema(BaseModel):
    dialogue_relation: str = "unknown"
    primary_intent: str = "unknown"
    sub_intent: str = "unknown"
    needs_retrieval: bool = False
    needs_clarification: bool = False
    planning_mode: str = "none"
    user_goal: str = ""
    confidence: float = 0.0
    missing_slots: list[str] = Field(default_factory=list)
    slots: dict[str, Any] = Field(default_factory=dict)


class ConversationStateSchema(BaseModel):
    stage: str = "new"
    dialogue_relation: str = "unknown"
    active_intent: str = "unknown"
    last_user_goal: str = ""
    course_name: str = ""
    chapter: str = ""
    knowledge_points: list[str] = Field(default_factory=list)
    missing_slots: list[str] = Field(default_factory=list)
    turn_count: int = 0


class ActionDecisionSchema(BaseModel):
    action: str = "direct_answer"
    reason: str = ""


class IntentPlanningAnalysisSchema(BaseModel):
    intent_card: IntentCardSchema
    conversation_state: ConversationStateSchema
    action_decision: ActionDecisionSchema


class IntentPlanningMiddlewareState(AgentState):
    intent_card: NotRequired[dict | None]
    conversation_state: NotRequired[dict | None]
    action_decision: NotRequired[dict | None]


class IntentPlanningMiddleware(AgentMiddleware[IntentPlanningMiddlewareState]):
    state_schema = IntentPlanningMiddlewareState

    def _extract_text_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    text = item.get("text")
                    if isinstance(text, str):
                        parts.append(text)
            return "\n".join(part for part in parts if part).strip()

        if isinstance(content, dict):
            text = content.get("text")
            if isinstance(text, str):
                return text.strip()

        return ""


    def _get_last_user_message(self, state: IntentPlanningMiddlewareState) -> str | None:
        messages = state.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                text = self._extract_text_content(msg.content)
                if text:
                    return text
        return None

    def _get_last_user_message_meta(
        self,
        state: IntentPlanningMiddlewareState,
    ) -> tuple[str | None, str | None]:
        messages = state.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                text = self._extract_text_content(msg.content)
                if text:
                    return text, getattr(msg, "id", None)
        return None, None


    def _get_recent_history(self, state: IntentPlanningMiddlewareState, limit: int = 6) -> str:
        messages = state.get("messages", [])
        lines: list[str] = []
        for msg in messages[-limit:]:
            role = getattr(msg, "type", "unknown")
            content = msg.content if isinstance(getattr(msg, "content", None), str) else str(getattr(msg, "content", ""))
            lines.append(f"{role}: {content[:300]}")
        return "\n".join(lines)

    def _build_analysis_prompt(self, user_input: str, recent_history: str, old_conversation_state: dict) -> str:
        return f"""
            You are an intent recognition and task orchestration module for a university teaching and research assistant system.
            Your job is NOT to answer the user.
            Your job is to analyze the current user turn together with recent conversation history and the previous conversation state.
            Return JSON only. Do not output any explanation.

            You must return exactly this schema:
            {{
            "intent_card": {{
                "dialogue_relation": "continue_current_task | refine_current_task | switch_task | insert_question | unknown",
                "primary_intent": "knowledge_qa | learning_support | courseware_generation | courseware_revision | assessment_generation_objective | assessment_generation_subjective | grading_feedback | research_support | unknown",
                "sub_intent": "concept_explanation | concept_comparison | chapter_review | exam_prep | study_plan | error_analysis | style_revision | structure_revision | single_choice_generation | multiple_choice_generation | judgment_generation | short_answer_generation | essay_generation | case_analysis_generation | objective_grading | subjective_feedback | literature_qa | proposal_support | general | unknown",
                "needs_retrieval": true,
                "needs_clarification": false,
                "planning_mode": "none | single_step | multi_step",
                "user_goal": "string",
                "confidence": 0.0,
                "missing_slots": ["string"],
                "slots": {{
                "course_name": "string",
                "chapter": "string",
                "knowledge_points": ["string"],
                "question_type": "string",
                "difficulty": "string",
                "question_count": 0,
                "target_students": "string",
                "output_format": "string",
                "source_material_provided": false,
                "grading_standard_provided": false
                }}
            }},

            "conversation_state": {{
                "stage": "new | clarifying | executing | done",
                "dialogue_relation": "continue_current_task | refine_current_task | switch_task | insert_question | unknown",
                "active_intent": "string",
                "last_user_goal": "string",
                "course_name": "string",
                "chapter": "string",
                "knowledge_points": ["string"],
                "missing_slots": ["string"],
                "turn_count": 0
            }},

            "action_decision": {{
                "action": "direct_answer | clarify | retrieve_then_answer | run_skill | multi_step_plan",
                "reason": "string"
            }}
            }}

            Decision rules:
            1. If the current turn continues the previous unfinished task, use "continue_current_task".
            2. If the current turn refines the previous task by changing format, difficulty, quantity, or style, use "refine_current_task".
            3. If the current turn starts a clearly different task, use "switch_task".
            4. If the current turn temporarily inserts a side question but does not replace the active task, use "insert_question".
            5. Use needs_clarification=true only when required information is missing for safe execution.
            6. Use needs_retrieval=true when course materials, chapter content, uploaded files, or knowledge bases are likely needed.
            7. Use planning_mode=multi_step for courseware generation, grading, complex question generation, and research support tasks.
            8. In conversation_state, inherit reusable task fields from previous conversation_state when dialogue_relation is continue_current_task or refine_current_task.
            9. Do not answer the user request itself.

            Previous conversation_state: {json.dumps(old_conversation_state, ensure_ascii=False)}

            Recent conversation history: {recent_history}

            Current user input: {user_input}
            """.strip()

    def _response_to_text(self, response_content: Any) -> str:
        """Normalize model output into plain text before JSON extraction."""
        return self._extract_text_content(response_content)

    def _strip_code_fences(self, text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("```"):
            stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
            stripped = re.sub(r"\s*```$", "", stripped)
        return stripped.strip()

    def _extract_json_object_text(self, text: str) -> str:
        """Extract the first complete top-level JSON object from text."""
        start = text.find("{")
        if start == -1:
            raise ValueError("No JSON object start found in model response")

        depth = 0
        in_string = False
        escape = False

        for index in range(start, len(text)):
            char = text[index]

            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]

        raise ValueError("No complete JSON object found in model response")

    def _fallback_analysis(self, user_input: str, old_conversation_state: dict) -> dict:
        lowered = user_input.strip().lower()
        question_mark = "?" in user_input or "？" in user_input
        planning_keywords = ["生成", "创建", "制作", "整理", "设计", "ppt", "课件", "报告", "方案", "计划"]
        clarify_keywords = ["帮我做一下", "优化一下", "改一下", "处理一下", "弄一下"]

        if any(keyword in lowered for keyword in clarify_keywords):
            primary_intent = "unknown"
            planning_mode = "single_step"
            action = "clarify"
            stage = "clarifying"
            needs_clarification = True
            reason = "fallback heuristic detected vague request"
        elif any(keyword in lowered for keyword in planning_keywords):
            primary_intent = "courseware_generation" if "ppt" in lowered or "课件" in lowered else "learning_support"
            planning_mode = "multi_step"
            action = "multi_step_plan"
            stage = "executing"
            needs_clarification = False
            reason = "fallback heuristic detected planning-oriented request"
        elif question_mark or lowered.startswith(("什么", "为什么", "如何", "怎么", "what", "why", "how")):
            primary_intent = "knowledge_qa"
            planning_mode = "none"
            action = "direct_answer"
            stage = old_conversation_state.get("stage", "new")
            needs_clarification = False
            reason = "fallback heuristic detected question-answer request"
        else:
            primary_intent = "learning_support"
            planning_mode = "single_step"
            action = "direct_answer"
            stage = old_conversation_state.get("stage", "new")
            needs_clarification = False
            reason = "fallback defaulted to lightweight direct answer"

        return {
            "intent_card": {
                "dialogue_relation": old_conversation_state.get("dialogue_relation", "unknown"),
                "primary_intent": primary_intent,
                "sub_intent": "general",
                "needs_retrieval": False,
                "needs_clarification": needs_clarification,
                "planning_mode": planning_mode,
                "user_goal": user_input[:100],
                "confidence": 0.35,
                "missing_slots": [],
                "slots": {},
            },
            "conversation_state": {
                **old_conversation_state,
                "stage": stage,
                "dialogue_relation": old_conversation_state.get("dialogue_relation", "unknown"),
                "active_intent": primary_intent,
                "turn_count": old_conversation_state.get("turn_count", 0),
                "last_user_goal": user_input[:100],
            },
            "action_decision": {
                "action": action,
                "reason": reason,
            },
        }

    def _analyze_turn(self, user_input: str, recent_history: str, old_conversation_state: dict) -> dict:
        prompt = self._build_analysis_prompt(user_input, recent_history, old_conversation_state)
        try:
            model = create_chat_model(thinking_enabled=False)
            structured_model = model.with_structured_output(IntentPlanningAnalysisSchema)
            structured_response = structured_model.invoke(prompt)
            if isinstance(structured_response, IntentPlanningAnalysisSchema):
                data = structured_response.model_dump()
            elif hasattr(structured_response, "model_dump"):
                data = structured_response.model_dump()
            else:
                raise TypeError(f"Unexpected structured response type: {type(structured_response)!r}")
            logger.warning("[intent_planning] analyzer_success_structured data=%r", data)
            return data
        except Exception:
            logger.exception("Intent planning structured output failed, falling back to text JSON extraction")

        try:
            model = create_chat_model(thinking_enabled=False)
            response = model.invoke(prompt)
            raw_text = self._response_to_text(response.content)
            stripped_text = self._strip_code_fences(raw_text)
            json_text = self._extract_json_object_text(stripped_text)
            logger.warning(
                "[intent_planning] analyzer_raw raw_text=%r stripped_text=%r json_text=%r",
                raw_text,
                stripped_text,
                json_text,
            )
            data = json.loads(json_text)
            logger.warning("[intent_planning] analyzer_success data=%r", data)
            return data
        except Exception:
            logger.exception("Intent planning analysis failed, using fallback")
            fallback = self._fallback_analysis(user_input, old_conversation_state)
            logger.warning("[intent_planning] analyzer_fallback data=%r", fallback)
            return fallback

    async def _aanalyze_turn(self, user_input: str, recent_history: str, old_conversation_state: dict) -> dict:
        prompt = self._build_analysis_prompt(user_input, recent_history, old_conversation_state)
        try:
            model = create_chat_model(thinking_enabled=False)
            structured_model = model.with_structured_output(IntentPlanningAnalysisSchema)
            structured_response = await structured_model.ainvoke(prompt)
            if isinstance(structured_response, IntentPlanningAnalysisSchema):
                data = structured_response.model_dump()
            elif hasattr(structured_response, "model_dump"):
                data = structured_response.model_dump()
            else:
                raise TypeError(f"Unexpected structured response type: {type(structured_response)!r}")
            logger.warning("[intent_planning] analyzer_success_structured_async data=%r", data)
            return data
        except Exception:
            logger.exception("Intent planning structured async output failed, falling back to text JSON extraction")

        try:
            model = create_chat_model(thinking_enabled=False)
            response = await model.ainvoke(prompt)
            raw_text = self._response_to_text(response.content)
            stripped_text = self._strip_code_fences(raw_text)
            json_text = self._extract_json_object_text(stripped_text)
            logger.warning(
                "[intent_planning] analyzer_raw_async raw_text=%r stripped_text=%r json_text=%r",
                raw_text,
                stripped_text,
                json_text,
            )
            data = json.loads(json_text)
            logger.warning("[intent_planning] analyzer_success_async data=%r", data)
            return data
        except Exception:
            logger.exception("Intent planning async analysis failed, using fallback")
            fallback = self._fallback_analysis(user_input, old_conversation_state)
            logger.warning("[intent_planning] analyzer_fallback_async data=%r", fallback)
            return fallback

    def _build_intent_context_message(self, intent_card: dict, conversation_state: dict, action_decision: dict) -> SystemMessage:
        content = (
            "<intent_planning_context>\n"
            f"dialogue_relation: {intent_card.get('dialogue_relation', '')}\n"
            f"primary_intent: {intent_card.get('primary_intent', '')}\n"
            f"user_goal: {intent_card.get('user_goal', '')}\n"
            f"confidence: {intent_card.get('confidence', '')}\n\n"
            "<conversation_state>\n"
            f"{json.dumps(conversation_state, ensure_ascii=False, indent=2)}\n"
            "</conversation_state>\n\n"
            "<action_decision>\n"
            f"{json.dumps(action_decision, ensure_ascii=False, indent=2)}\n"
            "</action_decision>\n\n"
            "Use this as explicit control context for the current turn.\n"
            "</intent_planning_context>"
        )
        return SystemMessage(name=_INTENT_CONTEXT_MESSAGE_NAME, content=content)

    def _build_remove_old_context_ops(self, messages: list[Any]) -> list[RemoveMessage]:
        ops: list[RemoveMessage] = []
        for msg in messages:
            if (
                getattr(msg, "name", None) == _INTENT_CONTEXT_MESSAGE_NAME
                and getattr(msg, "id", None)
            ):
                ops.append(RemoveMessage(id=msg.id))
        return ops

    def _should_inject_context(self, intent_card: dict, action_decision: dict) -> bool:
        """Inject planning context only when it can genuinely steer the next turn.

        Simple Q&A should still update state for UI/debugging, but should not keep
        feeding an explicit planning block back into the lead agent.
        """
        action = str(action_decision.get("action") or "").strip().lower()
        primary_intent = str(intent_card.get("primary_intent") or "").strip().lower()
        planning_mode = str(intent_card.get("planning_mode") or "").strip().lower()
        needs_clarification = bool(intent_card.get("needs_clarification"))
        return (
            action in {"multi_step_plan"}
            or planning_mode in {"multi_step"}
        )

    def _is_new_user_turn(
        self,
        old_conversation_state: dict,
        *,
        user_input: str,
        user_message_id: str | None,
    ) -> bool:
        previous_message_id = old_conversation_state.get("_last_intent_planning_user_message_id")
        previous_input = old_conversation_state.get("_last_intent_planning_user_input")

        if user_message_id and previous_message_id:
            return user_message_id != previous_message_id

        if user_message_id and not previous_message_id:
            return True

        return user_input != previous_input

    def _finalize_conversation_state(
        self,
        conversation_state: dict,
        old_conversation_state: dict,
        *,
        user_input: str,
        user_message_id: str | None,
    ) -> dict:
        updated_turn_count = old_conversation_state.get("turn_count", 0) + 1
        finalized = {
            **old_conversation_state,
            **conversation_state,
            "turn_count": updated_turn_count,
            "last_user_goal": conversation_state.get("last_user_goal") or user_input[:100],
            "_last_intent_planning_user_input": user_input,
        }
        if user_message_id is not None:
            finalized["_last_intent_planning_user_message_id"] = user_message_id
        return finalized

    @override
    def before_model(self, state: IntentPlanningMiddlewareState, runtime: Runtime) -> dict | None:
        user_input, user_message_id = self._get_last_user_message_meta(state)
        if not user_input:
            logger.warning("[intent_planning] skipped: no user_input in state")
            return None

        messages = list(state.get("messages") or [])
        old_conversation_state = state.get("conversation_state") or {}
        recent_history = self._get_recent_history(state)
        thread_id = (runtime.context or {}).get("thread_id")
        is_new_user_turn = self._is_new_user_turn(
            old_conversation_state,
            user_input=user_input,
            user_message_id=user_message_id,
        )

        if not is_new_user_turn:
            logger.warning(
                "[intent_planning] skipped: same user turn thread_id=%r user_message_id=%r user_input=%r",
                thread_id,
                user_message_id,
                user_input,
            )
            return None

        logger.warning(
            "[intent_planning] start thread_id=%r user_input=%r user_message_id=%r old_conversation_state=%r recent_history=%r",
            thread_id,
            user_input,
            user_message_id,
            old_conversation_state,
            recent_history,
        )

        analysis = self._analyze_turn(
            user_input=user_input,
            recent_history=recent_history,
            old_conversation_state=old_conversation_state,
        )

        intent_card = analysis.get("intent_card", {})
        conversation_state = self._finalize_conversation_state(
            analysis.get("conversation_state", {}),
            old_conversation_state,
            user_input=user_input,
            user_message_id=user_message_id,
        )
        action_decision = analysis.get("action_decision", {})
        should_inject = self._should_inject_context(intent_card, action_decision)

        logger.warning(
            "[intent_planning] prepared thread_id=%r intent_card=%r conversation_state=%r action_decision=%r should_inject=%r",
            thread_id,
            intent_card,
            conversation_state,
            action_decision,
            should_inject,
        )

        remove_ops = self._build_remove_old_context_ops(messages)
        message_updates: list[RemoveMessage | SystemMessage] = list(remove_ops)

        if should_inject:
            message_updates.append(
                self._build_intent_context_message(
                    intent_card=intent_card,
                    conversation_state=conversation_state,
                    action_decision=action_decision,
                )
            )

        result: dict[str, Any] = {
            "intent_card": intent_card,
            "conversation_state": conversation_state,
            "action_decision": action_decision,
        }

        if message_updates:
            result["messages"] = message_updates

        logger.warning("[intent_planning] returning result=%r", result)
        return result

    @override
    async def abefore_model(self, state: IntentPlanningMiddlewareState, runtime: Runtime) -> dict | None:
        user_input, user_message_id = self._get_last_user_message_meta(state)
        if not user_input:
            logger.warning("[intent_planning] skipped_async: no user_input in state")
            return None

        messages = list(state.get("messages") or [])
        old_conversation_state = state.get("conversation_state") or {}
        recent_history = self._get_recent_history(state)
        thread_id = (runtime.context or {}).get("thread_id")
        is_new_user_turn = self._is_new_user_turn(
            old_conversation_state,
            user_input=user_input,
            user_message_id=user_message_id,
        )

        if not is_new_user_turn:
            logger.warning(
                "[intent_planning] skipped_async: same user turn thread_id=%r user_message_id=%r user_input=%r",
                thread_id,
                user_message_id,
                user_input,
            )
            return None

        logger.warning(
            "[intent_planning] start_async thread_id=%r user_input=%r user_message_id=%r old_conversation_state=%r recent_history=%r",
            thread_id,
            user_input,
            user_message_id,
            old_conversation_state,
            recent_history,
        )

        analysis = await self._aanalyze_turn(
            user_input=user_input,
            recent_history=recent_history,
            old_conversation_state=old_conversation_state,
        )

        intent_card = analysis.get("intent_card", {})
        conversation_state = self._finalize_conversation_state(
            analysis.get("conversation_state", {}),
            old_conversation_state,
            user_input=user_input,
            user_message_id=user_message_id,
        )
        action_decision = analysis.get("action_decision", {})
        should_inject = self._should_inject_context(intent_card, action_decision)

        logger.warning(
            "[intent_planning] prepared_async thread_id=%r intent_card=%r conversation_state=%r action_decision=%r should_inject=%r",
            thread_id,
            intent_card,
            conversation_state,
            action_decision,
            should_inject,
        )

        remove_ops = self._build_remove_old_context_ops(messages)
        message_updates: list[RemoveMessage | SystemMessage] = list(remove_ops)

        if should_inject:
            message_updates.append(
                self._build_intent_context_message(
                    intent_card=intent_card,
                    conversation_state=conversation_state,
                    action_decision=action_decision,
                )
            )

        result: dict[str, Any] = {
            "intent_card": intent_card,
            "conversation_state": conversation_state,
            "action_decision": action_decision,
        }

        if message_updates:
            result["messages"] = message_updates

        logger.warning("[intent_planning] returning_async result=%r", result)
        return result
