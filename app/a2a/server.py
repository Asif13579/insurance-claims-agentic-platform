from app.agents.document_intelligence_agent import DocumentIntelligenceAgent

from app.a2a.client import A2AClient

from app.agents.intake_agent import IntakeAgent
from app.agents.document_agent import DocumentAgent
from app.agents.consistency_agent import ConsistencyAgent
from app.agents.claim_agent import ClaimAgent
from app.agents.review_agent import ReviewAgent
from app.agents.decision_agent import DecisionAgent


def create_a2a_client():

    # agents = {
    #     "intake_agent": IntakeAgent(),
    #     "document_agent": DocumentAgent(),
    #     "consistency_agent": ConsistencyAgent(),
    #     "claim_agent": ClaimAgent(),
    #     "review_agent": ReviewAgent(),
    #     "decision_agent": DecisionAgent(),
    # }
    agents = {
        "intake_agent": IntakeAgent(),
        "document_agent": DocumentAgent(),
        "document_intelligence_agent": DocumentIntelligenceAgent(),
        "consistency_agent": ConsistencyAgent(),
        "claim_agent": ClaimAgent(),
        "review_agent": ReviewAgent(),
        "decision_agent": DecisionAgent(),
    }

    return A2AClient(agents)
