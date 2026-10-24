"""
EcoLoop AI - Unit Tests for Multi-Agent Workflow
Tests individual agent logic, safety boundary enforcement, and orchestrator decisions.
"""

import pytest
from models.battery import BatteryInput
from agents.validation_agent import DataValidationAgent
from agents.health_agent import BatteryHealthAnalysisAgent
from agents.second_life_agent import SecondLifeRecommendationAgent
from agents.recycling_agent import RecyclingSustainabilityAgent
from agents.orchestrator import DecisionMakingOrchestrator


@pytest.fixture
def healthy_battery():
    return BatteryInput(
        battery_id="TEST-HEALTHY-01",
        model_name="NMC-622 EV Test Pack",
        pack_capacity_kwh=80.0,
        current_capacity_kwh=72.0,
        state_of_health_pct=90.0,
        nominal_voltage_v=400.0,
        current_voltage_v=395.0,
        operating_temp_c=22.0,
        cycle_count=350,
        internal_resistance_mohm=12.0,
        cell_voltage_delta_v=0.010,
        physical_condition="Normal",
        battery_weight_kg=450.0,
        chemistry="NMC-622"
    )


@pytest.fixture
def second_life_candidate():
    return BatteryInput(
        battery_id="TEST-SECOND-LIFE-02",
        model_name="NMC-811 Repurposing Candidate",
        pack_capacity_kwh=75.0,
        current_capacity_kwh=57.0,
        state_of_health_pct=76.0,
        nominal_voltage_v=360.0,
        current_voltage_v=352.0,
        operating_temp_c=24.0,
        cycle_count=1400,
        internal_resistance_mohm=18.0,
        cell_voltage_delta_v=0.020,
        physical_condition="Normal",
        battery_weight_kg=440.0,
        chemistry="NMC-811"
    )


@pytest.fixture
def hazardous_battery():
    return BatteryInput(
        battery_id="TEST-HAZARD-03",
        model_name="Damaged Cell Pack",
        pack_capacity_kwh=60.0,
        current_capacity_kwh=40.0,
        state_of_health_pct=66.0,
        nominal_voltage_v=360.0,
        current_voltage_v=330.0,
        operating_temp_c=55.0,  # Critical temp
        cycle_count=1900,
        internal_resistance_mohm=70.0,  # Critical IR
        cell_voltage_delta_v=0.150,  # Critical delta
        physical_condition="Swelling",  # Hazard
        battery_weight_kg=400.0,
        chemistry="NMC-622"
    )


def test_data_validation_agent_flags_hazard(hazardous_battery):
    agent = DataValidationAgent()
    result = agent.process(hazardous_battery)
    assert result.safety_override is True
    assert result.is_valid is False
    assert any(issue.severity == "critical" for issue in result.issues)


def test_health_agent_estimates_rul(second_life_candidate):
    agent = BatteryHealthAnalysisAgent()
    assessment = agent.process(second_life_candidate)
    assert assessment.condition_rating in ["Good", "Moderate Degradation"]
    assert assessment.estimated_rul_cycles > 0
    assert assessment.estimated_rul_years > 0.0


def test_second_life_agent_qualifies_candidate(second_life_candidate):
    health_agent = BatteryHealthAnalysisAgent()
    health = health_agent.process(second_life_candidate)
    sl_agent = SecondLifeRecommendationAgent()
    eval_res = sl_agent.process(second_life_candidate, health)
    assert eval_res.eligible_for_second_life is True
    assert len(eval_res.recommended_applications) > 0
    assert eval_res.overall_suitability_score > 60


def test_orchestrator_routes_hazard_to_inspect(hazardous_battery):
    orchestrator = DecisionMakingOrchestrator()
    result = orchestrator.process(hazardous_battery)
    assert result.final_lifecycle_decision == "INSPECT_OR_REPAIR"
    assert "SAFETY CRITICAL" in result.reasoning_factors[0]
    assert len(result.decision_trace) >= 3


def test_orchestrator_routes_second_life(second_life_candidate):
    orchestrator = DecisionMakingOrchestrator()
    result = orchestrator.process(second_life_candidate)
    assert result.final_lifecycle_decision == "EVALUATE_SECOND_LIFE"
    assert result.second_life_agent_result is not None
    assert result.second_life_agent_result.eligible_for_second_life is True


def test_orchestrator_routes_healthy_ev(healthy_battery):
    orchestrator = DecisionMakingOrchestrator()
    result = orchestrator.process(healthy_battery)
    assert result.final_lifecycle_decision == "CONTINUE_EV"
