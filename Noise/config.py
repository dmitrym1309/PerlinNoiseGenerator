# -*- coding: utf-8 -*-

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    'size': 100,
    'scale': 50.0,
    'seed': 10,
    'octaves': 6,
    'persistence': 0.5,
    'lacunarity': 2.0,
    'sea_level': 0.0,
    'map_type': 'noise',
    'view_type': '2d',
    'quality_3d': 'medium'
}

# Настройки качества 3D отображения
QUALITY_SETTINGS = {
    'low': (4, 25),    # (step, rcount) - низкое качество, быстрая отрисовка
    'medium': (2, 50),  # среднее качество
    'high': (1, 100)   # высокое качество, медленная отрисовка
}

# Настройки цветовых схем
COLOR_SCHEMES = {
    'terrain': 'terrain',  # стандартная схема для ландшафта
    'hot': 'hot',         # для температурных карт
    'coolwarm': 'coolwarm'  # альтернатива для температурных карт
}

# Настройки экспорта
EXPORT_SETTINGS = {
    'dpi': 300,  # разрешение при сохранении
    'formats': ['png', 'jpg', 'pdf']  # поддерживаемые форматы
}

# Версия программы
VERSION = "1.1" 