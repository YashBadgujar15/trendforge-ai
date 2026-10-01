import json, sys
sys.path.insert(0, r'D:\Heritage_Intelligence_Platform\trendforge-ai\backend')

src = r'C:\Users\ABCD\AppData\Local\Temp\res_frontend.json'
dst = r'C:\Users\ABCD\AppData\Local\Temp\res_frontend_full.txt'

with open(src, encoding='utf-8') as f:
    d = json.load(f)

def s(v, n=120):
    return str(v).encode('ascii','replace').decode()[:n]

out = []
meta = d.get('meta', {})

out.append('=== META ===')
out.append(f"mode:             {meta.get('mode')}")
out.append(f"model:            {meta.get('model')}")
out.append(f"title (root):     {d.get('title')}")
out.append(f"qualityScore:     {d.get('qualityScore')}")
out.append(f"generationTimeMs: {meta.get('generationTimeMs')}")
out.append(f"generatedAt:      {meta.get('generatedAt')}")

out.append('\n=== PIPELINE TRACE (all stages) ===')
for t in d.get('trace', []):
    out.append(f"  [{t.get('agent')}]")
    out.append(f"    decision: {s(t.get('decision',''), 100)}")
    out.append(f"    output:   {s(t.get('output',''), 120)}")

out.append('\n=== LINKEDIN ===')
li = d.get('linkedin', {})
out.append(f"hook:  {s(li.get('hook',''), 160)}")
out.append(f"body:  {s(li.get('body',''), 300)}")
out.append(f"cta:   {s(li.get('cta',''), 120)}")
out.append(f"chars: {li.get('chars')}")

out.append('\n=== X / TWITTER THREAD (all 5 tweets) ===')
for tw in d.get('twitter', []):
    out.append(f"  [{tw.get('num')}] ({tw.get('chars')} chars) {s(tw.get('text',''), 180)}")

out.append('\n=== INSTAGRAM CAROUSEL (all 5 slides) ===')
for sl in d.get('carousel', []):
    out.append(f"  Slide {sl.get('slide')} [{sl.get('type')}]")
    out.append(f"    headline: {s(sl.get('headline',''), 100)}")
    out.append(f"    subtext:  {s(sl.get('subtext',''), 100)}")

out.append('\n=== REEL STORYBOARD (all 5 scenes) ===')
reel = d.get('reel', {})
out.append(f"duration: {reel.get('duration')}")
for sc in reel.get('scenes', []):
    out.append(f"  [{sc.get('time')}] {sc.get('type')} — visual: {s(sc.get('visual',''), 80)}")
    out.append(f"    voiceover: {s(sc.get('voiceover',''), 100)}")

out.append('\n=== AI CRITIC ===')
critic = d.get('critic', {})
scores = critic.get('scores', {})
out.append('scores:')
for k, v in scores.items():
    out.append(f"  {k}: {v}")
out.append(f"aiSlopRisk:       {scores.get('aiSlopRisk')}")
out.append(f"detectedPhrases:  {critic.get('detectedPhrases')}")
out.append(f"issues count:     {len(critic.get('issues', []))}")
for iss in critic.get('issues', []):
    out.append(f"  - [{iss.get('severity')}] {s(iss.get('description',''), 100)}")
out.append(f"overallVerdict:   {s(critic.get('overallVerdict',''), 250)}")

out.append('\n=== BRIEF-SPECIFICITY CHECKS ===')
full = json.dumps(d).lower()
checks = {
    'water bottle':        'water bottle' in full,
    'hydration':           'hydration' in full,
    'temperature':         'temperature' in full or 'temp' in full,
    'reminders':           'reminder' in full,
    'college students':    'college' in full,
    'age 18-25':           '18' in full and '25' in full,
    'devchair (should be False)': 'devchair' in full,
    'chair demo (should be False)': 'ergonomic chair' in full,
}
for k, v in checks.items():
    out.append(f"  {k}: {v}")

with open(dst, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('done')
