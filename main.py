import threading
from tkinter.filedialog import askdirectory
import tkinter as tk
import pytube
import os
import moviepy.editor as mvp
import urllib.request
import eyed3


def download_thread(vid, title):
    if download_dir != "":
        path = download_dir
    else:
        path = str(os.path.expanduser("~"))
        if os.path.isdir(path + os.path.sep + "Downloads"):
            path += os.path.sep + "Downloads"
        elif os.path.isdir(path + os.path.sep + "Pobrane"):
            path += os.path.sep + "Pobrane"
    vid.streams.filter(file_extension='mp4').first().download(output_path=path, filename="tmp")
    vid_mp4 = mvp.VideoFileClip(path + os.path.sep + "tmp.mp4").subclip(0)
    mp3_path = path + os.path.sep + title + ".mp3"
    vid_mp4.audio.write_audiofile(mp3_path)
    """
    vid_thumbnail_url = vid.thumbnail_url
    urllib.request.urlretrieve(vid_thumbnail_url, path+os.path.sep+"tmp.png")
    try:
        audio_file = eyed3.load(mp3_path)
        audio_file.tag.images.set(3, open(path + os.path.sep +'tmp.png', 'rb'), 'image/png')
        audio_file.tag.save()
    except TypeError:
        pass
    os.remove(path + os.path.sep + "tmp.png")
    """
    os.remove(path + os.path.sep + "tmp.mp4")
    lbl_status.config(fg="green", text="Download succeed")


def download_fromyt():
    url = str(ent_url.get())
    try:
        vid = pytube.YouTube(url)
    except pytube.exceptions.RegexMatchError:
        lbl_status.config(fg="red", text="Provided URL seems to be invalid, try again")
        return 1
    except pytube.exceptions.LiveStreamError:
        lbl_status.config(fg="red", text="You can't download livestreams")
        return 1
    except pytube.exceptions.VideoUnavailable:
        lbl_status.config(fg="red", text="Video seems to be unavailable, check if it's privacy is set to public")
    title = vid.title
    lbl_status.config(fg="yellow", text="Downloading {}".format(title))
    thread = threading.Thread(target=download_thread, args=(vid, title))
    thread.start()


def ask_for_download_dir():
    global download_dir
    download_dir = askdirectory()


window = tk.Tk()
download_dir = ""
window.title("YoutubeDownloader")
window.resizable(width=False, height=False)
frm_main = tk.Frame(window, borderwidth=4)
frm_main.grid(row=0, column=0, padx=50, pady=5)
lbl_link = tk.Label(frm_main, text="Enter YouTube's video URL")
lbl_link.grid(row=0, column=0, padx=5)
ent_url = tk.Entry(frm_main, width=50)
ent_url.grid(row=1, column=0)
btn_dir = tk.Button(frm_main, text="Change download dir", command=lambda: ask_for_download_dir())
btn_dir.grid(row=1, column=2)
btn_ok = tk.Button(frm_main, text="Download as mp3", command=lambda: download_fromyt())
btn_ok.grid(row=1, column=1, padx=10)
lbl_status = tk.Label(frm_main, text="Waiting for URL")
lbl_status.grid(row=2, column=0)

window.mainloop()
"""
TODO:
    Dodawanie miniatur filmu jako okładki pliku .mp3
    Możliwość wyboru mp4/mp3
"""