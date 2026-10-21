"""Tool Call Latency Profiler Metrics.
100% Python Standard Library.
"""
import time
import math

class ToolCallLatencyProfilerMetrics:
    """MCP tool call latency profiler & P95/P99 telemetry collector."""

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self.records = {}

    def record_call(self, tool_name: str, duration_ms: float, is_error: bool = False):
        if tool_name not in self.records:
            self.records[tool_name] = []
        rec = self.records[tool_name]
        rec.append({"duration_ms": duration_ms, "is_error": is_error, "timestamp": time.time()})
        if len(rec) > self.window_size:
            rec.pop(0)

    def get_metrics(self, tool_name: str) -> dict:
        calls = self.records.get(tool_name, [])
        if not calls:
            return {"tool_name": tool_name, "total_calls": 0, "p50_ms": 0, "p95_ms": 0, "p99_ms": 0, "error_rate": 0.0}

        durations = sorted([c["duration_ms"] for c in calls])
        errors = sum(1 for c in calls if c["is_error"])
        n = len(durations)

        def percentile(p):
            idx = int(math.ceil((p / 100.0) * n)) - 1
            return round(durations[max(0, min(idx, n - 1))], 2)

        return {
            "tool_name": tool_name,
            "total_calls": n,
            "error_rate": round(errors / n, 4),
            "p50_ms": percentile(50),
            "p90_ms": percentile(90),
            "p95_ms": percentile(95),
            "p99_ms": percentile(99),
            "min_ms": round(durations[0], 2),
            "max_ms": round(durations[-1], 2),
            "avg_ms": round(sum(durations) / n, 2)
        }
