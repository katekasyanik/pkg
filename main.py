import tkinter as tk
from tkinter import colorchooser, messagebox
import numpy as np
from skimage import color


# Преобразование RGB в LAB
def rgb_to_lab(rgb):
    rgb_normalized = np.array(rgb) / 255.0  # Нормализация RGB
    lab = color.rgb2lab([[rgb_normalized]])[0][0]  # Преобразование
    return np.round(lab, 2)


# Преобразование LAB в RGB
def lab_to_rgb(lab):
    rgb_normalized = color.lab2rgb([[lab]])[0][0]
    rgb = np.clip(rgb_normalized * 255, 0, 255).astype(int)  # Обрезка значений
    return rgb


# Преобразование RGB в CMYK
def rgb_to_cmyk(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    k = 1 - max(r, g, b)
    if k == 1:
        return 0, 0, 0, 1
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)


# Преобразование CMYK в RGB
def cmyk_to_rgb(cmyk):
    c, m, y, k = cmyk
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)


# Функция обновления всех полей цвета
def update_all(rgb=None, lab=None, cmyk=None):
    if rgb is not None:
        lab = rgb_to_lab(rgb)
        cmyk = rgb_to_cmyk(rgb)
    elif lab is not None:
        rgb = lab_to_rgb(lab)
        cmyk = rgb_to_cmyk(rgb)
    elif cmyk is not None:
        rgb = cmyk_to_rgb(cmyk)
        lab = rgb_to_lab(rgb)

    rgb_label.config(text=f"RGB: {rgb}")
    lab_label.config(text=f"LAB: {lab}")
    cmyk_label.config(text=f"CMYK: {cmyk}")


# Функция выбора цвета из палитры
def choose_color():
    color_code = colorchooser.askcolor(title="Выберите цвет")
    if color_code and color_code[0]:
        rgb = tuple(map(int, color_code[0]))  # RGB значения
        update_all(rgb=rgb)
    else:
        messagebox.showwarning("Предупреждение", "Цвет не был выбран.")


# Создание окна
root = tk.Tk()
root.title("Цветовые модели: CMYK ↔ LAB ↔ RGB")

# Кнопка выбора цвета
color_button = tk.Button(root, text="Выбрать цвет", command=choose_color)
color_button.pack(pady=10)

# Метки для отображения значений
rgb_label = tk.Label(root, text="RGB: ")
rgb_label.pack(pady=5)

lab_label = tk.Label(root, text="LAB: ")
lab_label.pack(pady=5)

cmyk_label = tk.Label(root, text="CMYK: ")
cmyk_label.pack(pady=5)

root.mainloop()
