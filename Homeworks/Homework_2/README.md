Вариант №8

Задание №2  Разработать инструмент командной строки для визуализации графа зависимостей, включая транзитивные зависимости. Сторонние средства для получения зависимостей использовать нельзя. 
Зависимости определяются по имени пакета платформы .NET (nupkg). Для описания графа зависимостей используется представление Mermaid. Визуализатор должен выводить результат в виде сообщения об успешном 
выполнении и сохранять граф в файле формата png.

Конфигурационный файл имеет формат ini и содержит:

• Путь к программе для визуализации графов. 

• Имя анализируемого пакета. 

• Путь к файлу с изображением графа зависимостей.  

Все функции визуализатора зависимостей должны быть покрыты тестами.

Эта программа принимает конфигурационный файл и файл с расширением nupkg и на основе его содержания создает граф зафисимостей

Тестирование: В программе TestHomework_2.py было проведено тестирование эмулятора. Программа работает исправно.
