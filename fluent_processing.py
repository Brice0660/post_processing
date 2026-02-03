
from __future__ import annotations
import numpy as np
import subprocess
import sys
import time
from pathlib import Path

class FluentPostProcessing():
    def __init__(self, fluent_exe_path: Path, case_file_path: Path):
        self.fluent_exe_path = fluent_exe_path
        self.case_file_path = case_file_path
        self.work_dir = self.case_file_path.parent
        self.out_dir = self.work_dir / "images"
        self.jou_path = self.work_dir / "sequence_30_images.jou"
    
    def create_jou_content(self):
        self.out_dir.mkdir(parents=True, exist_ok=True)
        # --- Parameters of sequence ---
        start_z = 0.0
        end_z = 0.760  # 740 mm
        num_images_y = 30
        num_images_x = 45
        z_positions = np.linspace(start_z, end_z, num_images_y)

        start_x = -1.250
        end_x = 1.850 
        x_positions = np.linspace(start_x, end_x, num_images_x)
        # --- creating jou content ---
        jou_content = f"""/file/read-case-data "{self.case_file_path.as_posix()}"
            /file/confirm-overwrite? no
            /display/set-window 1
            /views/camera/projection orthographic
            """

        for i, z in enumerate(z_positions):
            s_name = f"plane_z_{i:02d}"
            img_name = f"images/side_{i:02d}.png"
            
            jou_content += f"""
                ; --- Image {i+1}/{num_images_y} at Z = {z:.4f} ---
                /surface/plane-surface {s_name} z {z:.4f}
                /display/set/contours surfaces {s_name} ()
                /display/contour/velocity-magnitude 0 35
                /views/auto-scale
                /views/camera/target 0 0 0
                /views/camera/position 0 1 0
                /views/camera/up-vector 0 0 1
                /views/camera/zoom-camera 6
                /views/camera/dolly-camera 0.2 1.5 0
                /display/save-picture "{img_name}"
                /surface/delete {s_name}
                """

        jou_content += f"""
            views/apply-mirror-planes symmetry ()
            """      

        for i, y in enumerate(x_positions):
            s_name = f"plane_x_{i:02d}"
            img_name = f"images/front_{i:02d}.png"
            
            jou_content += f"""
                ; --- Image {i+1}/{num_images_x} at x = {y:.4f} ---
                /surface/plane-surface {s_name} y {y:.4f}
                /display/set/contours surfaces {s_name} ()
                /display/contour/velocity-magnitude 0 35
                /views/camera/target 0 0 0
                /views/camera/position 1 0 0
                /views/camera/up-vector 0 0 1
                /views/auto-scale
                /views/camera/zoom-camera 4
                /views/camera/target 0 0 0.7
                /display/save-picture "{img_name}"
                /surface/delete {s_name}
                """
            


        jou_content += "\n/exit yes"
        
        self.jou_path.write_text(jou_content, encoding="utf-8")

    def create_images(self, timeout_s = 2000):
        cmd = [str(self.fluent_exe_path), "3d", "-t8", "-gu", "-i", str(self.jou_path)]
        start = time.time()
        proc = subprocess.Popen(
            cmd,
            cwd=str(self.work_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            )
        assert proc.stdout is not None
        try:
            for line in proc.stdout:
                print(line, end="")
                sys.stdout.flush()
                if time.time() - start > timeout_s:
                    proc.kill()
                    raise TimeoutError(f"Process was longer than {timeout_s}s.")
        finally:
            try:
                proc.stdout.close()
            except Exception:
                pass
        rc = proc.wait()
        if rc == 0:
            print(f"\n Images saved in: {self.out_dir}")
        else:
            print(f"\n Error occoured in process: (Code {rc})")