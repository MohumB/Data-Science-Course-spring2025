import subprocess

def run_pipeline():
    print("Loading data...")
    subprocess.run(["python", "scripts/load_data.py"])
    
    print("Preprocessing data...")
    subprocess.run(["python", "scripts/preprocess.py"])
    
    print("Feature Engineering...")
    subprocess.run(["python", "scripts/feature_engineering.py"])

if __name__ == "__main__":
    run_pipeline()
