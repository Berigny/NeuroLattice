from cli_agent.actions.load_kernel import load_brand_kernel
from lattice.coherence_graph import initialise_lattice
from rich import print

def boot_agent():
    print("[bold cyan]NeuroLattice Brand Agent Initialising...[/bold cyan]")
    kernel_data = load_brand_kernel()
    lattice = initialise_lattice(kernel_data)
    return lattice, kernel_data
