import tkinter as tk
from tkinter import filedialog
import subprocess
import threading
import time
import tkinter.ttk as ttk

# Função para escolher arquivos APK
def choose_apks():
    files = filedialog.askopenfilenames(filetypes=[("APK files", "*.apk")])
    apk_list.delete(0, tk.END)
    for file in files:
        apk_list.insert(tk.END, file)

# Função para instalar APKs em dispositivos selecionados
def install_apks():
    selected_devices = device_list.curselection()
    if not selected_devices:
        output_text.insert(tk.END, "Selecione pelo menos um dispositivo.\n")
        return

    apk_paths = apk_list.get(0, tk.END)
    if not apk_paths:
        output_text.insert(tk.END, "Selecione pelo menos um arquivo APK.\n")
        return

    total_apks = len(selected_devices) * len(apk_paths)

    adb_path = adb_entry.get().strip()
    if not adb_path:
        output_text.insert(tk.END, "Insira o caminho para a pasta do ADB.\n")
        return

    progress_bar['maximum'] = total_apks
    progress_bar['value'] = 0

    installed_apks.set(f"0 de {total_apks} APKs instalados")

    def install_thread(device_id, apk_path, total_apks):
        command = f'"{adb_path}/adb" -s {device_id} install -r "{apk_path}"'
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_text.insert(tk.END, f"Instalando APK no dispositivo {device_id}:\n")
        output_text.insert(tk.END, f"{result.stdout}{result.stderr}")
        output_text.insert(tk.END, "\n")

        progress_bar['value'] += 1
        installed_apks.set(f"{progress_bar['value']} de {total_apks} APKs instalados")

    for device_id in selected_devices:
        device_id = device_list.get(device_id)
        for apk_path in apk_paths:
            apk_path = apk_path.strip()
            t = threading.Thread(target=install_thread, args=(device_id, apk_path, total_apks))
            t.start()

# Função para desativar a depuração USB nos dispositivos selecionados
def disable_usb_debugging():
    selected_devices = device_list.curselection()
    if not selected_devices:
        output_text.insert(tk.END, "Selecione pelo menos um dispositivo.\n")
        return

    adb_path = adb_entry.get().strip()
    if not adb_path:
        output_text.insert(tk.END, "Insira o caminho para a pasta do ADB.\n")
        return

    for device_idx in selected_devices:
        device_id = device_list.get(device_idx)
        command = f'"{adb_path}/adb" -s {device_id} shell settings put global adb_enabled 0'
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_text.insert(tk.END, f"Depuração USB desativada para o dispositivo {device_id}:\n")
        output_text.insert(tk.END, result.stdout + result.stderr)
        output_text.insert(tk.END, "\n")

# Configurar a janela da interface
window = tk.Tk()
window.title("Instalador de APKs via ADB")

# Desativar a capacidade de maximizar a janela
window.resizable(width=False, height=False)
# Entrada para o caminho da pasta do ADB
adb_label = tk.Label(window, text="Caminho da Pasta do ADB:")
adb_label.pack()
adb_entry = tk.Entry(window, width=40)
adb_entry.pack(pady=5)

# Botão para escolher arquivos APK
choose_button = tk.Button(window, text="Escolher APKs", command=choose_apks)
choose_button.pack(pady=10)

# Lista de arquivos APK selecionados
apk_list = tk.Listbox(window, selectmode=tk.MULTIPLE, width=40, height=5)
apk_list.pack(pady=5)

# Botão para listar dispositivos
list_devices_button = tk.Button(window, text="Listar Dispositivos", command=lambda: list_devices(device_list, adb_entry.get()))
list_devices_button.pack(pady=10)

# Lista de dispositivos
device_list = tk.Listbox(window, selectmode=tk.MULTIPLE, width=40, height=5)
device_list.pack(pady=5)

# Botão para instalar APKs em dispositivos selecionados
install_button = tk.Button(window, text="Instalar APKs", command=install_apks)
install_button.pack(pady=10)

# Botão para desativar a depuração USB nos dispositivos selecionados
disable_usb_debugging_button = tk.Button(window, text="Desativar Depuração USB", command=disable_usb_debugging)
disable_usb_debugging_button.pack(pady=10)

# Barra de progresso para mostrar a porcentagem de instalação
progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

# Variável de controle para a mensagem de APKs instalados
installed_apks = tk.StringVar()

# Rótulo para exibir a mensagem de APKs instalados
installed_apks_label = tk.Label(window, textvariable=installed_apks)
installed_apks_label.pack(pady=10)

# Área de texto para exibir a saída do ADB
output_text = tk.Text(window, height=10, width=40)
output_text.pack()

# Função para listar dispositivos
def list_devices(device_list, adb_path):
    if not adb_path:
        output_text.insert(tk.END, "Insira o caminho para a pasta do ADB.\n")
        return

    result = subprocess.run(f'"{adb_path}/adb" devices', shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    devices = [line.split('\t')[0] for line in result.stdout.split('\n')[1:] if line.strip()]
    device_list.delete(0, tk.END)
    for device in devices:
        device_list.insert(tk.END, device)

window.mainloop()
