import subprocess


def run_command(command):
    """Runs a shell command and prints its output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)


def format_project():
    """Formats the entire project using black and isort."""
    print("Starting code formatting...")
    run_command("isort .")
    run_command("black .")
    print("Code formatting completed!")


if __name__ == "__main__":
    format_project()
