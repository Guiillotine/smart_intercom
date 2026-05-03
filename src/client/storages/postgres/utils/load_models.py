import os
import pkgutil
from pathlib import Path


def get_subfolder_paths(folder_path: Path):
    """
    Retrieves a list of all immediate subfolder paths inside the given folder.

    :param folder_path: Path object pointing to the directory to scan.
    :return: List of absolute paths (as strings) for each item inside the folder.
    """

    subfolder_paths = []
    for item in os.listdir(folder_path):  # noqa: PTH208
        item_path = os.path.join(folder_path, item)  # noqa: PTH118
        if os.path.isdir(item_path):
            subfolder_paths.append(item_path)
    return subfolder_paths


def load_all_models() -> None:
    """
    Dynamically imports all Python modules from 'models' subfolders inside
    'src/modules'.

    The function scans every immediate subfolder of 'src/modules', locates its 'models'
    folder, and imports all modules found there to ensure model registration or side
    effects.

    :note:
        Assumes the folder structure: src/modules/<subfolder>/models/*.py

    :raises ImportError: if any module cannot be imported.
    """

    path = "src.modules"
    models_folder = "models"

    modules = []
    modules_path = Path("src/modules").resolve()
    subfolders = get_subfolder_paths(modules_path)

    for subfolder in subfolders:
        separator = "/"
        if "/" not in subfolder:
            separator = "\\"
        module = subfolder.split(separator)[-1]
        walked_modules = pkgutil.walk_packages(
            path=[f"{subfolder}/models"], prefix=f"{path}.{module}.{models_folder}."
        )
        modules.extend(module_info.name for module_info in walked_modules)

    for module in modules:
        __import__(module)
