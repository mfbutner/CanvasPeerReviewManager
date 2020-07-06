from typing import Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from student import Student


class PeerReview:
    def __init__(self, reviewer: "Student", reviewed: "Student",
                 overall_comments: Optional[List[str]] = None,
                 rubric_review: Optional[Dict] = None):
        self.reviewer = reviewer
        self.reviewed = reviewed
        self.overall_comments = overall_comments if overall_comments is not None else []
        self.rubric_review = rubric_review

    def __str__(self) -> str:
        representation = f'Reviewer: {self.reviewer}\n' \
                         f'\tReviewed: {self.reviewed}\n' \
                         f'\t\tOverall Comments\n' \
                         f'\t\t\t' + "\t\t\t\n".join(self.overall_comments) + '\n'

        if self.rubric_review is not None:
            for criteria_name, evaluation in self.rubric_review.items():
                representation += f'\t\tCriteria: {criteria_name}\n' \
                                  f'\t\t\tmax points: {evaluation["max_points"]}\n' \
                                  f'\t\t\tpoints: {evaluation["points"]}\n' \
                                  f'\t\t\tComments: {evaluation["comments"]}\n'
        return representation

    def __repr__(self):
        return str(self)
