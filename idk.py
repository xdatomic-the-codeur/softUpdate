from pathlib import Path
from prettytable import PrettyTable
import os
import json
import subprocess


"""

                                                                                                                                                          
                                                                                                                                      bbbbbbbb            
WWWWWWWW                           WWWWWWWW iiii     ffffffffffffffff    iiii         GGGGGGGGGGGGG                                   b::::::b            
W::::::W                           W::::::Wi::::i   f::::::::::::::::f  i::::i     GGG::::::::::::G                                   b::::::b            
W::::::W                           W::::::W iiii   f::::::::::::::::::f  iiii    GG:::::::::::::::G                                   b::::::b            
W::::::W                           W::::::W        f::::::fffffff:::::f         G:::::GGGGGGGG::::G                                    b:::::b            
 W:::::W           WWWWW           W:::::Wiiiiiii  f:::::f       ffffffiiiiiii G:::::G       GGGGGGrrrrr   rrrrrrrrr   aaaaaaaaaaaaa   b:::::bbbbbbbbb    
  W:::::W         W:::::W         W:::::W i:::::i  f:::::f             i:::::iG:::::G              r::::rrr:::::::::r  a::::::::::::a  b::::::::::::::bb  
   W:::::W       W:::::::W       W:::::W   i::::i f:::::::ffffff        i::::iG:::::G              r:::::::::::::::::r aaaaaaaaa:::::a b::::::::::::::::b 
    W:::::W     W:::::::::W     W:::::W    i::::i f::::::::::::f        i::::iG:::::G    GGGGGGGGGGrr::::::rrrrr::::::r         a::::a b:::::bbbbb:::::::b
     W:::::W   W:::::W:::::W   W:::::W     i::::i f::::::::::::f        i::::iG:::::G    G::::::::G r:::::r     r:::::r  aaaaaaa:::::a b:::::b    b::::::b
      W:::::W W:::::W W:::::W W:::::W      i::::i f:::::::ffffff        i::::iG:::::G    GGGGG::::G r:::::r     rrrrrrraa::::::::::::a b:::::b     b:::::b
       W:::::W:::::W   W:::::W:::::W       i::::i  f:::::f              i::::iG:::::G        G::::G r:::::r           a::::aaaa::::::a b:::::b     b:::::b
        W:::::::::W     W:::::::::W        i::::i  f:::::f              i::::i G:::::G       G::::G r:::::r          a::::a    a:::::a b:::::b     b:::::b
         W:::::::W       W:::::::W        i::::::if:::::::f            i::::::i G:::::GGGGGGGG::::G r:::::r          a::::a    a:::::a b:::::bbbbbb::::::b
          W:::::W         W:::::W         i::::::if:::::::f            i::::::i  GG:::::::::::::::G r:::::r          a:::::aaaa::::::a b::::::::::::::::b 
           W:::W           W:::W          i::::::if:::::::f            i::::::i    GGG::::::GGG:::G r:::::r           a::::::::::aa:::ab:::::::::::::::b  
            WWW             WWW           iiiiiiiifffffffff            iiiiiiii       GGGGGG   GGGG rrrrrrr            aaaaaaaaaa  aaaabbbbbbbbbbbbbbbb   
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          

"""

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
        latest_version = version_data["WifiGraber"]["version"]

        if current_version != latest_version:
            print("Updating...")

            update_code_url = version_data["WifiGraber"]["codeUrl"]

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

def wifi()->list:
    try:
        # Try decoding with UTF-8 encoding
        wifi_data = (subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("utf-8").split("\n"))
    except UnicodeDecodeError:
        # If UTF-8 fails, try using 'latin-1' encoding
        wifi_data = (subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode("latin-1").split("\n"))

    profiles = []
    for line in wifi_data:
        if "Profil Tous les utilisateurs" in line:
            profile_name = line.split(":")[1][1:-1]
            profiles.append(profile_name)

    return profiles

def wifi_password(ssid: str) -> str:
    encodings = ["latin-1", "utf-8", "cp1252"]
    for encoding in encodings:
        try:
            command_output = subprocess.check_output(
                ["netsh", "wlan", "show", "profile", f"name=\"{ssid}\"", "key=clear"],
                encoding=encoding,
            )
            lines = command_output.split("\n")
            for line in lines:
                if "Contenu de la cl" in line:
                    password = line.partition(":")[2].strip()
                    return password
        except (UnicodeDecodeError, subprocess.CalledProcessError):
            continue  # Try the next encoding or next SSID

    return "N/A"

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
        os.system("cls")
    else:
        print("Program not configured.")
        config()
    
    table = PrettyTable()
    i=0
    table.field_names = ["Id", "SSID", "Password"]
    all_wifi = wifi()
    for ssid in all_wifi:
        table.add_row([i, ssid, wifi_password(ssid)])
        i=i+1
    print(table)


if __name__ == "__main__":
    main()
