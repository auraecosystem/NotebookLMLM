"""One-shot Python kernel using a separate interpreter process.

Process separation and timeout control are not a security sandbox. See SECURITY.md.
"""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any

from notebooklmlm.kernels.base import Kernel
from notebooklmlm.models import ExecutionResult

_WORKER = r'''
import contextlib, io, json, sys
payload = json.loads(sys.stdin.read())
stdout, stderr = io.StringIO(), io.StringIO()
namespace = {"__name__": "__main__"}
try:
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(compile(payload["code"], "<notebook-cell>", "exec"), namespace, namespace)
    result = {"status": "ok", "stdout": stdout.getvalue(), "stderr": stderr.getvalue()}
except BaseException as exc:
    result = {"status": "error", "stdout": stdout.getvalue(),
              "stderr": stderr.getvalue() + type(exc).__name__ + ": " + str(exc)}
sys.stdout.write(json.dumps(result))
'''


class PythonKernel(Kernel):
    language = "python"

    def __init__(self, timeout: float = 5.0, max_output_bytes: int = 1_000_000) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.timeout, self.max_output_bytes = timeout, max_output_bytes

    def execute(self, code: str, context: dict[str, Any] | None = None) -> ExecutionResult:
        if context:
            return ExecutionResult(status="error", stderr="Python context injection is not supported")
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-c", _WORKER],
                input=json.dumps({"code": code}), text=True, capture_output=True,
                timeout=self.timeout, check=False)
        except subprocess.TimeoutExpired:
            return ExecutionResult(status="error", stderr=f"Execution timed out after {self.timeout} seconds")
        if len(completed.stdout.encode("utf-8")) > self.max_output_bytes:
            return ExecutionResult(status="error", stderr="Python output exceeded configured limit")
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            return ExecutionResult(status="error", stderr=completed.stderr or "Python worker returned invalid output")
        return ExecutionResult(status=payload["status"], stdout=payload.get("stdout", ""),
                               stderr=payload.get("stderr", ""),
                               metadata={"returncode": completed.returncode})
