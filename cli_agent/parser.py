import argparse
import os

def _ensure_kernel_loaded(context) -> bool:
    if context.get('kernel_data') and context.get('lattice'):
        return True
    try:
        from cli_agent.actions.load_kernel import load_brand_kernel
        from lattice.coherence_graph import initialise_lattice
        kernel_file = os.environ.get('KERNEL_FILE', 'memory/brand_identity_kernel.json')
        context['kernel_data'] = load_brand_kernel(kernel_file)
        context['lattice'] = initialise_lattice(context['kernel_data'])
        print(f"Auto-loaded kernel from {kernel_file}.")
        return True
    except Exception as e:
        print(f"Error: Brand kernel not initialized. Run 'init' or set KERNEL_FILE. Details: {e}")
        return False

def init_command(args, context):
    from cli_agent.actions.load_kernel import load_brand_kernel
    from lattice.coherence_graph import initialise_lattice
    print(f"Initializing kernel from {args.kernel_file}")
    context['kernel_data'] = load_brand_kernel(args.kernel_file)
    context['lattice'] = initialise_lattice(context['kernel_data'])
    print("Kernel loaded successfully.")

def trace_command(args, context):
    if not _ensure_kernel_loaded(context):
        return

    from agents import agent_s1, agent_s2

    prompt = args.prompt
    brand_data = context['kernel_data']

    if args.system == 1:
        response = agent_s1.respond(prompt, brand_data)
    else:
        response = agent_s2.respond(prompt, brand_data)

    print(response)

    if args.log:
        # TODO: Implement logging
        print("Logging output...")

def interactive_command(args, context):
    if not _ensure_kernel_loaded(context):
        return

    from agents.mediator import run_interactive

    systems = args.systems
    modals = args.modal
    brand_data = context['kernel_data']

    s2_provider = args.s2_provider
    run_interactive(systems, modals, brand_data, s2_provider=s2_provider)

def report_command(args, context):
    import json
    import pathlib
    from collections import defaultdict

    BUS = pathlib.Path("/tmp/lattice_bus.jsonl")

    if not BUS.exists():
        print("Error: Log file not found. Run a session first.")
        return

    strain_by_modal = defaultdict(list)

    with BUS.open("r") as f:
        for line in f:
            try:
                log_entry = json.loads(line)
                strain = log_entry.get("strain")
                modal = log_entry.get("modal")
                turn = log_entry.get("turn")
                if strain is not None and modal is not None:
                    strain_by_modal[modal].append((turn, strain))
            except json.JSONDecodeError:
                continue

    print("Strain Report:")
    for modal, strains in strain_by_modal.items():
        print(f"\nModal: {modal}")
        for turn, strain in sorted(strains):
            print(f"  Turn {turn}: Strain = {strain}")

def setup_parser(context):
    parser = argparse.ArgumentParser(description='NeuroLattice CLI')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialise Brand Kernel')
    init_parser.add_argument('kernel_file', help='Path to the brand kernel JSON file')
    init_parser.set_defaults(func=init_command)

    # Trace command
    trace_parser = subparsers.add_parser('trace', help='Send a prompt to a system')
    trace_parser.add_argument('--system', type=int, choices=[1, 2], required=True, help='System to use (1 or 2)')
    trace_parser.add_argument('--modal', required=True, help='Modal for the prompt')
    trace_parser.add_argument('--prompt', required=True, help='Prompt for the system')
    trace_parser.add_argument('--log', action='store_true', help='Log outputs and strain')
    trace_parser.set_defaults(func=trace_command)

    # Interactive command
    interactive_parser = subparsers.add_parser('interactive', help='Run an interactive session between systems')
    interactive_parser.add_argument('--systems', nargs=2, metavar=('SYS1', 'SYS2'), required=True, help='Systems for interactive session (e.g., 1 2)')
    interactive_parser.add_argument('--modal', nargs='+', required=True, help='Modals for interactive session')
    interactive_parser.add_argument('--s2-provider', type=str, default=None, help='Specify the LLM provider for S2 (e.g., gemini, codex)')
    interactive_parser.set_defaults(func=interactive_command)

    # Report command
    report_parser = subparsers.add_parser('report', help='Generate a report')
    report_parser.add_argument('report_type', choices=['strain'], help='Type of report to generate')
    report_parser.set_defaults(func=report_command)

    return parser, subparsers
