"""Task complexity classification for routing between subagents."""

from enum import Enum


class TaskComplexity(Enum):
    """Complexity level of a task, used to select the appropriate subagent.

    Attributes:
        LIGHTWEIGHT: Simple, quick tasks that require few tool calls or minimal reasoning.
        GENERAL_PURPOSE: Complex, multi-step tasks requiring deep reasoning or heavy context usage.
    """

    LIGHTWEIGHT = "lightweight"
    GENERAL_PURPOSE = "general-purpose"


# Keywords that suggest a lightweight, quick task
_LIGHTWEIGHT_KEYWORDS = frozenset(
    {
        "what is",
        "what's",
        "who is",
        "who's",
        "when is",
        "when was",
        "where is",
        "define",
        "definition",
        "list",
        "show",
        "print",
        "echo",
        "lookup",
        "look up",
        "check",
        "get",
        "fetch",
        "find",
        "search",
        "count",
        "calculate",
        "compute",
        "convert",
        "translate",
        "summarize",
        "format",
        "rename",
        "move",
        "copy",
        "delete",
        "remove",
        "hello",
        "hi",
        "help",
        "ping",
        "status",
        "version",
    }
)

# Keywords that suggest a complex, multi-step task
_COMPLEX_KEYWORDS = frozenset(
    {
        "analyze",
        "analysis",
        "research",
        "investigate",
        "implement",
        "build",
        "create",
        "develop",
        "design",
        "architect",
        "refactor",
        "optimize",
        "debug",
        "fix",
        "resolve",
        "migrate",
        "integrate",
        "deploy",
        "configure",
        "setup",
        "generate",
        "compare",
        "evaluate",
        "review",
        "audit",
        "report",
        "benchmark",
        "test",
        "automate",
        "orchestrate",
        "coordinate",
        "plan",
        "schedule",
        "monitor",
        "track",
        "comprehensive",
        "thorough",
        "detailed",
        "complete",
        "step by step",
        "step-by-step",
    }
)

# Threshold: tasks shorter than this word count are likely lightweight
_LIGHTWEIGHT_WORD_THRESHOLD = 8


def classify_task(text: str) -> TaskComplexity:
    """Classify a task description as lightweight or general-purpose.

    Uses simple heuristics based on word count and keyword matching to
    determine whether a task should be routed to a lightweight subagent
    or the full general-purpose subagent.

    Lightweight tasks are short, simple, and require few tool calls.
    General-purpose tasks are complex, multi-step, or research-heavy.

    Args:
        text: The task description to classify.

    Returns:
        `TaskComplexity.LIGHTWEIGHT` for simple tasks,
        `TaskComplexity.GENERAL_PURPOSE` for complex tasks.
    """
    normalized = text.lower().strip()
    words = normalized.split()
    word_count = len(words)
    word_set = set(words)

    # Check for complex keywords first — they take priority.
    # Multi-word phrases are checked via substring match; single words via set lookup.
    for keyword in _COMPLEX_KEYWORDS:
        if " " in keyword:
            if keyword in normalized:
                return TaskComplexity.GENERAL_PURPOSE
        elif keyword in word_set:
            return TaskComplexity.GENERAL_PURPOSE

    # Very long tasks are always general-purpose
    if word_count > _LIGHTWEIGHT_WORD_THRESHOLD * 3:
        return TaskComplexity.GENERAL_PURPOSE

    # Check for lightweight keywords (same approach: phrase vs. word)
    for keyword in _LIGHTWEIGHT_KEYWORDS:
        if " " in keyword:
            if keyword in normalized:
                return TaskComplexity.LIGHTWEIGHT
        elif keyword in word_set:
            return TaskComplexity.LIGHTWEIGHT

    # Short tasks without explicit complex keywords default to lightweight
    if word_count <= _LIGHTWEIGHT_WORD_THRESHOLD:
        return TaskComplexity.LIGHTWEIGHT

    return TaskComplexity.GENERAL_PURPOSE
