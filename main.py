import tkinter as tk
from tkinter import filedialog, ttk
import vlc
import os

BG_COLOR = "#1e1e2f"
BTN_COLOR = "#3a3a5f"
TXT_COLOR = "white"

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Video Player")
        self.root.geometry("800x500")
        self.root.configure(bg=BG_COLOR)

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.playlist = []
        self.index = 0
        self.paused = False

        self.style()
        self.create_ui()

    def style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "TButton",
            background=BTN_COLOR,
            foreground="white",
            padding=10,
            font=("Segoe UI", 10)
        )

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="🎬 Simple Video Player",
            bg=BG_COLOR,
            fg=TXT_COLOR,
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=10)

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Playlist
        left_frame = tk.Frame(main_frame, bg=BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            left_frame,
            text="📂 Playlist",
            bg=BG_COLOR,
            fg=TXT_COLOR,
            font=("Segoe UI", 12)
        ).pack(anchor="w")

        self.listbox = tk.Listbox(
            left_frame,
            bg="#2a2a40",
            fg="white",
            selectbackground="#5a5aff",
            font=("Segoe UI", 10)
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.listbox.bind("<Double-Button-1>", self.play_selected)

        # Controls
        right_frame = tk.Frame(main_frame, bg=BG_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        ttk.Button(right_frame, text="➕ Add Videos", command=self.add_videos).pack(fill=tk.X, pady=5)
        ttk.Button(right_frame, text="⏮ Prev", command=self.prev_video).pack(fill=tk.X, pady=5)
        ttk.Button(right_frame, text="⏯ Play / Pause", command=self.play_pause).pack(fill=tk.X, pady=5)
        ttk.Button(right_frame, text="⏭ Next", command=self.next_video).pack(fill=tk.X, pady=5)

        # Volume
        tk.Label(
            right_frame,
            text="🔊 Volume",
            bg=BG_COLOR,
            fg=TXT_COLOR
        ).pack(pady=(20, 5))

        self.volume = ttk.Scale(
            right_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume
        )
        self.volume.set(70)
        self.volume.pack(fill=tk.X)

    def add_videos(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov")]
        )
        for file in files:
            self.playlist.append(file)
            self.listbox.insert(tk.END, os.path.basename(file))

    def play_video(self):
        if not self.playlist:
            return
        media = self.instance.media_new(self.playlist[self.index])
        self.player.set_media(media)
        self.player.play()
        self.player.audio_set_volume(int(self.volume.get()))
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.index)

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.paused = True
        else:
            if self.paused:
                self.player.play()
                self.paused = False
            else:
                self.play_video()

    def next_video(self):
        if self.index < len(self.playlist) - 1:
            self.index += 1
            self.play_video()

    def prev_video(self):
        if self.index > 0:
            self.index -= 1
            self.play_video()

    def play_selected(self, event):
        if self.listbox.curselection():
            self.index = self.listbox.curselection()[0]
            self.play_video()

    def set_volume(self, val):
        self.player.audio_set_volume(int(float(val)))


if __name__ == "__main__":
    root = tk.Tk()
    VideoPlayer(root)
    root.mainloop()

