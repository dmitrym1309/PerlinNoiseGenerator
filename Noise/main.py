# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os
from datetime import datetime
from noise_generator import NoiseGenerator
from visualization import MapVisualizer
from config import DEFAULT_SETTINGS, QUALITY_SETTINGS

class PerlinNoiseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор карт на основе шума Перлина v1.1")
        
        self.setup_save_directory()
        self.initialize_variables()
        self.create_gui()
        self.setup_visualization()
        self.generate_map()
    
    def setup_save_directory(self):
        self.save_dir = "generated_maps"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def initialize_variables(self):
        self.size = tk.IntVar(value=DEFAULT_SETTINGS['size'])
        self.scale = tk.DoubleVar(value=DEFAULT_SETTINGS['scale'])
        self.seed = tk.IntVar(value=DEFAULT_SETTINGS['seed'])
        self.octaves = tk.IntVar(value=DEFAULT_SETTINGS['octaves'])
        self.persistence = tk.DoubleVar(value=DEFAULT_SETTINGS['persistence'])
        self.lacunarity = tk.DoubleVar(value=DEFAULT_SETTINGS['lacunarity'])
        self.sea_level = tk.DoubleVar(value=DEFAULT_SETTINGS['sea_level'])
        self.map_type = tk.StringVar(value=DEFAULT_SETTINGS['map_type'])
        self.view_type = tk.StringVar(value=DEFAULT_SETTINGS['view_type'])
        self.quality_3d = tk.StringVar(value=DEFAULT_SETTINGS['quality_3d'])
    
    def create_gui(self):
        self.create_control_frame()
        self.create_menu()
    
    def create_control_frame(self):
        control_frame = ttk.LabelFrame(self.root, text="Параметры", padding="5")
        control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        controls = [
            ("Размер:", self.size, "entry", {"width": 10}),
            ("Масштаб:", self.scale, "scale", {"from_": 1, "to": 100}),
            ("Seed:", self.seed, "entry", {"width": 10}),
            ("Октавы:", self.octaves, "scale", {"from_": 1, "to": 10}),
            ("Persistence:", self.persistence, "scale", {"from_": 0, "to": 1}),
            ("Уровень моря:", self.sea_level, "scale", {"from_": -1, "to": 1}),
        ]
        
        for i, (label, var, control_type, options) in enumerate(controls):
            ttk.Label(control_frame, text=label).grid(row=i, column=0, sticky="w")
            if control_type == "entry":
                ttk.Entry(control_frame, textvariable=var, **options).grid(row=i, column=1, padx=5)
            elif control_type == "scale":
                ttk.Scale(control_frame, variable=var, orient="horizontal", **options).grid(row=i, column=1, padx=5)
        
        self.add_map_type_selector(control_frame, len(controls))
        self.add_view_controls(control_frame, len(controls) + 1)
        
        ttk.Button(control_frame, text="Генерировать", command=self.generate_map).grid(
            row=len(controls) + 3, column=0, columnspan=2, pady=10)
    
    def add_map_type_selector(self, parent, row):
        ttk.Label(parent, text="Тип карты:").grid(row=row, column=0, sticky="w")
        ttk.Combobox(parent, textvariable=self.map_type,
                    values=['noise', 'height', 'temperature']).grid(row=row, column=1, padx=5)
    
    def add_view_controls(self, parent, row):
        ttk.Label(parent, text="Вид:").grid(row=row, column=0, sticky="w")
        view_frame = ttk.Frame(parent)
        view_frame.grid(row=row, column=1, sticky="w")
        
        ttk.Radiobutton(view_frame, text="2D", variable=self.view_type,
                       value='2d', command=self.generate_map).pack(side="left")
        ttk.Radiobutton(view_frame, text="3D", variable=self.view_type,
                       value='3d', command=self.generate_map).pack(side="left")
        
        ttk.Label(parent, text="Качество 3D:").grid(row=row + 1, column=0, sticky="w")
        quality_combo = ttk.Combobox(parent, textvariable=self.quality_3d,
                                   values=['low', 'medium', 'high'])
        quality_combo.grid(row=row + 1, column=1, padx=5)
        quality_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_map())
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить карту", command=self.save_map)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def setup_visualization(self):
        self.fig = plt.Figure(figsize=(8, 8))
        self.visualizer = MapVisualizer(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)
        
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.grid(row=1, column=1, sticky="ew")
        NavigationToolbar2Tk(self.canvas, toolbar_frame).update()
    
    def get_quality_params(self):
        return QUALITY_SETTINGS.get(self.quality_3d.get(), QUALITY_SETTINGS['medium'])
    
    def generate_map(self):
        self.fig.clear()
        
        shape = (self.size.get(), self.size.get())
        world = NoiseGenerator.generate_perlin_noise(
            shape, 
            self.scale.get(), 
            self.seed.get(), 
            self.octaves.get(), 
            self.persistence.get(), 
            self.lacunarity.get()
        )
        
        if self.map_type.get() == 'height':
            world = NoiseGenerator.apply_height_map(world, self.sea_level.get())
            title = f'Карта высот (sea_level={self.sea_level.get():.2f})'
        elif self.map_type.get() == 'temperature':
            height_map = NoiseGenerator.apply_height_map(world, self.sea_level.get())
            world = NoiseGenerator.create_temperature_map(height_map)
            title = 'Карта температур'
        else:
            title = f'Шум Перлина (seed={self.seed.get()}, scale={self.scale.get():.1f})'
        
        if self.view_type.get() == '3d':
            step, rcount = self.get_quality_params()
            surf = self.visualizer.plot_3d(world, shape, step, rcount, title)
            self.fig.colorbar(surf)
        else:
            im = self.visualizer.plot_2d(world, title)
            self.fig.colorbar(im)
        
        self.canvas.draw()
    
    def save_map(self):
        filename = f"map_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.fig.savefig(os.path.join(self.save_dir, filename))
        messagebox.showinfo("Сохранение", f"Карта сохранена как {filename}")
    
    def show_about(self):
        messagebox.showinfo("О программе",
            "Генератор карт на основе шума Перлина\n"
            "Версия 1.1\n\n"
            "Программа для генерации и визуализации карт\n"
            "с использованием алгоритма шума Перлина")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerlinNoiseGUI(root)
    root.mainloop() 