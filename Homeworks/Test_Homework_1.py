import unittest
import os
import zipfile
import time
from unittest.mock import patch
from io import StringIO
from Homework_1 import VirtualFileSystem, main

class TestVirtualFileSystem(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Создание тестового ZIP-файла для виртуальной файловой системы
        cls.zip_path = 'test_vfs.zip'
        with zipfile.ZipFile(cls.zip_path, 'w') as zipf:
            zipf.writestr('test_file.txt', 'Hello, World!')
            zipf.writestr('test_dir/', '')
            zipf.writestr('test_dir/nested_file.txt', 'Nested file content')

    def setUp(self):
        # Инициализация виртуальной файловой системы перед каждым тестом
        self.vfs = VirtualFileSystem(self.zip_path)
        self.start_time = time.time()

    def test_ls_command(self):
        with open(self.vfs.extract_path / 'test_file.txt', 'w') as f:
            f.write("Test content")
        # Проверка команды ls: должен возвращать файлы в текущей директории
        files = self.vfs.list_files()
        self.assertIn('test_file.txt', files)
        self.assertIn('test_dir', files)

    def test_cd_command(self):
        os.makedirs(self.vfs.extract_path / 'test_dir', exist_ok=True)
        # Проверка команды cd: переход в папку и обратно
        self.vfs.change_directory('test_dir')
        self.assertEqual(self.vfs.current_path.name, 'test_dir')
        
        self.vfs.change_directory('..')
        self.assertEqual(self.vfs.current_path.name, 'virtual_fs')

    def test_uptime_command(self):
        # Проверка команды uptime: проверка, что время больше нуля
        with patch('time.time', return_value=self.start_time + 5):
            uptime = self.vfs.get_uptime()
            self.assertAlmostEqual(uptime, 5, delta=0.1)

    def test_whoami_command(self):
        # Проверка команды whoami: получение имени пользователя
        with patch('os.getlogin', return_value='test_user'):
            whoami = self.vfs.get_whoami()
            self.assertEqual(whoami, 'test_user')

    def test_uname_command(self):
        # Проверка команды uname: получение информации о системе
        with patch('platform.platform', return_value='Test_OS'):
            uname = self.vfs.get_uname()
            self.assertEqual(uname, 'Test_OS')

    def test_exit_command(self):
        valid_zip_path = 'D:/Config/Zip_File_config.zip'

        # Проверка команды exit: выход из программы
        with patch('sys.argv', ['Homework_1.py', valid_zip_path]):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue().strip()
                self.assertIn("Эмулятор запущен. Введите команду:", output)

    @classmethod
    def tearDownClass(cls):
        # Удаление тестового файла ZIP после завершения всех тестов
        if os.path.exists(cls.zip_path):
            os.remove(cls.zip_path)

if __name__ == '__main__':
    unittest.main()
