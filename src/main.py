import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.layer1_understanding.extractor import PrimaryUnderstandingEngine
from src.layer2_decision.decision_engine import ResearchDecisionEngine
from src.layer3_research.research_engine import ResearchSimulationEngine

app = FastAPI(title="AI Research Lab")

understanding_engine = PrimaryUnderstandingEngine()
decision_engine = ResearchDecisionEngine()
research_engine = ResearchSimulationEngine()

class UserInput(BaseModel):
    message: str

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Research Lab Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { background-color: #0B0F19; color: #94A3B8; font-family: system-ui, -apple-system, sans-serif; }
        .glass-panel { background: #111827; border: 1px solid #1E293B; border-radius: 12px; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden text-sm">

    <!-- Header -->
    <header class="h-14 border-b border-slate-800 bg-slate-900/60 px-4 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold">AI</div>
            <div>
                <h1 class="font-semibold text-white leading-tight">AI Research Lab</h1>
                <p class="text-xs text-slate-500">From Ideas to Discovery</p>
            </div>
        </div>

        <div class="w-1/3 relative">
            <input type="text" placeholder="Search in your research..." class="w-full bg-slate-950 border border-slate-800 rounded-lg py-1.5 px-3 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
        </div>

        <div class="flex items-center gap-4">
            <i data-lucide="bell" class="w-4 h-4 cursor-pointer hover:text-white"></i>
            <i data-lucide="settings" class="w-4 h-4 cursor-pointer hover:text-white"></i>
            <div class="flex items-center gap-2 pl-2 border-l border-slate-800">
                <div class="w-7 h-7 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-semibold">AC</div>
                <span class="text-xs text-slate-300 font-medium">Alex Carter</span>
            </div>
        </div>
    </header>

    <!-- Workspace -->
    <div class="flex flex-1 overflow-hidden">
        
        <!-- Sidebar -->
        <aside class="w-52 border-r border-slate-800 p-3 flex flex-col justify-between shrink-0">
            <nav class="space-y-1">
                <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg bg-blue-600 text-white font-medium"><i data-lucide="layout-dashboard" class="w-4 h-4"></i> Research Workspace</a>
                <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-800/50"><i data-lucide="compass" class="w-4 h-4"></i> Research Explorer</a>
                <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-800/50"><i data-lucide="box" class="w-4 h-4"></i> 3D Simulator</a>
                <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-400 hover:bg-slate-800/50"><i data-lucide="notebook" class="w-4 h-4"></i> Notebook</a>
            </nav>

            <div class="glass-panel p-3">
                <div class="flex items-center justify-between text-xs mb-1">
                    <span class="text-slate-400">Local Storage</span>
                    <span class="text-slate-200 font-semibold">12.4 GB / 50 GB</span>
                </div>
                <div class="w-full bg-slate-800 rounded-full h-1.5">
                    <div class="bg-blue-500 h-1.5 rounded-full" style="width: 25%"></div>
                </div>
            </div>
        </aside>

        <!-- Main Grid -->
        <main class="flex-1 p-4 grid grid-cols-12 gap-4 overflow-y-auto">
            
            <!-- Left: Specification & Sources -->
            <div class="col-span-3 space-y-4">
                <div class="glass-panel p-4">
                    <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Layer 1: Research Spec</h2>
                    <div id="spec-display" class="text-xs text-slate-300 space-y-1">
                        <p><strong class="text-slate-400">Objective:</strong> <span id="spec-obj" class="text-white">None</span></p>
                    </div>
                </div>

                <div class="glass-panel p-4">
                    <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Layer 3: Retrieved Research</h2>
                    <div id="sources-list" class="space-y-2 text-xs text-slate-400">
                        <p class="italic">Enter an objective to retrieve papers and tools...</p>
                    </div>
                </div>
            </div>

            <!-- Center: 3D Workspace Simulator -->
            <div class="col-span-6 glass-panel p-4 flex flex-col">
                <div class="flex items-center justify-between mb-3">
                    <div class="flex items-center gap-2">
                        <h2 class="text-white font-semibold">3D Simulation Workspace</h2>
                        <span id="evidence-badge" class="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-medium bg-amber-500/10 text-amber-400">Conceptual Visualization</span>
                    </div>
                </div>

                <div id="canvas-container" class="flex-1 w-full rounded-lg bg-slate-950 overflow-hidden relative"></div>
            </div>

            <!-- Right: AI Assistant Chat -->
            <div class="col-span-3 glass-panel p-4 flex flex-col justify-between">
                <div>
                    <h2 class="text-white font-semibold flex items-center gap-2 mb-3 border-b border-slate-800 pb-2">
                        <i data-lucide="sparkles" class="w-4 h-4 text-blue-400"></i> AI Research Assistant
                    </h2>

                    <div id="chat-messages" class="space-y-3 overflow-y-auto max-h-[calc(100vh-280px)] pr-1">
                        <div class="bg-blue-950/40 border border-blue-900/50 p-3 rounded-lg text-xs text-blue-200">
                            Describe your research idea or goal below.
                        </div>
                    </div>
                </div>

                <div class="mt-4 border-t border-slate-800 pt-3">
                    <div class="flex gap-2">
                        <input type="text" id="chat-input" placeholder="e.g. 3D holographic display..." class="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500">
                        <button onclick="handleSend()" class="bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-500"><i data-lucide="send" class="w-4 h-4"></i></button>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <script>
        lucide.createIcons();

        // Three.js Scene Setup
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const geometry = new THREE.OctahedronGeometry(1.2);
        const material = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
        const prism = new THREE.Mesh(geometry, material);
        scene.add(prism);

        camera.position.z = 3.5;

        function animate() {
            requestAnimationFrame(animate);
            prism.rotation.y += 0.008;
            renderer.render(scene, camera);
        }
        animate();

        async function handleSend() {
            const input = document.getElementById('chat-input');
            const messages = document.getElementById('chat-messages');
            const specObj = document.getElementById('spec-obj');
            const sourcesList = document.getElementById('sources-list');

            const text = input.value.trim();
            if (!text) return;

            messages.innerHTML += `<div class="bg-slate-800 p-2.5 rounded-lg text-xs text-slate-200"><strong>User:</strong> ${text}</div>`;
            input.value = '';

            const res = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await res.json();
            
            // Update Spec
            specObj.innerText = data.spec.objective || 'None';

            // Update Sources (Layer 3)
            sourcesList.innerHTML = data.sources.map(s => `
                <div class="p-2 bg-slate-900 border border-slate-800 rounded">
                    <p class="text-blue-400 font-semibold">${s.title}</p>
                    <p class="text-[10px] text-slate-500">${s.authors_or_org} • ${s.evidence_type}</p>
                    <p class="text-slate-300 mt-1">${s.summary}</p>
                </div>
            `).join('');

            // Update Chat
            messages.innerHTML += `
                <div class="bg-slate-900 border border-slate-800 p-2.5 rounded-lg text-xs space-y-1">
                    <p class="text-emerald-400 font-semibold">[Layer 2 Decision]</p>
                    <p class="text-slate-300">${data.decision.action}: ${data.decision.detail}</p>
                </div>
            `;
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTML_LAYOUT

@app.post("/api/process")
async def process_user_input(payload: UserInput):
    # Layer 1
    updated_spec = understanding_engine.parse_input(payload.message)
    
    # Layer 2
    next_action = decision_engine.determine_next_action(updated_spec)
    action_detail = next_action.get("question") or next_action.get("prompt", "")

    # Layer 3
    sources = []
    if updated_spec.objective:
        sources = research_engine.search_knowledge_base(updated_spec.objective.value)

    return {
        "spec": {
            "objective": updated_spec.objective.value if updated_spec.objective else None
        },
        "decision": {
            "action": next_action["action"].value,
            "detail": action_detail
        },
        "sources": [
            {
                "title": s.title,
                "authors_or_org": s.authors_or_org,
                "summary": s.summary,
                "evidence_type": s.evidence_type
            } for s in sources
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
