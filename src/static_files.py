import subprocess

def run():
    print("Copying static files")
    subprocess.Popen("cp -r ./templates/img ../", shell=True)
    subprocess.Popen("cp -r ./templates/css ../", shell=True)

if __name__ == "__main__":
    run()
