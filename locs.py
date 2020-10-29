import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) #path of this file

#config files
CONFIG_PATH = os.path.join(ROOT_DIR, r'\config')

#update scripts
UPDATESPATH = os.path.join(ROOT_DIR, r'\src\etl')
sys.path.append(os.path.abspath(UPDATESPATH)) #update path so we can reference the scripts

#test nd QA scripts
TESTPATH = os.path.join(ROOT_DIR, r'\src\test')
sys.path.append(os.path.abspath(TESTPATH))