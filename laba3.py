import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Функция загрузки изображения
def load_image():
    file_path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[("Изображения", "*.jpg;*.jpeg;*.png;*.bmp;*.tif")]
    )
    if not file_path:
        return
    global original_image, processed_image
    original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if original_image is None:
        messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
        return
    show_image(original_image, original_panel)

# Функция отображения изображения
def show_image(image, panel):
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    panel.config(image=image)
    panel.image = image

# Локальная пороговая обработка
def local_threshold():
    if original_image is None:
        messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
        return
    global processed_image
    block_size = 11  # Размер блока (должен быть нечетным)
    c_value = 2  # Постоянное значение, вычитаемое из среднего
    processed_image = cv2.adaptiveThreshold(
        original_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_value
    )
    show_image(processed_image, processed_panel)

# Адаптивная пороговая обработка
def adaptive_threshold():
    if original_image is None:
        messagebox.showerror("Ошибка", "Сначала загрузите изображение.")
        return
    global processed_image
    block_size = 11  # Размер блока (должен быть нечетным)
    c_value = 2  # Постоянное значение, вычитаемое из среднего
    processed_image = cv2.adaptiveThreshold(
        original_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_value
    )
    show_image(processed_image, processed_panel)

# Сохранение результата
def save_image():
    if processed_image is None:
        messagebox.showerror("Ошибка", "Нет обработанного изображения для сохранения.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("TIFF", "*.tif")]
    )
    if not file_path:
        return
    cv2.imwrite(file_path, processed_image)
    messagebox.showinfo("Успех", "Изображение сохранено успешно!")

# Создание окна приложения
root = tk.Tk()
root.title("Локальная и адаптивная пороговая обработка")

# Панели для отображения изображений
original_panel = tk.Label(root, text="Оригинал")
original_panel.grid(row=0, column=0, padx=10, pady=10)
processed_panel = tk.Label(root, text="Результат")
processed_panel.grid(row=0, column=1, padx=10, pady=10)

# Кнопки управления
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Загрузить изображение", command=load_image).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Локальная пороговая обработка", command=local_threshold).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Адаптивная пороговая обработка", command=adaptive_threshold).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Сохранить результат", command=save_image).grid(row=0, column=3, padx=5)

# Переменные для хранения изображений
original_image = None
processed_image = None

# Запуск основного цикла
root.mainloop()
