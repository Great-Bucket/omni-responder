# Omni-Responder: DGX Spark 🚨⚡

> **Autonomous, Privacy-First Emergency Dispatch on NVIDIA DGX Spark**  
> *The "See + Do" Remix: Edge vision perception (NVIDIA Cosmos Reasoner 2) coupled with deterministic, rule-based multi-agent crisis dispatch — all on-device.*

---

## 🌟 Overview

**Omni-Responder** is an edge-native, real-time emergency dispatch platform designed for the **NVIDIA DGX Spark** (Grace Blackwell GB10 with 128GB Unified Memory). It continuously analyzes surveillance and traffic camera video feeds locally, identifies physical crises (multi-vehicle pileups, chemical tanker ruptures, structural fires), and autonomously coordinates specialized sub-agents—**with zero raw video ever leaving the edge device**.

```mermaid
flowchart TD
    subgraph Edge ["NVIDIA DGX Spark (Edge - 128GB Unified Memory)"]
        A["Live Camera Feed / Simulated Streams<br>(data/video_clips/)"] --> B["Perception Engine<br>(NVIDIA Cosmos Reasoner 2 - Port 30082)"]
        B -->|"Structured JSON Context"| C["Master Incident Orchestrator<br>(deterministic rule engine — no LLM call)"]
        
        C --> D["🧪 Hazmat Sub-Agent"]
        C --> E["🚦 Traffic Sub-Agent"]
        C --> F["📻 Comms CAD Sub-Agent"]
        C --> G["📱 Emergency Response Notifier"]
        
        D --> D1["Local ERG 2024 Chemical DB<br>(data/hazmat_db.json)"]
        E --> E1["City Digital Signs (VMS) & Signal Controls"]
        F --> F1["911 CAD Dispatch Cards (CODE RED / AMBER)"]
        G --> G1["Field Alerts to Responders<br>(Telegram stand-in)"]
    end
```

---

## 🚀 Key Technical Highlights

1. **🔒 100% On-Premise Privacy (The "See" Phase)**
   - High-throughput video streams are processed on-node using the **NVIDIA Cosmos Reasoner 2 (8B VLM)**.
   - Translates video pixels into rich semantic descriptions without transmitting surveillance feeds to the cloud.

2. **⚡ Grace Blackwell 128GB Unified Memory (The "Do" Phase)**
   - The VSS stack loads the **8B Cosmos Reasoner VLM** and a **Nemotron Nano 9B FP8 NIM** into the shared GPU 0 memory pool — the unified-memory headroom is what makes co-residency possible.
   - **Dispatch itself does not use the LLM.** Once perception returns, orchestration is deterministic Python: rule evaluation, an ERG table lookup, and templated output. That is a design choice, not a shortcut — dispatch decisions that put responders in a hot zone should be reproducible and auditable, and a rules engine is both.

3. **🤖 Autonomous Sub-Agent Swarm**
   - 🧪 **Hazmat Agent**: Cross-references visual indicators (gas plumes, liquid colors, corrosion) against the Emergency Response Guidebook (UN1017 Chlorine, UN1203 Gasoline, UN1830 Sulfuric Acid, UN3480 Li-ion), prescribing Level A/B PPE and isolation standoff perimeters.
   - 🚦 **Traffic Agent**: Generates automated perimeter closures, Variable Message Sign (VMS) detour alerts, and emergency green-wave signal corridors.
   - 📻 **Comms Agent**: Synthesizes 911 Computer-Aided Dispatch (CAD) cards with priority codes and target responder unit routing.
   - 📱 **Emergency Response Notifier**: Broadcasts the finalized CAD dispatch summaries directly to field responders via secure Telegram API routing (automatically muted for routine 'All Clear' events), as a stand-in for actual emergency response communication.

---

## 📂 Repository Structure

