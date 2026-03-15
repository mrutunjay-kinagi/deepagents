"""Task complexity classification for sub-agent model selection."""

from __future__ import annotations

from enum import StrEnum

# Keywords that signal a lightweight task (simple lookups, reads, browsing)
_LIGHTWEIGHT_KEYWORDS = frozenset(
    {
        "browse",
        "check",
        "directory",
        "fetch",
        "find",
        "inspect",
        "list",
        "locate",
        "lookup",
        "metadata",
        "read",
        "search",
        "view",
    }
)

# Keywords that signal a complex task (reasoning, generation, transformation)
_COMPLEX_KEYWORDS = frozenset(
    {
        "analyse",
        "analyze",
        "compare",
        "create",
        "cross-reference",
        "debug",
        "design",
        "evaluate",
        "generate",
        "implement",
        "reason",
        "refactor",
        "synthesize",
        "write",
    }
)


class TaskComplexity(StrEnum):
    """Classification of task complexity for sub-agent model selection.

    Used to route tasks to the appropriate sub-agent:

    - `LIGHTWEIGHT` tasks are routed to a cheaper, faster model.
    - `COMPLEX` tasks fall back to the full-power model.
    """

    LIGHTWEIGHT = "lightweight"
    """Simple, fast tasks: directory browsing, metadata lookups, file reads."""

    COMPLEX = "complex"
    """Multi-step tasks that require deep reasoning, code generation, or analysis."""


def classify_task(description: str) -> TaskComplexity:
    """Classify a task description as lightweight or complex.

    Uses keyword heuristics on the task description. Complex indicators take
    precedence over lightweight ones when both are present in the same description.

    If the description matches neither category, falls back to `TaskComplexity.COMPLEX`
    to ensure correctness over cost savings.

    Args:
        description: Natural-language description of the task to classify.

    Returns:
        `TaskComplexity.COMPLEX` if the task appears complex or ambiguous,
        `TaskComplexity.LIGHTWEIGHT` if it appears to be a simple operation.
    """
    lower = description.lower()
    if any(keyword in lower for keyword in _COMPLEX_KEYWORDS):
        return TaskComplexity.COMPLEX
    if any(keyword in lower for keyword in _LIGHTWEIGHT_KEYWORDS):
        return TaskComplexity.LIGHTWEIGHT
    return TaskComplexity.COMPLEX
