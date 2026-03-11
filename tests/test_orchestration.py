#!/usr/bin/env python3
"""
Testes orquestração (sem Redis/Ollama obrigatórios).
Rode: python app/test_orchestration.py
Com Redis: pip install redis, inicie Redis e os testes de integração rodarão.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
os.chdir(REPO_ROOT)

def test_orchestration():
    from app.core.orchestration import is_cosmetic, get_int, strike_key
    assert is_cosmetic(["a.css", "b.md"]) is True
    assert is_cosmetic(["a.py"]) is False
    assert is_cosmetic([]) is False
    print("  orchestration is_cosmetic: ok")


class FakeRedis:
    def __init__(self):
        self.store = {}
        self.added = []

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value, ex=None):
        self.store[key] = value
        return True

    def delete(self, key):
        self.store.pop(key, None)
        return 1

    def xadd(self, stream_name, payload):
        self.added.append((stream_name, payload))
        return "1-0"

    def incr(self, key):
        current = int(self.store.get(key, "0")) + 1
        self.store[key] = str(current)
        return current

    def ping(self):
        return True


def test_run_degradation_cycle_requests_consensus():
    from app.core.orchestration import (
        KEY_CONSENSUS_IN_PROGRESS,
        KEY_OMISSION_COUNT,
        KEY_SPRINT_TASKS,
        run_degradation_cycle,
    )

    redis_client = FakeRedis()
    redis_client.store[KEY_OMISSION_COUNT] = "2"
    redis_client.store[KEY_SPRINT_TASKS] = "10"

    outcome = run_degradation_cycle(redis_client)

    assert outcome == "consensus_requested"
    assert redis_client.get(KEY_CONSENSUS_IN_PROGRESS) == "1"
    assert len(redis_client.added) == 2
    assert redis_client.added[0][1]["type"] == "consensus_loop_requested"
    assert redis_client.added[0][1]["status_code"] == "consensus_loop_requested"
    assert redis_client.added[0][1]["event_name"] == "orchestration.consensus_loop_requested"
    assert redis_client.added[0][1]["run_id"]
    assert redis_client.added[0][1]["trace_id"]


def test_record_invalid_output_emits_event_and_counts():
    from app.core.orchestration import KEY_INVALID_OUTPUT_COUNT, record_invalid_output

    redis_client = FakeRedis()

    total = record_invalid_output(
        redis_client,
        role_name="Developer",
        issue_id="42",
        schema="developer",
        missing_fields=["files_changed", "verification"],
    )

    assert total == 1
    assert redis_client.store[KEY_INVALID_OUTPUT_COUNT] == "1"
    assert redis_client.added[0][0] == "orchestrator:events"
    assert redis_client.added[0][1]["type"] == "openclaw_invalid_output"


def test_record_invalid_output_threshold_increments_issue_strike():
    from app.core.orchestration import INVALID_OUTPUT_THRESHOLD, record_invalid_output, strike_key
    from app.shared.issue_state import STATE_BACKLOG

    redis_client = FakeRedis()

    for _ in range(INVALID_OUTPUT_THRESHOLD):
        record_invalid_output(
            redis_client,
            role_name="Developer",
            issue_id="77",
            schema="developer",
            missing_fields=["files_changed"],
        )

    assert redis_client.store[strike_key("77")] == "1"
    assert redis_client.store["project:v1:issue:77:state"] == STATE_BACKLOG
    assert redis_client.added[-2][1]["type"] == "openclaw_invalid_output_threshold"
    assert redis_client.added[-1][1]["type"] == "issue_back_to_po"
    assert redis_client.added[-1][1]["target_state"] == STATE_BACKLOG

def test_redis_integration():
    try:
        from app.core.orchestration import get_redis, get_strikes, increment_strike, reset_strikes
        r = get_redis()
        r.ping()
        # cleanup
        reset_strikes(r, "test_run")
        n = increment_strike(r, "test_run")
        assert n == 1
        assert get_strikes(r, "test_run") == 1
        reset_strikes(r, "test_run")
        print("  Redis + strikes: ok")
    except Exception as e:
        print(f"  Redis + strikes: skip (Redis indisponível: {e})")

def main():
    print("==> Testes orquestração")
    test_orchestration()
    test_redis_integration()
    print("==> Concluído.")

if __name__ == "__main__":
    main()
