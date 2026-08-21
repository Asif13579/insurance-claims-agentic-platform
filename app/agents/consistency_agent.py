from app.models.claim_state import ClaimState
import time
from app.core.logging import get_logger
logger = get_logger("agent.consistency")

class ConsistencyAgent:

    REQUIRED_DOCUMENTS = {
        "police_report",
        "repair_estimate",
        "photo",
    }

    # Fields that should agree across documents
    CROSS_DOCUMENT_FIELDS = {
        "incident_date": "incident date",
        "incident_location": "incident location",
        "vehicle": "vehicle",
    }

    async def process(self, state: ClaimState) -> ClaimState:
        start = time.perf_counter()
        documents = state.get("documents", [])
        claim_id = state.get(
            "claim_id",
            "unknown",
        )

        logger.info(
            "claim_id=%s agent=consistency started",
            claim_id,
        )
        document_types = set()

        for document in documents:

            if isinstance(document, dict):
                document_type = document.get("document_type")
            else:
                document_type = getattr(
                    document,
                    "document_type",
                    None,
                )

            if document_type:
                document_types.add(document_type)

        issues = []

        # =================================================
        # 1. Missing required documents
        # =================================================

        missing = self.REQUIRED_DOCUMENTS - document_types

        if missing:
            issues.append(
                "Missing required documents: "
                f"{', '.join(sorted(missing))}"
            )

        # =================================================
        # 2. Unexpected documents
        # =================================================

        unexpected = document_types - self.REQUIRED_DOCUMENTS

        if unexpected:
            issues.append(
                "Unexpected document types: "
                f"{', '.join(sorted(unexpected))}"
            )

        # =================================================
        # 3. Invalid documents from DocumentAgent
        # =================================================

        invalid_documents = state.get(
            "invalid_documents",
            [],
        )

        for document in invalid_documents:

            filename = document.get(
                "filename",
                "",
            )

            reason = document.get(
                "reason",
                "Invalid document",
            )

            issues.append(
                f"{filename}: {reason}"
            )

        # =================================================
        # 4. Compare extracted document data
        # =================================================

        extracted_data = state.get(
            "extracted_data",
            {},
        )

        for field, label in self.CROSS_DOCUMENT_FIELDS.items():

            values = []

            for document_type, extraction in extracted_data.items():

                if not isinstance(extraction, dict):
                    continue

                value = extraction.get(field)

                # Ignore fields that were not extracted
                if value is None:
                    continue

                if isinstance(value, str) and not value.strip():
                    continue

                values.append(
                    (document_type, value)
                )

            # Nothing to compare
            if len(values) < 2:
                continue

            unique_values = {
                str(value).strip()
                for _, value in values
            }

            if len(unique_values) > 1:

                formatted_values = ", ".join(
                    f"{document_type}={value}"
                    for document_type, value in values
                )

                issues.append(
                    f"Conflicting {label}s: "
                    f"{formatted_values}"
                )

        # =================================================
        # 5. Compare customer intake data with documents
        # =================================================

        customer_data = state.get(
            "customer_data",
            {},
        )

        if isinstance(customer_data, dict):

            customer_document_fields = {
                "accident_date": "incident_date",
                "accident_location": "incident_location",
                "vehicle": "vehicle",
            }

            for customer_field, document_field in (
                customer_document_fields.items()
            ):

                customer_value = customer_data.get(
                    customer_field
                )

                if customer_value is None:
                    continue

                if (
                    isinstance(customer_value, str)
                    and not customer_value.strip()
                ):
                    continue

                for document_type, extraction in (
                    extracted_data.items()
                ):

                    if not isinstance(extraction, dict):
                        continue

                    document_value = extraction.get(
                        document_field
                    )

                    if document_value is None:
                        continue

                    if (
                        isinstance(document_value, str)
                        and not document_value.strip()
                    ):
                        continue

                    if str(customer_value).strip() != str(
                        document_value
                    ).strip():

                        issues.append(
                            f"Customer data conflicts with "
                            f"{document_type}: "
                            f"{customer_field}="
                            f"{customer_value}, "
                            f"{document_field}="
                            f"{document_value}"
                        )

        # =================================================
        # 6. Determine final consistency
        # =================================================

        consistent = len(issues) == 0

        reason = (
            "Claim documents and extracted information "
            "are consistent."
            if consistent
            else "; ".join(issues)
        )

        duration_ms = (
            time.perf_counter() - start
        ) * 1000

        logger.info(
            "claim_id=%s agent=consistency "
            "completed result=%s duration_ms=%.2f",
            claim_id,
            state.get("consistency_check"),
            duration_ms,
        )
        state["consistency_check"] = {
            "consistent": consistent,
            "issues": issues,
            "reason": reason,
        }

        return state