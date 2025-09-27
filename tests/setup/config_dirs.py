import os
import glob

def create_dir(path):
    try:
        os.mkdir(path)
        print(f"Directory '{path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{path}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_dir(path):
    files = glob.glob(f'{path}/*')
    for f in files:
        try:
            if not os.path.isdir(f):
                os.remove(f)
        except PermissionError:
            print(f"Permission denied: Unable to remove '{f}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    hfiles = glob.glob(f'{path}/.*')
    for hf in hfiles:
        try:
            if not os.path.isdir(hf):
                os.remove(hf)
        except PermissionError:
            print(f"Permission denied: Unable to delete '{hf}'.")
        except Exception as e:
            print(f"An error occurred: {e}")


def dir_setup(out_dir: str):
    """
    Create the directory structure for the given out path
    Args:
        out_dir: directory path to create (one or more directories and subdirectories)

    Returns:
        None
    """
    path_array = out_dir.split(os.path.sep)
    idx = 0
    mkpath = path_array[idx]
    while idx < len(path_array):
        print(f"\tChecking/creating output directory '{mkpath}'...")
        create_dir(mkpath)
        print(f"\tClearing out files in '{mkpath}', if they exists...")
        clean_dir(mkpath)
        if idx < len(path_array)-1:
            mkpath += f"{os.path.sep}{path_array[idx+1]}"
        idx += 1
