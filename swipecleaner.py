import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SwipeCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SwipeCleaner")
        self.root.configure(bg="#0f0f0f")
        self.root.geometry("1000x750")
        self.files = []
        self.index = 0
        self.delete_queue = []

        self.label = tk.Label(self.root, text="🧼 SwipeCleaner", font=("Segoe UI", 20, "bold"), fg="#00ffff", bg="#0f0f0f")
        self.label.pack(pady=20)

        self.choose_btn = tk.Button(self.root, text="📁 Choose Folder", command=self.choose_folder,
                                    bg="#1a1a2e", fg="#00ffff", font=("Segoe UI", 12, "bold"), padx=10, pady=5)
        self.choose_btn.pack()

        self.canvas = tk.Canvas(self.root, width=800, height=500, bg="#1f1f1f", highlightthickness=0)
        self.canvas.pack(pady=20)

        self.filename_label = tk.Label(self.root, text="", font=("Segoe UI", 14), fg="#ffffff", bg="#0f0f0f")
        self.filename_label.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#0f0f0f")
        btn_frame.pack(pady=20)

        self.left_btn = tk.Button(btn_frame, text="❌ Delete", command=self.swipe_left,
                                  bg="#ff4c4c", fg="white", font=("Segoe UI", 12, "bold"), padx=15, pady=10)
        self.left_btn.grid(row=0, column=0, padx=30)

        self.right_btn = tk.Button(btn_frame, text="✅ Keep", command=self.swipe_right,
                                   bg="#4caf50", fg="white", font=("Segoe UI", 12, "bold"), padx=15, pady=10)
        self.right_btn.grid(row=0, column=1, padx=30)

        self.stop_btn = tk.Button(self.root, text="🛑 Stop Cleaning", command=self.stop_cleaning,
                                  bg="#6666cc", fg="white", font=("Segoe UI", 12, "bold"), padx=20, pady=10)
        self.stop_btn.pack(pady=10)

        self.root.bind("<Left>", lambda e: self.swipe_left())
        self.root.bind("<Right>", lambda e: self.swipe_right())

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.folder = folder
        self.files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if not self.files:
            messagebox.showinfo("No Files", "No files found in this folder.")
            return
        self.index = 0
        self.delete_queue = []
        self.show_file()

    def show_file(self):
        self.canvas.delete("all")
        if self.index >= len(self.files):
            self.finish()
            return
        filepath = os.path.join(self.folder, self.files[self.index])
        self.filename_label.config(text=self.files[self.index])
        try:
            if filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img = Image.open(filepath)
                img.thumbnail((800, 500))
                self.tk_img = ImageTk.PhotoImage(img)
                self.canvas.create_image(400, 250, image=self.tk_img)
            elif filepath.lower().endswith(('.txt', '.md', '.log')):
                with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                    lines = file.readlines()
                    preview_text = ''.join(lines[:15])
                    self.canvas.create_text(400, 250, text=preview_text.strip(), fill="#00ffff", font=("Courier", 12), width=760)
            else:
                self.canvas.create_text(400, 250, text="📄 " + os.path.splitext(filepath)[1].upper() + " File",
                                        fill="#999", font=("Segoe UI", 24, "bold"))
        except Exception as e:
            print(f"Preview error: {e}")
            self.canvas.create_text(400, 250, text="Preview Error", fill="#888", font=("Segoe UI", 24, "bold"))

    def swipe_left(self):
        self.delete_queue.append(self.files[self.index])
        self.index += 1
        self.show_file()

    def swipe_right(self):
        self.index += 1
        self.show_file()

    def stop_cleaning(self):
        deleted = 0
        for f in self.delete_queue:
            try:
                os.remove(os.path.join(self.folder, f))
                deleted += 1
            except Exception as e:
                print(f"Error deleting {f}: {e}")
        messagebox.showinfo("Stopped", f"Deleted {deleted} files. Cleaning stopped.")
        self.root.quit()

    def finish(self):
        if not self.delete_queue:
            messagebox.showinfo("Done", "No files selected for deletion.")
            return
        confirm = messagebox.askyesno("Confirm Deletion", f"Delete {len(self.delete_queue)} files?")
        if confirm:
            deleted = 0
            for f in self.delete_queue:
                try:
                    os.remove(os.path.join(self.folder, f))
                    deleted += 1
                except Exception as e:
                    print(f"Failed to delete {f}: {e}")
            messagebox.showinfo("Done", f"Deleted {deleted} files.")
        else:
            messagebox.showinfo("Cancelled", "No files were deleted.")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SwipeCleanerApp(root)
    root.mainloop()
