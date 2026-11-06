import sqlite3

from notebooklmlm.kernels.python import PythonKernel
from notebooklmlm.kernels.sqlite import SQLiteKernel


def test_sqlite_kernel_binds_values_and_defaults_read_only(tmp_path):
    db = tmp_path / "app.db"
    connection = sqlite3.connect(db)
    connection.execute("CREATE TABLE people (name TEXT)")
    connection.execute("INSERT INTO people VALUES ('Ada')")
    connection.commit()
    connection.close()
    kernel = SQLiteKernel(db)
    result = kernel.execute("SELECT name FROM people WHERE name = :name", {"name": "Ada"})
    assert result.ok
    assert result.data["rows"] == [{"name": "Ada"}]
    assert kernel.execute("DELETE FROM people").status == "error"
    kernel.close()


def test_python_kernel_runs_and_times_out():
    result = PythonKernel(timeout=2).execute("print('hello')")
    assert result.ok
    assert result.stdout.strip() == "hello"
    timeout = PythonKernel(timeout=0.1).execute("while True: pass")
    assert timeout.status == "error"
    assert "timed out" in timeout.stderr
