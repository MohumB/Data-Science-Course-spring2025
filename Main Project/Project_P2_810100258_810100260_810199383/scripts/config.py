import os

BASE_DIR = "E:/403-2/DS/Data-Science-Course-spring2025/Main Project/Phase 1/Database Assets"
os.getcwd()
RAW_DATA_CSV = os.path.join(BASE_DIR, "raw_data.csv")
PREPROCESSED_CSV = os.path.join(BASE_DIR, "preprocessed_data.csv")
FEATURE_ENGINEERED_CSV = os.path.join(BASE_DIR, "feature_engineered_data.csv")
TXT =os.path.join(BASE_DIR,"David_Copperfield.txt")
DATABASE = os.path.join(os.getcwd(),"database/dataset.db")