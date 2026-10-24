"""
EcoLoop AI - Data Validation Agent
Validates battery telemetry inputs, checks data consistency, and flags safety overrides.
"""

import time
from typing import List
from models.battery import BatteryInput, ValidationResult, ValidationIssue
from agents.base import BaseAgent


class DataValidationAgent(BaseAgent):
    """
    Agent responsible for sanitizing telemetry data and detecting immediate safety hazards.
    """

    def __init__(self):
        super().__init__(
            name="Data Validation Agent",
            role="Input Sanitization, Range Checking & Immediate Safety Screening"
        )

    def process(self, battery: BatteryInput) -> ValidationResult:
        start_time = time.perf_counter()
        issues: List[ValidationIssue] = []
        safety_override = False

        # 1. Physical inspection screening
        hazardous_physical_states = ["Swelling", "Puncture", "Corrosion", "Seal Breach"]
        if battery.physical_condition in hazardous_physical_states:
            safety_override = True
            issues.append(
                ValidationIssue(
                    field="physical_condition",
                    severity="critical",
                    message=f"Severe physical condition '{battery.physical_condition}' detected. Immediate isolation required."
                )
            )

        # 2. Operating Temperature checks
        if battery.operating_temp_c > 50.0:
            safety_override = True
            issues.append(
                ValidationIssue(
                    field="operating_temp_c",
                    severity="critical",
                    message=f"Critical high temperature ({battery.operating_temp_c}°C > 50.0°C). Thermal runaway risk."
                )
            )
        elif battery.operating_temp_c > 42.0:
            issues.append(
                ValidationIssue(
                    field="operating_temp_c",
                    severity="warning",
                    message=f"Elevated operating temperature ({battery.operating_temp_c}°C). Requires active thermal monitoring."
                )
            )
        elif battery.operating_temp_c < 0.0:
            issues.append(
                ValidationIssue(
                    field="operating_temp_c",
                    severity="warning",
                    message=f"Sub-zero temperature ({battery.operating_temp_c}°C) limits charging kinetics."
                )
            )

        # 3. Cell voltage imbalance check
        if battery.cell_voltage_delta_v >= 0.12:
            safety_override = True
            issues.append(
                ValidationIssue(
                    field="cell_voltage_delta_v",
                    severity="critical",
                    message=f"Extreme cell voltage variance ({battery.cell_voltage_delta_v:.3f}V >= 0.12V) indicates internal cell failure."
                )
            )
        elif battery.cell_voltage_delta_v >= 0.05:
            issues.append(
                ValidationIssue(
                    field="cell_voltage_delta_v",
                    severity="warning",
                    message=f"Moderate cell voltage variance ({battery.cell_voltage_delta_v:.3f}V). Cell re-balancing recommended."
                )
            )

        # 4. State of Health vs Capacity sanity
        expected_cap = (battery.state_of_health_pct / 100.0) * battery.pack_capacity_kwh
        cap_discrepancy = abs(battery.current_capacity_kwh - expected_cap)
        if cap_discrepancy > 8.0:
            issues.append(
                ValidationIssue(
                    field="current_capacity_kwh",
                    severity="warning",
                    message=f"Discrepancy between reported SoH ({battery.state_of_health_pct}%) and current capacity ({battery.current_capacity_kwh} kWh)."
                )
            )

        # 5. Internal resistance check
        if battery.internal_resistance_mohm > 60.0:
            safety_override = True
            issues.append(
                ValidationIssue(
                    field="internal_resistance_mohm",
                    severity="critical",
                    message=f"Internal resistance abnormally high ({battery.internal_resistance_mohm} mΩ > 60.0 mΩ)."
                )
            )

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        self.last_execution_ms = round(elapsed_ms, 2)

        is_valid = not safety_override

        return ValidationResult(
            is_valid=is_valid,
            safety_override=safety_override,
            issues=issues,
            sanitized_input=battery,
            agent_status="completed",
            execution_time_ms=self.last_execution_ms
        )