```
omni-responder-dgx-spark/
├── src/
│   ├── perception/          # Live Cosmos Reasoner NIM & video ingestion pipeline
│   │   ├── __init__.py
│   │   └── vss_pipeline.py
│   ├── orchestrator/        # Rule-based multi-agent dispatch loop
│   │   ├── __init__.py
│   │   └── incident_manager.py
│   ├── agents/              # Specialized domain sub-agents
│   │   ├── __init__.py
│   │   ├── hazmat_agent.py  # ERG 2024 chemical lookup & PPE selector
│   │   ├── traffic_agent.py # VMS detour broadcast & perimeter locks
│   │   └── comms_agent.py   # 911 CAD card generation
│   ├── notifiers/           # Outbound dispatch alerting
│   │   ├── __init__.py
│   │   └── telegram_notifier.py
│   ├── config/              # Hardware and endpoint configurations
│   │   ├── __init__.py
│   │   └── settings.py
│   └── main.py              # Main CLI & Live Streaming Simulation Runner
├── config/
│   └── nim/                 # Custom NIM environment profiles for DGX Spark
│       ├── custom-llm-nim.env
│       └── custom-vlm-nim.env
├── data/
│   ├── hazmat_db.json       # Local Emergency Response Guidebook dataset
│   ├── scenarios.json       # Crisis test cases & GPS coordinates
│   └── video_clips/         # Local clips only — NOT distributed with this repo
├── dashboard/               # Offline command dashboard (no npm, no CDN)
│   ├── server.py            # Event bus + static server
│   ├── adapter.py           # Bridges the pipeline to the dashboard
│   ├── index.html
│   └── fixtures/            # Synthetic replay data
├── docs/
│   └── EVENT_CONTRACT.md    # Event envelope schema
├── tests/                   # Automated unit & integration test suites
│   ├── test_pipeline.py
│   ├── test_vss_pipeline.py
│   └── test_telegram_notifier.py
├── pyproject.toml           # Project metadata & packaging
├── requirements.txt         # Core dependencies
└── README.md
```

---

## 🛠️ Developer Quickstart

### 1. Clone & Setup
```bash
git clone https://github.com/Great-Bucket/omni-responder-dgx-spark.git
cd omni-responder-dgx-spark

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies (or run with zero dependencies using standard library)
pip install -r requirements.txt
```

---

### 2. Running Omni-Responder

#### 🎬 A. Live Continuous Streaming Simulation (Recommended)
Streams the live temporal camera feed, runs Cosmos Reasoner AI analysis, and dispatches sub-agents:

```bash
# Chemical Tanker Collision (Scenario 1):
python3 -m src.main --video data/video_clips/scenario_1.mp4 --stream

# Real Multi-Vehicle Incident (Scenario 3):
python3 -m src.main --video data/video_clips/video_sample_1.mov --stream
```

#### ⚡ B. Instant Direct Analysis
Process any video file immediately without stream pacing:
```bash
python3 -m src.main --video data/video_clips/video_sample_1.mov --location "5th Ave & Market St Intersection"
```

#### 🔌 C. Output Raw JSON (For Frontend / API Integration)
```bash
python3 -m src.main --video data/video_clips/scenario_1.mp4 --json
```

---

### 3. Running the Omni-Responder Dashboard (UI)

To launch the web command center:

```bash
# On the DGX Spark
python dashboard/server.py --no-replay
```

Because the DGX is a remote server, you must forward port 8080 to your local machine to view the UI.
**On your Mac / local machine:**
```bash
ssh -L 8080:localhost:8080 <USER>@<DGX_IP_ADDRESS>
```
Then open your browser to `http://localhost:8080` to access the Command Center. Click **Upload** to select a video clip and **Run** to start the autonomous pipeline.

---

### 4. Running Automated Tests

```bash
# Run all perception and agent orchestration tests
python3 -m tests.test_vss_pipeline
python3 -m tests.test_pipeline
python3 -m tests.test_telegram_notifier
```

The tests need neither a DGX Spark nor a running model — they run anywhere with
Python 3.10+. **They do reference clips that are not distributed with this
repository, so bring your own:** without them `tests.test_pipeline` logs a
`No such file or directory` warning for `data/video_clips/scenario_1.mp4` and
still passes. That warning is expected and is not a failure.

---

## 🖥️ Deploying on NVIDIA DGX Spark

### 1. Launch NVIDIA VSS Stack on Spark
From the `video-search-and-summarization` directory on the Spark:

