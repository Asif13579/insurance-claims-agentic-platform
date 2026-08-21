from app.repositories.claim_repository import ClaimRepository


def test_create_and_get_claim(db):

    repository = ClaimRepository(db)

    claim = repository.create_claim(
        claim_id="CLM-REPO-001",
        customer_id="CUS-REPO-001",
        customer_message="Repository test claim",
    )

    assert claim.claim_id == "CLM-REPO-001"
    assert claim.customer_id == "CUS-REPO-001"
    assert claim.status == "RECEIVED"

    stored = repository.get_claim("CLM-REPO-001")

    assert stored is not None
    assert stored.claim_id == "CLM-REPO-001"
    assert stored.customer_id == "CUS-REPO-001"


def test_update_claim(db):

    repository = ClaimRepository(db)

    repository.create_claim(
        claim_id="CLM-REPO-002",
        customer_id="CUS-REPO-002",
        customer_message="Repository update test",
    )

    updated = repository.update_claim(
        claim_id="CLM-REPO-002",
        status="APPROVED",
        claim_complete=True,
        final_decision="APPROVE",
    )

    assert updated is not None
    assert updated.status == "APPROVED"
    assert updated.claim_complete == "true"
    assert updated.final_decision == "APPROVE"

    stored = repository.get_claim("CLM-REPO-002")

    assert stored.status == "APPROVED"
    assert stored.claim_complete == "true"
    assert stored.final_decision == "APPROVE"


def test_get_missing_claim_returns_none(db):

    repository = ClaimRepository(db)

    result = repository.get_claim(
        "CLM-DOES-NOT-EXIST"
    )

    assert result is None


def test_update_missing_claim_returns_none(db):

    repository = ClaimRepository(db)

    result = repository.update_claim(
        claim_id="CLM-DOES-NOT-EXIST",
        status="APPROVED",
        claim_complete=True,
        final_decision="APPROVE",
    )

    assert result is None


def test_duplicate_claim_id_raises_error(db):

    repository = ClaimRepository(db)

    repository.create_claim(
        claim_id="CLM-REPO-DUPLICATE",
        customer_id="CUS-REPO-001",
        customer_message="First claim",
    )

    from sqlalchemy.exc import IntegrityError

    try:
        repository.create_claim(
            claim_id="CLM-REPO-DUPLICATE",
            customer_id="CUS-REPO-002",
            customer_message="Duplicate claim",
        )
    except IntegrityError:
        db.rollback()
    else:
        raise AssertionError(
            "Expected IntegrityError for duplicate claim_id"
        )


def test_transaction_rolls_back_on_error(db):

    from sqlalchemy.exc import IntegrityError

    repository = ClaimRepository(db)

    repository.create_claim(
        claim_id="CLM-ROLLBACK-001",
        customer_id="CUS-ROLLBACK-001",
        customer_message="Original claim",
    )

    try:
        repository.create_claim(
            claim_id="CLM-ROLLBACK-001",
            customer_id="CUS-ROLLBACK-002",
            customer_message="Duplicate claim",
        )
    except IntegrityError:
        db.rollback()

    stored = repository.get_claim(
        "CLM-ROLLBACK-001"
    )

    assert stored is not None
    assert stored.customer_id == "CUS-ROLLBACK-001"