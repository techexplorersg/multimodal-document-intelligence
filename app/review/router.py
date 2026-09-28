from enum import Enum

from app.validation.confidence import (
    ConfidencePolicy,
    FieldPrediction,
    validate_confidence,
)


class ReviewDecision(str, Enum):
    AUTO_ACCEPT = "auto_accept"
    HUMAN_REVIEW = "human_review"
    REJECT = "reject"


def route_prediction(
    prediction: FieldPrediction,
    policy: ConfidencePolicy,
) -> ReviewDecision:

    validate_confidence(prediction)

    if prediction.confidence >= (
        policy.auto_accept_threshold
    ):
        return ReviewDecision.AUTO_ACCEPT

    if prediction.confidence >= (
        policy.review_threshold
    ):
        return ReviewDecision.HUMAN_REVIEW

    return ReviewDecision.REJECT
