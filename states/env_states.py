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
    num_sprints: int = 0

    raw_codes: str = ""
    codes: Dict[str, str] = field(default_factory=dict)
    review_comments: List[str] = field(default_factory=list)
    code_review_done: bool = False

    commands: List[str] = field(default_factory=list)
    test_reports: List[str] = field(default_factory=list)
    error_summary: List[str] = field(default_factory=list)

    done_works: List[str] = field(default_factory=list)
    undone_works: List[str] = field(default_factory=list)

    requirements: List[str] = field(default_factory=list)
    manual: str = ""