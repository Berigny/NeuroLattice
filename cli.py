import argparse
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from cli_agent.parser import setup_parser

if __name__ == "__main__":
    context = {'kernel_data': None, 'lattice': None}
    parser, subparsers = setup_parser(context)

    import shlex

    if len(sys.argv) > 1:
        # Non-interactive mode
        args = parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args, context)
        else:
            parser.print_help()
    else:
        # Interactive mode
        print("NeuroLattice CLI. Type 'exit' to quit.")
        while True:
            try:
                cmd_line = input("> ")
                if cmd_line.lower() == 'exit':
                    break
                
                if not cmd_line:
                    continue

                args = parser.parse_args(shlex.split(cmd_line))
                if hasattr(args, 'func'):
                    args.func(args, context)
                else:
                    parser.print_help()
            except SystemExit:
                # argparse throws this when --help is used.
                pass
            except Exception as e:
                print(f"Error: {e}")