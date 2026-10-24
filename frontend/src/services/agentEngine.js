/**
 * EcoLoop AI - Client-Side Multi-Agent Simulation & API Client
 * Provides 100% parity with the Python FastAPI backend logic for GitHub Pages standalone execution.
 */

export const SAMPLE_SCENARIOS = [
  {
    id: "scenario-second-life",
    title: "⚡ Prime Second-Life (76% SoH)",
    subtitle: "Solar Microgrid & Energy Buffer",
    battery: {
      battery_id: "BAT-NMC-760-SL",
      model_name: "Tesla Model 3 Long Range Module",
      chemistry: "NMC-811",
      state_of_health_pct: 76.0,
      pack_capacity_kwh: 75.0,
      current_capacity_kwh: 57.0,
      cycle_count: 1420,
      operating_temp_c: 24.5,
      internal_resistance_mohm: 17.5,
      cell_voltage_delta_v: 0.018,
      nominal_voltage_v: 360.0,
      current_voltage_v: 355.2,
      physical_condition: "Normal",
      battery_weight_kg: 440.0
    }
  },
  {
    id: "scenario-healthy-ev",
    title: "🚗 Healthy EV Pack (89% SoH)",
    subtitle: "Continue Automotive Use",
    battery: {
      battery_id: "BAT-EV-HEALTHY-890",
      model_name: "Hyundai Ioniq 5 E-GMP Pack",
      chemistry: "NMC-622",
      state_of_health_pct: 89.0,
      pack_capacity_kwh: 77.4,
      current_capacity_kwh: 68.9,
      cycle_count: 410,
      operating_temp_c: 22.0,
      internal_resistance_mohm: 11.2,
      cell_voltage_delta_v: 0.009,
      nominal_voltage_v: 697.0,
      current_voltage_v: 692.0,
      physical_condition: "Normal",
      battery_weight_kg: 475.0
    }
  },
  {
    id: "scenario-safety-hazard",
    title: "⚠️ Critical Hazard (Overheating)",
    subtitle: "Physical Swelling & Isolation",
    battery: {
      battery_id: "BAT-HAZARD-CRIT-911",
      model_name: "Nissan Leaf Gen 2 Pack",
      chemistry: "NMC-622",
      state_of_health_pct: 67.0,
      pack_capacity_kwh: 40.0,
      current_capacity_kwh: 26.8,
      cycle_count: 1820,
      operating_temp_c: 53.4,
      internal_resistance_mohm: 58.0,
      cell_voltage_delta_v: 0.145,
      nominal_voltage_v: 360.0,
      current_voltage_v: 338.0,
      physical_condition: "Swelling",
      battery_weight_kg: 303.0
    }
  },
  {
    id: "scenario-deep-recycle",
    title: "♻️ Depleted Pack (46% SoH)",
    subtitle: "Direct Mineral Recovery",
    battery: {
      battery_id: "BAT-RECYCLE-EOL-460",
      model_name: "Chevy Bolt Gen 1 Pack",
      chemistry: "NMC-622",
      state_of_health_pct: 46.0,
      pack_capacity_kwh: 60.0,
      current_capacity_kwh: 27.6,
      cycle_count: 3100,
      operating_temp_c: 25.0,
      internal_resistance_mohm: 44.5,
      cell_voltage_delta_v: 0.065,
      nominal_voltage_v: 350.0,
      current_voltage_v: 332.0,
      physical_condition: "Normal",
      battery_weight_kg: 430.0
    }
  },
  {
    id: "scenario-backup-ups",
    title: "🔋 UPS / Telecom (69% SoH)",
    subtitle: "Emergency Standby Reserve",
    battery: {
      battery_id: "BAT-UPS-RESID-690",
      model_name: "Renault Zoe Pack",
      chemistry: "NMC-622",
      state_of_health_pct: 69.0,
      pack_capacity_kwh: 52.0,
      current_capacity_kwh: 35.8,
      cycle_count: 1690,
      operating_temp_c: 21.0,
      internal_resistance_mohm: 22.0,
      cell_voltage_delta_v: 0.028,
      nominal_voltage_v: 400.0,
      current_voltage_v: 392.0,
      physical_condition: "Normal",
      battery_weight_kg: 326.0
    }
  }
];

