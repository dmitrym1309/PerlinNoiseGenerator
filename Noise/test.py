import noise
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
import argparse
import os
from tkinter import messagebox


def generate_perlin_noise(shape, scale, seed, octaves, persistence, lacunarity):
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

def apply_height_map(noise_map, sea_level=0):
    """Преобразует карту шума в карту высот с водой"""
    terrain = np.copy(noise_map)
    terrain[terrain < sea_level] = sea_level
    return terrain

def create_temperature_map(height_map, base_temp=20):
    """Создает карту температур на основе высоты"""
    temp_map = base_temp - (height_map * 20)
    return temp_map

class PerlinNoiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор карт на основе шума Перлина v1.0")
        
        # Создаем папку для сохранения карт
        self.save_dir = "generated_maps"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # Параметры по умолчанию
        self.size = tk.IntVar(value=100)
        self.scale = tk.DoubleVar(value=50.0)
        self.seed = tk.IntVar(value=10)
        self.octaves = tk.IntVar(value=6)
        self.persistence = tk.DoubleVar(value=0.5)
        self.lacunarity = tk.DoubleVar(value=2.0)
        self.sea_level = tk.DoubleVar(value=0.0)
        self.map_type = tk.StringVar(value='noise')
        self.view_type = tk.StringVar(value='2d')
        self.quality_3d = tk.StringVar(value='medium')
        
        # Создаем фрейм для элементов управления
        control_frame = ttk.LabelFrame(root, text="Параметры", padding="5")
        control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Добавляем элементы управления
        ttk.Label(control_frame, text="Размер:").grid(row=0, column=0, sticky="w")
        ttk.Entry(control_frame, textvariable=self.size, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(control_frame, text="Масштаб:").grid(row=1, column=0, sticky="w")
        ttk.Scale(control_frame, from_=1, to=100, variable=self.scale, orient="horizontal").grid(row=1, column=1, padx=5)
        
        ttk.Label(control_frame, text="Seed:").grid(row=2, column=0, sticky="w")
        ttk.Entry(control_frame, textvariable=self.seed, width=10).grid(row=2, column=1, padx=5)
        
        ttk.Label(control_frame, text="Октавы:").grid(row=3, column=0, sticky="w")
        ttk.Scale(control_frame, from_=1, to=10, variable=self.octaves, orient="horizontal").grid(row=3, column=1, padx=5)
        
        ttk.Label(control_frame, text="Persistence:").grid(row=4, column=0, sticky="w")
        ttk.Scale(control_frame, from_=0, to=1, variable=self.persistence, orient="horizontal").grid(row=4, column=1, padx=5)
        
        ttk.Label(control_frame, text="Уровень моря:").grid(row=5, column=0, sticky="w")
        ttk.Scale(control_frame, from_=-1, to=1, variable=self.sea_level, orient="horizontal").grid(row=5, column=1, padx=5)
        
        ttk.Label(control_frame, text="Тип карты:").grid(row=6, column=0, sticky="w")
        ttk.Combobox(control_frame, textvariable=self.map_type, 
                    values=['noise', 'height', 'temperature']).grid(row=6, column=1, padx=5)
        
        # Добавляем переключатель режима отображения
        ttk.Label(control_frame, text="Вид:").grid(row=7, column=0, sticky="w")
        ttk.Radiobutton(control_frame, text="2D", variable=self.view_type, 
                       value='2d', command=self.generate_map).grid(row=7, column=1, sticky="w")
        ttk.Radiobutton(control_frame, text="3D", variable=self.view_type, 
                       value='3d', command=self.generate_map).grid(row=7, column=1, sticky="e")
        
        # Добавляем выбор качества 3D
        ttk.Label(control_frame, text="Качество 3D:").grid(row=8, column=0, sticky="w")
        quality_combo = ttk.Combobox(control_frame, textvariable=self.quality_3d,
                                   values=['low', 'medium', 'high'])
        quality_combo.grid(row=8, column=1, padx=5)
        quality_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_map())
        
        # Кнопка генерации
        ttk.Button(control_frame, text="Генерировать", command=self.generate_map).grid(row=9, column=0, columnspan=2, pady=10)
        
        # Создаем область для отображения карты
        self.fig = plt.Figure(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)
        
        # Добавляем панель инструментов для навигации
        toolbar_frame = ttk.Frame(root)
        toolbar_frame.grid(row=1, column=1, sticky="ew")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        # Добавляем меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить карту", command=self.save_map)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        # Генерируем начальную карту
        self.generate_map()
    
    def get_quality_params(self):
        quality = self.quality_3d.get()
        if quality == 'low':
            return 4, 25  # step, rcount
        elif quality == 'medium':
            return 2, 50
        else:  # high
            return 1, 100

    def generate_map(self):
        self.fig.clear()
        
        # Получаем данные карты
        shape = (self.size.get(), self.size.get())
        world = generate_perlin_noise(
            shape, 
            self.scale.get(), 
            self.seed.get(), 
            self.octaves.get(), 
            self.persistence.get(), 
            self.lacunarity.get()
        )
        
        if self.map_type.get() == 'height':
            world = apply_height_map(world, self.sea_level.get())
            title = f'Карта высот (sea_level={self.sea_level.get():.2f})'
        elif self.map_type.get() == 'temperature':
            height_map = apply_height_map(world, self.sea_level.get())
            world = create_temperature_map(height_map)
            title = 'Карта температур'
        else:
            title = f'Шум Перлина (seed={self.seed.get()}, scale={self.scale.get():.1f})'
        
        if self.view_type.get() == '3d':
            step, rcount = self.get_quality_params()
            
            ax = self.fig.add_subplot(111, projection='3d')
            x, y = np.meshgrid(np.linspace(0, shape[0]-1, shape[0]//step),
                             np.linspace(0, shape[1]-1, shape[1]//step))
            
            world_downsampled = world[::step, ::step]
            
            surf = ax.plot_surface(x, y, world_downsampled,
                                 cmap='terrain',
                                 linewidth=0,
                                 antialiased=False,
                                 rcount=rcount,
                                 ccount=rcount)
            
            ax.set_title(title)
            self.fig.colorbar(surf)
            
            ax.view_init(elev=30, azim=45)
            
            ax.set_box_aspect([1, 1, 0.5])
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Высота')
            
            ax.set_xlim(0, shape[0])
            ax.set_ylim(0, shape[1])
            ax.set_zlim(world.min(), world.max())
            
        else:
            ax = self.fig.add_subplot(111)
            im = ax.imshow(world, cmap='terrain')
            ax.set_title(title)
            self.fig.colorbar(im)
        
        self.canvas.draw()

    def save_map(self):
        from datetime import datetime
        filename = f"map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.fig.savefig(os.path.join(self.save_dir, filename))
        tk.messagebox.showinfo("Сохранение", f"Карта сохранена как {filename}")
    
    def show_about(self):
        tk.messagebox.showinfo("О программе",
            "Генератор карт на основе шума Перлина\n"
            "Версия 1.0\n\n"
            "Программа для генерации и визуализации карт\n"
            "с использованием алгоритма шума Перлина")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerlinNoiseGUI(root)
    root.mainloop()