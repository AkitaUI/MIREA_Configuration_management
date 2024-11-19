import sys
import zipfile
import time
import platform

class VirtualFileSystem:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.zip_file = None
        self.zip_contents = []
        self.current_path = "/"
        self.start_time = time.time()

        self.setup_virtual_fs()

    def setup_virtual_fs(self):
        """Открываем ZIP-файл и сохраняем его содержимое"""
        if not zipfile.is_zipfile(self.zip_path):
            print("Error: The specified file is not a valid zip file.")
            sys.exit(1)

        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            self.zip_file = zip_ref
            self.zip_contents = zip_ref.namelist()

    def list_files(self):
        """Возвращает файлы и папки в текущей директории"""
        path = self.current_path.lstrip("/")
        if path:
            path = f"{path}/"

        # Фильтруем файлы и папки, которые находятся в текущей директории
        contents = set()
        for item in self.zip_contents:
            if item.startswith(path) and item != path:
                relative_path = item[len(path):]
                first_component = relative_path.split("/", 1)[0]
                contents.add(first_component)

        return sorted(contents)

    def change_directory(self, dir_name):
        """Меняет текущую директорию"""
        if dir_name == "..":
            if self.current_path != "/":
                self.current_path = "/".join(self.current_path.rstrip("/").split("/")[:-1])
                if not self.current_path:
                    self.current_path = "/"
        else:
            new_path = f"{self.current_path.rstrip('/')}/{dir_name}".lstrip("/")
            if not new_path.endswith("/"):
                new_path += "/"

            # Проверяем, есть ли такая директория в архиве
            for item in self.zip_contents:
                if item.startswith(new_path):
                    self.current_path = f"/{new_path}".rstrip("/")
                    return

            print(f"cd: no such file or directory: {dir_name}")

    def get_uptime(self):
        """Возвращает время работы эмулятора"""
        return time.time() - self.start_time

    def get_whoami(self):
        """Возвращает имя пользователя"""
        return "virtual_user"

    def get_uname(self):
        """Возвращает информацию о системе"""
        return platform.platform()


def main():
    if len(sys.argv) != 2:
        print("Usage: python Homework_1.py <path_to_zip>")
        sys.exit(1)

    zip_path = sys.argv[1]
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
