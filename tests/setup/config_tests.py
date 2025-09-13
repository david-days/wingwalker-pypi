import pytest
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
            os.remove(f)
        except PermissionError:
            print(f"Permission denied: Unable to remove '{f}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    hfiles = glob.glob(f'{path}/.*')
    for hf in hfiles:
        try:
            os.remove(hf)
        except PermissionError:
            print(f"Permission denied: Unable to delete '{hf}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

@pytest.fixture(scope='session')
def dir_setup():
    # Create the output dir
    output_dir = "out"
    print(f"\tChecking/creating output directory '{output_dir}'...")
    create_dir(output_dir)
    print(f"\tClearing out files in '{output_dir}', if they exists...")
    clean_dir(output_dir)


