import pytest

go = pytest.importorskip("plotly.graph_objects")


def test_plotly_figure_creation():
    fig = go.Figure()
    assert fig.data == ()
