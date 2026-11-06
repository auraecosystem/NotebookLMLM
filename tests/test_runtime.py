from notebooklmlm.kernels.python import PythonKernel
from notebooklmlm.runtime import NotebookRuntime


def test_runtime_dispatches_and_counts():
    runtime = NotebookRuntime()
    runtime.register_kernel(PythonKernel(timeout=2))
    result = runtime.execute("python", "print(2 + 2)")
    assert result.ok
    assert result.execution_count == 1
    runtime.close()
