import os
import sys
import configparser
import subprocess
from pathlib import Path

class DependencyVisualizer:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.package_name = self.config['Main']['PackageName']
        self.output_path = Path(self.config['Main']['OutputPath'])
        self.visualizer_path = self.config['Main']['VisualizerPath']
        self.dependencies = {}

    def _load_config(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def extract_dependencies(self, package_path):
        print(f"Извлечение зависимостей для пакета: {package_path}")
        # Пример зависимостей
        self.dependencies = {
            self.package_name: ["DependencyA", "DependencyB"],
            "DependencyA": ["DependencyC"],
            "DependencyB": [],
            "DependencyC": []
        }
        print(f"Зависимости: {self.dependencies}")

    def generate_mermaid_graph(self):
        lines = ["graph TD"]
        for parent, children in self.dependencies.items():
            for child in children:
                lines.append(f"    {parent} --> {child}")
        return "\n".join(lines)

    def save_mermaid_file(self, mermaid_graph, output_file):
        with open(output_file, 'w') as f:
            f.write(mermaid_graph)

    def generate_image(self, mermaid_file):
        command = [self.visualizer_path, "-i", mermaid_file, "-o", self.output_path]
        subprocess.run(command, check=True)

    def run(self, package_path):
        print("Запуск процесса анализа зависимостей...")
        self.extract_dependencies(package_path)  # Убедитесь, что метод вызывается
        mermaid_graph = self.generate_mermaid_graph()
        temp_mermaid_file = "temp_graph.mmd"
        self.save_mermaid_file(mermaid_graph, temp_mermaid_file)
        self.generate_image(temp_mermaid_file)
        os.remove(temp_mermaid_file)
        print(f"Граф сохранен в {self.output_path}")

if __name__ == "__main__":
    try:
        # Получаем аргументы командной строки
        config_path = sys.argv[1]  # Путь к конфигурационному файлу
        package_path = sys.argv[2]  # Путь к пакету для анализа

        # Выводим полученные параметры для проверки
        print(f"Конфигурация: {config_path}, Пакет: {package_path}")

        # Создаем объект DependencyVisualizer и запускаем анализ
        visualizer = DependencyVisualizer(config_path)
        visualizer.run(package_path)
        
    except Exception as e:
        # Если возникает ошибка, выводим её сообщение
        print(f"Произошла ошибка: {e}")