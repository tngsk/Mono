import argparse
import sys
from pathlib import Path


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Template for setting up a CLI using argparse.
    Inspired by Mono's main.py CLI structure.
    """
    parser = argparse.ArgumentParser(
        prog="MyConverter",
        description="A template CLI tool for converting files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python my_cli.py input.txt

  # Specify output file
  python my_cli.py input.txt -o output.txt

  # Enable verbose logging
  python my_cli.py input.txt -v
        """,
    )

    # Positional argument (Required)
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the input file to process.",
    )

    # Optional argument with a default value
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Path to the output file (defaults to input_file name with .out extension).",
    )

    # List of optional arguments (nargs="+")
    parser.add_argument(
        "-c",
        "--css",
        nargs="+",
        type=Path,
        default=None,
        help="Path to CSS files to embed (can specify multiple).",
    )

    # Boolean flag (store_true)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable detailed logging output.",
    )

    return parser


def main() -> int:
    """
    Main entry point for the CLI application.
    Returns the exit code (0 for success, 1 for error).
    """
    parser = create_argument_parser()

    # Parse arguments provided by the user
    args = parser.parse_args()

    # Determine output file path if not provided
    output_file = args.output
    if output_file is None:
        output_file = args.input_file.with_suffix(".out")

    # Example of how to use the parsed arguments
    print("=== CLI Application Started ===")
    print(f"Input File:  {args.input_file}")
    print(f"Output File: {output_file}")

    if args.css:
        print(f"CSS Files:   {[str(p) for p in args.css]}")

    if args.verbose:
        print("[DEBUG] Verbose mode is ENABLED. Detailed logs will be shown.")

    # Simulate some processing...
    try:
        if not args.input_file.exists():
            print(f"Error: Input file '{args.input_file}' does not exist.")
            return 1

        print("Processing complete!")
        return 0
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    # sys.exit ensures the proper OS return code is passed back to the terminal
    sys.exit(main())
