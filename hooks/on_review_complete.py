import os

from github import Github

from core.event_bus import bus


def handle_review_complete(payload: dict):
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ["GITHUB_REPO"])
    pr = repo.get_pull(payload["pr_number"])

    passed = payload["results"]["overall_passed"]
    summary = payload["results"]["summary"]
    icon = "\u2705" if passed else "\u274c"

    comment = f"## {icon} Revisión automática por IA\n\n{summary}"
    pr.create_issue_comment(comment)
    print(f"[Hook] Comentario publicado en PR #{payload['pr_number']}")


bus.subscribe("review.complete", handle_review_complete)