export function runClientSideAgentPipeline(b) {
  const startTime = performance.now();
  const trace = [];
  const valIssues = [];
  let safetyOverride = false;

  // Step 1: Data Validation Agent
  const t1 = performance.now();
  if (b.physical_condition !== "Normal") {
    safetyOverride = true;
    valIssues.push(`Severe physical anomaly '${b.physical_condition}' detected.`);
  }
  if (b.operating_temp_c > 50.0) {
    safetyOverride = true;
    valIssues.push(`Critical operating temperature (${b.operating_temp_c}°C > 50.0°C).`);
  } else if (b.operating_temp_c > 42.0) {
    valIssues.push(`Elevated temperature (${b.operating_temp_c}°C). Requires thermal monitoring.`);
  }
  if (b.cell_voltage_delta_v >= 0.12) {
    safetyOverride = true;
    valIssues.push(`Extreme cell delta (${b.cell_voltage_delta_v.toFixed(3)}V >= 0.12V).`);
  }
  if (b.internal_resistance_mohm > 60.0) {
    safetyOverride = true;
    valIssues.push(`Internal resistance abnormally high (${b.internal_resistance_mohm} mΩ).`);
  }
  const valLatency = (performance.now() - t1).toFixed(1);

  trace.push({
    step_number: 1,
    agent_name: "Data Validation Agent",
    action: "Telemetry Ingestion & Safety Screening",
    reasoning: `Validated ${b.battery_id}: SoH=${b.state_of_health_pct}%, Temp=${b.operating_temp_c}°C, Condition='${b.physical_condition}'`,
    rule_applied: "Rule-VAL-01: Screening physical casing and electro-thermal bounds",
    timestamp: new Date().toLocaleTimeString()
  });

  // Step 2: Battery Health Analysis Agent
  const t2 = performance.now();
  const reasonsForInspection = [...valIssues];
  let conditionRating = "Optimal";

  if (b.physical_condition !== "Normal") {
    conditionRating = "Critical Safety Hazard";
  } else if (b.state_of_health_pct >= 85.0 && b.cell_voltage_delta_v < 0.03) {
    conditionRating = "Optimal";
  } else if (b.state_of_health_pct >= 75.0 && b.cell_voltage_delta_v < 0.05) {
    conditionRating = "Good (Degraded)";
  } else if (b.state_of_health_pct >= 60.0) {
    conditionRating = "Moderate Degradation";
  } else if (b.state_of_health_pct >= 45.0) {
    conditionRating = "Severe Degradation";
    reasonsForInspection.push(`SoH deeply degraded (${b.state_of_health_pct}% < 60%)`);
  } else {
    conditionRating = "Critical Safety Hazard";
    reasonsForInspection.push("Exhausted cell capacity below safe operation envelope");
  }

  let thermalStatus = "Normal Window";
  if (b.operating_temp_c > 48.0 || b.operating_temp_c < -10.0) {
    thermalStatus = "Severe Thermal Risk";
  } else if (b.operating_temp_c > 38.0) {
    thermalStatus = "Elevated";
  }

  let cellBalance = "Balanced";
  if (b.cell_voltage_delta_v > 0.08) {
    cellBalance = "Severe Imbalance";
  } else if (b.cell_voltage_delta_v > 0.035) {
    cellBalance = "Mild Imbalance";
  }

  let irStatus = "Acceptable";
  if (b.internal_resistance_mohm > 50.0) {
    irStatus = "Dangerous";
  } else if (b.internal_resistance_mohm > 30.0) {
    irStatus = "High";
  }

  let rulCycles = 0;
  let rulYears = 0.0;
  if (conditionRating !== "Critical Safety Hazard" && b.physical_condition === "Normal") {
    const remainingSoh = Math.max(0, b.state_of_health_pct - 55.0);
    rulCycles = Math.round(remainingSoh / 0.016);
    rulYears = parseFloat((rulCycles / 250.0).toFixed(1));
  }
  const healthLatency = (performance.now() - t2).toFixed(1);

  trace.push({
    step_number: 2,
    agent_name: "Battery Health Analysis Agent",
    action: "Degradation & Useful Life Modeling",
    reasoning: `Determined Condition='${conditionRating}', Projected RUL=${rulCycles} cycles (~${rulYears} yrs), Imbalance='${cellBalance}'`,
    rule_applied: "Rule-HLT-04: Deterministic degradation modeling & RUL estimation",
    timestamp: new Date().toLocaleTimeString()
  });

  // Step 3: Decision-Making Orchestrator
  let decision = "";
  let summary = "";
  let confidence = 90;
  let reasoningFactors = [];

  if (safetyOverride || conditionRating === "Critical Safety Hazard") {
    decision = "INSPECT_OR_REPAIR";
    confidence = 96;
    reasoningFactors = [
      `SAFETY OVERRIDE: Physical condition '${b.physical_condition}' or critical thermal/cell delta anomaly.`,
      "Second-life repurposing strictly rejected to prevent thermal runaway hazard.",
      "Mandatory certified laboratory diagnostic before authorized disposal."
    ];
    summary = `Battery ${b.battery_id} displays critical safety hazard flags. Immediate physical isolation and certified inspection required. Repurposing is strictly barred.`;

    trace.push({
      step_number: 3,
      agent_name: "Decision-Making Orchestrator",
      action: "Safety Policy Enforcement",
      reasoning: "Safety anomaly encountered. Diverting from second-life path to Hazardous Inspection & Materials Recovery.",
      rule_applied: "Rule-ORC-CRITICAL: Safety first override halts secondary repurposing",
      timestamp: new Date().toLocaleTimeString()
    });
  } else if (b.state_of_health_pct >= 82.0) {
    decision = "CONTINUE_EV";
    confidence = 93;
    reasoningFactors = [
      `High State of Health (${b.state_of_health_pct}%) remains well within automotive performance envelope.`,
      `Uniform cell balance (${b.cell_voltage_delta_v.toFixed(3)}V) and low internal resistance (${b.internal_resistance_mohm} mΩ).`,
      "Retaining pack in vehicle or deploying in Certified Pre-Owned EV avoids premature recycling."
    ];
    summary = `Battery ${b.battery_id} is in healthy condition (${b.state_of_health_pct}% SoH). Continue vehicle operation. Premature removal would lead to unnecessary lifecycle waste.`;

    trace.push({
      step_number: 3,
      agent_name: "Decision-Making Orchestrator",
      action: "Automotive Retention Assessment",
      reasoning: "SoH exceeds 82% threshold with zero anomalous flags. Recommending automotive continuation.",
      rule_applied: "Rule-ORC-RETAIN: Automotive retention prioritized over secondary cascade",
      timestamp: new Date().toLocaleTimeString()
    });
  } else if (b.state_of_health_pct >= 62.0) {
    decision = "EVALUATE_SECOND_LIFE";
    confidence = 92;
    reasoningFactors = [
      `Capacity (${b.state_of_health_pct}% SoH) is retired from EV duty, but ideal for stationary energy storage.`,
      `Stable electrochemical baseline provides ~${rulYears} years of clean solar buffering before recycling.`,
      "Repurposing for stationary storage extends useful product lifecycle and cuts total cost of ownership."
    ];
    summary = `Battery ${b.battery_id} is prime for second-life repurposing (${b.state_of_health_pct}% SoH). Highest suitability: Stationary Solar Microgrid Storage (94%).`;

    trace.push({
      step_number: 3,
      agent_name: "Decision-Making Orchestrator",
      action: "Second-Life Pathway Routing",
      reasoning: `SoH is within 62-82% sweet spot. Routing to Second-Life Agent for application matching and Recycling Agent for circular baseline.`,
      rule_applied: "Rule-ORC-2ND-LIFE: Repurpose retired automotive packs before recycling",
      timestamp: new Date().toLocaleTimeString()
    });
  } else {
    decision = "RECYCLE_NOW";
    confidence = 94;
    reasoningFactors = [
      `State of Health (${b.state_of_health_pct}%) is below viable second-life threshold (62%).`,
      "Elevated internal resistance causes excessive heat dissipation during stationary cycling.",
      "Direct hydrometallurgical recycling optimizes recovery of critical materials (Lithium, Nickel, Cobalt, Graphite)."
    ];
    summary = `Battery ${b.battery_id} has reached end-of-life exhaustion (${b.state_of_health_pct}% SoH). Immediate transfer to an authorized closed-loop recycling facility is recommended.`;

    trace.push({
      step_number: 3,
      agent_name: "Decision-Making Orchestrator",
      action: "Closed-Loop Recycling Allocation",
      reasoning: "SoH below 62% threshold. Secondary economics non-viable. Triggering full material recovery routing.",
      rule_applied: "Rule-ORC-RECYCLE: Direct cathode mineral recovery for depleted packs",
      timestamp: new Date().toLocaleTimeString()
    });
  }

  // Material and recycling metrics
  const w = b.battery_weight_kg;
  const isNmc = b.chemistry.includes("NMC");
  const liKg = parseFloat((w * (isNmc ? 0.035 : 0.028)).toFixed(1));
  const niKg = isNmc ? parseFloat((w * 0.18).toFixed(1)) : 0;
  const coKg = isNmc ? parseFloat((w * 0.05).toFixed(1)) : 0;
  const cuKg = parseFloat((w * 0.09).toFixed(1));
  const alKg = parseFloat((w * 0.14).toFixed(1));
  const grKg = parseFloat((w * 0.15).toFixed(1));

  const co2Avoided = Math.round(w * 3.85);
  const wasteDiverted = parseFloat((w * 0.94).toFixed(1));
  const waterSaved = Math.round(w * 260.0);

  trace.push({
    step_number: 4,
    agent_name: "Decision-Making Orchestrator",
    action: "Consolidated Lifecycle Recommendation",
    reasoning: `Synthesized multi-agent inputs. Assigned lifecycle path '${decision}' with ${confidence}% consensus.`,
    rule_applied: "Rule-ORC-SYNTHESIS: Multi-agent consensus with explainability audit",
    timestamp: new Date().toLocaleTimeString()
  });

  const totalTime = parseFloat((performance.now() - startTime).toFixed(1));

  return {
    battery_id: b.battery_id,
    final_lifecycle_decision: decision,
    decision_summary: summary,
    confidence_score_pct: confidence,
    reasoning_factors: reasoningFactors,
    safety_disclaimer: "Advisory guidance based on deterministic agent heuristics. Does not replace physical laboratory testing (UL 1974 / IEC 62619).",
    is_simulated_ai: true,
    ai_logic_type: "Deterministic Multi-Agent Rule Engine with Simulated Reasoning Trace",
    execution_pipeline: [
      "Data Validation Agent",
      "Battery Health Analysis Agent",
      "Decision-Making Orchestrator",
      decision === "EVALUATE_SECOND_LIFE" ? "Second-Life Recommendation Agent" : "Recycling & Sustainability Agent"
    ],
    decision_trace: trace,
    validation_agent_result: {
      is_valid: !safetyOverride,
      safety_override: safetyOverride,
      issues: valIssues.map(msg => ({ field: "telemetry", severity: "critical", message: msg })),
      execution_time_ms: parseFloat(valLatency)
    },
    health_agent_result: {
      battery_id: b.battery_id,
      state_of_health_pct: b.state_of_health_pct,
      condition_rating: conditionRating,
      estimated_rul_cycles: rulCycles,
      estimated_rul_years: rulYears,
      degradation_rate_index: 18.2,
      thermal_status: thermalStatus,
      cell_balance_status: cellBalance,
      internal_resistance_health: irStatus,
      flag_professional_inspection: reasonsForInspection.length > 0,
      inspection_reasons: reasonsForInspection,
      model_name: "Deterministic Degradation Estimation Heuristic (Demo Model v1.2)",
      execution_time_ms: parseFloat(healthLatency)
    },
    second_life_agent_result: {
      battery_id: b.battery_id,
      eligible_for_second_life: decision === "EVALUATE_SECOND_LIFE",
      overall_suitability_score: decision === "EVALUATE_SECOND_LIFE" ? 91 : 0,
      recommended_applications: decision === "EVALUATE_SECOND_LIFE" ? [
        {
          application_name: "Stationary Solar Microgrid Storage",
          category: "Grid & Renewables",
          suitability_score: 94,
          suitability_tier: "Highly Recommended",
          confidence_level_pct: 92,
          primary_advantages: [
            "Low continuous discharge (0.3C) minimizes cell stress",
            "Stationary thermal management stabilizes pack temperature",
            "Extends pack lifecycle by 5 to 8 years before recycling"
          ],
          technical_limitations: [
            "Requires multi-string BMS with passive cell balancing",
            "Lower volumetric density than newly minted cells"
          ],
          safety_requirements: ["UL 1974 re-certification", "NFPA 855 fire suppression barrier"],
          estimated_lifespan_years: Math.min(8.5, Math.max(2.0, rulYears * 1.2))
        },
        {
          application_name: "Residential Backup Power & Critical UPS",
          category: "Resilience & Emergency Power",
          suitability_score: 88,
          suitability_tier: "Suitable",
          confidence_level_pct: 89,
          primary_advantages: [
            "Standby float operation involves infrequent cycling",
            "Emergency power availability without deep daily cycles",
            "40-60% capital expenditure savings vs new home storage"
          ],
          technical_limitations: ["High-voltage inverter isolation mandatory"],
          safety_requirements: ["Dedicated outdoor/garage installation"],
          estimated_lifespan_years: Math.min(10.0, Math.max(3.0, rulYears * 1.4))
        }
      ] : [],
      non_viable_applications: decision !== "EVALUATE_SECOND_LIFE" ? ["Stationary Microgrids", "Residential Backup"] : []
    },
    recycling_agent_result: {
      battery_id: b.battery_id,
      eligible_for_recycling: true,
      priority_level: safetyOverride ? "Emergency Hazard Priority" : (b.state_of_health_pct < 60 ? "High Priority End-of-Life" : "Standard Circular Baseline"),
      estimated_waste_diverted_kg: wasteDiverted,
      estimated_co2_avoided_kg: co2Avoided,
      estimated_water_saved_liters: waterSaved,
      total_recovered_materials_kg: parseFloat((liKg + niKg + coKg + cuKg + alKg + grKg).toFixed(1)),
      potential_material_recovery: [
        { element_name: "Lithium (Li₂CO₃ eq)", estimated_kg: liKg, recovery_purity_pct: 96.5, market_value_usd: Math.round(liKg * 18.5) },
        { element_name: "Battery-Grade Nickel", estimated_kg: niKg, recovery_purity_pct: 99.2, market_value_usd: Math.round(niKg * 16.0) },
        { element_name: "Cobalt Sulfate", estimated_kg: coKg, recovery_purity_pct: 98.8, market_value_usd: Math.round(coKg * 28.0) },
        { element_name: "Refined Copper", estimated_kg: cuKg, recovery_purity_pct: 99.5, market_value_usd: Math.round(cuKg * 9.2) },
        { element_name: "Aluminum Casings", estimated_kg: alKg, recovery_purity_pct: 97.0, market_value_usd: Math.round(alKg * 2.4) },
        { element_name: "Purified Graphite", estimated_kg: grKg, recovery_purity_pct: 95.0, market_value_usd: Math.round(grKg * 1.8) }
      ],
      recommended_recycling_method: safetyOverride ? "Inert Cryogenic Shredding & Hydrometallurgical Extraction" : "Closed-Loop Direct Hydrometallurgical Refining",
      compliance_standards: [
        "EU Battery Regulation 2023/1542",
        "EPA Resource Conservation and Recovery Act (RCRA 40 CFR 273)"
      ],
      authorized_facilities_recommended: [
        "Redwood Materials Recycling Complex",
        "Li-Cycle Spoke & Hub Network"
      ]
    },
    total_execution_time_ms: totalTime
  };
}
