from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import os

def download_video(file_name_var):
    url = url_entry.get()
    save_path = save_path_var.get()
    file_name = file_name_var.get()
    
    try:
        yt = YouTube(url)
        
        title_label.config(text='Título: ' + yt.title)
        
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
        resolutions = [stream.resolution for stream in streams]
        resolutions.sort(key=lambda x: int(x[:-1]))
        
        quality_combobox['values'] = resolutions
        quality_combobox.current(0)
        
        # Obter a qualidade selecionada
        quality_choice = quality_combobox.get()
        stream = streams[resolutions.index(quality_choice)]
        
        file_size = stream.filesize
        
        def download_with_progress():
            stream.download(output_path=save_path, filename=file_name)
            download_btn['state'] = 'normal'
            status_label.config(text='Vídeo baixado com sucesso')
            
            # Renomeio do arquivo baixado para adicionar extensão .mp4
            original_path = os.path.join(save_path, file_name)
            new_file_name = os.path.join(save_path, file_name + '.mp4')
            os.rename(original_path, new_file_name)
            os.startfile(new_file_name)
        
        download_thread = threading.Thread(target=download_with_progress)
        download_thread.start()
        
    except VideoUnavailable:
        status_label.config(text='Erro: Vídeo não disponível')
    except Exception as e:
        print(e)
        status_label.config(text='Erro ao baixar o vídeo')

# Configuração da interface 
root = tk.Tk()
root.title("Baixador de Vídeos do YouTube")

url_label = ttk.Label(root, text='URL do YouTube:')
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

file_name_label = ttk.Label(root, text='Nome do arquivo:')
file_name_label.grid(row=1, column=0, padx=5, pady=5)

file_name_var = tk.StringVar()
file_name_entry = ttk.Entry(root, textvariable=file_name_var, width=40)
file_name_entry.grid(row=1, column=1, columnspan=1, padx=5, pady=5)

save_path_label = ttk.Label(root, text='Salvar em:')
save_path_label.grid(row=2, column=0, padx=5, pady=5)

save_path_var = tk.StringVar()
save_path_entry = ttk.Entry(root, textvariable=save_path_var, width=40)
save_path_entry.grid(row=2, column=1, padx=5, pady=5)

browse_button = ttk.Button(root, text='Browse', command=lambda: save_path_var.set(filedialog.askdirectory()))
browse_button.grid(row=2, column=2, padx=5, pady=5)


quality_combobox = ttk.Combobox(root, width=20)

download_btn = ttk.Button(root, text='Baixar', command=lambda: download_video(file_name_var))
download_btn.grid(row=4, column=0, columnspan=3, pady=10)


title_label = ttk.Label(root, text='Título: ')
title_label.grid(row=6, column=0, columnspan=3)

status_label = ttk.Label(root, text='')
status_label.grid(row=7, column=0, columnspan=3)

root.mainloop()
