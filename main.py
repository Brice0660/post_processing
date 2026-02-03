
from pathlib import Path

from fluent_processing import FluentPostProcesser

fluent_exe_path = Path(r"C:\Program Files\ANSYS Inc\v232\fluent\ntbin\win64\fluent.exe")
case_file_path = Path(r"C:\Jon\BFH\BRT\26\Aero\CFD\New_side_V1\New_side_V1.cas.h5")

fluent_processer = FluentPostProcesser(fluent_exe_path, case_file_path)

# fluent_processer.create_jou_content()

# fluent_processer.create_images()

fluent_processer.get_excel_data()

fluent_processer.write_to_forcesheet()