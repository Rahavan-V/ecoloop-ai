"""
EcoLoop AI - Battery Health Analysis Agent
Computes electrochemical degradation indices, Remaining Useful Life (RUL) estimations,
and identifies safety inspection flags using transparent deterministic models.
"""

import time
from typing import List
from models.battery import BatteryInput, HealthAssessment
from agents.base import BaseAgent


class BatteryHealthAnalysisAgent(BaseAgent):
    """
    Analyzes battery electrochemical parameters, calculates degradation indices,
    and projects Remaining Useful Life (RUL) using deterministic heuristic equations.
    """

    def __init__(self):
        super().__init__(
            name="Battery Health Analysis Agent",
            role="Electro-Chemical Degradation Modeling & Useful Life Estimation"
        )
        self.model_label = "Deterministic Degradation Estimation Heuristic (Demo Model v1.2)"

    def process(self, battery: BatteryInput) -> HealthAssessment:
        start_time = time.perf_counter()
        reasons_for_inspection: List[str] = []

        # 1. Condition Rating determination
        soh = battery.state_of_health_pct
        if battery.physical_condition != "Normal":
            condition = "Critical Safety Hazard"
            reasons_for_inspection.append(f"Physical anomaly: {battery.physical_condition}")
        elif soh >= 85.0 and battery.cell_voltage_delta_v < 0.03:
            condition = "Optimal"
        elif soh >= 75.0 and battery.cell_voltage_delta_v < 0.05:
            condition = "Good"
        elif soh >= 60.0:
            condition = "Moderate Degradation"
        elif soh >= 45.0:
            condition = "Severe Degradation"
            reasons_for_inspection.append(f"State of Health deeply degraded ({soh:.1f}% < 60%)")
        else:
            condition = "Critical Safety Hazard"
            reasons_for_inspection.append(f"End-of-Life exhaustion: SoH ({soh:.1f}%) below minimum safe threshold")

        # 2. Thermal Status Assessment
        if battery.operating_temp_c > 48.0 or battery.operating_temp_c < -10.0:
            thermal_status = "Severe Thermal Risk"
            reasons_for_inspection.append(f"Abnormal operating temperature: {battery.operating_temp_c}°C")
        elif battery.operating_temp_c > 38.0:
            thermal_status = "Elevated"
        elif battery.operating_temp_c < 5.0:
            thermal_status = "Cold-Throttled"
        else:
            thermal_status = "Normal"

        # 3. Cell Imbalance Status
        if battery.cell_voltage_delta_v > 0.08:
            cell_balance = "Severe Imbalance"
            reasons_for_inspection.append(f"Cell delta variance ({battery.cell_voltage_delta_v:.3f}V) indicates weak/shorted cell")
        elif battery.cell_voltage_delta_v > 0.035:
            cell_balance = "Mild Imbalance"
        else:
            cell_balance = "Balanced"

        # 4. Internal Resistance Health
        if battery.internal_resistance_mohm > 50.0:
            ir_health = "Dangerous"
            reasons_for_inspection.append(f"Elevated internal impedance ({battery.internal_resistance_mohm} mΩ) risks overheating under load")
        elif battery.internal_resistance_mohm > 30.0:
            ir_health = "High"
        elif battery.internal_resistance_mohm > 15.0:
            ir_health = "Acceptable"
        else:
            ir_health = "Low"

        # 5. Remaining Useful Life (RUL) Estimation
        # Model assumption: End-of-First-Life at 80% SoH, End-of-Second-Life at 55% SoH.
        # Average degradation per cycle approx 0.015% to 0.025% depending on chemistry and stress.
        stress_multiplier = 1.0
        if battery.operating_temp_c > 35.0 or battery.operating_temp_c < 5.0:
            stress_multiplier += 0.3
        if battery.cell_voltage_delta_v > 0.04:
            stress_multiplier += 0.2
        if battery.internal_resistance_mohm > 25.0:
            stress_multiplier += 0.25

        base_loss_per_cycle = 0.016 * stress_multiplier
        remaining_soh_allowance = max(0.0, soh - 55.0)

        if condition == "Critical Safety Hazard" or battery.physical_condition != "Normal":
            estimated_rul_cycles = 0
            estimated_rul_years = 0.0
        else:
            estimated_rul_cycles = int(remaining_soh_allowance / (base_loss_per_cycle or 0.01))
            # Assuming ~250 equivalent full cycles per year in second-life stationary storage
            estimated_rul_years = round(estimated_rul_cycles / 250.0, 1)

        degradation_rate_index = round(base_loss_per_cycle * 1000.0, 2)  # Index per 1000 cycles
        flag_inspection = len(reasons_for_inspection) > 0

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        self.last_execution_ms = round(elapsed_ms, 2)

        return HealthAssessment(
            battery_id=battery.battery_id,
            state_of_health_pct=round(soh, 1),
            condition_rating=condition,
            estimated_rul_cycles=estimated_rul_cycles,
            estimated_rul_years=estimated_rul_years,
            degradation_rate_index=degradation_rate_index,
            thermal_status=thermal_status,
            cell_balance_status=cell_balance,
            internal_resistance_health=ir_health,
            flag_professional_inspection=flag_inspection,
            inspection_reasons=reasons_for_inspection,
            model_name=self.model_label,
            agent_status="completed",
            execution_time_ms=self.last_execution_ms
        )
