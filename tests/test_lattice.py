import unittest
from neuro_lattice.lattice_builder import build_tetrahedral_lattice, build_cubic_lattice

class TestLatticeIntegrity(unittest.TestCase):

    def test_tetrahedral_lattice_symmetry(self):
        lattice = build_tetrahedral_lattice()
        # Check for symmetry properties
        self.assertTrue(lattice.is_symmetric(), "Tetrahedral lattice should be symmetric")

    def test_cubic_lattice_symmetry(self):
        lattice = build_cubic_lattice()
        # Check for symmetry properties
        self.assertTrue(lattice.is_symmetric(), "Cubic lattice should be symmetric")

    def test_tetrahedral_lattice_eigenvalues(self):
        lattice = build_tetrahedral_lattice()
        eigenvalues = lattice.calculate_eigenvalues()
        # Check if eigenvalues meet expected criteria
        self.assertTrue(all(ev >= 0 for ev in eigenvalues), "Eigenvalues should be non-negative")

    def test_cubic_lattice_eigenvalues(self):
        lattice = build_cubic_lattice()
        eigenvalues = lattice.calculate_eigenvalues()
        # Check if eigenvalues meet expected criteria
        self.assertTrue(all(ev >= 0 for ev in eigenvalues), "Eigenvalues should be non-negative")

if __name__ == '__main__':
    unittest.main()