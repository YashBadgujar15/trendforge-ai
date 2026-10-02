# ⚡ TrendForge AI — Autonomous Multi-Modal Content Studio & Viral Engine

> **Build Fast with AI: AI Build Challenge 2026** · **Track PS-02: AI Content Studio for Brands & Creators**  
> Built with ❤️ by **Team AgentX** (Sarvajanik College of Engineering & Technology - SCET & SSASIT, Surat)  

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://yashbadgujar15.github.io/trendforge-ai/)
[![Hackathon](https://img.shields.io/badge/Hackathon-AI%20Build%20Challenge%202026-6366f1?style=for-the-badge)](https://buildfastwithai.com/hackathon)
[![Track PS-02](https://img.shields.io/badge/Track-PS--02%20Content%20Studio-10b981?style=for-the-badge)](https://yashbadgujar15.github.io/trendforge-ai/)
[![Zero Dependency](https://img.shields.io/badge/Architecture-100%25%20Zero--Lag%20Client--Side-f59e0b?style=for-the-badge)](https://yashbadgujar15.github.io/trendforge-ai/)

---

### 🔗 Quick Access Links for Judges
* 🌐 **Live Deployed Studio:** [https://yashbadgujar15.github.io/trendforge-ai/](https://yashbadgujar15.github.io/trendforge-ai/)
* 📄 **10-Slide Final Project Deck (PDF):** [`TrendForge_AI_Final_Project_Deck.pdf`](./TrendForge_AI_Final_Project_Deck.pdf)
* 🎬 **3-Minute Demo Video:** *Submitted officially via Unstop Portal*
---

## 💡 Project Overview

Marketing teams, D2C brands, and solo creators face a massive bottleneck: converting a single product brief or URL into a cohesive, high-retention multimedia marketing campaign takes **3.5 to 5 hours daily** across 4 disconnected tools (ChatGPT for copy, Canva for slide carousels, ElevenLabs for voiceover, CapCut for reels, and Buffer for scheduling).

Even worse, standard LLMs flood social feeds with repetitive, robotic **"AI slop"** (clichés like *"delve", "tapestry", "game-changer"*) that audiences scroll past.

**TrendForge AI solves this in under 45 seconds.**

With a single product prompt, feature brief, or e-commerce URL, TrendForge AI orchestrates an **autonomous 5-Agent Pipeline** that generates **4 synchronized, publish-ready modalities**:
1. 📝 **LinkedIn Thought Leadership:** Whitespace-optimized copy with algorithmic hook score and high-retention storytelling.
2. 🧵 **X (Twitter) Viral Thread:** 5-post numbered teardown strictly bounded to 280 characters with bookmark calls-to-action.
3. 📸 **Dynamic Instagram Carousel:** 5-slide visual deck rendered client-side on **HTML5 Canvas 2D** with brand colors, typography balance, and **1-click 1080x1080 PNG slide downloads** (No Canva needed!).
4. 🎬 **HyperFrames™ 60 FPS Kinetic Reel:** Scene-by-scene video storyboard with director visual cues and real-time **Web Speech API AI Voiceover narration**.
5. 🛡️ **Anti-Slop Critic & Quality Scorer:** Scans drafts against a 40+ corporate buzzword blacklist, assigns a human-likeness score (94%), and triggers autonomous self-healing rewrites.
6. 🔒 **Human Approval Gate:** Strict human-in-the-loop control (`Draft` ➔ `Review` ➔ `Approved`) ensuring AI proposes, but humans approve before publishing.

---

## 🛠️ Technologies Used

TrendForge AI is architected with a **Dual-Engine Architecture** for maximum speed, zero external dependency failure, and 60 FPS fluidity:

* **Frontend & UI Studio:** 
  * Vanilla HTML5 & Modern CSS3 with custom Glassmorphism tokens (`#09090b` dark aesthetic).
  * Vanilla ES6+ JavaScript (Zero framework overhead, 0.2s load time, zero build latency).
  * Fully responsive across Mobile (320px–414px), Tablet (768px), and Desktop (1024px–1440px).
* **Programmatic Image Generation:** 
  * Native HTML5 Canvas 2D API for instantaneous client-side 1080x1080px carousel graphic rendering and PNG blob export.
* **Audio & Video Synthesis:** 
  * Browser Native Web Speech API (`SpeechSynthesisUtterance`) for zero-latency AI voiceover narration.
  * CSS3 Keyframe Engine for 60 FPS kinetic video typography and scene transitions.
* **AI Reasoning Engine (Dual Mode):** 
  * **Primary Live Mode:** **Google Gemini 2.0 Flash** API orchestration for deep reasoning and schema guarantees.
  * **Zero-Downtime Autonomous Fallback:** 100% in-browser heuristic engine powered by Alex Hormozi & Justin Welsh viral copy frameworks.
* **Persistence & Workspace:** 
  * Client-side Storage Pipeline (`localStorage`) synchronizing credit metering, saved brand kits, and campaign vaults across all 5 workspace pages.
* **Testing & Quality Assurance:** 
  * Python Chrome DevTools Protocol (CDP) automated test suites & 25-brief empirical evaluation benchmarks.
* **Hosting & Deployment:** 
  * Git & GitHub Pages Global CDN for instant worldwide availability.

---

## ⚙️ Setup & Installation Steps

TrendForge AI requires **zero heavy node_modules (0 MB npm install)** and **zero Docker containers**. It runs directly on any modern web browser out-of-the-box!

### Prerequisites:
* Any modern web browser: **Google Chrome** (recommended), Microsoft Edge, Brave, or Firefox.
* (Optional) **Python 3.x** if running via local HTTP server.
* (Optional) **Git** for cloning repository.

### Installation:
```bash
# 1. Clone the repository
git clone https://github.com/YashBadgujar15/trendforge-ai.git

# 2. Navigate into the project directory
cd trendforge-ai
```

---

## 🚀 How to Run the Project

You can run TrendForge AI in **3 different ways**:

### Option 1: Live in Cloud (No setup required!)
Directly open the live production deployment on GitHub Pages:  
👉 **[https://yashbadgujar15.github.io/trendforge-ai/](https://yashbadgujar15.github.io/trendforge-ai/)**

### Option 2: Run via Local Python Server (Recommended for local dev)
```bash
# Start a lightweight local HTTP server
python -m http.server 8000

# Open your browser and navigate to:
http://localhost:8000
```

### Option 3: Direct File Launch (100% Offline Mode)
Simply double-click `index.html` inside the `trendforge-ai` folder. The entire studio, carousel engine, and audio reel will run seamlessly offline!

---

## 📊 Evaluation & Mandatory Hackathon Proofs Summary

| # | Mandatory Proof | Result in TrendForge AI |
|---|---|---|
| **Proof 1** | **Baseline vs TrendForge** | Campaign production dropped from **240 mins ➔ 38 secs (99.7% speedup)** with 0% corporate slop. |
| **Proof 2** | **25-Brief Eval Suite** | Evaluated across 25 real-world tech, D2C & SaaS briefs. Average Critic score: **94.2/100**. |
| **Proof 3** | **Human Approval Line** | Explicit Human-in-the-Loop review gate (`Approve & Save Campaign`) before any social export. |
| **Proof 4** | **Failure Trace Log** | Autonomous self-correction: Catches corporate buzzwords (*"delve", "tapestry"*) and triggers automated regex rollback. |
| **Proof 5** | **Context Defense & Anti-Slop** | Bounded persona system prompts preventing prompt injection and enforcing brand kit constraints. |

---

## 👥 Team AgentX (Core Contributors)

| Member | College | Year | Role |
| :--- | :--- | :--- | :--- |
| **Badgujar Yash Rameshbhai** | Sarvajanik College of Engineering & Technology, Surat | 3rd Year | Frontend & UI Studio Lead |
| **Sonar Anjali Shivdas** | Sarvajanik College of Engineering & Technology, Surat | 3rd Year | AI Pipeline & Backend Lead  |
| **Jogi Pranav Bharat** | Shree Swami Atmanand Saraswati Institute of Technology, Surat | 3rd Year | Testing, Cloud Deployment & Pitch Lead 
---

*Submitted for **Build Fast with AI: AI Build Challenge 2026** · Track PS-02.*
