"""Tests for deepagents._task_model — task complexity classification."""

from deepagents._task_model import TaskComplexity, classify_task


class TestTaskComplexityEnum:
    """Tests for the TaskComplexity enum values."""

    def test_lightweight_value(self) -> None:
        assert TaskComplexity.LIGHTWEIGHT == "lightweight"

    def test_complex_value(self) -> None:
        assert TaskComplexity.COMPLEX == "complex"

    def test_is_string_subclass(self) -> None:
        assert isinstance(TaskComplexity.LIGHTWEIGHT, str)
        assert isinstance(TaskComplexity.COMPLEX, str)


class TestClassifyTask:
    """Tests for the classify_task heuristic function."""

    # --- lightweight indicators ---

    def test_browse_is_lightweight(self) -> None:
        assert classify_task("browse the project directory") == TaskComplexity.LIGHTWEIGHT

    def test_list_is_lightweight(self) -> None:
        assert classify_task("list all files in the src folder") == TaskComplexity.LIGHTWEIGHT

    def test_lookup_is_lightweight(self) -> None:
        assert classify_task("lookup the version metadata") == TaskComplexity.LIGHTWEIGHT

    def test_fetch_is_lightweight(self) -> None:
        assert classify_task("fetch the README file contents") == TaskComplexity.LIGHTWEIGHT

    def test_find_is_lightweight(self) -> None:
        assert classify_task("find the configuration file") == TaskComplexity.LIGHTWEIGHT

    def test_search_is_lightweight(self) -> None:
        assert classify_task("search for occurrences of TODO in the codebase") == TaskComplexity.LIGHTWEIGHT

    def test_read_is_lightweight(self) -> None:
        assert classify_task("read the pyproject.toml file") == TaskComplexity.LIGHTWEIGHT

    def test_locate_is_lightweight(self) -> None:
        assert classify_task("locate the test helper utilities") == TaskComplexity.LIGHTWEIGHT

    def test_check_is_lightweight(self) -> None:
        assert classify_task("check if the output directory exists") == TaskComplexity.LIGHTWEIGHT

    def test_inspect_is_lightweight(self) -> None:
        assert classify_task("inspect the current working directory") == TaskComplexity.LIGHTWEIGHT

    def test_view_is_lightweight(self) -> None:
        assert classify_task("view the contents of config.yaml") == TaskComplexity.LIGHTWEIGHT

    def test_metadata_is_lightweight(self) -> None:
        assert classify_task("retrieve the package metadata") == TaskComplexity.LIGHTWEIGHT

    # --- complex indicators ---

    def test_analyze_is_complex(self) -> None:
        assert classify_task("analyze the security vulnerabilities") == TaskComplexity.COMPLEX

    def test_write_is_complex(self) -> None:
        assert classify_task("write a unit test for the auth module") == TaskComplexity.COMPLEX

    def test_implement_is_complex(self) -> None:
        assert classify_task("implement a new caching layer") == TaskComplexity.COMPLEX

    def test_generate_is_complex(self) -> None:
        assert classify_task("generate a comprehensive report") == TaskComplexity.COMPLEX

    def test_debug_is_complex(self) -> None:
        assert classify_task("debug the failing integration test") == TaskComplexity.COMPLEX

    def test_refactor_is_complex(self) -> None:
        assert classify_task("refactor the data pipeline") == TaskComplexity.COMPLEX

    def test_design_is_complex(self) -> None:
        assert classify_task("design the new API schema") == TaskComplexity.COMPLEX

    def test_compare_is_complex(self) -> None:
        assert classify_task("compare the performance of two models") == TaskComplexity.COMPLEX

    def test_evaluate_is_complex(self) -> None:
        assert classify_task("evaluate the test coverage") == TaskComplexity.COMPLEX

    def test_synthesize_is_complex(self) -> None:
        assert classify_task("synthesize the research findings") == TaskComplexity.COMPLEX

    def test_create_is_complex(self) -> None:
        assert classify_task("create a new module for logging") == TaskComplexity.COMPLEX

    def test_reason_is_complex(self) -> None:
        assert classify_task("reason about the best approach") == TaskComplexity.COMPLEX

    # --- precedence: complex wins over lightweight ---

    def test_complex_wins_over_lightweight(self) -> None:
        # "analyze" (complex) + "find" (lightweight) → complex wins
        assert classify_task("analyze and find patterns in the data") == TaskComplexity.COMPLEX

    def test_complex_wins_when_both_present(self) -> None:
        assert classify_task("search for files and write a summary report") == TaskComplexity.COMPLEX

    # --- case insensitivity ---

    def test_case_insensitive_lightweight(self) -> None:
        assert classify_task("BROWSE the project") == TaskComplexity.LIGHTWEIGHT

    def test_case_insensitive_complex(self) -> None:
        assert classify_task("ANALYZE the codebase") == TaskComplexity.COMPLEX

    # --- ambiguous / unknown → falls back to complex ---

    def test_unknown_description_defaults_to_complex(self) -> None:
        assert classify_task("do something with the data") == TaskComplexity.COMPLEX

    def test_empty_string_defaults_to_complex(self) -> None:
        assert classify_task("") == TaskComplexity.COMPLEX
