from pathlib import Path
import os
import json
import subprocess
 
confFile = Path("./conf/config.json")
confData = {
    "name": "idk",
    "version": "0.0.1",
    "updateUrl": "https://raw.githubusercontent.com/xdatomic-the-codeur/softUpdate/main/version.json"
}
 
def config():
    #Config
    print("Configuration...")
    os.system('cls')
    os.system(f"TITLE {"Configuration du programme"}")
    with open("./conf/config.json", "x") as conf:
        json.dump(confData, conf, indent=4)
    print("Conf file successfuly created")
 
def update(v):
    commande = "curl -s https://raw.githubusercontent.com/xdatomic-the-codeur/softUpdate/main/version.json"
    version_info = subprocess.run(commande, capture_output=True, text=True, shell=True)
    if version_info.returncode == 0:
        version_info = json.loads(version_info.stdout)
        print("Last version : "+ version_info["idk"]['version'])
        if(v != version_info["idk"]['version']):
            print("Updating...")
            update = version_info["idk"]['codeUrl']
            os.remove("./index.py")
            commande = "curl -s "+ update + " -o index.py"
            version_info = subprocess.run(commande, capture_output=True, text=True, shell=True)
            if version_info.returncode == 0:
                #Update json file
                conf = open("./conf/config.json", "r")
                data = json.load(conf)
                conf.close()
                data["version"] = version_info["idk"]["version"]
 
                conf = open("./conf/config.json", "w+")
                conf.write(json.dumps(data))
                conf.close()
 
                print("Update finished ! Please restart python file.")
            else:
                print("Erreur:")
                print(version_info.stderr)
        else:
            print("Program is up to date")
 
if confFile.is_file():
    print("Program is config")
    configFile = open('./conf/config.json')
    configFile = json.load(configFile)
    version = configFile['version']
    print("Program version : "+ version)
    update(version)
else:
    print("Program not config")
    config()
