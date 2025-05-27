"""Main entry point for the CLI application."""
import sys
from .cli import cli

def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        print("\nAborted!")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
