from app.models.customer_data import CustomerData
from app.models.claim_state import ClaimState


class IntakeAgent:

    def __init__(self, llm=None):
        self.llm = llm

    async def process(
        self,
        state: ClaimState
    ) -> ClaimState:

        message = state.get("customer_message", "")

        if not message.strip():
            return {
                **state,
                "status": "INVALID",
                "customer_data": {}
            }

        # -----------------------------------------
        # Deterministic fallback for tests
        # -----------------------------------------

        if self.llm is None:
            customer_data = CustomerData(
                description=message
            )

            return {
                **state,
                "customer_data": customer_data.model_dump(),
                "status": "RECEIVED"
            }

        # -----------------------------------------
        # LLM structured extraction
        # -----------------------------------------

        structured_llm = self.llm.with_structured_output(
            CustomerData
        )

        prompt = f"""
You are an insurance claim intake agent.

Extract structured information from the customer's message.

Rules:
- Do not invent information.
- If a field is not mentioned, return null.
- Preserve the meaning of the customer's statement.
- Extract dates only when explicitly provided.
- Extract estimated claim amounts when explicitly provided.
- Identify whether hospitalization occurred.
- Return only the structured CustomerData fields.

Customer message:

{message}
"""

        customer_data = await structured_llm.ainvoke(prompt)

        return {
            **state,
            "customer_data": customer_data.model_dump(),
            "status": "RECEIVED"
        }