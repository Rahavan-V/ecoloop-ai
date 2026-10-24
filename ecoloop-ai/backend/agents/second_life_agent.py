"""
EcoLoop AI - Second-Life Recommendation Agent
Evaluates battery suitability for stationary solar storage, backup UPS, and low-demand microgrids.
Provides transparent suitability scores, limitations, and safety requirements.
"""

import time
from typing import List
from models.battery import BatteryInput, HealthAssessment, SecondLifeEvaluation, ApplicationRecommendation
from agents.base import BaseAgent


class SecondLifeRecommendationAgent(BaseAgent):
    """
    Evaluates repurposing potential of degraded EV packs for stationary and light industrial roles.
    Adheres strictly to safety boundaries (never recommends damaged or critically degraded packs).
    """

    def __init__(self):
        super().__init__(
            name="Second-Life Recommendation Agent",
            role="Secondary Application Matching & Multi-Criteria Viability Scoring"
        )

    def process(self, battery: BatteryInput, health: HealthAssessment) -> SecondLifeEvaluation:
        start_time = time.perf_counter()
        soh = health.state_of_health_pct
        is_safe = (
            battery.physical_condition == "Normal" and
            not health.flag_professional_inspection and
            health.thermal_status in ["Normal", "Elevated"] and
            health.internal_resistance_health != "Dangerous"
        )

        recommendations: List[ApplicationRecommendation] = []
        non_viable: List[str] = []

        if not is_safe or soh < 55.0:
            # Not eligible for direct second life
            non_viable = [
                "Stationary Commercial Solar Microgrid Storage",
                "Residential Backup Power & UPS Systems",
                "Off-Grid Agricultural & Water Pumping Storage",
                "Light Industrial AGVs & Warehouse Forklifts"
            ]
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            self.last_execution_ms = round(elapsed_ms, 2)
            return SecondLifeEvaluation(
                battery_id=battery.battery_id,
                eligible_for_second_life=False,
                overall_suitability_score=0,
                recommended_applications=[],
                non_viable_applications=non_viable,
                economic_viability_rating="Ineligible due to Safety/Health Thresholds",
                agent_status="completed",
                execution_time_ms=self.last_execution_ms
            )

        # 1. Stationary Solar Energy Storage
        # Ideal SoH: 70% - 85%
        solar_score = int(min(98, max(40, soh * 1.15 - (battery.cell_voltage_delta_v * 200))))
        solar_tier = "Highly Recommended" if solar_score >= 80 else ("Suitable" if solar_score >= 65 else "Marginal")
        recommendations.append(
            ApplicationRecommendation(
                application_name="Stationary Solar Microgrid Storage",
                category="Grid & Renewables",
                suitability_score=solar_score,
                suitability_tier=solar_tier,
                confidence_level_pct=91,
                primary_advantages=[
                    "Low continuous C-rate discharge (0.2C - 0.5C) minimizes cell stress",
                    "Stationary thermal management keeps pack in ideal 20°C - 25°C window",
                    "Extends battery lifecycle by 5 to 8 years before recycling"
                ],
                technical_limitations=[
                    "Requires multi-string Battery Management System (BMS) with cell balancing",
                    "Lower volumetric energy density compared to brand new NMC cells"
                ],
                safety_requirements=[
                    "UL 1974 certified repurposing assessment",
                    "Fire suppression enclosure and thermal runaway mitigation barrier"
                ],
                estimated_lifespan_years=min(8.5, max(2.0, health.estimated_rul_years * 1.2))
            )
        )

        # 2. Residential Backup Power & UPS Systems
        # Ideal SoH: 65% - 80%
        ups_score = int(min(95, max(35, soh * 1.05 - (battery.internal_resistance_mohm * 0.4))))
        ups_tier = "Highly Recommended" if ups_score >= 80 else ("Suitable" if ups_score >= 60 else "Marginal")
        recommendations.append(
            ApplicationRecommendation(
                application_name="Residential Backup Power & Critical UPS",
                category="Resilience & Emergency Power",
                suitability_score=ups_score,
                suitability_tier=ups_tier,
                confidence_level_pct=88,
                primary_advantages=[
                    "Standby float operation involves infrequent cycling",
                    "Delivers high instantaneous emergency reliability without daily deep cycles",
                    "Cost savings of 40-60% vs newly manufactured home storage units"
                ],
                technical_limitations=[
                    "Requires certified high-voltage isolation inverter",
                    "Annual capacity recalibration mandatory"
                ],
                safety_requirements=[
                    "Outdoor or dedicated garage installation compliant with NFPA 855",
                    "Audible early thermal warning sensors"
                ],
                estimated_lifespan_years=min(10.0, max(3.0, health.estimated_rul_years * 1.4))
            )
        )

        # 3. Off-Grid Agricultural & Water Pumping Storage
        # Ideal SoH: 60% - 75%
        agri_score = int(min(90, max(30, soh * 0.95 - (battery.cycle_count * 0.005))))
        agri_tier = "Suitable" if agri_score >= 65 else "Marginal"
        recommendations.append(
            ApplicationRecommendation(
                application_name="Off-Grid Agricultural & Irrigation Storage",
                category="Rural & Agricultural Electrification",
                suitability_score=agri_score,
                suitability_tier=agri_tier,
                confidence_level_pct=84,
                primary_advantages=[
                    "Daytime solar charge buffer for night-time irrigation pumping",
                    "Decentralized energy access for remote farming installations",
                    "Tolerant of moderate capacity variance"
                ],
                technical_limitations=[
                    "Demands ruggedized ingress protection (IP65) against dust and moisture",
                    "Ambient outdoor temperature swings require active HVAC shelter"
                ],
                safety_requirements=[
                    "Secondary containment barrier for flood and pest protection",
                    "Automated disconnect switches"
                ],
                estimated_lifespan_years=min(6.0, max(2.0, health.estimated_rul_years * 0.9))
            )
        )

        # Non-viable applications check
        if soh < 78.0 or battery.internal_resistance_mohm > 25.0:
            non_viable.append("High-Speed Highway EV Re-installation (Discharge C-rate too demanding)")
        if soh < 72.0:
            non_viable.append("Airport Ground Support AGVs (High payload torque demands)")

        overall_score = int(sum(r.suitability_score for r in recommendations) / len(recommendations))
        econ_rating = "Excellent Commercial Repurposing Value" if overall_score >= 75 else "Moderate Repurposing Value"

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        self.last_execution_ms = round(elapsed_ms, 2)

        return SecondLifeEvaluation(
            battery_id=battery.battery_id,
            eligible_for_second_life=True,
            overall_suitability_score=overall_score,
            recommended_applications=recommendations,
            non_viable_applications=non_viable,
            economic_viability_rating=econ_rating,
            agent_status="completed",
            execution_time_ms=self.last_execution_ms
        )
