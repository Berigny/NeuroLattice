from setuptools import setup, find_packages

setup(
    name="neuro_lattice",
    version="0.1.1",
    description="Symmetry-driven coherence framework for next-gen intelligence",
    author="David Berigny",
    packages=find_packages(include=["neuro_lattice", "neuro_lattice.*"]),
    install_requires=[
        "networkx",
        "matplotlib",
        "pandas",
        "opencv-python",
        "numpy",
        "scikit-image",
        "scikit-learn"
    ],
)
