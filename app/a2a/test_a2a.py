import asyncio

from app.a2a.server import create_a2a_client
from app.models.claim_state import ClaimState


async def process_claim(
    client,
    state: ClaimState
):

    print("\n[1] Calling intake_agent...")
    state = await client.send("intake_agent",state)
    print("\n[2] Calling document_agent...")
    state = await client.send("document_agent",state)
    print("\n[3] Calling consistency_agent...")
    state = await client.send("consistency_agent",state)
    print("\n[4] Calling claim_agent...")
    state = await client.send("claim_agent",state)

    return state


async def main():

    client = create_a2a_client()

    print("Registered Agents:")
    print(client.list_agents())

    request: ClaimState = {
        "claim_id": "CLM-1001",

        "customer_id": "CUST-1001",

        "customer_message": (
            "I was hospitalized and need to submit a medical claim."
        ),

        "documents": [
            {
                "filename": "medical_report.pdf",
                "document_type": "medical_report"
            },
            {
                "filename": "insurance_policy.pdf",
                "document_type": "insurance_policy"
            }
        ],

        "status": "RECEIVED"
    }

    result = await process_claim(
        client,
        request
    )

    print("\n==============================")
    print("FINAL CLAIM RESULT")
    print("==============================")

    print(result)


if __name__ == "__main__":
    asyncio.run(main())