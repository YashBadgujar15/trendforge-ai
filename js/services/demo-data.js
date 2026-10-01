// ============================================================
// TrendForge AI — Demo Data Service
// Realistic predefined content for Demo Mode
// ============================================================

export const DEMO_BRIEF = "Launching a smart ergonomic chair for remote developers.";

export const PIPELINE_STEPS = [
  { id: 'brief',     label: 'Analyzing brief',               time: 600 },
  { id: 'audience',  label: 'Identifying target audience',   time: 500 },
  { id: 'strategy',  label: 'Generating platform strategies',time: 700 },
  { id: 'linkedin',  label: 'Writing LinkedIn post',         time: 800 },
  { id: 'twitter',   label: 'Crafting X thread',             time: 700 },
  { id: 'carousel',  label: 'Designing carousel slides',     time: 900 },
  { id: 'reel',      label: 'Building reel storyboard',      time: 600 },
  { id: 'slop',      label: 'Running anti-slop analysis',    time: 500 },
  { id: 'critic',    label: 'Critic evaluating outputs',     time: 800 },
  { id: 'refine',    label: 'Refining outputs',              time: 600 },
  { id: 'ready',     label: 'Campaign ready',                time: 300 },
];

export const DEMO_CAMPAIGN = {
  title: "Smart Ergonomic Chair Launch",
  brief: DEMO_BRIEF,
  generationTime: "47s",
  platforms: 4,
  assets: 9,
  qualityScore: 91,
  timestamp: new Date().toISOString(),

  linkedin: {
    hook: "I spent 6 years debugging my posture. Then I built the chair that fixes it for developers like me.",
    body: `Most remote developers don't have a back problem. They have a chair problem.

After 6 years of coding 10+ hours a day, I realized my setup was silently destroying my productivity — not because of bad tools, but because of a bad chair.

So we built something different.

Introducing the DevChair Pro — the first ergonomic chair engineered specifically for developers:

→ Adaptive lumbar that adjusts to your coding posture (not your "meeting posture")
→ Built-in cable management for your setup
→ Keyboard-tilt armrests that match wrist angles during extended typing
→ Thermal mesh that keeps you focused, not sweating

We tested it with 500+ developers across 18 months. The result? Average deep-work sessions increased by 41 minutes per day.

That's 170+ extra hours of focused coding per year. Per developer.

The best code is written by developers who aren't fighting their environment.

Your setup should work for you — not against you.

👉 Early access opens next week. Comment "CHAIR" and I'll send the link directly.`,
    cta: "Comment 'CHAIR' below for early access.",
    chars: 1247,
    compliance: true,
    approved: false,
  },

  twitter: [
    {
      num: 1,
      text: "I spent 6 years building software and silently destroying my back.\n\nThen I realized: most developer ergonomics advice is completely wrong.\n\nHere's what actually works for engineers who code 8+ hours daily 🧵",
      chars: 224,
    },
    {
      num: 2,
      text: "The problem isn't just sitting — it's how *developers* sit.\n\nWe lean forward during debugging.\nWe slump during Zoom calls.\nWe shift constantly while reading code.\n\nGeneric ergonomic chairs aren't designed for any of this.",
      chars: 221,
    },
    {
      num: 3,
      text: "After 18 months of testing with 500+ developers, we found:\n\n• 73% experienced daily back or neck discomfort\n• 61% said it affected their focus after hour 4\n• 89% had never adjusted their lumbar support\n\nThe chair industry has failed developers.",
      chars: 245,
    },
    {
      num: 4,
      text: "So we built DevChair Pro — engineered from the ground up for developer workflows:\n\n→ Adaptive lumbar for coding posture (not meeting posture)\n→ Keyboard-angle armrests\n→ Built-in cable routing\n→ Thermal mesh back panel\n\nNot a \"gaming chair\" in disguise.",
      chars: 252,
    },
    {
      num: 5,
      text: "The result? Developers using DevChair Pro averaged 41 more minutes of deep-work per day.\n\nThat's 170+ extra focused hours per year.\n\nYour setup is your competitive advantage.\n\nEarly access next week → RT to save your spot 🔥",
      chars: 228,
    },
  ],

  carousel: [
    {
      slide: 1,
      type: "hook",
      headline: "Your chair is stealing your best code.",
      subtext: "The average developer loses 41 min/day to discomfort-related distraction.",
      bg: "#0a0a1a",
      accent: "#6366f1",
    },
    {
      slide: 2,
      type: "problem",
      headline: "Generic chairs weren't built for developers.",
      subtext: "You code differently than you work. Your chair doesn't know that.",
      points: ["Lean forward when debugging", "Shift postures every 20 min", "Type for hours, not meetings"],
      bg: "#0f0f20",
      accent: "#8b5cf6",
    },
    {
      slide: 3,
      type: "insight",
      headline: "500 developers. 18 months. One finding.",
      subtext: "73% experience daily discomfort. 89% have never adjusted their lumbar.",
      stats: [{ val: "73%", label: "Daily discomfort" }, { val: "41min", label: "Lost focus/day" }, { val: "89%", label: "Never adjusted chair" }],
      bg: "#0d0d1e",
      accent: "#6366f1",
    },
    {
      slide: 4,
      type: "solution",
      headline: "Introducing DevChair Pro.",
      subtext: "The first chair engineered for the developer workflow.",
      features: ["Adaptive coding-posture lumbar", "Keyboard-tilt armrests", "Built-in cable management", "Thermal mesh focus panel"],
      bg: "#0a0a1a",
      accent: "#10b981",
    },
    {
      slide: 5,
      type: "cta",
      headline: "Get 170 extra hours of focus per year.",
      subtext: "Early access opens next week.",
      cta: "Follow + Comment 'CHAIR'",
      bg: "#080814",
      accent: "#6366f1",
    },
  ],

  reel: {
    duration: "0:30",
    scenes: [
      { time: "00:00", type: "HOOK",    visual: "Developer slouching, back pain", voiceover: "What if your chair is your biggest productivity killer?", text: "Your chair is costing you code.", duration: "5s" },
      { time: "00:05", type: "PROBLEM", visual: "Split screen: generic chair vs developer posture", voiceover: "Most developers lose 41 minutes of focus every single day.", text: "41 min/day. Lost to discomfort.", duration: "7s" },
      { time: "00:12", type: "INSIGHT", visual: "Data visualization of 500 developers", voiceover: "We studied 500 engineers over 18 months.", text: "500 devs. 18 months. 1 conclusion.", duration: "8s" },
      { time: "00:20", type: "PRODUCT", visual: "DevChair Pro reveal, slow rotation", voiceover: "Introducing DevChair Pro — built for how developers actually work.", text: "DevChair Pro.", duration: "7s" },
      { time: "00:27", type: "CTA",     visual: "Clean product shot with URL overlay", voiceover: "Early access next week. Link in bio.", text: "Early access → Link in bio", duration: "3s" },
    ],
  },

  critic: {
    scores: {
      humanLikeness:    91,
      hookStrength:     87,
      platformFit:      94,
      brandConsistency: 96,
      clarity:          89,
      ctaStrength:      82,
      aiSlopRisk:       "LOW",
    },
    detectedPhrases: ["innovative solution", "game-changing", "seamless experience"],
    issues: [
      { severity: "medium", platform: "LinkedIn", description: "Opening hook could be more specific to developer identity.", action: "Regenerated with personal founder POV.", status: "resolved" },
      { severity: "low",    platform: "X",        description: "Thread #3 stats need source attribution for credibility.", action: "Added qualifier 'based on internal testing'.",    status: "resolved" },
      { severity: "low",    platform: "Carousel",  description: "Slide 3 text density exceeded safe visual area.",         action: "Reduced body copy, increased stat size.",           status: "resolved" },
    ],
    overallVerdict: "Strong campaign. Human-first voice maintained across all platforms. Anti-slop filter cleared 3 generic phrases. CTA consistency improved post-refinement.",
    approved: false,
  },

  trace: [
    { agent: "Planner",            input: "Product brief: DevChair Pro for remote developers", decision: "Selected LinkedIn, X, Instagram, Reel. Tone: Founder. Audience: Remote developers 25–40.", output: "Campaign structure defined. 4 platform strategies queued.", status: "done" },
    { agent: "Content Generator",  input: "Platform strategies + brand kit", decision: "LinkedIn: founder story angle. X: data-driven thread. Carousel: visual stats. Reel: hook-problem-solution arc.", output: "4 platform content drafts produced.", status: "done" },
    { agent: "Visual Generator",   input: "Carousel brief + brand colors", decision: "5 slides: hook, problem, insight, solution, CTA. Dark premium palette. Stat-forward design.", output: "5 carousel slides rendered (HTML/CSS). Reel storyboard structured.", status: "done" },
    { agent: "Critic",             input: "All 4 platform drafts", decision: "Detected 3 AI-slop phrases. LinkedIn hook weak. Carousel slide 3 text overflow.", output: "3 issues flagged. Sent back to Refiner.", status: "done" },
    { agent: "Refiner",            input: "3 flagged issues from Critic", decision: "LinkedIn hook rewritten with first-person founder voice. 3 slop phrases removed. Carousel slide 3 layout adjusted.", output: "Refined drafts on all 3 issues.", status: "done" },
    { agent: "Final Output",       input: "Refined content from all agents", decision: "Quality gate passed. All scores above 80. Human approval gate triggered.", output: "Campaign package ready for human review.", status: "done" },
  ],
};

export const ANALYTICS_DATA = {
  campaigns: 47,
  avgGenerationTime: "52s",
  platformCompliance: 96,
  avgCriticScore: 89,
  humanApprovalRate: 78,
  avgEditsRequired: 1.4,
  benchmarkCategories: [
    { name: "SaaS Products",   trendforge: 91, traditional: 38, briefs: 10 },
    { name: "D2C Brands",      trendforge: 88, traditional: 35, briefs: 8  },
    { name: "Creator Content", trendforge: 94, traditional: 42, briefs: 7  },
  ],
  weeklyActivity: [12, 8, 15, 11, 19, 14, 9],
  platformBreakdown: [
    { platform: "LinkedIn",  count: 47, compliance: 97 },
    { platform: "X",         count: 45, compliance: 95 },
    { platform: "Instagram", count: 43, compliance: 96 },
    { platform: "Reel",      count: 38, compliance: 91 },
  ],
};