```bash
deploy/docker/scripts/dev-profile.sh up -p base \
  -H DGX-SPARK \
  --llm nvidia/NVIDIA-Nemotron-Nano-9B-v2-FP8 \
  --llm-env-file ~/omni-responder-dgx-spark/config/nim/custom-llm-nim.env \
  --vlm nvidia/cosmos-reason2-8b \
  --vlm-env-file ~/omni-responder-dgx-spark/config/nim/custom-vlm-nim.env
```

### 2. Active Endpoints on DGX Spark:
* **Cosmos Reasoner 2 VLM (API)**: `http://localhost:30082/v1`
* **VSS Web Chat UI**: `http://<SPARK_IP>:3000`
* **Nemotron Nano 9B FP8 LLM**: loaded into the shared GPU 0 memory pool by the launch command above. Deployed and available, but **not called by this application** — see Key Highlight 2.

---

## 📊 Datasets & Provenance

Since real-world surveillance of catastrophic events is highly sensitive and restricted, we built a comprehensive test suite using publicly available and synthetic data:
* **Video Streams (`data/video_clips/`)** — *not included in this repository; supply your own clips locally.* High-fidelity simulated crash scenarios and open-source highway dashcam clips. They represent challenging real-world edge cases (lighting changes, camera shake, partial occlusions).
* **Chemical Hazards (`data/hazmat_db.json`)**: Sourced directly from the official **2024 Emergency Response Guidebook (ERG)**, mapping visual indicators to UN numbers, protective action distances, and PPE levels.

---

## 🚧 Known Limitations & Next Steps

* **Limitations:** 
  * The perception layer currently decodes at 1 FPS. While sufficient for incident detection, tracking individual high-speed vehicles requires a higher sampling rate.
  * The VLM context window (16k) limits us to 4-frame bursts. We are mitigating this via intelligent frame selection (persistent pixel deviation).
* **Next Steps:**
  * **Audio Perception**: Ingest audio streams for tire screech and crash impact sound classification.
  * **Dynamic VLM Prompting**: Allow the Orchestrator LLM to inject specific questions back into the VLM (e.g., "I see a spill. What color is the liquid?") in a multi-turn edge feedback loop.

---

## 👥 Team

Built by three people over three days at the **NVIDIA Spark Hack Series**,
Seattle, 14–16 August 2026.

| | |
|---|---|
| **Vishal Shah** | [github.com/vshah-se](https://github.com/vshah-se) |
| **Bilal Khan** | [stragentech.com](https://www.stragentech.com) |
| **Reed O'Beirne** | [github.com/Great-Bucket](https://github.com/Great-Bucket) |

---

## 📜 Provenance

This repository is a clean-history copy of the hackathon project originally
developed at
[github.com/vshah-se/omni-responder-dgx-spark](https://github.com/vshah-se/omni-responder-dgx-spark).

**No video ships with this
repository.**

## 🖧 What you need to run it

**Got a DGX Spark and looking for something to run on it? This is ready to go.**

Omni-Responder is built for the **NVIDIA DGX Spark** (Grace Blackwell GB10,
128 GB unified memory) running the NVIDIA VSS blueprint with the Cosmos
Reasoner 2 VLM served locally. On that hardware it runs end to end today.

Three things to do after cloning:

1. **Bring your own video.** No clips ship with this repository. Drop any
   `.mp4` or `.mov` into `data/video_clips/` — traffic camera footage, dashcam
   clips, or simulated incidents. Name two of them `scenario_1.mp4` and
   `scenario_2.mp4` if you want the named scenarios in `data/scenarios.json` to
   resolve.
2. **Point it at your Spark.** The endpoints in `src/config/settings.py` default
   to `<DGX_IP_ADDRESS>` placeholders. Override them with the `SPARK_HOST`,
   `NIM_ENDPOINT_URL` and `VSS_ENDPOINT_URL` environment variables, or edit the
   file.
3. **Launch the VSS stack**, as in the deployment section below, then run the
   pipeline or the dashboard.

**No Spark? You can still see the dashboard.** Fixture-replay mode needs nothing
but Python — no GPU, no models, no network:

```bash
cd dashboard && python server.py --fixture fixtures/tanker_i5.jsonl --loop
```

---

## 🛡️ License

Apache 2.0 License.
