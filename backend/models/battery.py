"""
EcoLoop AI - Battery Data Schemas & Models
Defines structured schemas for battery telemetry, health analysis,
second-life recommendations, recycling impact, and orchestration results.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BatteryInput(BaseModel):
    """Input telemetry data for an electric vehicle battery pack."""
    battery_id: str = Field(default="BAT-2026-EV-901", description="Unique battery identifier")
    model_name: str = Field(default="NMC-622 Standard Pack", description="Battery chemistry and pack name")
    pack_capacity_kwh: float = Field(default=64.0, ge=1.0, le=300.0, description="Original nominal capacity in kWh")
    current_capacity_kwh: float = Field(default=48.6, ge=0.0, le=300.0, description="Measured available capacity in kWh")
    state_of_health_pct: float = Field(default=75.9, ge=0.0, le=100.0, description="Calculated State of Health (SoH) %")
    nominal_voltage_v: float = Field(default=360.0, ge=12.0, le=1000.0, description="Nominal pack voltage in Volts")
    current_voltage_v: float = Field(default=355.2, ge=0.0, le=1000.0, description="Current terminal voltage in Volts")
    operating_temp_c: float = Field(default=24.5, ge=-40.0, le=120.0, description="Pack operating temperature in Celsius")
    cycle_count: int = Field(default=1420, ge=0, le=20000, description="Total charge/discharge equivalent cycles")
    internal_resistance_mohm: float = Field(default=18.5, ge=0.1, le=500.0, description="Internal resistance in milliOhms")
    cell_voltage_delta_v: float = Field(default=0.022, ge=0.0, le=2.0, description="Max voltage difference between cells in Volts")
    physical_condition: str = Field(default="Normal", description="Physical inspection flag: Normal, Swelling, Puncture, Corrosion, Seal Breach")
    battery_weight_kg: float = Field(default=420.0, ge=10.0, le=2000.0, description="Total physical weight of battery pack in kg")
    chemistry: str = Field(default="NMC-622", description="Battery chemistry: NMC-622, NMC-811, LFP, NCA")


class ValidationIssue(BaseModel):
    field: str
    severity: str  # "warning" or "critical"
    message: str


class ValidationResult(BaseModel):
    is_valid: bool
    safety_override: bool
    issues: List[ValidationIssue]
    sanitized_input: Optional[BatteryInput] = None
    agent_status: str = "completed"
    execution_time_ms: float = 0.0


class HealthAssessment(BaseModel):
    battery_id: str
    state_of_health_pct: float
    condition_rating: str  # Optimal, Good, Moderate Degradation, Severe Degradation, Critical Safety Hazard
    estimated_rul_cycles: int
    estimated_rul_years: float
    degradation_rate_index: float
    thermal_status: str  # Normal, Elevated, Cold-Throttled, Severe Thermal Risk
    cell_balance_status: str  # Balanced, Mild Imbalance, Severe Imbalance
    internal_resistance_health: str  # Low, Acceptable, High, Dangerous
    flag_professional_inspection: bool
    inspection_reasons: List[str]
    model_name: str = "Deterministic Degradation Estimation Heuristic (Demo Model v1.2)"
    agent_status: str = "completed"
    execution_time_ms: float = 0.0


class ApplicationRecommendation(BaseModel):
    application_name: str
    category: str
    suitability_score: int  # 0 to 100
    suitability_tier: str  # Highly Recommended, Suitable, Marginal, Not Recommended
    confidence_level_pct: int
    primary_advantages: List[str]
    technical_limitations: List[str]
    safety_requirements: List[str]
    estimated_lifespan_years: float


class SecondLifeEvaluation(BaseModel):
    battery_id: str
    eligible_for_second_life: bool
    overall_suitability_score: int
    recommended_applications: List[ApplicationRecommendation]
    non_viable_applications: List[str]
    economic_viability_rating: str
    agent_status: str = "completed"
    execution_time_ms: float = 0.0


class MaterialRecovery(BaseModel):
    element_name: str
    estimated_kg: float
    recovery_purity_pct: float
    market_value_usd: float


class SustainabilityMetrics(BaseModel):
    battery_id: str
    eligible_for_recycling: bool
    priority_level: str  # High Priority, Standard, Scheduled, Emergency Hazard
    estimated_waste_diverted_kg: float
    estimated_co2_avoided_kg: float
    estimated_water_saved_liters: float
    potential_material_recovery: List[MaterialRecovery]
    total_recovered_materials_kg: float
    recommended_recycling_method: str  # Hydrometallurgical, Closed-loop Direct, Pyrometallurgical
    compliance_standards: List[str]
    authorized_facilities_recommended: List[str]
    agent_status: str = "completed"
    execution_time_ms: float = 0.0


class DecisionStep(BaseModel):
    step_number: int
    agent_name: str
    action: str
    reasoning: str
    rule_applied: str
    timestamp: str


class OrchestrationResult(BaseModel):
    battery_id: str
    final_lifecycle_decision: str  # CONTINUE_EV, SECOND_LIFE_REUSE, INSPECT_AND_REPAIR, RECYCLE_NOW
    decision_summary: str
    confidence_score_pct: int
    reasoning_factors: List[str]
    safety_disclaimer: str
    is_simulated_ai: bool = True
    ai_logic_type: str = "Deterministic Multi-Agent Rule Engine with Simulated Reasoning Trace"
    execution_pipeline: List[str]
    decision_trace: List[DecisionStep]
    validation_agent_result: Optional[ValidationResult] = None
    health_agent_result: Optional[HealthAssessment] = None
    second_life_agent_result: Optional[SecondLifeEvaluation] = None
    recycling_agent_result: Optional[SustainabilityMetrics] = None
    total_execution_time_ms: float = 0.0
