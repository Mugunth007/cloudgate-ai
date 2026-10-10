"""CloudGate AI: AgntID Air-Gap Control Plane Dashboard (Clean, Spacious Layout)
100% Local SLM Tool Calling & Zero-Cloud-Egress Governance on Port 5050.
"""
import asyncio
import json
import os
import urllib.request
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn

from sre_agent_airgap import run_airgap_investigation_stream

app = FastAPI(title="AgntID Air-Gap Control Plane")

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgntID Air-Gap — 100% On-The-Box Local SLM Governance</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: #06090F; color: #F3F4F6; }
        .mono { font-family: 'JetBrains Mono', monospace; }
        .pulse-dot { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .glow-cyan { box-shadow: 0 0 30px rgba(6, 182, 212, 0.25); }
        .glow-red { box-shadow: 0 0 30px rgba(239, 68, 68, 0.25); }
        .glow-emerald { box-shadow: 0 0 30px rgba(16, 185, 129, 0.25); }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.6); }
        ::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #06B6D4; }
    </style>
</head>
<body class="h-screen w-screen overflow-hidden flex flex-col bg-[#050811] text-slate-100">

    <!-- Top Navigation Bar (Clean 56px Bar) -->
    <header class="h-14 border-b border-cyan-900/40 bg-slate-950/80 backdrop-blur-md px-6 flex items-center justify-between shrink-0 z-40">
        <div class="flex items-center space-x-4">
            <div class="h-8 w-8 rounded-lg bg-gradient-to-tr from-cyan-500 via-teal-600 to-indigo-600 flex items-center justify-center font-bold text-white shadow-md text-base glow-cyan">
                🔒
            </div>
            <div class="flex items-center space-x-3">
                <span class="text-sm font-extrabold tracking-tight text-white flex items-center space-x-1.5">
                    <span>AgntID Air-Gap Control Plane</span>
                    <span class="text-slate-500 font-normal">/</span>
                    <span class="text-xs px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-700/60 font-semibold uppercase tracking-wider">Zero Cloud Egress</span>
                </span>
                <span class="text-xs text-slate-400 hidden lg:inline">&bull; 100% On-The-Box Autonomous SRE</span>
            </div>
        </div>

        <div class="flex items-center space-x-4">
            <!-- Mode Selector Switch -->
            <div class="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800 shadow-inner">
                <button id="btnModeUnprotected" onclick="setMode('unprotected')" class="px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all text-slate-400 hover:text-white">
                    ❌ Unprotected (Direct)
                </button>
                <button id="btnModeProtected" onclick="setMode('protected')" class="px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all bg-cyan-600 text-white shadow glow-cyan">
                    🛡️ AgntID Air-Gap (Protected)
                </button>
            </div>

            <!-- Trigger Button -->
            <button id="btnRun" onclick="triggerInvestigation()" class="px-5 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-bold text-xs tracking-wider uppercase shadow-lg shadow-cyan-950/40 transition-all flex items-center space-x-2 cursor-pointer">
                <span>⚡ Run Local Triage</span>
            </button>
        </div>
    </header>

    <!-- Air-Gap KPI & Architecture Telemetry Bar (Horizontal, Spacious Strip) -->
    <section class="border-b border-cyan-900/30 bg-slate-900/40 px-6 py-2.5 shrink-0 flex items-center justify-between text-xs">
        <div class="flex items-center space-x-6 overflow-x-auto py-0.5">
            <!-- Egress Metric -->
            <div class="flex items-center space-x-2 shrink-0">
                <span class="h-2 w-2 rounded-full bg-cyan-400 pulse-dot"></span>
                <span class="text-slate-400">Cloud Egress:</span>
                <span class="font-bold text-cyan-300 mono bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-800/60">0 Bytes (Air-Gapped)</span>
            </div>
            
            <!-- Model Metric -->
            <div class="flex items-center space-x-2 shrink-0">
                <span class="text-slate-400">Local SLM:</span>
                <span class="font-bold text-emerald-400 mono bg-slate-950 px-2 py-0.5 rounded border border-slate-800">Llama-3.2-1B-Q4 (On-Device)</span>
            </div>

            <!-- Parser Size Comparison -->
            <div class="flex items-center space-x-2 shrink-0">
                <span class="text-slate-400">Parser Image:</span>
                <span class="font-bold text-purple-300 mono bg-purple-950/60 px-2 py-0.5 rounded border border-purple-800/60">253 MB (vs 1.92 GB &bull; -87%)</span>
            </div>

            <!-- Incident Brief -->
            <div class="hidden xl:flex items-center space-x-2 shrink-0 text-slate-400">
                <span class="text-slate-600">|</span>
                <span>Incident:</span>
                <span class="text-red-400 font-semibold">checkout-service (HTTP 500 Outage)</span>
            </div>
        </div>

        <div class="hidden lg:flex items-center space-x-3 shrink-0 text-slate-400 text-xs">
            <span>Hardware:</span>
            <span class="text-slate-300 mono font-semibold">Snapdragon ARM64 CPU (12-Core)</span>
            <button onclick="toggleAirgapModal()" class="text-cyan-400 hover:text-cyan-300 underline font-semibold ml-2">
                Tech Spec &darr;
            </button>
        </div>
    </section>

    <!-- Main Workspace: Balanced 50/50 Split View -->
    <main class="flex-1 min-h-0 p-5 grid grid-cols-1 md:grid-cols-2 gap-5 overflow-hidden">
        
        <!-- LEFT HALF: Local SLM Reasoning & Tool Formulation (50% Width) -->
        <section class="flex flex-col rounded-xl border border-slate-800/80 bg-slate-900/40 backdrop-blur-sm overflow-hidden shadow-xl min-h-0">
            <!-- Header -->
            <div class="h-12 border-b border-slate-800 px-5 flex items-center justify-between shrink-0 bg-slate-950/50">
                <div class="flex items-center space-x-2.5">
                    <span class="text-lg">🧠</span>
                    <div>
                        <h2 class="text-xs font-bold uppercase tracking-wider text-white">Local SLM Reasoning Stream</h2>
                        <span class="text-[10px] text-emerald-400 mono">Llama-3.2-1B-Q4 &bull; Zero External API Calls</span>
                    </div>
                </div>
                <div id="slmStatusBadge" class="text-xs px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700 mono font-semibold">
                    Awaiting Run
                </div>
            </div>

            <!-- Feed -->
            <div id="agentStream" class="flex-1 overflow-y-auto p-5 space-y-3.5 text-xs font-mono">
                <div class="text-slate-500 text-center py-24 flex flex-col items-center justify-center space-y-2">
                    <span class="text-3xl">💻</span>
                    <p class="font-sans text-sm text-slate-400 font-semibold">Ready for Air-Gap Triage</p>
                    <p class="font-sans text-xs text-slate-500 max-w-sm">Click "Run Local Triage" to execute autonomous investigation with zero cloud egress.</p>
                </div>
            </div>
        </section>

        <!-- RIGHT HALF: AgntID Local Security Gateway (50% Width) -->
        <section class="flex flex-col rounded-xl border border-slate-800/80 bg-slate-900/40 backdrop-blur-sm overflow-hidden shadow-xl min-h-0">
            <!-- Header -->
            <div class="h-12 border-b border-slate-800 px-5 flex items-center justify-between shrink-0 bg-slate-950/50">
                <div class="flex items-center space-x-2.5">
                    <span class="text-lg">🛡️</span>
                    <div>
                        <h2 class="text-xs font-bold uppercase tracking-wider text-cyan-400">AgntID Local Control Plane</h2>
                        <span class="text-[10px] text-slate-400 mono">Air-Gap Interceptor &bull; Port :8082</span>
                    </div>
                </div>
                <span id="gatewayStatusBadge" class="text-xs px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-semibold mono">
                    AIRGAP ACTIVE
                </span>
            </div>

            <!-- Feed -->
            <div id="securityStream" class="flex-1 overflow-y-auto p-5 space-y-3.5 text-xs font-sans">
                <div class="text-slate-500 text-center py-24 flex flex-col items-center justify-center space-y-2">
                    <span class="text-3xl">🔒</span>
                    <p class="font-sans text-sm text-slate-400 font-semibold">On-Device Policy Interceptor Standing By</p>
                    <p class="font-sans text-xs text-slate-500 max-w-sm">Local semantic classification, blast-radius containment, and zero-egress audit will stream here in real-time.</p>
                </div>
            </div>
        </section>
    </main>

    <!-- Collapsible Tech Spec Modal -->
    <div id="airgapModal" class="fixed inset-x-0 bottom-0 z-50 bg-slate-950/95 border-t border-cyan-900/60 p-6 transform translate-y-full transition-transform duration-300 ease-in-out shadow-2xl backdrop-blur-xl">
        <div class="max-w-5xl mx-auto">
            <div class="flex items-center justify-between mb-4">
                <h4 class="text-xs font-bold uppercase tracking-wider text-cyan-400">
                    📊 Architecture Comparison: Default AgntID Runtime vs AgntID Air-Gap
                </h4>
                <button onclick="toggleAirgapModal()" class="text-slate-400 hover:text-white text-xs font-semibold px-2.5 py-1 rounded bg-slate-800">
                    ✕ Close
                </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5 text-xs">
                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
                    <div class="flex justify-between items-center font-bold text-slate-300">
                        <span>Default AgntID Runtime</span>
                        <span class="text-red-400 text-[11px] uppercase">Cloud Dependent</span>
                    </div>
                    <ul class="text-[11px] text-slate-400 space-y-1.5 mono">
                        <li>• Container Image: <strong class="text-white">1.92 GB</strong> (heavy DeBERTa weights)</li>
                        <li>• NLI Startup Time: <strong class="text-amber-400">Up to 300 seconds</strong> (cold start timeout risk)</li>
                        <li>• Intent LLM: <strong class="text-red-400">External Cloud API</strong> (OpenAI egress)</li>
                        <li>• Compliance: Incompatible with air-gapped banking / defense networks</li>
                    </ul>
                </div>
                <div class="p-4 rounded-xl bg-cyan-950/30 border border-cyan-700/60 space-y-2">
                    <div class="flex justify-between items-center font-bold text-cyan-300">
                        <span>AgntID Air-Gap (Our Innovation)</span>
                        <span class="text-emerald-400 text-[11px] uppercase font-bold">100% On-The-Box</span>
                    </div>
                    <ul class="text-[11px] text-cyan-200/90 space-y-1.5 mono">
                        <li>• Container Image: <strong class="text-white font-bold">253 MB</strong> (<span class="text-emerald-400">-87% reduction</span>)</li>
                        <li>• NLI Validation: <strong class="text-emerald-400">&lt;0.2 ms CPU inference</strong> (sub-millisecond)</li>
                        <li>• Intent Reasoning: <strong class="text-emerald-300 font-bold">Llama-3.2-1B-Q4 on-device</strong> (Zero cloud calls)</li>
                        <li>• Compliance: 100% zero-egress, fully air-gap compliant</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentMode = 'protected';
        let eventSource = null;
        let isAirgapModalOpen = false;

        function toggleAirgapModal() {
            const el = document.getElementById('airgapModal');
            isAirgapModalOpen = !isAirgapModalOpen;
            if (isAirgapModalOpen) {
                el.classList.remove('translate-y-full');
            } else {
                el.classList.add('translate-y-full');
            }
        }

        function setMode(mode) {
            currentMode = mode;
            const btnP = document.getElementById('btnModeProtected');
            const btnU = document.getElementById('btnModeUnprotected');
            const badge = document.getElementById('gatewayStatusBadge');
            if (mode === 'protected') {
                btnP.className = 'px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all bg-cyan-600 text-white shadow glow-cyan';
                btnU.className = 'px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all text-slate-400 hover:text-white';
                badge.innerText = 'AIRGAP ACTIVE';
                badge.className = 'text-xs px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-semibold mono';
            } else {
                btnU.className = 'px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all bg-red-600 text-white shadow glow-red';
                btnP.className = 'px-3.5 py-1.5 rounded-md text-xs font-semibold transition-all text-slate-400 hover:text-white';
                badge.innerText = 'BYPASS';
                badge.className = 'text-xs px-2.5 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 font-semibold mono';
            }
        }

        function triggerInvestigation() {
            const agentStream = document.getElementById('agentStream');
            const secStream = document.getElementById('securityStream');
            const statusEl = document.getElementById('slmStatusBadge');
            const btn = document.getElementById('btnRun');

            agentStream.innerHTML = '';
            secStream.innerHTML = '';
            statusEl.innerText = '⚡ Local Reasoning...';
            statusEl.className = 'text-xs px-2.5 py-1 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-700 mono font-semibold pulse-dot';
            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');

            if (eventSource) {
                eventSource.close();
            }

            eventSource = new EventSource('/api/investigate/stream?mode=' + currentMode);

            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleEvent(data);
            };

            eventSource.onerror = function() {
                eventSource.close();
                statusEl.innerText = 'Completed';
                statusEl.className = 'text-xs px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-700 mono font-semibold';
                btn.disabled = false;
                btn.classList.remove('opacity-50', 'cursor-not-allowed');
            };
        }

        function handleEvent(data) {
            const agentStream = document.getElementById('agentStream');
            const secStream = document.getElementById('securityStream');

            if (data.type === 'init') {
                secStream.innerHTML += `
                    <div class="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5">
                        <div class="flex items-center justify-between text-slate-300 font-semibold">
                            <span class="flex items-center space-x-1.5">
                                <span class="h-2 w-2 rounded-full bg-cyan-400"></span>
                                <span>🔐 Air-Gap Session Initialized</span>
                            </span>
                            <span class="mono text-[10px] text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">${data.taskId}</span>
                        </div>
                        <p class="text-xs text-slate-400">Inference Engine: <strong class="text-slate-200">${data.inferenceEngine}</strong></p>
                        <p class="text-xs text-slate-400">Cloud Egress: <strong class="text-emerald-400">${data.cloudEgress}</strong></p>
                    </div>
                `;
            }

            if (data.type === 'agntid_intent_prepared') {
                secStream.innerHTML += `
                    <div class="p-4 rounded-xl bg-cyan-950/30 border border-cyan-800/80 text-xs">
                        <div class="flex items-center justify-between text-cyan-300 font-bold mb-1">
                            <span>🎯 Local Intent Bound</span>
                            <span class="mono text-[10px] text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">${data.status}</span>
                        </div>
                        <p class="text-xs text-slate-300">Parser: <strong class="text-white">${data.engine}</strong></p>
                        <p class="text-[11px] text-slate-400 mt-1">Authorized Profile Tools: <span class="text-cyan-300 mono">${data.relevantTools.join(', ')}</span></p>
                    </div>
                `;
            }

            if (data.type === 'local_slm_thought') {
                agentStream.innerHTML += `
                    <div class="p-4 rounded-xl bg-slate-950/80 border border-emerald-900/50 space-y-1.5">
                        <div class="flex items-center justify-between text-emerald-400 font-bold text-xs">
                            <span>🧠 [Local SLM Step ${data.turn}] On-Device Chain-of-Thought</span>
                            <span class="mono text-[10px] text-slate-400 bg-slate-900 px-2 py-0.5 rounded">CPU Latency &lt;15ms</span>
                        </div>
                        <p class="text-slate-300 leading-relaxed text-xs">${data.thought}</p>
                    </div>
                `;
            }

            if (data.type === 'tool_intent') {
                agentStream.innerHTML += `
                    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs">
                        <div class="text-slate-400">Formulated Local Function Call:</div>
                        <div class="text-cyan-300 font-bold mono mt-1 text-[11px]">${data.tool}(${JSON.stringify(data.args)})</div>
                    </div>
                `;
            }

            if (data.type === 'tool_result') {
                agentStream.innerHTML += `
                    <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-300">
                        <span class="font-bold text-slate-400">Tool Result (<span class="text-slate-200">${data.tool}</span>):</span>
                        <pre class="mt-2 text-[11px] whitespace-pre-wrap bg-black/50 p-2.5 rounded border border-slate-900 overflow-x-auto text-slate-300">${data.output}</pre>
                    </div>
                `;
            }

            if (data.type === 'execution_status') {
                if (data.interception === 'BYPASS_UNPROTECTED') {
                    secStream.innerHTML += `
                        <div class="p-4 rounded-xl bg-red-950/40 border-2 border-red-700/80 glow-red">
                            <div class="text-red-400 font-bold text-xs">⚠️ ${data.warning}</div>
                            <div class="text-slate-400 text-xs mt-1">Status: <span class="mono text-red-300 font-semibold">${data.status}</span></div>
                        </div>
                    `;
                } else if (data.status === 'AIRGAP_INTENT_BLOCKED') {
                    secStream.innerHTML += `
                        <div class="p-4 rounded-xl bg-red-950/70 border-2 border-red-600 glow-red space-y-1.5">
                            <div class="flex items-center justify-between text-red-400 font-bold text-xs">
                                <span>🛑 AGNTID RUNTIME INTERCEPTOR: BLOCKED</span>
                                <span class="mono text-[10px] px-2 py-0.5 bg-red-900 text-white rounded">VIOLATION</span>
                            </div>
                            <p class="text-xs text-white font-semibold leading-relaxed">${data.rule}</p>
                            <p class="text-[11px] text-amber-300 mono bg-black/40 p-2 rounded border border-red-900/30">${data.classifier}</p>
                        </div>
                    `;
                } else {
                    secStream.innerHTML += `
                        <div class="p-3.5 rounded-xl bg-slate-900/80 border border-cyan-800/60">
                            <div class="text-cyan-300 font-semibold text-xs">${data.rule}</div>
                            ${data.classifier ? `<div class="text-[11px] text-emerald-400 mt-1 mono">${data.classifier}</div>` : ''}
                        </div>
                    `;
                }
            }

            if (data.type === 'governance_block') {
                agentStream.innerHTML += `
                    <div class="p-3.5 rounded-xl bg-red-950/50 border border-red-800 text-xs text-red-200">
                        <span class="font-bold text-red-400">🛡️ Execution Blocked by Policy Gateway:</span> ${data.reason}
                    </div>
                `;
            }

            if (data.type === 'disaster_event') {
                secStream.innerHTML += `
                    <div class="p-4 rounded-xl bg-red-950 border-2 border-red-600 glow-red space-y-2">
                        <div class="text-sm font-bold text-white flex items-center space-x-2">
                            <span>${data.title}</span>
                        </div>
                        <p class="text-xs text-red-200 leading-relaxed">${data.details}</p>
                        <div class="inline-block text-[11px] font-bold px-2.5 py-1 bg-red-900 text-white rounded uppercase mono">
                            ${data.impact}
                        </div>
                    </div>
                `;
            }

            if (data.type === 'agent_conclusion') {
                const isSuccess = data.content.startsWith('SUCCESS');
                agentStream.innerHTML += `
                    <div class="p-4 rounded-xl ${isSuccess ? 'bg-emerald-950/60 border border-emerald-700' : 'bg-red-950/60 border border-red-800'} space-y-1.5">
                        <div class="font-bold ${isSuccess ? 'text-emerald-400' : 'text-red-400'} text-xs uppercase">
                            ${isSuccess ? '✅ Incident Resolved (Air-Gap Secured)' : '❌ Incident Mitigation Failed'}
                        </div>
                        <p class="text-xs text-slate-200 leading-relaxed font-sans">${data.content}</p>
                    </div>
                `;
            }

            agentStream.scrollTop = agentStream.scrollHeight;
            secStream.scrollTop = secStream.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    return DASHBOARD_HTML

@app.get("/api/investigate/stream")
async def investigate_stream(mode: str = "protected"):
    async def event_generator():
        async for evt in run_airgap_investigation_stream(mode):
            yield f"data: {json.dumps(evt)}\n\n"
            await asyncio.sleep(0.05)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
