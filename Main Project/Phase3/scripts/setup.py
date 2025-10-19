#!/usr/bin/env python3
"""
Enhanced setup script that unifies installation commands and verification.
This script handles the complex dependency chain for LLaMA fine-tuning with Unsloth.
"""

import subprocess
import sys
import os
import logging
from pathlib import Path

# Configure logging to provide clear feedback during installation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class UnifiedSetup:
    """
    Handles the complete setup process for LLaMA fine-tuning environment.
    This class orchestrates all installation steps in the correct order.
    """
    
    def __init__(self):
        self.logger = logger
        self.python_executable = sys.executable
        
    def run_command(self, cmd, description, check=True, capture_output=True):
        """
        Execute a command with proper logging and error handling.
        
        Args:
            cmd: Command to execute (list of strings)
            description: Human-readable description for logging
            check: Whether to raise exception on failure
            capture_output: Whether to capture stdout/stderr
        """
        self.logger.info(f"🔄 {description}...")
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=capture_output, 
                text=True, 
                check=check
            )
            
            # Log any important output
            if result.stdout and result.stdout.strip():
                # Only log first few lines to avoid spam
                lines = result.stdout.strip().split('\n')
                for line in lines[:3]:  # Show first 3 lines
                    if line.strip():
                        self.logger.info(f"   {line}")
                if len(lines) > 3:
                    self.logger.info(f"   ... ({len(lines)-3} more lines)")
            
            self.logger.info(f"✅ {description} completed successfully")
            return result
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ {description} failed: {e}")
            if e.stderr:
                self.logger.error(f"Error details: {e.stderr}")
            if not check:
                return e
            raise
    
    def setup_repository(self):
        """Clone and navigate to the project repository."""
        # Check if we're already in the right directory
        if os.path.exists("setup.py"):
            self.logger.info("📁 Already in project directory")
            return
            
        # Clone repository if not exists
        if not os.path.exists("Data-Science-Course-spring2025"):
            self.run_command([
                "git", "clone", 
                "https://github.com/nelyasi71/Data-Science-Course-spring2025.git"
            ], "Cloning repository")
        
        # Navigate to project directory
        project_path = "Data-Science-Course-spring2025/Main Project/Phase3/scripts"
        if os.path.exists(project_path):
            os.chdir(project_path)
            self.logger.info(f"📁 Changed to directory: {os.getcwd()}")
        else:
            self.logger.warning(f"⚠️  Project path not found: {project_path}")
    
    def install_pytorch_with_cuda(self):
        """Install PyTorch with CUDA support first, as it's the foundation."""
        self.run_command([
            self.python_executable, "-m", "pip", "install",
            "torch==2.6.0+cu124", 
            "torchvision==0.21.0+cu124", 
            "torchaudio==2.6.0+cu124",
            "--index-url", "https://download.pytorch.org/whl/cu124"
        ], "Installing PyTorch with CUDA support")
    
    def install_poetry_and_tools(self):
        """Install Poetry and other build tools."""
        # Install Poetry
        self.run_command([
            self.python_executable, "-m", "pip", "install", "poetry"
        ], "Installing Poetry")
        
        # Upgrade pip to specific version for compatibility
        self.run_command([
            self.python_executable, "-m", "pip", "install", "pip==24.2"
        ], "Upgrading pip to compatible version")
    
    def install_unsloth_and_dependencies(self):
        """Install Unsloth and related dependencies."""
        # Install Unsloth with no-deps flag to avoid conflicts
        self.run_command([
            self.python_executable, "-m", "pip", "install",
            "unsloth[colab] @ git+https://github.com/unslothai/unsloth.git",
            "--no-deps"
        ], "Installing Unsloth (no dependencies)")
        
        # Install additional required packages
        self.run_command([
            self.python_executable, "-m", "pip", "install",
            "bitsandbytes", "unsloth_zoo"
        ], "Installing additional ML packages")
    
    def setup_project_files(self):
        """Create necessary project files and install in development mode."""
        # Create README if it doesn't exist
        if not os.path.exists("README.md"):
            Path("README.md").touch()
            self.logger.info("📄 Created README.md")
        
        # Install project in development mode
        # if os.path.exists("setup.py"):
        #     self.run_command([
        #         self.python_executable, "-m", "pip", "install", "-e", "."
        #     ], "Installing project in development mode")
        # else:
        #     self.logger.warning("⚠️  No setup.py found, skipping project installation")
    
    def install_poetry_dependencies(self):
        """Install dependencies via Poetry if pyproject.toml exists."""
        if os.path.exists("pyproject.toml"):
            self.run_command([
                "poetry", "install", "--no-root"
            ], "Installing Poetry dependencies")
        else:
            self.logger.info("📦 No pyproject.toml found, skipping Poetry installation")
    
    def verify_installation(self):
        """Verify the installation by testing key imports."""
        self.logger.info("🔍 Verifying installation...")
        
        # Test imports that are critical for the project
        test_imports = [
            ("torch", "PyTorch"),
            ("transformers", "Transformers"),
            ("datasets", "Datasets"),
            ("peft", "PEFT"),
            ("trl", "TRL"),
        ]
        
        verification_code = """
import sys
try:
    # Test critical imports
    import torch
    print(f"✅ PyTorch {torch.__version__} (CUDA: {torch.cuda.is_available()})")
    
    import transformers
    print(f"✅ Transformers {transformers.__version__}")
    
    import datasets
    print(f"✅ Datasets {datasets.__version__}")
    
    import peft
    print(f"✅ PEFT {peft.__version__}")
    
    import trl
    print(f"✅ TRL {trl.__version__}")
    
    # Try to import unsloth
    try:
        from unsloth import FastLanguageModel
        print("✅ Unsloth imported successfully")
    except ImportError as e:
        print(f"⚠️  Unsloth import warning: {e}")
    
    print("🎉 Core verification passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
"""
        
        # Run verification in a separate process to avoid import conflicts
        result = subprocess.run([
            self.python_executable, "-c", verification_code
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Log verification output
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    self.logger.info(f"Verification: {line}")
            self.logger.info("✅ Installation verification passed")
        else:
            self.logger.error("❌ Installation verification failed")
            if result.stderr:
                self.logger.error(f"Error: {result.stderr}")
            raise RuntimeError("Installation verification failed")
    
    def run_complete_setup(self):
        """Execute the complete setup process in the correct order."""
        self.logger.info("🚀 Starting unified setup process...")
        
        try:
            # Step 1: Repository setup
            #self.setup_repository()
            
            # Step 2: Install PyTorch first (foundational dependency)
            self.install_pytorch_with_cuda()
            
            # Step 3: Install build tools
            self.install_poetry_and_tools()
            
            # Step 4: Install Unsloth and ML packages
            self.install_unsloth_and_dependencies()
            
            # Step 5: Setup project files
            self.setup_project_files()
            
            # Step 6: Install Poetry dependencies if available
            self.install_poetry_dependencies()
            
            # Step 7: Verify everything works
            self.verify_installation()
            
            self.logger.info("🎉 Complete setup finished successfully!")
            
        except Exception as e:
            self.logger.error(f"💥 Setup failed: {e}")
            raise

def main():
    """Main entry point for the unified setup script."""
    setup = UnifiedSetup()
    setup.run_complete_setup()

if __name__ == "__main__":
    main()