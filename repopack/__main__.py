from .cli import run_cli

# This is the main entry point for the repopack command-line application.
# It checks if the script is being run directly (not imported as a module)
# and if so, it calls the run_cli function to start the CLI.

if __name__ == "__main__":
    run_cli()  # type: ignore
    # Note: The type: ignore comment is added because run_cli is imported
    # from a local module and mypy might not be able to infer its type.
