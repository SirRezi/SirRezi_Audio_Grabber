import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube
from moviepy.editor import *
import os

def choose_download_path():
    chosen_path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, chosen_path)

def download_audio():
    media_link = url_entry.get()
    audio_format = format_var.get()
    download_path = path_entry.get()

    try:
        if "youtube.com" in media_link:
            yt = YouTube(media_link)
            video = yt.streams.filter(only_audio=True).first()

            if audio_format == "mp3":
                audio_file = video.download(output_path=download_path, filename="audio")
                video_clip = AudioFileClip(audio_file)
                video_clip.write_audiofile(os.path.join(download_path, "audio.mp3"))
            elif audio_format == "wav":
                audio_file = video.download(output_path=download_path, filename="audio")
                video_clip = AudioFileClip(audio_file)
                video_clip.write_audiofile(os.path.join(download_path, "audio.wav"), codec='pcm_s16le')
            else:
                result_label.config(text="Ungültiges Audioformat. Bitte wähle zwischen 'mp3' oder 'wav'.")
                return

            result_label.config(text=f"Das Audio wurde als {audio_format} heruntergeladen nach: {download_path}")
        elif "spotify.com" in media_link:
            result_label.config(text="Spotify-Links werden noch nicht unterstützt.")
        else:
            result_label.config(text="Nur YouTube- und Spotify-Links werden unterstützt.")
    except Exception as e:
        result_label.config(text=f"Ein Fehler ist aufgetreten: {e}")

root = tk.Tk()
root.title("Audio Downloader")
root.geometry("400x300")  
root.configure(bg="#2c3e50") 

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), foreground="#ecf0f1", background="#2c3e50") 
style.configure("TButton", font=("Arial", 12), foreground="#000000", background="#e74c3c", borderwidth=1)  # Schriftfarbe geändert

made_by_label = tk.Label(root, text="Made by Sirrezi 2024", font=("Arial", 10), fg="#ecf0f1", bg="#2c3e50")
made_by_label.pack(side=tk.BOTTOM, pady=(5, 10))  

url_label = ttk.Label(root, text="YouTube oder Spotify Link:")
url_label.pack(padx=10, pady=(10, 5))  
url_entry = ttk.Entry(root, width=40)
url_entry.pack(padx=10, pady=5)

format_label = ttk.Label(root, text="Audioformat wählen:")
format_label.pack(padx=10, pady=5)
format_var = tk.StringVar(root)
format_var.set("mp3")
format_dropdown = ttk.OptionMenu(root, format_var, "mp3", "wav")
format_dropdown.pack(padx=10, pady=5)

path_label = ttk.Label(root, text="Speicherort:")
path_label.pack(padx=10, pady=5)
path_frame = ttk.Frame(root, style="TFrame")  
path_frame.pack(padx=10, pady=5, anchor="center") 
path_entry = ttk.Entry(path_frame, width=30)
path_entry.pack(side=tk.LEFT)
path_button = ttk.Button(path_frame, text="Durchsuchen", command=choose_download_path)
path_button.pack(side=tk.LEFT)

download_button = ttk.Button(root, text="Herunterladen", command=download_audio)
download_button.pack(padx=10, pady=10)

result_label = ttk.Label(root, text="", foreground="green", background="#2c3e50")
result_label.pack(padx=10, pady=5)

root.mainloop()
