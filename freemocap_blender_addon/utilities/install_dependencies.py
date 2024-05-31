import subprocess
import sys

REQUIRED_PACKAGES = ["opencv-contrib-python", "matplotlib"]


def check_and_install_dependencies():
    print("Checking if required packages are installed...")
    # get path of blender internal python executable
    python_executable = str(sys.executable)

    try:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    except:
        subprocess.call([python_executable, "-m", "ensurepip", "--user"])
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])

    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    print("\nInstalled packages:", installed_packages, "\n")

    packages_to_install = []
    for package_name in REQUIRED_PACKAGES:
        if package_name in installed_packages:
            print(f"{package_name} already installed!")
        else:
            print(f"{package_name} not installed, will install...")
            packages_to_install.append(package_name)

    if len(packages_to_install) > 0:
        subprocess.call([python_executable, "-m", "ensurepip", "--user"])
        # update pip
        subprocess.call([python_executable, "-m", "pip", "install", "--upgrade", "pip"])

    for package_name in packages_to_install:
        print(f"Installing {package_name}...")
        subprocess.call([python_executable, "-m", "pip", "install", package_name])

        print(f"{package_name} installed successfully!")

    print("All required packages installed! Done!")


if __name__ == "__main__":
    check_and_install_dependencies()
