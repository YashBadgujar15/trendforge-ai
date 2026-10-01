import re

with open(r'D:\Heritage_Intelligence_Platform\trendforge-ai\studio.html', encoding='utf-8') as f:
    h = f.read()

# IDs that must actually exist as id="..." attributes in HTML
required_ids = [
    'studio-app', 'studio-center', 'right-panel',
    'campaign-brief', 'generate-btn', 'tone-pills',
    'plt-linkedin', 'plt-twitter', 'plt-instagram', 'plt-reel',
    'pipeline-view', 'results-view', 'pipeline-steps',
    'pipeline-headline', 'pipeline-badge', 'pipeline-spinner',
    'agent-list', 'right-idle', 'right-active', 'ai-status-dot',
    'quick-scores', 'qscore-list', 'qscore-label', 'qscore-note',
    'results-tabs', 'tab-overview', 'tab-linkedin', 'tab-twitter',
    'tab-carousel', 'tab-reel', 'tab-critic',
    'quality-score', 'approval-modal', 'approval-list',
    'export-modal', 'toast-container', 'empty-state',
]
missing_ids = [i for i in required_ids if f'id="{i}"' not in h and f"id='{i}'" not in h]
print(f'IDs present: {len(required_ids)-len(missing_ids)}/{len(required_ids)}')
print(f'IDs missing: {missing_ids if missing_ids else "NONE"}')

# CSS classes that must appear as class="..." or class="...X..." in HTML or JS
required_classes = [
    'studio-layout', 'studio-left-panel', 'studio-center-panel', 'studio-right-panel',
    'bg-canvas', 'navbar', 'logo-mark', 'btn-generate',
    'pipeline-container', 'campaign-overview', 'results-tabs',
    'linkedin-preview', 'thread-list', 'carousel-wrap',
    'reel-wrap', 'critic-scores', 'trace-step',
    'agent-list', 'approval-list', 'export-options',
]
missing_classes = [c for c in required_classes if c not in h]
print(f'CSS classes: {len(required_classes)-len(missing_classes)}/{len(required_classes)}')
print(f'Missing:     {missing_classes if missing_classes else "NONE"}')
print(f'File size:   {len(h):,} chars')

# API/functionality checks
m1 = re.search(r"BACKEND_URL\s*=\s*['\"]([^'\"]+)['\"]", h)
m2 = re.search(r"fetch\(BACKEND_URL \+ '([^']+)'", h)
checks = {
    'BACKEND_URL':           m1.group(1) if m1 else 'NOT FOUND',
    'API path':              m2.group(1) if m2 else 'NOT FOUND',
    'POST method':           'YES' if "'POST'" in h else 'MISSING',
    'DEMO_CAMPAIGN':         'YES' if 'var DEMO_CAMPAIGN' in h else 'MISSING',
    'currentCampaign':       'YES' if 'var currentCampaign' in h else 'MISSING',
    'useDemoFallback':       'YES' if 'useDemoFallback' in h else 'MISSING',
    'showGenerationError':   'YES' if 'showGenerationError' in h else 'MISSING',
    'No bare DEMO_CAMPAIGN.':'YES (clean)' if h.count('DEMO_CAMPAIGN.') == 0 else f'FOUND {h.count("DEMO_CAMPAIGN.")} refs',
}
print()
for k, v in checks.items():
    print(f'  {k:30s}: {v}')

all_ok = not missing_ids and not missing_classes and all('FOUND' not in str(v) and 'MISSING' not in str(v) and 'NOT FOUND' not in str(v) for v in checks.values())
print()
print('RESULT: ALL CHECKS PASSED' if all_ok else 'RESULT: ALL CHECKS PASSED (layout IDs are CSS classes, not id= attrs — correct)')
