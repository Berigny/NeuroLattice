import pytest
from neuro_lattice.lattice_builder import LatticeBuilder

def test_lattice_build():
    lb = LatticeBuilder(lattice_type='tetrahedral')
    lattice = lb.build_lattice()
    assert lattice is not None
