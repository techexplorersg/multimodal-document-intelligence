from dataclasses import dataclass


@dataclass(frozen=True)
class FieldPrediction:
    name: str
    value: str | float | int | None
    confidence: float


@dataclass(frozen=True)
class ConfidencePolicy:
    auto_accept_threshold: float = 0.90
    review_threshold: float = 0.70


def validate_confidence(
    prediction: FieldPrediction,
) -> None:
    if not 0.0 <= prediction.confidence <= 1.0:
        raise ValueError(
            f"Invalid confidence for {prediction.name}: "
            f"{prediction.confidence}"
        )
