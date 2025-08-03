class LatticeBuilder:
    def __init__(self, lattice_type='tetrahedral', size=1.0):
        self.lattice_type = lattice_type
        self.size = size
        self.lattice = None

    def build_lattice(self):
        if self.lattice_type == 'tetrahedral':
            self.lattice = self._build_tetrahedral_lattice()
        elif self.lattice_type == 'cubic':
            self.lattice = self._build_cubic_lattice()
        else:
            raise ValueError("Unsupported lattice type. Choose 'tetrahedral' or 'cubic'.")
        return self.lattice

    def _build_tetrahedral_lattice(self):
        # Logic to build a tetrahedral lattice
        # Placeholder for actual implementation
        return "Tetrahedral lattice structure"

    def _build_cubic_lattice(self):
        # Logic to build a cubic lattice
        # Placeholder for actual implementation
        return "Cubic lattice structure"

    def set_lattice_parameters(self, lattice_type, size):
        self.lattice_type = lattice_type
        self.size = size

    def get_lattice(self):
        return self.lattice