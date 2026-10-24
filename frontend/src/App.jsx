import React, { useState, useEffect } from 'react';
import { SAMPLE_SCENARIOS, runClientSideAgentPipeline } from './services/agentEngine';

export default function App() {
  const [selectedScenarioId, setSelectedScenarioId] = useState(SAMPLE_SCENARIOS[0].id);
  const [battery, setBattery] = useState({ ...SAMPLE_SCENARIOS[0].battery });
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const [isCheckingBackend, setIsCheckingBackend] = useState(false);

  // Execute pipeline whenever battery state changes
  useEffect(() => {
    async function runPipeline() {
      if (isBackendConnected) {
        try {
          const res = await fetch('http://localhost:8000/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(battery)
          });
          if (res.ok) {
            const data = await res.json();
            setAnalysisResult(data);
            return;
          }
        } catch (err) {
          console.warn("Backend unavailable, using client agent simulation:", err);
        }
      }
      // Autonomous client-side simulation engine (GitHub Pages mode)
      const clientResult = runClientSideAgentPipeline(battery);
      setAnalysisResult(clientResult);
    }
    runPipeline();
  }, [battery, isBackendConnected]);

  const handleScenarioSelect = (scenario) => {
    setSelectedScenarioId(scenario.id);
    setBattery({ ...scenario.battery });
  };

  const handleInputChange = (field, value) => {
    setBattery(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const testBackendConnection = async () => {
    setIsCheckingBackend(true);
    try {
      const res = await fetch('http://localhost:8000/api/health');
      if (res.ok) {
        setIsBackendConnected(true);
        alert('Connected to Python FastAPI backend at http://localhost:8000!');
      } else {
        setIsBackendConnected(false);
        alert('FastAPI backend responded with error.');
      }
    } catch (e) {
      setIsBackendConnected(false);
      alert('FastAPI backend is offline (http://localhost:8000).\nRunning in Standalone Autonomous Multi-Agent Simulation Mode (GitHub Pages ready)!');
    } finally {
      setIsCheckingBackend(false);
    }
  };

  if (!analysisResult) return null;

  const decision = analysisResult.final_lifecycle_decision;
  const isSecondLife = decision === 'EVALUATE_SECOND_LIFE';
  const isHazard = decision === 'INSPECT_OR_REPAIR';
  const isRetain = decision === 'CONTINUE_EV';

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-eco-500 selection:text-slate-950">
      
      {/* Top Advisory Banner */}
      <div className="bg-emerald-950/80 border-b border-emerald-500/30 px-4 py-2 text-xs md:text-sm text-emerald-200 flex flex-wrap items-center justify-between gap-2 shadow-inner">
        <div className="flex items-center space-x-2">
          <span className="p-1 bg-emerald-500/20 text-emerald-400 rounded">ℹ️</span>
          <span><strong>Advisory Guidance Only:</strong> Agent recommendations do not replace certified physical testing (UL 1974 / IEC 62619). Damaged or swollen packs are strictly routed to qualified inspection.</span>
        </div>
        <div className="flex items-center space-x-3 text-xs">
          <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-emerald-900/60 border border-emerald-500/40 text-emerald-300 font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping mr-1.5"></span>
            Multi-Agent Engine Active
          </span>
        </div>
      </div>

      {/* Header */}
      <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-slate-950 font-bold text-xl shadow-lg shadow-emerald-500/20">
              🌱
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-emerald-400 bg-clip-text text-transparent">
                  EcoLoop AI
                </h1>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                  Agentic v1.0
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                Autonomous EV Battery Waste Prevention &amp; Second-Life Orchestration
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border bg-slate-800/80 border-slate-700 text-slate-300">
              <span className={`w-2 h-2 rounded-full ${isBackendConnected ? 'bg-emerald-400' : 'bg-teal-400'}`}></span>
              <span>{isBackendConnected ? 'FastAPI Connected' : 'Autonomous Client Engine (GitHub Pages)'}</span>
            </div>
            <button
              onClick={testBackendConnection}
              disabled={isCheckingBackend}
              className="px-2.5 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-colors"
            >
              {isCheckingBackend ? 'Pinging...' : 'Connect FastAPI'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6 flex-1 w-full">

        {/* Demo Scenarios */}
        <section className="bg-slate-900/80 rounded-2xl border border-slate-800 p-4 shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Curated Demo Battery Scenarios</span>
            <span className="text-xs text-slate-400">Click to instantly dispatch agents with real-world telemetry</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
            {SAMPLE_SCENARIOS.map(s => (
              <button
                key={s.id}
                onClick={() => handleScenarioSelect(s)}
                className={`text-left p-2.5 rounded-xl border transition-all duration-150 group ${
                  selectedScenarioId === s.id
                    ? 'border-emerald-500 bg-emerald-950/40 text-emerald-300'
                    : 'border-slate-800 bg-slate-950/70 hover:border-emerald-500/50 hover:bg-slate-900 text-slate-300'
                }`}
              >
                <div className="text-xs font-bold group-hover:text-emerald-300">{s.title}</div>
                <div className="text-[10px] text-slate-400 truncate mt-0.5">{s.subtitle}</div>
              </button>
            ))}
          </div>
        </section>

        {/* Agent Workflow Pipeline Visualizer */}
        <section className="bg-slate-900/70 rounded-2xl border border-slate-800 p-4 sm:p-5 relative overflow-hidden shadow-xl">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
            <div className="flex items-center space-x-2">
              <span className="flex h-2.5 w-2.5 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-200">
                Autonomous Multi-Agent Workflow Pipeline
              </h2>
            </div>
            <div className="text-xs font-mono text-slate-400 bg-slate-950/80 px-3 py-1 rounded-lg border border-slate-800">
              Pipeline Latency: <span className="text-emerald-400 font-bold">{analysisResult.total_execution_time_ms} ms</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Step 1</span>
                <h3 className="text-xs font-bold text-slate-200 mt-1">Data Validation Agent</h3>
                <p className="text-[11px] text-slate-400 mt-1">Screening bounds, sensor anomalies &amp; safety hazards</p>
              </div>
              <div className="mt-2 text-[10px] font-mono text-emerald-400">Status: Complete</div>
            </div>

            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Step 2</span>
                <h3 className="text-xs font-bold text-slate-200 mt-1">Battery Health Agent</h3>
                <p className="text-[11px] text-slate-400 mt-1">Estimating SoH, cell balance &amp; Useful Life</p>
              </div>
              <div className="mt-2 text-[10px] font-mono text-emerald-400">Status: Complete</div>
            </div>

            <div className="bg-slate-950/70 border border-emerald-500/40 rounded-xl p-3 flex flex-col justify-between shadow-lg shadow-emerald-950/40">
              <div>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-500/30">Step 3 (Core)</span>
                <h3 className="text-xs font-bold text-emerald-300 mt-1">Decision Orchestrator</h3>
                <p className="text-[11px] text-slate-400 mt-1">Synthesizing findings &amp; selecting optimal path</p>
              </div>
              <div className="mt-2 text-[10px] font-mono text-emerald-400">Consensus Reached</div>
            </div>

            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Step 4A</span>
                <h3 className="text-xs font-bold text-slate-200 mt-1">Second-Life Agent</h3>
                <p className="text-[11px] text-slate-400 mt-1">Solar microgrid, UPS &amp; agricultural matching</p>
              </div>
              <div className={`mt-2 text-[10px] font-mono ${isSecondLife ? 'text-emerald-400' : 'text-slate-400'}`}>
                {isSecondLife ? 'Evaluated' : 'Bypassed'}
              </div>
            </div>

            <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-3 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">Step 4B</span>
                <h3 className="text-xs font-bold text-slate-200 mt-1">Recycling Agent</h3>
                <p className="text-[11px] text-slate-400 mt-1">Critical mineral yields (Li, Ni, Co) &amp; CO₂ avoided</p>
              </div>
              <div className="mt-2 text-[10px] font-mono text-emerald-400">Circular Impact Done</div>
            </div>
          </div>
        </section>

        {/* Workspace Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left Form (4 cols) */}
          <div className="lg:col-span-4 bg-slate-900/80 rounded-2xl border border-slate-800 p-5 shadow-xl space-y-4 sticky top-20">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-200">Battery Telemetry Input</h2>
              <button
                onClick={() => handleScenarioSelect(SAMPLE_SCENARIOS[0])}
                className="text-[11px] font-medium text-emerald-400 hover:underline"
              >
                Reset
              </button>
            </div>

            <div className="space-y-4 text-xs">
              <div>
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Battery ID</label>
                <input
                  type="text"
                  value={battery.battery_id}
                  onChange={e => handleInputChange('battery_id', e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                />
              </div>

              {/* SoH Slider */}
              <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                <div className="flex justify-between items-center mb-1">
                  <span className="font-semibold text-slate-300">State of Health (SoH)</span>
                  <span className="font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
                    {battery.state_of_health_pct.toFixed(1)}%
                  </span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="100"
                  step="0.5"
                  value={battery.state_of_health_pct}
                  onChange={e => handleInputChange('state_of_health_pct', parseFloat(e.target.value))}
                  className="w-full accent-emerald-500 cursor-pointer"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Pack Size (kWh)</label>
                  <input
                    type="number"
                    value={battery.pack_capacity_kwh}
                    onChange={e => handleInputChange('pack_capacity_kwh', parseFloat(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Cycles</label>
                  <input
                    type="number"
                    value={battery.cycle_count}
                    onChange={e => handleInputChange('cycle_count', parseInt(e.target.value, 10))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Temp (°C)</label>
                  <input
                    type="number"
                    value={battery.operating_temp_c}
                    onChange={e => handleInputChange('operating_temp_c', parseFloat(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Resistance (mΩ)</label>
                  <input
                    type="number"
                    value={battery.internal_resistance_mohm}
                    onChange={e => handleInputChange('internal_resistance_mohm', parseFloat(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Cell Δ (V)</label>
                  <input
                    type="number"
                    step="0.005"
                    value={battery.cell_voltage_delta_v}
                    onChange={e => handleInputChange('cell_voltage_delta_v', parseFloat(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Weight (kg)</label>
                  <input
                    type="number"
                    value={battery.battery_weight_kg}
                    onChange={e => handleInputChange('battery_weight_kg', parseFloat(e.target.value))}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 font-mono text-slate-200 focus:border-emerald-500 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Physical Integrity</label>
                <select
                  value={battery.physical_condition}
                  onChange={e => handleInputChange('physical_condition', e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1.5 text-slate-200 focus:border-emerald-500 focus:outline-none"
                >
                  <option value="Normal">Normal — No Deformation</option>
                  <option value="Swelling">Swelling — Pouch Expansion (Hazard)</option>
                  <option value="Corrosion">Corrosion — Terminal Oxidation</option>
                  <option value="Puncture">Puncture / Structural Compromise</option>
                  <option value="Seal Breach">Seal Breach / Electrolyte Odor</option>
                </select>
              </div>
            </div>
          </div>

          {/* Right Dashboard Results (8 cols) */}
          <div className="lg:col-span-8 space-y-6">

            {/* Decision Orchestrator Card */}
            <div className="bg-gradient-to-br from-slate-900 to-slate-950 rounded-2xl border border-emerald-500/40 p-5 shadow-2xl relative overflow-hidden">
              <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-800">
                <div>
                  <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-400 font-semibold">Orchestrator Consensus</span>
                  <h3 className="text-base font-extrabold text-white">Final Life-Cycle Decision</h3>
                </div>

                <div className={`px-3.5 py-1.5 rounded-xl font-bold text-xs uppercase tracking-wider border ${
                  isSecondLife ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/50' :
                  isRetain ? 'bg-blue-500/20 text-blue-300 border-blue-500/50' :
                  isHazard ? 'bg-red-500/20 text-red-300 border-red-500/50 animate-pulse' :
                  'bg-amber-500/20 text-amber-300 border-amber-500/50'
                }`}>
                  {decision.replace(/_/g, ' ')}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 my-4">
                <div className="md:col-span-3">
                  <p className="text-sm text-slate-200 leading-relaxed font-medium">
                    {analysisResult.decision_summary}
                  </p>
                </div>
                <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800 text-center flex flex-col justify-center">
                  <span className="text-[10px] font-mono text-slate-400 uppercase">Confidence</span>
                  <span className="text-2xl font-black text-emerald-400">{analysisResult.confidence_score_pct}%</span>
                </div>
              </div>

              <div className="bg-slate-950/60 rounded-xl p-3.5 border border-slate-800 space-y-2">
                <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold block">
                  Transparent Decision Rationale:
                </span>
                <ul className="space-y-1.5 text-xs text-slate-300">
                  {analysisResult.reasoning_factors.map((f, i) => (
                    <li key={i} className="flex items-start space-x-2">
                      <span className="text-emerald-400 mt-0.5">•</span>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Health Analysis Card */}
            <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-5 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-sm font-extrabold text-white">Battery Health &amp; Degradation Analysis</h3>
                <span className="text-xs px-2.5 py-1 rounded-full font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  {analysisResult.health_agent_result?.condition_rating}
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">Estimated RUL</span>
                  <span className="text-lg font-bold text-white mt-0.5 block">{analysisResult.health_agent_result?.estimated_rul_years} yrs</span>
                  <span className="text-[10px] text-slate-400 font-mono">~{analysisResult.health_agent_result?.estimated_rul_cycles} cycles</span>
                </div>
                <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">Cell Imbalance</span>
                  <span className="text-lg font-bold text-white mt-0.5 block">{battery.cell_voltage_delta_v.toFixed(3)} V</span>
                  <span className="text-[10px] text-emerald-400 font-mono">{analysisResult.health_agent_result?.cell_balance_status}</span>
                </div>
                <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">Thermal Profile</span>
                  <span className="text-lg font-bold text-white mt-0.5 block">{battery.operating_temp_c} °C</span>
                  <span className="text-[10px] text-emerald-400 font-mono">{analysisResult.health_agent_result?.thermal_status}</span>
                </div>
                <div className="bg-slate-950/70 p-3 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">Impedance</span>
                  <span className="text-lg font-bold text-white mt-0.5 block">{battery.internal_resistance_mohm} mΩ</span>
                  <span className="text-[10px] text-emerald-400 font-mono">{analysisResult.health_agent_result?.internal_resistance_health}</span>
                </div>
              </div>
            </div>

            {/* Second-Life Recommendations */}
            <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-5 shadow-xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-sm font-extrabold text-white">Recommended Second-Life Applications</h3>
                <span className={`text-xs px-2.5 py-1 rounded-full font-semibold border ${
                  isSecondLife ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' : 'bg-red-500/20 text-red-300 border-red-500/30'
                }`}>
                  {isSecondLife ? 'Eligible for Repurposing' : 'Ineligible for Second-Life'}
                </span>
              </div>

              {isSecondLife ? (
                <div className="space-y-3">
                  {analysisResult.second_life_agent_result?.recommended_applications.map((app, idx) => (
                    <div key={idx} className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="text-xs font-bold text-white">{app.application_name}</span>
                          <span className="text-[10px] text-slate-400 block">{app.category}</span>
                        </div>
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          {app.suitability_score}% Suitability
                        </span>
                      </div>
                      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full" style={{ width: `${app.suitability_score}%` }}></div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 text-center text-xs text-slate-400">
                  Second-life repurposing not recommended for this battery condition. Safety boundaries protect against thermal hazards and accelerated degradation.
                </div>
              )}
            </div>

            {/* Circular Recycling & Sustainability Impact */}
            <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-5 shadow-xl space-y-4">
              <h3 className="text-sm font-extrabold text-white pb-3 border-b border-slate-800">
                Closed-Loop Recycling &amp; Sustainability Benefits
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">CO₂ Avoided</span>
                  <span className="text-base font-extrabold text-white">{analysisResult.recycling_agent_result?.estimated_co2_avoided_kg} kg CO₂e</span>
                </div>
                <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">Landfill Diverted</span>
                  <span className="text-base font-extrabold text-white">{analysisResult.recycling_agent_result?.estimated_waste_diverted_kg} kg</span>
                </div>
                <div className="bg-slate-950/70 p-3.5 rounded-xl border border-slate-800">
                  <span className="text-[10px] text-slate-400 uppercase font-mono block">Water Saved</span>
                  <span className="text-base font-extrabold text-white">{(analysisResult.recycling_agent_result?.estimated_water_saved_liters || 0).toLocaleString()} L</span>
                </div>
              </div>
            </div>

            {/* Decision Trace Timeline */}
            <div className="bg-slate-900/80 rounded-2xl border border-slate-800 p-5 shadow-xl space-y-3">
              <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider pb-2 border-b border-slate-800">
                Explainable Decision Trace &amp; Audit Log
              </h3>
              <div className="space-y-2.5">
                {analysisResult.decision_trace.map((t, idx) => (
                  <div key={idx} className="flex items-start space-x-3 p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 text-xs">
                    <span className="w-5 h-5 rounded-full bg-slate-800 text-emerald-400 flex items-center justify-center font-mono font-bold text-[10px] shrink-0 mt-0.5">
                      {t.step_number}
                    </span>
                    <div className="space-y-0.5 flex-1">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-200">{t.agent_name}</span>
                        <span className="text-[10px] font-mono text-slate-400">{t.action}</span>
                      </div>
                      <p className="text-slate-300 text-[11px]">{t.reasoning}</p>
                      <div className="text-[10px] font-mono text-emerald-400/80">{t.rule_applied}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-950 py-6 px-4 mt-8">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
          <div>EcoLoop AI — Agentic AI-Powered Autonomous EV Battery Waste Prevention</div>
          <div>Static GitHub Pages &amp; FastAPI Compatible</div>
        </div>
      </footer>

    </div>
  );
}
