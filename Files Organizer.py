import os
import shutil
from tkinter import *
from tkinter import filedialog, messagebox
from datetime import datetime
import pandas as pd

# Variables globales
selected_folder = ""

# ---------- FUNCIONES PRINCIPALES ----------

def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory(title="Selecciona la carpeta con archivos")
    if selected_folder:
        label_folder.config(text=f"📁 Carpeta: {selected_folder}")
    else:
        label_folder.config(text="Carpeta no seleccionada")

def classify_files():
    if not selected_folder:
        messagebox.showwarning("Carpeta no seleccionada", "Por favor selecciona una carpeta.")
        return

    files = [f for f in os.listdir(selected_folder) if os.path.isfile(os.path.join(selected_folder, f))]
    if not files:
        messagebox.showinfo("Sin archivos", "No se encontraron archivos en la carpeta seleccionada.")
        return

    criterion = organization_criterion.get()
    log_data = []

    for filename in files:
        source_path = os.path.join(selected_folder, filename)
        name, ext = os.path.splitext(filename)

        if criterion == "extension":
            folder_name = ext[1:].upper() if ext else "NO_EXTENSION"
        elif criterion == "date":
            timestamp = os.path.getmtime(source_path)
            folder_name = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        elif criterion == "name":
            folder_name = name.split("_")[0].upper()
        else:
            folder_name = "UNKNOWN"

        target_folder = os.path.join(selected_folder, folder_name)
        os.makedirs(target_folder, exist_ok=True)
        shutil.move(source_path, os.path.join(target_folder, filename))

        log_data.append({
            "filename": filename,
            "organized_by": folder_name,
            "criterion": criterion
        })

    # Guardar log
    log_df = pd.DataFrame(log_data)
    log_df.to_csv(os.path.join(selected_folder, "classification_log.csv"), index=False)
    messagebox.showinfo("Proceso completado", f"Se organizaron {len(files)} archivos.")

# ---------- INTERFAZ GRÁFICA ----------

root = Tk()
root.title("Excel/CSV Classifier")
root.geometry("500x300")
organization_criterion = StringVar(value="extension")
root.config(padx=20, pady=20)

Label(root, text="Organizar archivos por:", font=("Arial", 12)).pack(pady=5)
Radiobutton(root, text="Extensión", variable=organization_criterion, value="extension").pack(anchor="w")
Radiobutton(root, text="Fecha de modificación", variable=organization_criterion, value="date").pack(anchor="w")
Radiobutton(root, text="Nombre parcial (antes del guion bajo)", variable=organization_criterion, value="name").pack(anchor="w")

Button(root, text="Seleccionar Carpeta", command=select_folder).pack(pady=10)
label_folder = Label(root, text="Carpeta no seleccionada", fg="gray")
label_folder.pack()

Button(root, text="Organizar Archivos", command=classify_files, bg="blue", fg="white").pack(pady=20)

root.mainloop()

