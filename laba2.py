import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pandas as pd

def get_image_info(filepath):
    try:
        with Image.open(filepath) as img:
            info = {
                "Имя файла": os.path.basename(filepath),
                "Размер (пикс)": f"{img.width}x{img.height}",
                "Разрешение (dpi)": f"{img.info.get('dpi', (0, 0))[0]} dpi",
                "Глубина цвета": img.mode,
                "Сжатие": img.info.get("compression", "Нет")
            }
            return info
    except Exception as e:
        return {
            "Имя файла": os.path.basename(filepath),
            "Ошибка": str(e)
        }

def process_folder():
    folder = filedialog.askdirectory(title="Выберите папку с изображениями")
    if not folder:
        return

    supported_formats = (".jpg", ".jpeg", ".gif", ".tif", ".bmp", ".png", ".pcx")

    image_data = []

    try:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(supported_formats):
                    filepath = os.path.join(root, file)
                    image_info = get_image_info(filepath)
                    image_data.append(image_info)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось обработать папку: {e}")
        return

    if not image_data:
        messagebox.showinfo("Результат", "В выбранной папке нет поддерживаемых изображений.")
        return

    show_results(image_data)

def show_results(data):
    df = pd.DataFrame(data)
    output_file = "image_info.xlsx"
    df.to_excel(output_file, index=False)

    top = tk.Toplevel(root)
    top.title("Результаты")
    text = tk.Text(top, wrap=tk.NONE, width=120, height=30)
    text.insert(tk.END, df.to_string(index=False))
    text.pack(fill=tk.BOTH, expand=True)
    tk.Label(top, text=f"Результаты также сохранены в файл: {output_file}").pack()

root = tk.Tk()
root.title("Чтение информации из графических файлов")

btn_select_folder = tk.Button(root, text="Выбрать папку", command=process_folder)
btn_select_folder.pack(pady=20)

root.mainloop()
