"""
EcoLoop AI - Decision-Making Orchestrator Agent
Coordinates multi-agent workflows, enforces safety boundaries,
synthesizes agent outputs into lifecycle decisions, and provides an explainable decision trace.
"""

import time
from datetime import datetime
from typing import List, Dict, Any

from models.battery import (
    BatteryInput,
    ValidationResult,
    HealthAssessment,
    SecondLifeEvaluation,
    SustainabilityMetrics,
    DecisionStep,
    OrchestrationResult,
)
from agents.base import BaseAgent
from agents.validation_agent import DataValidationAgent
from agents.health_agent import BatteryHealthAnalysisAgent
from agents.second_life_agent import SecondLifeRecommendationAgent
from agents.recycling_agent import RecyclingSustainabilityAgent


class DecisionMakingOrchestrator(BaseAgent):
    """
    Autonomous orchestrator that dispatches sub-agents in a sequential pipeline,
    dynamically activates recommendation paths based on health outcomes,
    and generates an explainable decision trace.
    """

    def __init__(self):
        super().__init__(
            name="Decision-Making Orchestrator Agent",
            role="Agentic Pipeline Coordination, Policy Enforcement & Life-Cycle Arbitration"
        )
        self.validation_agent = DataValidationAgent()
        self.health_agent = BatteryHealthAnalysisAgent()
        self.second_life_agent = SecondLifeRecommendationAgent()
        self.recycling_agent = RecyclingSustainabilityAgent()

    def process(self, battery: BatteryInput) -> OrchestrationResult:
        pipeline_start = time.perf_counter()
        trace: List[DecisionStep] = []
        pipeline_stages: List[str] = []
        reasoning_factors: List[str] = []

        now_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # STAGE 1: Data Validation & Safety Screening
        pipeline_stages.append("Data Validation Agent")
        trace.append(
            DecisionStep(
                step_number=1,
                agent_name="Data Validation Agent",
                action="Telemetry Ingestion & Safety Screening",
                reasoning=f"Validating {battery.battery_id}: SoH={battery.state_of_health_pct}%, Temp={battery.operating_temp_c}°C, Condition='{battery.physical_condition}'",
                rule_applied="Rule-VAL-01: Check physical integrity, delta voltages, and thermal thresholds",
                timestamp=now_str
            )
        )

        validation_res: ValidationResult = self.validation_agent.process(battery)

        # STAGE 2: Battery Health Analysis Agent
        pipeline_stages.append("Battery Health Analysis Agent")
        health_res: HealthAssessment = self.health_agent.process(battery)

        trace.append(
            DecisionStep(
                step_number=2,
                agent_name="Battery Health Analysis Agent",
                action="Electro-Chemical Degradation Modeling",
                reasoning=f"Computed Condition='{health_res.condition_rating}', Estimated RUL={health_res.estimated_rul_cycles} cycles (~{health_res.estimated_rul_years} yrs), IR Health='{health_res.internal_resistance_health}'",
                rule_applied="Rule-HLT-04: Project degradation trajectories & identify cell imbalance",
                timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
            )
        )

        # STAGE 3: Orchestrator Arbitration & Dynamic Branching
        final_decision: str = ""
        decision_summary: str = ""
        confidence_pct: int = 90
        second_life_res = None
        recycling_res = None

        # Check safety override first
        if validation_res.safety_override or health_res.condition_rating == "Critical Safety Hazard":
            final_decision = "INSPECT_OR_REPAIR"
            confidence_pct = 96
            pipeline_stages.append("Recycling & Sustainability Agent")
            recycling_res = self.recycling_agent.process(battery, health_res)

            reasoning_factors.extend([
                f"SAFETY CRITICAL: Physical condition '{battery.physical_condition}' or extreme thermal/voltage anomaly detected.",
                "Second-life repurposing strictly disqualified to prevent thermal runaway hazard.",
                "Mandatory professional disassembly inspection before authorized recycling facility transfer."
            ])

            decision_summary = (
                f"Battery {battery.battery_id} exhibits critical safety hazard indicators. "
                "Immediate isolation and qualified laboratory inspection required. Repurposing is prohibited."
            )

            trace.append(
                DecisionStep(
                    step_number=3,
                    agent_name="Decision-Making Orchestrator",
                    action="Safety Policy Enforcement",
                    reasoning="Physical/thermal threshold violated. Diverting away from Second-Life Agent directly to Hazardous Inspection & Materials Recovery.",
                    rule_applied="Rule-ORC-CRITICAL: Safety-First Mandate overrides standard repurposing",
                    timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
                )
            )

        elif health_res.state_of_health_pct >= 82.0 and not health_res.flag_professional_inspection:
            final_decision = "CONTINUE_EV"
            confidence_pct = 93
            reasoning_factors.extend([
                f"High State of Health ({health_res.state_of_health_pct}%) remains well within automotive operational envelope.",
                f"Low degradation index ({health_res.degradation_rate_index}) and balanced cells ({battery.cell_voltage_delta_v:.3f}V delta).",
                "Retaining battery in vehicle or remanufacturing for Certified Pre-Owned EV avoids premature life-cycle termination."
            ])
            decision_summary = (
                f"Battery {battery.battery_id} is healthy ({health_res.state_of_health_pct}% SoH). "
                "Continue automotive operation. Premature removal would lead to unnecessary life-cycle waste."
            )

            trace.append(
                DecisionStep(
                    step_number=3,
                    agent_name="Decision-Making Orchestrator",
                    action="Automotive Retention Assessment",
                    reasoning="SoH exceeds 82% threshold with zero anomalous flags. Recommending automotive continuation.",
                    rule_applied="Rule-ORC-RETAIN: Automotive retention prioritized over secondary cascade",
                    timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
                )
            )

        elif 62.0 <= health_res.state_of_health_pct < 82.0:
            final_decision = "EVALUATE_SECOND_LIFE"
            confidence_pct = 92
            pipeline_stages.append("Second-Life Recommendation Agent")
            pipeline_stages.append("Recycling & Sustainability Agent")

            second_life_res = self.second_life_agent.process(battery, health_res)
            recycling_res = self.recycling_agent.process(battery, health_res)

            reasoning_factors.extend([
                f"Battery capacity ({health_res.state_of_health_pct}% SoH) is retired from primary EV service, but possesses strong secondary utility.",
                f"Stable electrochemical baseline provides ~{health_res.estimated_rul_years} years of additional stationary service life.",
                "Repurposing for stationary storage delays recycling and maximizes lifecycle resource efficiency."
            ])

            top_app = second_life_res.recommended_applications[0].application_name if second_life_res.recommended_applications else "Stationary Storage"
            decision_summary = (
                f"Battery {battery.battery_id} is ideal for second-life repurposing ({health_res.state_of_health_pct}% SoH). "
                f"Top recommended secondary application: {top_app}."
            )

            trace.append(
                DecisionStep(
                    step_number=3,
                    agent_name="Decision-Making Orchestrator",
                    action="Second-Life Pathway Routing",
                    reasoning=f"SoH is within 62-82% sweet spot. Routing to Second-Life Agent for application matching and Recycling Agent for circular baseline.",
                    rule_applied="Rule-ORC-2ND-LIFE: Repurpose retired automotive packs before recycling",
                    timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
                )
            )

        else:
            # Below 62% SoH
            final_decision = "RECYCLE_NOW"
            confidence_pct = 94
            pipeline_stages.append("Recycling & Sustainability Agent")
            recycling_res = self.recycling_agent.process(battery, health_res)

            reasoning_factors.extend([
                f"State of Health ({health_res.state_of_health_pct}%) is below the viable threshold (62%) for safe secondary commercial storage.",
                "Elevated internal resistance reduces efficiency and increases thermal burden in stationary setups.",
                "Direct hydrometallurgical recycling optimizes recovery of critical materials (Lithium, Nickel, Cobalt, Graphite)."
            ])

            decision_summary = (
                f"Battery {battery.battery_id} has reached end-of-service degradation ({health_res.state_of_health_pct}% SoH). "
                "Immediate routing to authorized closed-loop recycling facility is recommended."
            )

            trace.append(
                DecisionStep(
                    step_number=3,
                    agent_name="Decision-Making Orchestrator",
                    action="Closed-Loop Recycling Allocation",
                    reasoning="SoH below 62% threshold. Secondary economics non-viable. Triggering full material recovery routing.",
                    rule_applied="Rule-ORC-RECYCLE: Direct cathode mineral recovery for depleted packs",
                    timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
                )
            )

        # Final Synthesis Step
        trace.append(
            DecisionStep(
                step_number=len(trace) + 1,
                agent_name="Decision-Making Orchestrator",
                action="Consolidated Lifecycle Recommendation",
                reasoning=f"Synthesized inputs across {len(pipeline_stages)} agents. Assigned decision '{final_decision}' with {confidence_pct}% confidence.",
                rule_applied="Rule-ORC-SYNTHESIS: Multi-agent consensus with explainability audit",
                timestamp=datetime.now().strftime("%H:%M:%S.%f")[:-3]
            )
        )

        total_elapsed_ms = round((time.perf_counter() - pipeline_start) * 1000.0, 2)
        self.last_execution_ms = total_elapsed_ms

        safety_disclaimer = (
            "NOTICE: EcoLoop AI recommendations are advisory guidance based on deterministic agent decision heuristics. "
            "They do NOT replace certified physical and electrical laboratory testing (e.g., UL 1974, IEC 62619). "
            "No battery may be commissioned into second-life service without certified professional inspection."
        )

        return OrchestrationResult(
            battery_id=battery.battery_id,
            final_lifecycle_decision=final_decision,
            decision_summary=decision_summary,
            confidence_score_pct=confidence_pct,
            reasoning_factors=reasoning_factors,
            safety_disclaimer=safety_disclaimer,
            is_simulated_ai=True,
            ai_logic_type="Deterministic Multi-Agent Rule Engine with Simulated Reasoning Trace",
            execution_pipeline=pipeline_stages,
            decision_trace=trace,
            validation_agent_result=validation_res,
            health_agent_result=health_res,
            second_life_agent_result=second_life_res,
            recycling_agent_result=recycling_res,
            total_execution_time_ms=total_elapsed_ms
        )
