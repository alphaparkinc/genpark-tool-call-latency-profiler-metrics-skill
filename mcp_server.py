"""MCP Server for Tool Call Latency Profiler Metrics.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import ToolCallLatencyProfilerMetrics

profiler = ToolCallLatencyProfilerMetrics()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "record_call",
                                "description": "Record tool call duration and success/error status",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "tool_name": {"type": "string"},
                                        "duration_ms": {"type": "number"},
                                        "is_error": {"type": "boolean", "default": False}
                                    },
                                    "required": ["tool_name", "duration_ms"]
                                }
                            },
                            {
                                "name": "get_metrics",
                                "description": "Get P50, P90, P95, P99 latency and error telemetry for a tool",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "tool_name": {"type": "string"}
                                    },
                                    "required": ["tool_name"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "record_call":
                    profiler.record_call(
                        tool_name=args.get("tool_name", ""),
                        duration_ms=args.get("duration_ms", 0.0),
                        is_error=args.get("is_error", False)
                    )
                    res = {"recorded": True}
                elif call_name == "get_metrics":
                    res = profiler.get_metrics(args.get("tool_name", ""))
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
