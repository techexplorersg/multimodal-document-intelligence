from dataclasses import dataclass

from app.review.router import (
    ReviewDecision,
    route_prediction,
)
from app.validation.confidence import (
    ConfidencePolicy,
    FieldPrediction,
)


@dataclass(frozen=True)
class DocumentDecision:
    decision: ReviewDecision
    review_fields: tuple[str, ...]
    rejected_fields: tuple[str, ...]


def route_document(
    predictions: list[FieldPrediction],
    policy: ConfidencePolicy,
) -> DocumentDecision:

    review_fields = []
    rejected_fields = []

    for prediction in predictions:
        decision = route_prediction(
            prediction,
            policy,
        )

        if decision == ReviewDecision.HUMAN_REVIEW:
            review_fields.append(
                prediction.name
            )

        elif decision == ReviewDecision.REJECT:
            rejected_fields.append(
                prediction.name
            )

    if rejected_fields:
        overall = ReviewDecision.REJECT

    elif review_fields:
        overall = ReviewDecision.HUMAN_REVIEW

    else:
        overall = ReviewDecision.AUTO_ACCEPT

    return DocumentDecision(
        decision=overall,
        review_fields=tuple(review_fields),
        rejected_fields=tuple(rejected_fields),
    )
