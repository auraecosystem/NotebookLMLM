from notebooklmlm.notebook import NotebookDocument


def test_notebook_round_trip(tmp_path):
    notebook = NotebookDocument()
    notebook.add_cell("markdown", "# Analysis")
    notebook.add_cell("code", "print('hello')")
    path = tmp_path / "sample.nlm"
    notebook.save(path)
    loaded = NotebookDocument.load(path)
    assert loaded.format_version == 1
    assert [cell.cell_type for cell in loaded.cells] == ["markdown", "code"]
    assert loaded.cells[1].source == "print('hello')"
