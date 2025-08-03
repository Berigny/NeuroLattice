# NeuroLattice

NeuroLattice is a Python package designed for simulating and analyzing lattice structures in a networked environment. This project provides tools for building various types of lattices, applying perturbations, measuring performance metrics, and visualizing the results.

## Features

- **Lattice Construction**: Create tetrahedral and cubic lattices with customizable parameters.
- **Routing Engine**: Implement packet routing logic that distinguishes between System 1 and System 2 behaviors.
- **Performance Metrics**: Calculate strain, coherence, and drift measures to evaluate lattice performance.
- **Perturbation Simulation**: Inject adversarial attacks or data poisoning into the system to test resilience.
- **Visualization**: Plot network structures and dynamics for better understanding and analysis.

## Live Demo

A live demonstration of the NeuroLattice functionality can be found in the Jupyter notebook located in the `notebooks` directory. The notebook showcases the process of building a lattice, applying perturbations, measuring outcomes, and visualizing results.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/berigny/NeuroLattice/blob/main/notebooks/neuro_lattice_demo.ipynb)

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Running Tests

To ensure the integrity of the package, unit tests are provided in the `tests` directory. You can run the tests using:

```
pytest
```

## Contributing

We welcome contributions to the NeuroLattice project! Please refer to the `CONTRIBUTING.md` file for guidelines on how to collaborate.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.