# Insurance Claims Agentic Platform

An AI-powered insurance claims processing platform built with **FastAPI, LangGraph, PostgreSQL, and Agent-to-Agent (A2A) communication**.

The platform demonstrates an end-to-end agentic claims workflow in which specialized agents collaborate to process an insurance claim from intake through document validation, document intelligence, consistency analysis, claim assessment, review, and final decision.

The project is designed as a **working agentic platform prototype**, with deterministic document extraction available as a reliable fallback when an LLM/API key is not configured.

---

# Project Status

## Implemented

The core claims-processing platform is implemented and integrated end-to-end.

### API & Application

- FastAPI REST API
- Claim creation and retrieval
- Claim lifecycle management
- Request/response validation
- Authentication
- Structured application logging
- Service/repository architecture
- Duplicate claim protection

### Agentic Architecture

- Shared `ClaimState`
- Specialized agents with clear responsibilities
- Agent-to-Agent (A2A) communication layer
- LangGraph workflow orchestration
- Conditional workflow routing
- Review routing for inconsistent claims
- Final decision generation

### Specialized Agents

- **Intake Agent**
  - Processes initial claim information
  - Identifies customer/claim information
  - Determines document requirements

- **Document Agent**
  - Validates submitted documents
  - Identifies missing/invalid documents
  - Routes valid documents for further processing

- **Document Intelligence Agent**
  - Reads available document content
  - Performs deterministic structured extraction
  - Extracts fields such as:
    - incident date
    - incident location
    - vehicle
    - incident type
    - estimated amount
    - hospital information
    - diagnosis
    - treatment
  - Supports LLM-based extraction when configured
  - Uses deterministic fallback extraction when an LLM is unavailable

- **Consistency Agent**
  - Compares claim information and extracted document information
  - Identifies inconsistencies
  - Determines whether additional review is required

- **Claim Agent**
  - Assesses claim information
  - Produces claim-level assessment

- **Review Agent**
  - Handles claims requiring additional review
  - Provides a controlled review path before final decision

- **Decision Agent**
  - Produces the final claim decision
  - Supports outcomes such as approval, rejection, or review

### Persistence

- PostgreSQL
- SQLAlchemy
- Repository pattern
- Claim status persistence
- Final decision persistence
- Database migrations with Alembic

### Testing

The project has an automated test suite covering:

- Unit tests
- Agent tests
- Document extraction tests
- Workflow tests
- Routing tests
- API tests
- Database/service behavior
- End-to-end claim processing scenarios

Current test status:

```text
103 passed