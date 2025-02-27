# -*- coding: utf-8 -*-
import noise
import numpy as np

class NoiseGenerator:
    @staticmethod
    def generate_perlin_noise(shape, scale, seed, octaves, persistence, lacunarity):
        """Генерирует карту шума Перлина с заданными параметрами"""
        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise3(i/scale, 
                                        j/scale, 
                                        seed,
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity)
        return world

    @staticmethod
    def apply_height_map(noise_map, sea_level=0):
        """Преобразует карту шума в карту высот с водой"""
        terrain = np.copy(noise_map)
        terrain[terrain < sea_level] = sea_level
        return terrain

    @staticmethod
    def create_temperature_map(height_map, base_temp=20):
        """Создает карту температур на основе высоты"""
        temp_map = base_temp - (height_map * 20)
        return temp_map 