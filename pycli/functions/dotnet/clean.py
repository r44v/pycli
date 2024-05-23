import pathlib
import os
import shutil

def run():
    """
    Removes a obj & bin folders recusivly
    """
    def remove_if_exists(path: pathlib.Path):
        if path.exists():
            shutil.rmtree(path)
            print(f"Removed {path}")
    for root, dirs, files in os.walk('.'):
        # check if folder is dotnet project root
        if not any(f.endswith('.csproj') for f in files):
            break

        root_path = pathlib.Path(root)
        remove_if_exists(root_path / 'obj')
        remove_if_exists(root_path / 'bin')
        
    print("Done")