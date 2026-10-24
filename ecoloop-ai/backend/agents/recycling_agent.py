"""
EcoLoop AI - Recycling and Sustainability Agent
Estimates circular economy benefits, closed-loop material recovery,
and provides certified e-waste recycling facility routing.
"""

import time
from typing import List
from models.battery import BatteryInput, HealthAssessment, SustainabilityMetrics, MaterialRecovery
from agents.base import BaseAgent


class RecyclingSustainabilityAgent(BaseAgent):
    """
    Computes material yield (Lithium, Nickel, Cobalt, Graphite, Aluminum, Copper)
    and environmental benefits (CO2 avoided, waste diverted) from responsible battery end-of-life processing.
    """

    def __init__(self):
        super().__init__(
            name="Recycling & Sustainability Agent",
            role="Circular Material Yield Estimation & Closed-Loop Recycling Logistics"
        )

    def process(self, battery: BatteryInput, health: HealthAssessment) -> SustainabilityMetrics:
        start_time = time.perf_counter()
        weight_kg = battery.battery_weight_kg
        chem = battery.chemistry.upper()

        # Material fraction heuristic estimates based on industry benchmarks (NMC vs LFP)
        if "NMC" in chem:
            # NMC Chemistry: High Nickel & Cobalt content
            ni_fraction = 0.18
            co_fraction = 0.05
            mn_fraction = 0.05
            li_fraction = 0.035
            graphite_fraction = 0.16
            cu_fraction = 0.09
            al_fraction = 0.14
        elif "LFP" in chem:
            # Lithium Iron Phosphate (no Co, no Ni)
            ni_fraction = 0.0
            co_fraction = 0.0
            mn_fraction = 0.0
            li_fraction = 0.028
            graphite_fraction = 0.15
            cu_fraction = 0.10
            al_fraction = 0.15
        else:
            # Default / NCA
            ni_fraction = 0.15
            co_fraction = 0.03
            mn_fraction = 0.02
            li_fraction = 0.032
            graphite_fraction = 0.15
            cu_fraction = 0.09
            al_fraction = 0.14

        # Calculate recovered masses and approximate commodity values (Demo figures)
        materials: List[MaterialRecovery] = []

        # Lithium Carbonate Equivalent
        li_kg = round(weight_kg * li_fraction, 1)
        materials.append(MaterialRecovery(
            element_name="Lithium (Li₂CO₃ eq)",
            estimated_kg=li_kg,
            recovery_purity_pct=96.5,
            market_value_usd=round(li_kg * 18.5, 2)
        ))

        # Nickel
        if ni_fraction > 0:
            ni_kg = round(weight_kg * ni_fraction, 1)
            materials.append(MaterialRecovery(
                element_name="Battery-Grade Nickel",
                estimated_kg=ni_kg,
                recovery_purity_pct=99.2,
                market_value_usd=round(ni_kg * 16.0, 2)
            ))

        # Cobalt
        if co_fraction > 0:
            co_kg = round(weight_kg * co_fraction, 1)
            materials.append(MaterialRecovery(
                element_name="Cobalt Sulfate",
                estimated_kg=co_kg,
                recovery_purity_pct=98.8,
                market_value_usd=round(co_kg * 28.0, 2)
            ))

        # Copper
        cu_kg = round(weight_kg * cu_fraction, 1)
        materials.append(MaterialRecovery(
            element_name="Refined Copper Current Collectors",
            estimated_kg=cu_kg,
            recovery_purity_pct=99.5,
            market_value_usd=round(cu_kg * 9.2, 2)
        ))

        # Aluminum
        al_kg = round(weight_kg * al_fraction, 1)
        materials.append(MaterialRecovery(
            element_name="Aluminum Casings & Foils",
            estimated_kg=al_kg,
            recovery_purity_pct=97.0,
            market_value_usd=round(al_kg * 2.4, 2)
        ))

        # Graphite
        graphite_kg = round(weight_kg * graphite_fraction, 1)
        materials.append(MaterialRecovery(
            element_name="Purified Synthetic Graphite",
            estimated_kg=graphite_kg,
            recovery_purity_pct=95.0,
            market_value_usd=round(graphite_kg * 1.8, 2)
        ))

        total_recovered_kg = round(sum(m.estimated_kg for m in materials), 1)

        # Environmental metrics
        # Benchmark: Recycling 1 kg of lithium-ion battery avoids ~3.8 kg CO2 vs virgin extraction
        co2_avoided_kg = round(weight_kg * 3.85, 1)
        # Avoided water extraction: ~250 liters per kg of battery raw material extraction
        water_saved_liters = round(weight_kg * 260.0, 0)
        waste_diverted_kg = round(weight_kg * 0.94, 1)  # 94% mass diversion from landfills

        # Determine priority level and recycling method
        is_hazard = (
            battery.physical_condition != "Normal" or
            health.thermal_status == "Severe Thermal Risk" or
            health.internal_resistance_health == "Dangerous"
        )

        if is_hazard:
            priority = "Emergency Hazard Priority"
            method = "Inert Cryogenic Shredding & Hydrometallurgical Leaching"
        elif health.state_of_health_pct < 60.0:
            priority = "High Priority End-of-Life"
            method = "Closed-Loop Direct Hydrometallurgical Cathode-to-Cathode Refining"
        else:
            priority = "Standard Lifecycle Staging"
            method = "Selective Disassembly & Cell-Level Secondary Sortation"

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        self.last_execution_ms = round(elapsed_ms, 2)

        return SustainabilityMetrics(
            battery_id=battery.battery_id,
            eligible_for_recycling=True,
            priority_level=priority,
            estimated_waste_diverted_kg=waste_diverted_kg,
            estimated_co2_avoided_kg=co2_avoided_kg,
            estimated_water_saved_liters=water_saved_liters,
            potential_material_recovery=materials,
            total_recovered_materials_kg=total_recovered_kg,
            recommended_recycling_method=method,
            compliance_standards=[
                "EU Battery Regulation 2023/1542 (Digital Battery Passport compliance)",
                "EPA Resource Conservation and Recovery Act (RCRA 40 CFR 273)",
                "UN 38.3 Dangerous Goods Transport Certification"
            ],
            authorized_facilities_recommended=[
                "Redwood Materials Recycling Complex (Sparks, NV)",
                "Li-Cycle Spoke & Hub Commercial Network",
                "Cirba Solutions Hydromet Facility"
            ],
            agent_status="completed",
            execution_time_ms=self.last_execution_ms
        )
