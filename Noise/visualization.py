# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class MapVisualizer:
    def __init__(self, figure):
        self.fig = figure
        
    def plot_2d(self, data, title):
        """Отображение 2D карты"""
        ax = self.fig.add_subplot(111)
        im = ax.imshow(data, cmap='terrain')
        ax.set_title(title)
        return im
        
    def plot_3d(self, data, shape, step, rcount, title):
        """Отображение 3D карты"""
        ax = self.fig.add_subplot(111, projection='3d')
        x, y = np.meshgrid(np.linspace(0, shape[0]-1, shape[0]//step),
                          np.linspace(0, shape[1]-1, shape[1]//step))
        
        world_downsampled = data[::step, ::step]
        
        surf = ax.plot_surface(x, y, world_downsampled,
                             cmap='terrain',
                             linewidth=0,
                             antialiased=False,
                             rcount=rcount,
                             ccount=rcount)
        
        ax.set_title(title)
        ax.view_init(elev=30, azim=45)
        ax.set_box_aspect([1, 1, 0.5])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Высота')
        
        ax.set_xlim(0, shape[0])
        ax.set_ylim(0, shape[1])
        ax.set_zlim(data.min(), data.max())
        
        return surf 