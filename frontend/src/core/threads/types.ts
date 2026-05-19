import type { Message, Thread } from "@langchain/langgraph-sdk";

import type { Todo } from "../todos";

export interface IntentCard {
  dialogue_relation?: string;
  primary_intent?: string;
  sub_intent?: string;
  needs_retrieval?: boolean;
  needs_clarification?: boolean;
  planning_mode?: string;
  confidence?: number;
  user_goal?: string;
  missing_slots?: string[];
  slots?: Record<string, unknown>;
}

export interface ConversationState {
  stage?: string;
  dialogue_relation?: string;
  active_intent?: string;
  turn_count?: number;
  last_user_goal?: string;
  course_name?: string;
  chapter?: string;
  knowledge_points?: string[];
  missing_slots?: string[];
  _last_intent_planning_user_input?: string;
  _last_intent_planning_user_message_id?: string;
}

export interface ActionDecision {
  action?: string;
  reason?: string;
}

export interface AgentThreadState extends Record<string, unknown> {
  title: string;
  messages: Message[];
  artifacts: string[];
  todos?: Todo[];
  intent_card?: IntentCard;
  conversation_state?: ConversationState;
  action_decision?: ActionDecision;
}

export interface AgentThreadContext extends Record<string, unknown> {
  thread_id: string;
  model_name: string | undefined;
  thinking_enabled: boolean;
  is_plan_mode: boolean;
  subagent_enabled: boolean;
  reasoning_effort?: "minimal" | "low" | "medium" | "high";
  agent_name?: string;
}

export interface AgentThread extends Thread<AgentThreadState> {
  context?: AgentThreadContext;
}
