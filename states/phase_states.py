from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PhaseStates:
    gui: str = ""
    modality: str = ""
    language: str = "python"

    product_backlog: str = ""
    product_acceptance_criteria: str = ""
    product_backlog_comments: str = ""

    current_sprint_backlog: str = ""
    current_sprint_goal: str = ""
    current_sprint_acceptance_criteria: str = ""
    num_sprints: int = 0

    raw_codes: str = ""
    codes: Dict[str, str] = field(default_factory=dict)
    workspace: str = ""
    review_comments: str = ""

    commands: List[str] = field(default_factory=list)
    test_reports: str = ""
    error_summary: str = ""

    done_works: List[str] = ""
    undone_works: List[str] = ""

    requirements: str = ""
    manual: str = ""
