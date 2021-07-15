import time

import numpy as np
import scipy
import streamlit as st

# from __tmp import tmp
# from config import SRC_DIR, TMP_DIR


# @st.cache   
# def init_tmp_dir():
#     # mkdir
#     import os
#     if not os.path.exists(TMP_DIR):
#         os.makedirs(TMP_DIR)
#     # delete files
#     for f in os.listdir(TMP_DIR):
#         os.remove(os.path.join(TMP_DIR, f))


# def refresh_page():
#     tmp_py_path = SRC_DIR / '__tmp.py'
#     with open(tmp_py_path, 'w+') as f:
#         f.write('import streamlit as st\n')
#         f.write('\n')
#         f.write('def tmp():\n')
#         f.write(f'  if False:\n')
#         f.write(f'      st.markdown("{np.random.randint(0, 10000)}")\n')
#     time.sleep(0.1)
#     tmp()


def is_picklable(obj):
    try:
        pickle.dumps(obj)
    except pickle.PicklingError:
        return False
    return True


import json
import os
import pickle
import warnings
from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
from matplotlib.pyplot import Figure


def validate_path(file_path: Union[str, Path]):
    for folder in list(Path(file_path).parents)[::-1]:
        try:
            os.stat(folder)
        except:
            os.mkdir(folder)


def save_data(data, file_path: Union[str, Path], encoding: str = "utf-8"):
    '''
    Saves data to file
    '''

    if type(file_path) == str:
        file_path = Path(file_path)

    validate_path(file_path)

    if file_path.suffix == '.pickle':
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    elif file_path.suffix == '.json':
        with open(file_path, 'wb') as file:
            json.dump(data, file)
    elif type(data) == Figure:
        data.save_fig(file_path)
    else:
        with open(file_path, 'w+', encoding=encoding) as file:
            file.write(data)


@st.cache
def read_data(file_path: Union[str, Path, list, dict, set], encoding: str = "utf-8"):
    """
    Saves data to file_path
    @param file_path:
    @param encoding:
    @return:
    """

    if type(file_path) == str:
        file_path = Path(file_path)

    validate_path(file_path)

    data = None

    if not os.path.exists(file_path):
        warnings.warn(f'   File not found: {file_path}', Warning)
        return None

    if file_path.suffix == '.pickle':
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
    elif file_path.suffix == '.json':
        with open(file_path, 'rb') as file:
            data = json.load(file)
    elif file_path.suffix == '.jpg' or file_path.suffix == '.png':
        data = plt.imread(file_path, format='PNG')
    else:
        with open(file_path, 'r+', encoding=encoding) as file:
            data = file.read()
    return data
