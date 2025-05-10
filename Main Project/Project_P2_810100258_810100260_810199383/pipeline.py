import subprocess
from pathlib import Path

def run_pipeline():
    script_dir = Path(__file__).parent
    db_path = script_dir / "database" / "dataset.db"
    text_csv = script_dir / "../../Phase 1/CSV/text.csv"
    cleaned_text_csv = script_dir / "../../Phase 1/CSV/cleaned_text.csv"
    sentences_csv = script_dir / '../../Phase 1/CSV/sentences.csv'

    print("Loading data...")
    subprocess.run(["python", "scripts/load_data.py",db_path,text_csv])
    
    print("Preprocessing data...")
    subprocess.run(["python", "scripts/preprocess.py",text_csv,cleaned_text_csv])
    
    print("Feature Engineering...")
    subprocess.run(["python", "scripts/feature_engineering.py",cleaned_text_csv,sentences_csv])

    print("Importing sentences to database...")
    subprocess.run(["python", "scripts/import_to_db.py",sentences_csv,db_path])

if __name__ == "__main__":
    run_pipeline()


