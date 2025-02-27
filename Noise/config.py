# -*- coding: utf-8 -*-

# ��������� �� ���������
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

# ��������� �������� 3D �����������
QUALITY_SETTINGS = {
    'low': (4, 25),    # (step, rcount) - ������ ��������, ������� ���������
    'medium': (2, 50),  # ������� ��������
    'high': (1, 100)   # ������� ��������, ��������� ���������
}

# ��������� �������� ����
COLOR_SCHEMES = {
    'terrain': 'terrain',  # ����������� ����� ��� ���������
    'hot': 'hot',         # ��� ������������� ����
    'coolwarm': 'coolwarm'  # ������������ ��� ������������� ����
}

# ��������� ��������
EXPORT_SETTINGS = {
    'dpi': 300,  # ���������� ��� ����������
    'formats': ['png', 'jpg', 'pdf']  # �������������� �������
}

# ������ ���������
VERSION = "1.1" 