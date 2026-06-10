import subprocess
import sys
from typing import Union

# Dependencies can be:
#   - a plain string: pip package name (e.g. "tomllib")
#   - a dict for git sources:
#       { "git": "https://github.com/user/repo", "branch": "main" }
#   - a dict for local paths:
#       { "path": "/home/user/path/to/repo" }
#       { "path": "/home/user/path/to/repo", "branch": "development" }
#   - Optionally include "name" to specify the installed package name
#     used for checking if already installed:
#       { "git": "...", "branch": "dev", "name": "my-package" }
#       { "path": "/some/repo", "name": "my-package" }
OPTIONAL_DEPENDENCIES = ["tomllib"] #, "opencv-contrib-python", "matplotlib"]

DependencySpec = Union[str, dict]


def _is_installed(python_executable: str, package_name: str) -> bool:
    """Check if a package is already installed using `pip show`."""
    try:
        subprocess.check_output(
            [python_executable, '-m', 'pip', 'show', package_name],
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def _build_pip_arg(dep: dict) -> str:
    """Build a pip-installable string from a dependency dict.

    - Git remote: "git+https://github.com/user/repo@development"
    - Local path: "/home/user/path/to/repo"
    - Local path + branch: "git+file:///home/user/path/to/repo@development"
    """
    if "git" in dep:
        git_url = dep["git"]
        branch = dep.get("branch", "main")
        return f"git+{git_url}@{branch}"
    elif "path" in dep:
        path = dep["path"]
        branch = dep.get("branch")
        if branch:
            return f"git+file://{path}@{branch}"
        return path
    else:
        raise ValueError(f"Dependency dict must contain 'git' or 'path' key: {dep}")


def _resolve_package_name(dep: str | dict) -> str:
    """Get the human-readable package name for a dependency, used for
    progress messages and the already-installed check."""
    if isinstance(dep, dict):
        # Use explicit name if provided
        if "name" in dep:
            return dep["name"]
        # Derive from git URL
        if "git" in dep:
            git_url = dep["git"].rstrip("/")
            return git_url.split("/")[-1].replace(".git", "")
        # Derive from local path — use the directory name
        if "path" in dep:
            from pathlib import Path
            return Path(dep["path"]).name
    return dep


def check_and_install_dependencies(dependencies: list[DependencySpec] | None = None):
    if dependencies is None:
        dependencies = OPTIONAL_DEPENDENCIES
    print("Checking if required packages are installed...")
    # get path of blender internal python executable
    python_executable = str(sys.executable)

    try:
        # ------ ensure pip is available ------
        try:
            subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        except subprocess.CalledProcessError:
            subprocess.call([python_executable, "-m", "ensurepip", "--user"])

        # ------ figure out what's missing ------
        packages_to_install: list[str | dict] = []
        for dep in dependencies:
            dep_name = _resolve_package_name(dep)

            if _is_installed(python_executable, dep_name):
                print(f"{dep_name} already installed!")
            else:
                print(f"{dep_name} not installed, will install...")
                packages_to_install.append(dep)

        if not packages_to_install:
            print("All required packages already installed! Done!")
            return

        # ------ prepare pip ------
        subprocess.call([python_executable, "-m", "ensurepip", "--user"])
        subprocess.call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])

        # ------ install ------
        for dep in packages_to_install:
            dep_name = _resolve_package_name(dep)

            if isinstance(dep, dict):
                pip_arg = _build_pip_arg(dep)
                print(f"Installing {dep_name} from source ({pip_arg})...")
            else:
                pip_arg = dep
                print(f"Installing {dep_name}...")

            subprocess.call([python_executable, "-m", "pip", "install", pip_arg])
            print(f"{dep_name} installed successfully!")

        print("All required packages installed! Done!")
    except Exception as e:
        print(f"Error installing packages: {e}")
        print(f"\n[FREEMOCAP-BLENDER-ADDON-INIT] - Optional dependencies {dependencies} not installed, some functionality may not work! \n"
              f"Check the error above for more information.\n"
              f" If it's a permissions issue, try running Blender as an administrator (Windows) or using sudo (Linux). "
              f"\nYou should only have to do this once, the packages will be installed and available for future Blender sessions.")



if __name__ == "__main__":
    check_and_install_dependencies()
