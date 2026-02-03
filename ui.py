
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from fluent_processing import FluentPostProcesser

class FluentProcessingUI():
    def __init__(self):
        self.fluent_exe_path = Path(r"C:\Program Files\ANSYS Inc\v252\fluent\ntbin\win64\fluent.exe")
        self.root = tk.Tk()
        self.root.geometry("450x100")
        self.root.title("Fluent Post-Processing")
        # create buttons and lables
        self.bt_select_folder = tk.Button(self.root, text="Add new Case", command=self.select_folder)
        self.bt_view_images = tk.Button(self.root, text="View Images", command=self.view_images)
        self.label = tk.Label(self.root, text="No Folder Selected")
        # place buttons and lables
        self.bt_view_images.grid(row=1, column=1)
        self.bt_select_folder.grid(row=1, column=2)
        self.label.grid(row=2, column=2)
        self.main_loop()

    def main_loop(self):
        self.root.mainloop()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.label.config(text=f"Selected folder:\n{folder}")
            self.case_file_path = Path(folder)
            self.bt_run_post_processing = tk.Button(self.root, text="Run Post-Processing", command=self.run_post_processing)
            self.bt_run_post_processing.grid(row=1, column=3)

    def view_images(self):
        pass

    def run_post_processing(self):
        fluent_processer = FluentPostProcesser(self.fluent_exe_path, self.case_file_path)
        fluent_processer.create_jou_content()
        fluent_processer.create_images()