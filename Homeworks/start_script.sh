echo "Подготовка к сборке..."
mkdir -p virtual_fs

echo "Запуск тестов..."
py -m unittest discover -s . -p "Test_*.py" > test_results.txt
cat test_results.txt

echo "Очистка временных файлов..."
rm -rf __pycache__ build dist virtual_fs

echo "Скрипт завершен."
