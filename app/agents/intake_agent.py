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

        system_prompt = """
You are an insurance claim intake agent.

Your task is to extract factual information from the customer's message
and populate the provided CustomerData schema.

Extraction rules:
- Extract only information explicitly stated by the customer.
- Never invent, assume, or infer missing information.
- If a field is not explicitly mentioned, return null.
- Preserve the customer's meaning.
- Preserve dates exactly as stated.
- Do not convert relative dates into absolute dates.
- Extract estimated claim amounts only when explicitly stated.
- Identify hospitalization only when explicitly supported by the message.
- Extract hospital name, diagnosis, and treatment only when explicitly mentioned.
"""

        user_prompt = f"""
Customer message:

{message}
"""
        customer_data = await structured_llm.ainvoke([
            ("system", system_prompt),
            ("human", user_prompt),
        ])
        #customer_data = await structured_llm.ainvoke(prompt)

        return {
            **state,
            "customer_data": customer_data.model_dump(),
            "status": "RECEIVED"
        }