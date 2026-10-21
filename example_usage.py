"""Example usage for Tool Call Latency Profiler Metrics."""
from client import ToolCallLatencyProfilerMetrics
import json

profiler = ToolCallLatencyProfilerMetrics()

for dur in [12.4, 15.1, 14.8, 45.2, 19.8, 120.5, 16.3]:
    profiler.record_call("rag_retriever", dur, is_error=(dur > 100))

metrics = profiler.get_metrics("rag_retriever")
print(json.dumps(metrics, indent=2))
