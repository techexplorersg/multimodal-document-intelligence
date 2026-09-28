from app.review.document_router import (
    route_document,
)
from app.review.router import (
    ReviewDecision,
)
from app.validation.confidence import (
    ConfidencePolicy,
    FieldPrediction,
)


POLICY = ConfidencePolicy(
    auto_accept_threshold=0.90,
    review_threshold=0.70,
)


def test_high_confidence_document_auto_accepts():

    predictions = [
        FieldPrediction(
            "invoice_number",
            "INV-1001",
            0.98,
        ),
        FieldPrediction(
            "total",
            1250.00,
            0.96,
        ),
    ]

    decision = route_document(
        predictions,
        POLICY,
    )

    assert (
        decision.decision
        == ReviewDecision.AUTO_ACCEPT
    )


def test_uncertain_field_routes_to_review():

    predictions = [
        FieldPrediction(
            "invoice_number",
            "INV-1001",
            0.97,
        ),
        FieldPrediction(
            "total",
            1250.00,
            0.78,
        ),
    ]

    decision = route_document(
        predictions,
        POLICY,
    )

    assert (
        decision.decision
        == ReviewDecision.HUMAN_REVIEW
    )

    assert "total" in decision.review_fields


def test_low_confidence_field_rejects_document():

    predictions = [
        FieldPrediction(
            "invoice_number",
            "INV-1001",
            0.96,
        ),
        FieldPrediction(
            "total",
            None,
            0.40,
        ),
    ]

    decision = route_document(
        predictions,
        POLICY,
    )

    assert (
        decision.decision
        == ReviewDecision.REJECT
    )

    assert "total" in decision.rejected_fields
