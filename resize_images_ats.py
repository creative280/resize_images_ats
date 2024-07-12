import os
import glob
from PIL import Image
from tkinter import Tk, filedialog, simpledialog

def resize_image(input_path, output_path, max_size=(1920, 1080), output_format='PNG', quality=85, compress_level=6):
    try:
        with Image.open(input_path) as img:
            img.thumbnail(max_size, Image.LANCZOS)
            img = img.convert("RGB")  # Convertir a RGB para WebP y otros formatos
            
            # Ajustar el nombre del archivo de salida basado en el formato de salida
            if output_format == 'ORIGINAL':
                output_file = output_path
            else:
                output_file = f"{os.path.splitext(output_path)[0]}.{output_format.lower()}"

            # Guardar la imagen con los parámetros adecuados
            if output_format == 'PNG':
                img.save(output_file, format=output_format, optimize=True, compress_level=compress_level)
            elif output_format == 'WEBP':
                img.save(output_file, format=output_format, optimize=True, quality=quality)
            elif output_format == 'ORIGINAL':
                img.save(output_file, optimize=True)
            else:
                print(f"Formato de salida no soportado: {output_format}")
                return

        print(f"Imagen guardada en: {output_file}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def batch_resize_images(input_dir, output_dir, max_size=(1920, 1080), output_format='PNG', quality=85, compress_level=6):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for img_path in glob.glob(f"{input_dir}/*"):
        if img_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_name = os.path.basename(img_path)
            output_path = os.path.join(output_dir, img_name)
            resize_image(img_path, output_path, max_size, output_format, quality, compress_level)

def select_folder(prompt):
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    folder_selected = filedialog.askdirectory(title=prompt)
    return folder_selected

def select_output_format():
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    formats = ["PNG", "WEBP", "ORIGINAL"]
    output_format = simpledialog.askstring("Formato de salida", f"Elige el formato de salida ({', '.join(formats)}):")
    if output_format and output_format.upper() in formats:
        return output_format.upper()
    else:
        print("Formato de salida no válido. Se usará PNG por defecto.")
        return 'PNG'

if __name__ == "__main__":
    print("Selecciona la carpeta de entrada:")
    input_directory = select_folder("Selecciona la carpeta de entrada")
    print("Selecciona la carpeta de salida:")
    output_directory = select_folder("Selecciona la carpeta de salida")
    output_format = select_output_format()

    if input_directory and output_directory:
        batch_resize_images(input_directory, output_directory, output_format=output_format, quality=80, compress_level=6)
    else:
        print("No se seleccionaron carpetas válidas.")
