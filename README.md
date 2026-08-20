# Insurance Claims Agentic Platform

An AI-powered insurance claims processing platform built with **FastAPI, LangGraph, and Agent-to-Agent (A2A) communication**.

The platform orchestrates multiple specialized agents to process an insurance claim from customer intake through document validation, document intelligence, consistency checking, claim assessment, review, and final decision.

---

## Project Status

### Implemented

- FastAPI REST API
- Claim lifecycle management
- Shared `ClaimState`
- SQLAlchemy repository/service layer
- Intake Agent
- Document Agent
- Document Intelligence Agent
- Consistency Agent
- Claim Agent
- Review Agent
- Decision Agent
- LangGraph workflow orchestration
- Conditional workflow routing
- A2A agent communication
- Automated unit and workflow tests

### In Progress

- Production-grade LLM intake
- Real PDF extraction
- OCR
- Image/document validation
- Advanced document classification
- LLM-based document extraction
- Customer/document consistency analysis
- Final adjuster-ready claim package

### Planned

- PostgreSQL production deployment
- Authentication and authorization
- Observability and tracing
- Docker
- CI/CD
- Production cloud deployment

---

# 1. Architecture

The platform follows an agentic workflow where each specialized agent performs one responsibility.

```text
                        ┌──────────────────┐
                        │    FastAPI API    │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │   Claim Service  │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │    LangGraph     │
                        │     Workflow     │
                        └────────┬─────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
        Intake Agent       Document Agent    Document Intelligence
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                                 ▼
                       Consistency Agent
                                 │
                     ┌───────────┴───────────┐
                     │                       │
                Consistent               Inconsistent
                     │                       │
                     ▼                       ▼
                Claim Agent            Review Agent
                     │                       │
                     └───────────┬───────────┘
                                 │
                                 ▼
                         Decision Agent
                                 │
                                 ▼
                           Final Result
