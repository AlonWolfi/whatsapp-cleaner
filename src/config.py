from pathlib import Path

# import os
# PROJECT_DIR = Path(os.path.abspath(os.curdir))
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / 'data'
SRC_DIR = PROJECT_DIR / 'src'
ASSETS_DIR = PROJECT_DIR / 'src' / 'assets'
TMP_DIR = DATA_DIR / 'tmp'




