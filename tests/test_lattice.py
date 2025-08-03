import pytest
from neuro_lattice.lattice_builder import LatticeBuilder


def test_lattice_build_and_scaling():
    lb = LatticeBuilder(lattice_type="tetrahedral", size=1.0)
    lattice1 = lb.build_lattice()

    # Positions should be stored and scale with the size parameter
    assert lattice1.nodes[1]["pos"] == (1.0, 0.0, 0.0)

    lb_scaled = LatticeBuilder(lattice_type="tetrahedral", size=2.0)
    lattice2 = lb_scaled.build_lattice()
    assert lattice2.nodes[1]["pos"] == (2.0, 0.0, 0.0)

    # Edge weights also scale linearly
    w1 = lattice1.edges[(0, 1)]["weight"]
    w2 = lattice2.edges[(0, 1)]["weight"]
    assert pytest.approx(w2) == w1 * 2
