"""
TrendForge AI — Backend Tests
Run with: pytest tests/ -v
(from backend/ directory with venv activated)
"""
import json
import os
import sys
import pytest

# Make sure the backend package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


VALID_PAYLOAD = {
    "brief": "Launching a SaaS tool for indie developers that automates code reviews.",
    "platforms": ["linkedin", "twitter", "instagram", "reel"],
    "tone": "Founder"
}


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

class TestHealth:
    def test_health_returns_200(self, client):
        res = client.get('/api/health')
        assert res.status_code == 200

    def test_health_json_structure(self, client):
        res = client.get('/api/health')
        data = json.loads(res.data)
        assert 'status' in data
        assert data['status'] == 'ok'

    def test_health_has_mode(self, client):
        res = client.get('/api/health')
        data = json.loads(res.data)
        assert 'mode' in data
        assert data['mode'] in ('ai', 'mock')


# ---------------------------------------------------------------------------
# Generate endpoint — request validation
# ---------------------------------------------------------------------------

class TestGenerateValidation:
    def test_missing_brief_returns_error(self, client):
        res = client.post('/api/generate',
                          data=json.dumps({"platforms": ["linkedin"]}),
                          content_type='application/json')
        assert res.status_code in (400, 415, 422)

    def test_empty_brief_returns_error(self, client):
        res = client.post('/api/generate',
                          data=json.dumps({"brief": "   ", "platforms": ["linkedin"]}),
                          content_type='application/json')
        assert res.status_code in (400, 422)

    def test_missing_body_returns_error(self, client):
        # Empty string parses as None JSON → brief is empty → 422
        res = client.post('/api/generate', data='', content_type='application/json')
        assert res.status_code in (400, 422)

    def test_non_json_returns_error(self, client):
        res = client.post('/api/generate',
                          data='not-json',
                          content_type='text/plain')
        # Flask returns 415 Unsupported Media Type for non-JSON
        assert res.status_code in (400, 415)

    def test_error_response_has_error_key(self, client):
        res = client.post('/api/generate',
                          data=json.dumps({}),
                          content_type='application/json')
        data = json.loads(res.data)
        assert 'error' in data


# ---------------------------------------------------------------------------
# Generate endpoint — response structure
# ---------------------------------------------------------------------------

class TestGenerateResponseStructure:
    def test_returns_200(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        assert res.status_code == 200

    def test_top_level_keys_present(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        for key in ('title', 'qualityScore', 'linkedin', 'twitter',
                    'carousel', 'reel', 'critic', 'trace', 'meta'):
            assert key in data, f"Missing top-level key: {key}"

    def test_meta_fields(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        meta = data['meta']
        assert 'mode' in meta
        assert meta['mode'] in ('ai', 'mock')
        assert 'brief' in meta
        assert 'generationTimeMs' in meta

    def test_quality_score_is_numeric(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        assert isinstance(data['qualityScore'], (int, float))
        assert 0 <= data['qualityScore'] <= 100

    def test_linkedin_structure(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        li = data['linkedin']
        for key in ('hook', 'body', 'cta', 'chars'):
            assert key in li, f"LinkedIn missing key: {key}"
        assert isinstance(li['chars'], int)

    def test_twitter_is_list_of_5(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        tweets = data['twitter']
        assert isinstance(tweets, list)
        assert len(tweets) == 5
        for tw in tweets:
            assert 'text' in tw
            assert 'chars' in tw

    def test_carousel_is_list_of_5(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        slides = data['carousel']
        assert isinstance(slides, list)
        assert len(slides) == 5
        for s in slides:
            assert 'headline' in s
            assert 'slide' in s

    def test_reel_structure(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        reel = data['reel']
        assert 'duration' in reel
        assert 'scenes' in reel
        assert isinstance(reel['scenes'], list)
        assert len(reel['scenes']) == 5

    def test_critic_scores_structure(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        scores = data['critic']['scores']
        for key in ('humanLikeness', 'hookStrength', 'platformFit',
                    'brandConsistency', 'clarity', 'ctaStrength', 'aiSlopRisk'):
            assert key in scores, f"Critic scores missing: {key}"

    def test_trace_is_list(self, client):
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        data = json.loads(res.data)
        trace = data['trace']
        assert isinstance(trace, list)
        assert len(trace) >= 1
        for entry in trace:
            assert 'agent' in entry
            assert 'output' in entry


# ---------------------------------------------------------------------------
# Mock vs AI routing
# ---------------------------------------------------------------------------

class TestMockRouting:
    """These tests verify the mock generator returns the correct mode flag.
    They run regardless of whether GEMINI_API_KEY is set — we force mock mode
    by temporarily patching the flag inside main.py."""

    def test_mock_mode_flag(self, client, monkeypatch):
        import main as m
        monkeypatch.setattr(m, '_KEY_CONFIGURED', False)
        res = client.post('/api/generate',
                          data=json.dumps(VALID_PAYLOAD),
                          content_type='application/json')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data['meta']['mode'] == 'mock'

    def test_mock_mode_health(self, client, monkeypatch):
        import main as m
        monkeypatch.setattr(m, '_KEY_CONFIGURED', False)
        res = client.get('/api/health')
        data = json.loads(res.data)
        assert data['mode'] == 'mock'


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

class TestCORS:
    def test_options_preflight(self, client):
        res = client.options('/api/generate',
                             headers={'Origin': 'http://localhost:3000',
                                      'Access-Control-Request-Method': 'POST'})
        # flask-cors should respond 200 or 204 with CORS headers
        assert res.status_code in (200, 204)
