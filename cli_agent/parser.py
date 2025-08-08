import argparse
from cli_agent.actions.trace_modal import trace_modal_input
from cli_agent.actions.evaluate_resonance import evaluate_resonance

def trace_command(args, kernel, lattice):
    prime = trace_modal_input(args.modal, args.event, kernel)
    resonance = evaluate_resonance(prime, kernel['brand_identity_kernel']['resonance_map'])
    print(f"Prime [{prime}] detected for {args.modal}/{args.event}")
    print(f"Resonates most strongly with {resonance[0]}")

def setup_parser(kernel, lattice):
    parser = argparse.ArgumentParser(description='NeuroLattice CLI')
    subparsers = parser.add_subparsers()

    # Trace command
    trace_parser = subparsers.add_parser('trace', help='Trace a modal input')
    trace_parser.add_argument('--modal', required=True, help='Modal domain to trace')
    trace_parser.add_argument('--event', required=True, help='Event to trace')
    trace_parser.set_defaults(func=trace_command)

    return parser
