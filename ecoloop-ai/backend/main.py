"""
EcoLoop AI - FastAPI Backend Application
Exposes REST endpoints for the multi-agent battery lifecycle analysis pipeline.
"""

import json
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.battery import (
    BatteryInput,
    OrchestrationResult,
    ValidationResult,
    HealthAssessment,
    SecondLifeEvaluation,
    SustainabilityMetrics,
)
from agents.orchestrator import DecisionMakingOrchestrator
from agents.validation_agent import DataValidationAgent
from agents.health_agent import BatteryHealthAnalysisAgent
from agents.second_life_agent import SecondLifeRecommendationAgent
from agents.recycling_agent import RecyclingSustainabilityAgent

app = FastAPI(
    title="EcoLoop AI API",
    description="Agentic AI-powered autonomous EV battery waste prevention & lifecycle orchestration system.",
    version="1.0.0"
)

# Enable CORS for local development and deployed frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = DecisionMakingOrchestrator()
validation_agent = DataValidationAgent()
health_agent = BatteryHealthAnalysisAgent()
second_life_agent = SecondLifeRecommendationAgent()
recycling_agent = RecyclingSustainabilityAgent()

SCENARIOS_FILE = Path(__file__).parent / "data" / "sample_batteries.json"


@app.get("/")
def read_root():
    """System health and agent roster."""
    return {
        "system": "EcoLoop AI",
        "description": "Agentic AI-Powered Autonomous EV Battery Waste Prevention System",
        "status": "online",
        "version": "1.0.0",
        "active_agents": [
            {
                "name": orchestrator.name,
                "role": orchestrator.role,
                "type": "Orchestrator"
            },
            {
                "name": validation_agent.name,
                "role": validation_agent.role,
                "type": "Data Validation"
            },
            {
                "name": health_agent.name,
                "role": health_agent.role,
                "type": "Electro-Chemical Assessment"
            },
            {
                "name": second_life_agent.name,
                "role": second_life_agent.role,
                "type": "Secondary Application Matching"
            },
            {
                "name": recycling_agent.name,
                "role": recycling_agent.role,
                "type": "Circular Material Recovery"
            }
        ],
        "workflow": "Battery Data -> Validation Agent -> Health Agent -> Orchestrator -> (Second-Life Agent | Recycling Agent) -> Final Decision"
    }


@app.get("/api/health")
def health_check():
    """Simple ping endpoint for connectivity checks."""
    return {"status": "healthy", "service": "ecoloop-ai-backend"}


@app.get("/api/scenarios")
def get_sample_scenarios() -> List[Dict[str, Any]]:
    """Retrieve curated demo battery scenarios for immediate interactive testing."""
    if not SCENARIOS_FILE.exists():
        raise HTTPException(status_code=404, detail="Sample scenarios data file not found.")
    try:
        with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load scenarios: {str(e)}")


@app.post("/api/analyze", response_model=OrchestrationResult)
def analyze_battery(battery: BatteryInput) -> OrchestrationResult:
    """
    Executes the full autonomous multi-agent lifecycle decision pipeline.
    Coordinates validation, electrochemical degradation analysis, second-life evaluation,
    material recycling yield estimation, and explainable decision trace generation.
    """
    try:
        result = orchestrator.process(battery)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failure: {str(e)}")


@app.post("/api/validate", response_model=ValidationResult)
def run_validation_only(battery: BatteryInput) -> ValidationResult:
    """Run standalone data validation agent."""
    return validation_agent.process(battery)


@app.post("/api/health-analysis", response_model=HealthAssessment)
def run_health_only(battery: BatteryInput) -> HealthAssessment:
    """Run standalone battery health analysis agent."""
    return health_agent.process(battery)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
