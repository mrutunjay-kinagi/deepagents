"""Unit tests for task complexity classification."""

import pytest

from deepagents._task_model import TaskComplexity, classify_task


class TestTaskComplexityEnum:
    """Tests for the TaskComplexity enum."""

    def test_lightweight_value(self) -> None:
        """TaskComplexity.LIGHTWEIGHT has the expected string value."""
        assert TaskComplexity.LIGHTWEIGHT.value == "lightweight"

    def test_general_purpose_value(self) -> None:
        """TaskComplexity.GENERAL_PURPOSE has the expected string value."""
        assert TaskComplexity.GENERAL_PURPOSE.value == "general-purpose"

    def test_enum_members(self) -> None:
        """TaskComplexity has exactly two members."""
        assert set(TaskComplexity) == {TaskComplexity.LIGHTWEIGHT, TaskComplexity.GENERAL_PURPOSE}


class TestClassifyTask:
    """Tests for the classify_task heuristic."""

    # --- Lightweight cases ---

    @pytest.mark.parametrize(
        "text",
        [
            "What is Python?",
            "Who is the president?",
            "List all files",
            "Check the status",
            "Get the version",
            "Hello",
            "Hi there",
            "Help",
            "Count the items",
            "Calculate 2 + 2",
            "Convert 5 kg to pounds",
            "Show me the current time",
            "Fetch the URL",
            "Find the file",
        ],
    )
    def test_lightweight_tasks(self, text: str) -> None:
        """Simple, short tasks are classified as lightweight."""
        assert classify_task(text) == TaskComplexity.LIGHTWEIGHT

    # --- General-purpose cases ---

    @pytest.mark.parametrize(
        "text",
        [
            "Analyze the entire codebase for security vulnerabilities",
            "Research the history of artificial intelligence and write a report",
            "Implement a new authentication system with OAuth2",
            "Build a REST API with rate limiting and caching",
            "Design a microservices architecture for the payment system",
            "Refactor the legacy codebase to use modern patterns",
            "Debug the intermittent production crash",
            "Migrate the database schema to support multi-tenancy",
            "Optimize the query performance for the analytics dashboard",
            "Deploy the application to Kubernetes with auto-scaling",
            "Generate a comprehensive test suite for the payment module",
            "Review the entire pull request for correctness and style",
            "Benchmark the different sorting algorithms and compare them",
            "Plan the sprint and schedule tasks for the team",
        ],
    )
    def test_general_purpose_tasks(self, text: str) -> None:
        """Complex, multi-step tasks are classified as general-purpose."""
        assert classify_task(text) == TaskComplexity.GENERAL_PURPOSE

    def test_empty_string(self) -> None:
        """An empty string is treated as a very short task (lightweight)."""
        result = classify_task("")
        assert result == TaskComplexity.LIGHTWEIGHT

    def test_whitespace_only(self) -> None:
        """A whitespace-only string is treated as lightweight."""
        result = classify_task("   ")
        assert result == TaskComplexity.LIGHTWEIGHT

    def test_case_insensitive(self) -> None:
        """Classification is case-insensitive."""
        lower_result = classify_task("analyze the data")
        upper_result = classify_task("ANALYZE the data")
        assert lower_result == TaskComplexity.GENERAL_PURPOSE
        assert upper_result == TaskComplexity.GENERAL_PURPOSE
        assert lower_result == upper_result

    def test_very_long_task_is_general_purpose(self) -> None:
        """Very long task descriptions default to general-purpose."""
        long_text = " ".join(["word"] * 50)
        assert classify_task(long_text) == TaskComplexity.GENERAL_PURPOSE

    def test_returns_task_complexity_instance(self) -> None:
        """classify_task always returns a TaskComplexity instance."""
        result = classify_task("some task")
        assert isinstance(result, TaskComplexity)
