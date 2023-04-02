import subprocess

if __name__ == "__main__":
    program = subprocess.Popen("pyinstaller --onefile --name llonvne_judger_server api.py"
                               , shell=True, text=True, stderr=subprocess.PIPE,stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    program.wait()
    print(program.stdout.read())
