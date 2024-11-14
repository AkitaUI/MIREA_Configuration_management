import os
import sys
import zipfile
import time
import platform
from pathlib import Path

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.extract_path = Path("virtual_fs")
        self.current_path = self.extract_path
        self.start_time = time.time()

        self.setup_virtual_fs()

    def setup_virtual_fs(self):
        if not self.extract_path.exists():
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_path)

    def list_files(self):
        return os.listdir(self.current_path)

    def change_directory(self, dir_name):
        if dir_name == "..":
            self.current_path = self.current_path.parent
        else:
            new_path = self.current_path / dir_name
            if new_path.exists() and new_path.is_dir():
                self.current_path = new_path
            else:
                print(f"cd: no such file or directory: {dir_name}")

    def get_uptime(self):
        return time.time() - self.start_time

    def get_whoami(self):
        return os.getlogin()

    def get_uname(self):
        return platform.platform()

def main():
    print("Запуск стартового скрипта...")
    script_path = "start_script.sh"
    if os.path.exists(script_path):
        bash_path = r"D:\Config\Git\bin\bash.exe"
        result = subprocess.run([bash_path, script_path], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("Ошибка при запуске стартового скрипта:", result.stderr)
            sys.exit(1)
    else:
        print("Стартовый скрипт не найден.")
        
    global start_time
    
    if len(sys.argv) != 2:
        print("Usage: python emulator.py <path_to_zip>")
        sys.exit(1)

    zip_path = sys.argv[1]
    if not zipfile.is_zipfile(zip_path):
        print("Error: The specified file is not a valid zip file.")
        sys.exit(1)

    global start_time
    start_time = time.time()
    vfs = VirtualFileSystem(zip_path)

    print("Эмулятор запущен. Введите команду:")
    while True:
        command = input(f"{vfs.current_path}> ").strip()
        if command == "exit":
            break
        elif command.startswith("cd "):
            dir_name = command.split(" ", 1)[1] if " " in command else ""
            vfs.change_directory(dir_name)
        elif command == "ls":
            files = vfs.list_files()
            print("\n".join(files))
        elif command == "uptime":
            print(f"Uptime: {vfs.get_uptime():.2f} seconds")
        elif command == "whoami":
            print(vfs.get_whoami())
        elif command == "uname":
            print(vfs.get_uname())
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
