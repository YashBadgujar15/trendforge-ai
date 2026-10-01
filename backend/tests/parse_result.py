import json, sys

src  = sys.argv[1]
dest = sys.argv[2]

with open(src, encoding='utf-8') as f:
    d = json.load(f)

out = []
meta = d.get('meta', {})
out.append('mode=' + str(meta.get('mode')))
out.append('model=' + str(meta.get('model')))
out.append('title=' + str(d.get('title')))
out.append('qualityScore=' + str(d.get('qualityScore')))
out.append('genMs=' + str(meta.get('generationTimeMs')))
out.append('---TRACE---')
for t in d.get('trace', []):
    line = str(t.get('agent', '')) + ': ' + str(t.get('output', ''))[:90]
    out.append(line.encode('ascii', 'replace').decode())
out.append('---LINKEDIN---')
out.append(str(d.get('linkedin', {}).get('hook', '')).encode('ascii', 'replace').decode()[:160])
out.append('---TWEET1---')
tw = d.get('twitter', [])
out.append(str(tw[0].get('text', '') if tw else '').encode('ascii', 'replace').decode()[:160])
out.append('---SLIDE1---')
sl = d.get('carousel', [])
if sl:
    out.append((str(sl[0].get('headline', '')) + ' | ' + str(sl[0].get('subtext', ''))[:80]).encode('ascii', 'replace').decode())
out.append('---CRITIC---')
out.append(str(d.get('critic', {}).get('overallVerdict', '')).encode('ascii', 'replace').decode()[:160])
full = json.dumps(d).lower()
out.append('---CHECKS---')
out.append('journal_burnout_mental=' + str(any(w in full for w in ['journal', 'burnout', 'mental health', 'mental'])))
out.append('professional_working='   + str(any(w in full for w in ['professional', 'working'])))
out.append('water_bottle='           + str('water bottle' in full))
out.append('college='                + str('college' in full))
out.append('devchair='               + str('devchair' in full))
out.append('top_keys='               + str(list(d.keys())))

with open(dest, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print('done')
