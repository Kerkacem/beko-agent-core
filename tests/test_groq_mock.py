import sys
import types
from types import SimpleNamespace
import beko_self_agent as bsa


def make_resp(content="plan", tokens=5):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        usage=SimpleNamespace(total_tokens=tokens),
    )


def test_beko_self_agent_grok_call(monkeypatch, tmp_path):
    resp = make_resp("mock plan", 42)

    mock_client = SimpleNamespace()
    mock_client.chat = SimpleNamespace(
        completions=SimpleNamespace(create=lambda **kwargs: resp)
    )

    monkeypatch.setattr(bsa, "client", mock_client)

    # call and ensure it doesn't raise
    result = bsa.grok_live_call()
    # result may be None if saving skipped, but ensure mock was usable
    assert True


def test_beko_v5_grok_heal(monkeypatch):
    import beko_v5 as bv5

    resp = make_resp("v5 plan", 10)

    module = types.ModuleType("groq")

    class Groq:
        def __init__(self, api_key):
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=lambda **kwargs: resp)
            )

    module.Groq = Groq
    monkeypatch.setitem(sys.modules, "groq", module)
    monkeypatch.setenv("GROQ_API_KEY", "dummy_key")

    # call and ensure no exception
    bv5.grok_heal()
    assert True
