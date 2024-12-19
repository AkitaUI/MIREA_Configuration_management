import re
import sys
import json
from collections import defaultdict

def parse_config(input_text): 
    constants = {}

    def parse_value(value): 
        if value.isdigit(): 
            return int(value) 
        elif value.startswith("q(") and value.endswith(")"): 
            return value[2:-1] 
        elif value.startswith("[") and value.endswith("]"): 
            return [parse_value(v.strip()) for v in value[1:-1].split(",")] 
        elif value.startswith("#{") and value.endswith("}"): 
            constant_name = value[2:-1].strip()
            if constant_name not in constants: 
                raise ValueError(f"Undefined constant: {constant_name}") 
            return constants[constant_name] 
        else: 
            return value 

    def parse_line(line): 
        if "->" in line: 
            value, name = map(str.strip, line.split("->")) 
            # Убираем завершающий символ `;` из названия константы
            name = name.rstrip(";")
            if not re.fullmatch(r"[A-Z]+", name): 
                raise ValueError(f"Invalid name syntax: {name}") 
            return name, value
        else: 
            raise ValueError(f"Invalid line syntax: {line}") 

    lines = input_text.splitlines() 
    clean_lines = []

    # Удаляем комментарии 
    multiline_comment = False 
    for line in lines: 
        line = line.strip() 
        if multiline_comment: 
            if "*/" in line: 
                multiline_comment = False 
                line = line.split("*/", 1)[1] 
            else: 
                continue 

        if "/*" in line: 
            multiline_comment = True 
            line = line.split("/*", 1)[0] 

        clean_lines.append(line) 

    # Собираем строки
    parsed_lines = []
    for line in clean_lines: 
        line = line.strip() 
        if line: 
            parsed_lines.append(parse_line(line)) 

    # Первый проход: добавляем строки без ссылок на другие константы
    unresolved_lines = []
    for name, value in parsed_lines:
        try:
            constants[name] = parse_value(value)
        except ValueError:
            # Если не удалось обработать строку, откладываем её
            unresolved_lines.append((name, value))

    # Второй проход: обрабатываем отложенные строки
    while unresolved_lines:
        progress = False
        for name, value in unresolved_lines[:]:  # Итерируем копию списка
            try:
                constants[name] = parse_value(value)
                unresolved_lines.remove((name, value))
                progress = True
            except ValueError:
                pass  # Ещё не готовы, пропускаем

        if not progress:
            # Если не удалось обработать ни одной строки, это циклическая зависимость
            unresolved_names = [name for name, _ in unresolved_lines]
            raise ValueError(f"Circular or undefined dependencies detected: {unresolved_names}")

    return constants

def constants_to_toml(constants): 
    toml_lines = [] 
    for key, value in constants.items(): 
        if isinstance(value, str): 
            toml_lines.append(f"{key} = \"{value}\"") 
        elif isinstance(value, int): 
            toml_lines.append(f"{key} = {value}") 
        elif isinstance(value, list): 
            toml_values = ", ".join(json.dumps(v) for v in value) 
            toml_lines.append(f"{key} = [{toml_values}]") 
    return "\n".join(toml_lines)

def main():
    print("Программа запущена")  # Отладочный вывод
    try:
        input_text = sys.stdin.read()
        print("Входной текст:", input_text)  # Проверяем входной текст
        constants = parse_config(input_text)
        toml_output = constants_to_toml(constants)
        print(toml_output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()