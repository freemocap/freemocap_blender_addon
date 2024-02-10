import subprocess
import sys

from ajc27_freemocap_blender_addon.system.configure_logging.configure_logging import (
    LogStrings
)

REQUIRED_PACKAGES = ["opencv-contrib-python", "matplotlib"]


def check_and_install_dependencies():
    print(LogStrings.INFO, "Checking if required packages are installed...")
    # get path of blender internal python executable
    python_executable = str(sys.executable)

    try:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    except:
        subprocess.call([python_executable, "-m", "ensurepip", "--user"])
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])

    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    print(LogStrings.DEBUG, "Installed packages:", installed_packages)

    packages_to_install = []
    for package_name in REQUIRED_PACKAGES:
        if package_name in installed_packages:
            print(LogStrings.DEBUG, f"{package_name} already installed!")
        else:
            print(LogStrings.DEBUG, f"{package_name} not installed, will install...")
            packages_to_install.append(package_name)

    if len(packages_to_install) > 0:
        subprocess.call([python_executable, "-m", "ensurepip", "--user"])
        # update pip
        subprocess.call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])

    for package_name in packages_to_install:
        print(LogStrings.INFO, f"Installing {package_name}...")
        subprocess.call([python_executable, "-m", "pip", "install", package_name])

        print(LogStrings.INFO, f"{package_name} installed successfully!")

    print(LogStrings.INFO, "All required packages installed! Done!")


if __name__ == "__main__":
    check_and_install_dependencies()
