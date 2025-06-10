#!/usr/bin/env python3
"""
Training Pipeline Automation Script
Orchestrates the entire model training workflow from data loading to model training.
"""

import argparse
import logging
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
import json
from test import test

class TrainingPipeline:
    """Automated training pipeline for LLaMA fine-tuning"""
    
    def __init__(self, config_path: str = None):
        self.setup_logging()
        self.config = self.load_config(config_path) if config_path else self.default_config()
        self.pipeline_start_time = datetime.now()
        
    def setup_logging(self):
        """Configure logging for the pipeline"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                #logging.FileHandler(f'training_pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def default_config(self):
        """Default configuration for the training pipeline"""
        return {
            "data": {
                "input_file": "/content/Data-Science-Course-spring2025/Main Project/Phase 1/Crawling/David_Copperfield.txt",
                "dataset_output_dir": "/content/Data-Science-Course-spring2025/Main Project/Phase3/processed_dataset",
                "max_lines": None
            },
            "model": {
                "model_name": "meta-llama/Llama-3.2-3B-Instruct",
                "output_dir": "./llama-lora-finetuned",
                "max_seq_length": 1024,
                "load_in_8bit": True
            },
            "training": {
                "per_device_train_batch_size": 2,
                "gradient_accumulation_steps": 4,
                "num_train_epochs": 2,
                "learning_rate": 3e-4,
                "save_steps": 500
            }
        }
    
    def load_config(self, config_path: str):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            self.logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load config from {config_path}: {e}")
            self.logger.info("Using default configuration")
            return self.default_config()
    
    def validate_environment(self):
        """Validate that the environment is properly set up"""
        self.logger.info("🔍 Validating environment...")
        
        # Check if required files exist
        required_files = ["load_training_data.py", "train_model.py"]
        for file in required_files:
            if not Path(file).exists():
                raise FileNotFoundError(f"Required file not found: {file}")
        
        # Check if input data file exists
        if not Path(self.config["data"]["input_file"]).exists():
            raise FileNotFoundError(f"Training data file not found: {self.config['data']['input_file']}")
        
        # Check Python version
        if sys.version_info < (3, 8):
            raise RuntimeError("Python 3.8 or higher is required")
        
        self.logger.info("✅ Environment validation passed")
    
    def install_dependencies(self):
        """Install required dependencies"""
        self.logger.info("📦 Installing dependencies...")
        
        try:
            # Run setup.py to install dependencies
            result = subprocess.run([
                sys.executable, "setup.py", "install"
            ], capture_output=True, text=True, check=True)
            
            self.logger.info("✅ Dependencies installed successfully")
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Failed to install dependencies: {e}")
            self.logger.error(f"Error output: {e.stderr}")
            raise
    
    def load_and_preprocess_data(self):
        """Stage 1: Data Loading and Preprocessing"""
        self.logger.info("📊 Stage 1: Loading and preprocessing data...")
        
        try:
            # Import and run data loading
            sys.path.append(".")
            from load_training_data import load_text_data
            
            dataset = load_text_data(
                file_path=self.config["data"]["input_file"],
                max_lines=self.config["data"].get("max_lines")
            )
            
            # Save processed dataset
            os.makedirs(self.config["data"]["dataset_output_dir"], exist_ok=True)
            dataset.save_to_disk(self.config["data"]["dataset_output_dir"])
            
            self.logger.info(f"✅ Data loaded and saved: {len(dataset)} samples")
            return self.config["data"]["dataset_output_dir"]
            
        except Exception as e:
            self.logger.error(f"❌ Data loading failed: {e}")
            raise
    
    def train_model(self, dataset_path: str):
        """Stage 2: Model Training"""
        self.logger.info("🚀 Stage 2: Training model...")
        
        try:
            # Prepare training arguments
            training_args = [
                sys.executable, "train_model.py",
                "--dataset_path", dataset_path,
                "--model_name", self.config["model"]["model_name"],
                "--output_dir", self.config["model"]["output_dir"]
            ]
            
            # Run training
            result = subprocess.run(
                training_args,
                capture_output=True,
                text=True,
                check=True
            )
            
            self.logger.info("✅ Model training completed successfully")
            self.logger.info(f"Model saved to: {self.config['model']['output_dir']}")
            
            return self.config["model"]["output_dir"]
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Model training failed: {e}")
            self.logger.error(f"Error output: {e.stderr}")
            raise
    
    def validate_trained_model(self, model_path: str):
        """Validate that the trained model was saved correctly"""
        self.logger.info("🔍 Validating trained model...")
        
        required_files = ["config.json", "pytorch_model.bin", "tokenizer.json"]
        model_dir = Path(model_path)
        
        missing_files = []
        for file in required_files:
            if not (model_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.logger.warning(f"⚠️ Some model files may be missing: {missing_files}")
        else:
            self.logger.info("✅ Model validation passed")
        
        # Log model directory contents
        if model_dir.exists():
            files = list(model_dir.iterdir())
            self.logger.info(f"Model directory contains {len(files)} files")
    
    def generate_training_report(self, model_path: str):
        """Generate a training summary report"""
        end_time = datetime.now()
        duration = end_time - self.pipeline_start_time
        
        report = {
            "training_summary": {
                "start_time": self.pipeline_start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": duration.total_seconds() / 60,
                "model_path": model_path,
                "dataset_path": self.config["data"]["dataset_output_dir"],
                "configuration": self.config
            }
        }
        
        report_path = f"training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"📋 Training report saved to: {report_path}")
        self.logger.info(f"🎉 Training pipeline completed in {duration.total_seconds()/60:.2f} minutes")
    
    def run_training_pipeline(self):
        """Execute the complete training pipeline"""
        self.logger.info("🚀 Starting Training Pipeline")
        self.logger.info("=" * 50)
        
        try:
            # Stage 0: Environment validation and setup
            self.validate_environment()
            self.install_dependencies()
            
            # Stage 1: Data Loading and Preprocessing
            dataset_path = self.load_and_preprocess_data()


            perplexity = test(model_path, self.config["data"]["input_file"])  # Call the evaluation function
            self.logger.info(f"Perplexity: {perplexity}")
            
            model_path = self.train_model(dataset_path)
            
            # Stage 3: Validation
            self.validate_trained_model(model_path)
            
            perplexity = test(model_path, self.config["data"]["input_file"])  # Call the evaluation function
            self.logger.info(f"Perplexity: {perplexity}")
            
            # Stage 4: Generate report
            self.generate_training_report(model_path)
            
            self.logger.info("🎉 Training pipeline completed successfully!")
            return model_path
            
        except Exception as e:
            self.logger.error(f"❌ Training pipeline failed: {e}")
            raise


def main():
    """Main entry point for the training pipeline"""
    parser = argparse.ArgumentParser(description="Automated Training Pipeline for LLaMA Fine-tuning")
    
    parser.add_argument(
        "--config", 
        type=str, 
        help="Path to configuration JSON file (optional)"
    )
    
    parser.add_argument(
        "--data-file",
        type=str,
        help="Path to training data file (overrides config)"
    )
    
    parser.add_argument(
        "--model-name",
        type=str,
        default="meta-llama/Llama-3.2-3B-Instruct",
        help="HuggingFace model name to fine-tune"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./llama-lora-finetuned",
        help="Directory to save the trained model"
    )
    
    parser.add_argument(
        "--max-lines",
        type=int,
        help="Maximum number of lines to load from training data"
    )
    
    args = parser.parse_args()
    
    # Create pipeline instance
    pipeline = TrainingPipeline(config_path=args.config)
    
    # Override config with command line arguments if provided
    if args.data_file:
        pipeline.config["data"]["input_file"] = args.data_file
    if args.model_name:
        pipeline.config["model"]["model_name"] = args.model_name
    if args.output_dir:
        pipeline.config["model"]["output_dir"] = args.output_dir
    if args.max_lines:
        pipeline.config["data"]["max_lines"] = args.max_lines
    
    # Run the training pipeline
    try:
        model_path = pipeline.run_training_pipeline()
        print(f"\n✅ SUCCESS: Model trained and saved to {model_path}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FAILURE: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
