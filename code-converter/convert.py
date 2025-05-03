# Import standard libraries
import os
import shutil
from pathlib import Path
from datetime import datetime

# Import third-party libraries
from nbformat import read, write, v4 as nbf
from nbformat import NO_CONVERT

# Define current directory
CURRENT_DIR = Path(__file__).parent

# Function to convert Python script to Jupyter notebook
def py_to_ipynb(py_file_path, output_path):
    """
    Convert a Python script with '# %%' markers to a .ipynb notebook.

    Args:
        py_file_path (Path): Path to the .py file.
        output_path (Path): Destination path for the .ipynb file.
    """
    print(f"\n🔄 Converting: {py_file_path.name} → {output_path.name}")
    with open(py_file_path, 'r') as f:
        lines = f.readlines()

    cells = []
    code_buffer = []

    for line in lines:
        if line.strip().startswith('# %%'):
            if code_buffer:
                cells.append(nbf.new_code_cell(''.join(code_buffer)))
                code_buffer = []
        else:
            code_buffer.append(line)

    if code_buffer:
        cells.append(nbf.new_code_cell(''.join(code_buffer)))

    notebook = nbf.new_notebook(cells=cells)
    with open(output_path, 'w', encoding='utf-8') as f:
        write(notebook, f)

# Function to convert Jupyter notebook to Python script with cell markers
def ipynb_to_py(ipynb_file_path, output_path):
    """
    Convert a .ipynb notebook into a .py script using '# %%' cell markers.

    Args:
        ipynb_file_path (Path): Path to the .ipynb file.
        output_path (Path): Destination path for the .py file.
    """
    print(f"\n🔄 Converting: {ipynb_file_path.name} → {output_path.name}")
    with open(ipynb_file_path, 'r', encoding='utf-8') as f:
        notebook = read(f, as_version=NO_CONVERT)

    with open(output_path, 'w') as f:
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                f.write("# %%\n")
                f.write(cell.source + '\n\n')

# Function to back up and clean converted files
def backup_and_clean(extension):
    """
    Move all files of the given extension (excluding key scripts) to a timestamped backup directory.

    Args:
        extension (str): File extension to back up (e.g., 'py', 'ipynb').
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = CURRENT_DIR / f"{extension}_backup_{timestamp}"

    print(f"\n📦 Creating versioned backup folder:")
    print(backup_dir)

    backup_dir.mkdir()

    for f in CURRENT_DIR.glob(f"*.{extension}"):
        if f.name not in {"converter.py", "main.py"}:
            print(f"\n📁 Moving {f.name} →")
            print(backup_dir / f.name)
            shutil.move(f, backup_dir / f.name)

# Function to perform batch conversion
def convert(source_ext, dest_ext, convert_fn):
    """
    Convert all files from one extension to another using a specified function.

    Args:
        source_ext (str): Source file extension.
        dest_ext (str): Destination file extension.
        convert_fn (function): Function to apply for conversion.
    """
    source_folder = CURRENT_DIR
    source_files = list(source_folder.glob(f"*.{source_ext}"))

    if not source_files:
        print(f"\n❌ No .{source_ext} files found in:")
        print(source_folder)
        return

    for f in source_files:
        out_file = f.with_suffix(f".{dest_ext}")
        convert_fn(f, out_file)

    backup_and_clean(source_ext)

# Function to trigger conversion by option number
def convert_by_number(conversion_index):
    """
    Dispatch conversion logic based on a numeric option.

    Args:
        conversion_index (int): 1 for ipynb→py, 2 for py→ipynb.

    Raises:
        ValueError: If an unsupported index is provided.
    """
    if conversion_index == 1:
        convert("ipynb", "py", ipynb_to_py)
    elif conversion_index == 2:
        convert("py", "ipynb", py_to_ipynb)
    else:
        raise ValueError(f"Unsupported conversion index: {conversion_index}")


# Command center
# Convert all .ipynb files to .py
# convert_by_number(1)

# Convert all .py files to .ipynb
convert_by_number(2)

# Print confirmation message
print("\n✅ converter.py successfully executed")
