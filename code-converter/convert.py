import os
import nbformat as nbf
from pathlib import Path

source_dir = Path(__file__).parent  # Adjust if needed

for filename in os.listdir(source_dir):
    if filename.endswith(".py") and filename != "converter.py":  # Avoid self-conversion
        py_path = os.path.join(source_dir, filename)
        ipynb_path = os.path.join(source_dir, filename.replace(".py", ".ipynb"))

        with open(py_path, 'r') as f:
            code = f.read()

        nb = nbf.v4.new_notebook()
        nb['cells'] = [nbf.v4.new_code_cell(code)]

        with open(ipynb_path, 'w') as f:
            nbf.write(nb, f)

# Print confirmation message
print("\n✅ converter.py successfully executed")