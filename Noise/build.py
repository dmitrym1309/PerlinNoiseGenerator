import PyInstaller.__main__
import sys
import os

# Получаем текущую директорию
current_dir = os.path.dirname(os.path.abspath(__file__))

# Определяем пути к файлам
main_file = os.path.join(current_dir, 'test.py')
readme_file = os.path.join(current_dir, 'README.txt')
icon_path = os.path.join(current_dir, 'icon.ico')

# Проверяем существование основного файла
if not os.path.exists(main_file):
    print(f"Ошибка: Файл {main_file} не найден!")
    sys.exit(1)

# Определяем имя выходного файла
output_name = "PerlinNoiseGenerator"

# Базовые параметры
params = [
    main_file,  # основной файл с абсолютным путем
    '--name=%s' % output_name,
    '--onefile',
    '--noconsole',
    '--clean',
]

# Добавляем README, если он существует
if os.path.exists(readme_file):
    params.append(f'--add-data={readme_file};.')

# Добавляем иконку, если она существует
if os.path.exists(icon_path):
    params.append(f'--icon={icon_path}')

print(f"Сборка {main_file} в exe...")
print(f"Параметры сборки: {params}")

# Запускаем PyInstaller
PyInstaller.__main__.run(params)