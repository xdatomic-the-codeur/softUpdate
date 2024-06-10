from pathlib import Path
import os
import json
import subprocess

# Configuration file path
conf_file = Path("./conf/config.json")

# Default configuration data
default_conf_data = {
    "name": "idk",
    "version": "0.0.1",
    "updateUrl": "https://raw.githubusercontent.com/xdatomic-the-codeur/softUpdate/main/version.json"
}


def config():
    print("Configuration...")
    os.system("clear")  # Clear the terminal screen

    if not conf_file.is_file():
        # Create the configuration file with default data
        with conf_file.open("w") as conf:
            json.dump(default_conf_data, conf, indent=4)
        print("Conf file successfully created")
    else:
        print("Configuration file already exists.")


def update(current_version):
    update_url = "https://raw.githubusercontent.com/xdatomic-the-codeur/softUpdate/main/version.json"

    try:
        update_info = subprocess.run(
            ["curl", "-s", update_url], capture_output=True, text=True
        )
        update_info.check_returncode()  # Raise an exception on non-zero exit code

        version_data = json.loads(update_info.stdout)
        latest_version = version_data["idk"]["version"]

        if current_version != latest_version:
            print("Updating...")

            update_code_url = version_data["idk"]["codeUrl"]

            try:
                # Use shutil.move or similar for secure file replacement
                os.replace("./index.py", "./index.py.bak")  # Backup current file (optional)
                subprocess.run(
                    ["curl", "-s", update_code_url, "-o", "index.py"], capture_output=True, text=True
                ).check_returncode()  # Raise an exception on non-zero exit code

                # Update the version in the configuration file
                with conf_file.open("r") as conf:
                    data = json.load(conf)
                data["version"] = latest_version
                with conf_file.open("w") as conf:
                    json.dump(data, conf, indent=4)

                print("Update finished! Please restart the program.")

            except subprocess.CalledProcessError as e:
                print("Error during update download:", e.stderr)
                # Consider restoring the backup if necessary

        else:
            print("Program is up to date.")

    except subprocess.CalledProcessError as e:
        print("Error checking for updates:", e.stderr)


def main():
    """The main program entry point.

    Checks for configuration file existence and calls config() or update() accordingly.
    """

    if conf_file.is_file():
        print("Program is configured.")
        with conf_file.open("r") as conf:
            config_data = json.load(conf)
        current_version = config_data["version"]
        print("Program version:", current_version)
        update(current_version)
    else:
        print("Program not configured.")
        config()


if __name__ == "__main__":
    main()
