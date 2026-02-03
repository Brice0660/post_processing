
from pathlib import Path

from ui import FluentProcessingUI
from fluent_processing import FluentPostProcesser

fluent_exe_path = Path(r"C:\Program Files\ANSYS Inc\v232\fluent\ntbin\win64\fluent.exe")
case_file_path = Path(r"C:\Jon\BFH\BRT\26\Aero\CFD\New_side_V1\New_side_V1.cas.h5")

fluent_processing_ui = FluentProcessingUI()