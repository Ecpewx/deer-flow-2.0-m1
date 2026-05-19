import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { AgentThreadState } from "@/core/threads";

function formatConfidence(confidence: number | undefined) {
  if (typeof confidence !== "number" || Number.isNaN(confidence)) {
    return null;
  }
  return `${Math.round(confidence * 100)}%`;
}

export function ExplicitPlanningPanel({
  values,
}: {
  values?: AgentThreadState;
}) {
  if (!values) return null;
  
  const intentCard = values.intent_card;
  const conversationState = values.conversation_state;
  const actionDecision = values.action_decision;

  if (!intentCard && !conversationState && !actionDecision) {
    return null;
  }

  const confidence = formatConfidence(intentCard?.confidence);
  const primaryIntent = intentCard?.primary_intent || "unknown";
  const dialogueRelation = intentCard?.dialogue_relation;

  return (
    <div className="mx-auto w-full max-w-(--container-width-md) px-4 pt-4 md:px-0">
      <Card className="gap-4 border-dashed bg-muted/30 py-4">
        <CardHeader className="px-4 pb-0 md:px-5">
          <CardTitle className="text-sm">Explicit Planning Context</CardTitle>
          <CardDescription>
            Live intent analysis injected before the lead agent responds.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 px-4 text-sm md:grid-cols-3 md:px-5">
          <section className="space-y-2">
            <div className="text-muted-foreground text-xs font-medium uppercase">
              Intent
            </div>
            <div className="flex flex-wrap gap-2">
              <Badge variant={primaryIntent === "unknown" ? "outline" : "secondary"}>
                {primaryIntent}
              </Badge>
              {dialogueRelation ? (
                <Badge variant="outline">{dialogueRelation}</Badge>
              ) : null}
              {confidence ? <Badge variant="outline">{confidence}</Badge> : null}
            </div>
            <p className="text-foreground/90 leading-6">
              {intentCard?.user_goal || "No user goal extracted yet."}
            </p>
          </section>

          <section className="space-y-2">
            <div className="text-muted-foreground text-xs font-medium uppercase">
              Conversation State
            </div>
            <div className="flex flex-wrap gap-2">
              {conversationState?.stage ? (
                <Badge variant="secondary">{conversationState.stage}</Badge>
              ) : (
                <Badge variant="outline">no stage</Badge>
              )}
              {typeof conversationState?.turn_count === "number" ? (
                <Badge variant="outline">
                  turn {conversationState.turn_count}
                </Badge>
              ) : null}
            </div>
            <p className="text-foreground/90 leading-6">
              {conversationState?.last_user_goal ||
                "No rolling conversation goal yet."}
            </p>
          </section>

          <section className="space-y-2">
            <div className="text-muted-foreground text-xs font-medium uppercase">
              Action Decision
            </div>
            <div className="flex flex-wrap gap-2">
              {actionDecision?.action ? (
                <Badge>{actionDecision.action}</Badge>
              ) : (
                <Badge variant="outline">no action</Badge>
              )}
            </div>
            <p className="text-foreground/90 leading-6">
              {actionDecision?.reason || "No decision reason available yet."}
            </p>
          </section>
        </CardContent>
      </Card>
    </div>
  );
}
