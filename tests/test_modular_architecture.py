from notebooklmlm.bookmarks import BookmarkRegistry
from notebooklmlm.core.engine import NotebookEngine
from notebooklmlm.core.session import NotebookSession
from notebooklmlm.kernels.python import PythonKernel
from notebooklmlm.security.permissions import ExecutionPolicy

def test_modular_bookmarks_package(tmp_path):
    with BookmarkRegistry(tmp_path/"b.db") as registry:
        item=registry.add("q1","SELECT * FROM t WHERE id=:id"); assert item.name=="q1"
        registry.validate_parameters(item,{"id":1})

def test_engine_policy_denies_python_by_default():
    engine=NotebookEngine(policy=ExecutionPolicy()); engine.register_kernel(PythonKernel(timeout=2)); session=engine.create_session()
    result=engine.execution.execute("python","print('blocked')",session=session)
    assert result.status=="denied" and session.state.execution_count==1
    engine.close()

def test_session_close_clears_state():
    session=NotebookSession(); session.state.variables["x"]=1; session.close()
    assert session.closed and not session.state.variables
