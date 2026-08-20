import pytest

from app.agents.intake_agent import IntakeAgent


@pytest.mark.asyncio
async def test_intake_agent_creates_customer_data():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1001",
        "customer_id": "CUST-1001",
        "customer_message": (
            "I was hospitalized after an accident."
        ),
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert "customer_data" in result

    assert (
        result["customer_data"]["description"]
        == "I was hospitalized after an accident."
    )

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.agents.intake_agent import IntakeAgent
from app.models.customer_data import CustomerData


@pytest.mark.asyncio
async def test_intake_agent_creates_customer_data():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1001",
        "customer_id": "CUST-1001",
        "customer_message": (
            "I was hospitalized after an accident."
        ),
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert "customer_data" in result

    assert (
        result["customer_data"]["description"]
        == "I was hospitalized after an accident."
    )


@pytest.mark.asyncio
async def test_intake_agent_extracts_structured_data_with_llm():

    structured_llm = MagicMock()

    structured_llm.ainvoke = AsyncMock(
        return_value=CustomerData(
            incident_type="vehicle_accident",
            incident_date="2026-08-15",
            incident_location="Bangalore",
            hospitalized=True,
            hospital_name="City Hospital",
            diagnosis="Fracture",
            treatment="Surgery",
            estimated_amount=50000,
            description="I had a car accident and was hospitalized."
        )
    )

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    agent = IntakeAgent(llm=llm)

    state = {
        "claim_id": "CLM-1002",
        "customer_id": "CUST-1002",
        "customer_message": (
            "I had a car accident on August 15 in Bangalore. "
            "I was hospitalized at City Hospital with a fracture "
            "and underwent surgery. The estimated cost is 50000."
        ),
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert result["status"] == "RECEIVED"

    assert result["customer_data"]["incident_type"] == "vehicle_accident"
    assert result["customer_data"]["incident_date"] == "2026-08-15"
    assert result["customer_data"]["incident_location"] == "Bangalore"
    assert result["customer_data"]["hospitalized"] is True
    assert result["customer_data"]["hospital_name"] == "City Hospital"
    assert result["customer_data"]["estimated_amount"] == 50000

    llm.with_structured_output.assert_called_once_with(
        CustomerData
    )

    structured_llm.ainvoke.assert_awaited_once()


@pytest.mark.asyncio
async def test_intake_agent_handles_empty_message():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1003",
        "customer_id": "CUST-1003",
        "customer_message": "",
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert result["status"] == "INVALID"
    assert result["customer_data"] == {}


@pytest.mark.asyncio
async def test_intake_agent_preserves_existing_state():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1004",
        "customer_id": "CUST-1004",
        "customer_message": "My car was damaged.",
        "status": "PROCESSING",
        "documents": [],
        "custom_field": "preserve-me",
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-1004"
    assert result["customer_id"] == "CUST-1004"
    assert result["documents"] == []
    assert result["custom_field"] == "preserve-me"


import pytest
from unittest.mock import AsyncMock, MagicMock

from app.agents.intake_agent import IntakeAgent
from app.models.customer_data import CustomerData


@pytest.mark.asyncio
async def test_intake_agent_creates_customer_data():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1001",
        "customer_id": "CUST-1001",
        "customer_message": (
            "I was hospitalized after an accident."
        ),
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert "customer_data" in result

    assert (
        result["customer_data"]["description"]
        == "I was hospitalized after an accident."
    )


@pytest.mark.asyncio
async def test_intake_agent_extracts_structured_data_with_llm():

    structured_llm = MagicMock()

    structured_llm.ainvoke = AsyncMock(
        return_value=CustomerData(
            incident_type="vehicle_accident",
            incident_date="2026-08-15",
            incident_location="Bangalore",
            hospitalized=True,
            hospital_name="City Hospital",
            diagnosis="Fracture",
            treatment="Surgery",
            estimated_amount=50000,
            description="I had a car accident and was hospitalized."
        )
    )

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    agent = IntakeAgent(llm=llm)

    state = {
        "claim_id": "CLM-1002",
        "customer_id": "CUST-1002",
        "customer_message": (
            "I had a car accident on August 15 in Bangalore. "
            "I was hospitalized at City Hospital with a fracture "
            "and underwent surgery. The estimated cost is 50000."
        ),
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert result["status"] == "RECEIVED"

    assert result["customer_data"]["incident_type"] == "vehicle_accident"
    assert result["customer_data"]["incident_date"] == "2026-08-15"
    assert result["customer_data"]["incident_location"] == "Bangalore"
    assert result["customer_data"]["hospitalized"] is True
    assert result["customer_data"]["hospital_name"] == "City Hospital"
    assert result["customer_data"]["estimated_amount"] == 50000

    llm.with_structured_output.assert_called_once_with(
        CustomerData
    )

    structured_llm.ainvoke.assert_awaited_once()


@pytest.mark.asyncio
async def test_intake_agent_handles_empty_message():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1003",
        "customer_id": "CUST-1003",
        "customer_message": "",
        "status": "PROCESSING"
    }

    result = await agent.process(state)

    assert result["status"] == "INVALID"
    assert result["customer_data"] == {}


@pytest.mark.asyncio
async def test_intake_agent_preserves_existing_state():

    agent = IntakeAgent()

    state = {
        "claim_id": "CLM-1004",
        "customer_id": "CUST-1004",
        "customer_message": "My car was damaged.",
        "status": "PROCESSING",
        "documents": [],
        "custom_field": "preserve-me",
    }

    result = await agent.process(state)

    assert result["claim_id"] == "CLM-1004"
    assert result["customer_id"] == "CUST-1004"
    assert result["documents"] == []
    assert result["custom_field"] == "preserve-me"


@pytest.mark.asyncio
async def test_intake_agent_preserves_unknown_fields_as_none():

    structured_llm = MagicMock()

    structured_llm.ainvoke = AsyncMock(
        return_value=CustomerData(
            incident_type="vehicle_accident",
            description="My car was damaged yesterday."
        )
    )

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    agent = IntakeAgent(llm=llm)

    state = {
        "claim_id": "CLM-1005",
        "customer_id": "CUST-1005",
        "customer_message": "My car was damaged yesterday.",
    }

    result = await agent.process(state)

    customer_data = result["customer_data"]

    assert customer_data["incident_type"] == "vehicle_accident"
    assert customer_data["description"] == "My car was damaged yesterday."

    assert customer_data["incident_location"] is None
    assert customer_data["hospitalized"] is None
    assert customer_data["hospital_name"] is None
    assert customer_data["diagnosis"] is None
    assert customer_data["treatment"] is None
    assert customer_data["estimated_amount"] is None


@pytest.mark.asyncio
async def test_intake_agent_does_not_invent_missing_information():

    structured_llm = MagicMock()

    structured_llm.ainvoke = AsyncMock(
        return_value=CustomerData(
            description="My car was damaged."
        )
    )

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    agent = IntakeAgent(llm=llm)

    state = {
        "claim_id": "CLM-1006",
        "customer_id": "CUST-1006",
        "customer_message": "My car was damaged.",
    }

    result = await agent.process(state)

    customer_data = result["customer_data"]

    assert customer_data["description"] == "My car was damaged."
    assert customer_data["incident_date"] is None
    assert customer_data["incident_location"] is None
    assert customer_data["estimated_amount"] is None
    assert customer_data["hospitalized"] is None


@pytest.mark.asyncio
async def test_intake_agent_extracts_structured_data_with_llm():

    structured_llm = MagicMock()

    structured_llm.ainvoke = AsyncMock(
        return_value=CustomerData(
            incident_type="vehicle_accident",
            incident_date="2026-08-15",
            incident_location="Bangalore",
            hospitalized=True,
            hospital_name="City Hospital",
            diagnosis="Fracture",
            treatment="Surgery",
            estimated_amount=50000,
            description="I had a car accident and was hospitalized."
        )
    )

    llm = MagicMock()
    llm.with_structured_output.return_value = structured_llm

    agent = IntakeAgent(llm=llm)

    state = {
        "claim_id": "CLM-1002",
        "customer_id": "CUST-1002",
        "customer_message": (
            "I had a car accident on August 15 in Bangalore. "
            "I was hospitalized at City Hospital with a fracture "
            "and underwent surgery. The estimated cost is 50000."
        ),
    }

    result = await agent.process(state)

    assert result["status"] == "RECEIVED"
    assert result["customer_data"]["hospitalized"] is True