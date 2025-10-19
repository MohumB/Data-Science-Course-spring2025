import subprocess

subprocess.run(["python", "scripts/import_to_db.py"])
subprocess.run(["python", "scripts/load_data.py"])
subprocess.run(["python", "scripts/preprocess.py"])
subprocess.run(["python", "scripts/feature_engineering.py"])
