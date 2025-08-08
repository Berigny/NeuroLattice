import argparse
from cli_agent.agent import boot_agent
from cli_agent.parser import setup_parser

if __name__ == "__main__":
    lattice, kernel_data = boot_agent()
    parser = setup_parser(kernel_data, lattice)
    
    while True:
        try:
            cmd = input("> ")
            if cmd.lower() == 'exit':
                break
            args = parser.parse_args(cmd.split())
            args.func(args, kernel_data, lattice)
        except SystemExit:
            # This is to prevent argparse from exiting the script
            pass
        except Exception as e:
            print(f"Error: {e}")
