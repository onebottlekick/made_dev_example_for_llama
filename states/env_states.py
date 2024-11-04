from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EnvStates:
    modality: str = ""
    language: str = "python"

    product_backlog: List[str] = field(default_factory=list)
    product_acceptance_criteria: List[str] = field(default_factory=list)
    product_backlog_comments: str = ""

    all_sprint_backlog: List[str] = field(default_factory=list)
    all_sprint_goals: List[str] = field(default_factory=list)
    all_sprint_acceptance_criteria: List[str] = field(default_factory=list)
    current_sprint_backlog: str = ""
    current_sprint_goals: str = ""
    current_sprint_acceptance_criteria: str = ""
    num_sprints: int = 0

    raw_codes: str = ""
    codes: Dict[str, str] = field(default_factory=dict)
    review_comments: str = ""
    code_review_done: bool = False

    commands: List[str] = field(default_factory=list)
    test_reports: str = ""
    error_summary: str = ""

    done_works: List[str] = field(default_factory=list)
    undone_works: List[str] = field(default_factory=list)

    requirements: Dict[str, str] = field(default_factory=dict)
    manual: Dict[str, str] = field(default_factory=dict)