from core.event_bus import bus
from agents.orchestrator import Orchestrator


def handle_pr_opened(payload: dict):
    print(f"[Hook] PR abierto: #{payload['number']} — {payload['title']}")
    results = Orchestrator().run(payload)
    bus.publish("review.complete", {
        "pr_number": payload["number"],
        "results": results,
    })


bus.subscribe("pr.opened", handle_pr_opened)
