#!/bin/bash
# nnUNetv2 Development Environment Setup Script
# This script sets up a complete development environment for nnUNetv2
# Run this from the root of the nnUNet repository

set -e  # Exit on error

echo "======================================"
echo "nnUNetv2 Development Environment Setup"
echo "======================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 0. Verify we're in the nnUNet repository
echo -e "${YELLOW}[1/5] Verifying repository structure...${NC}"
if [ ! -d "nnunetv2" ] || [ ! -f "setup.py" ]; then
    echo -e "${RED}Error: This script must be run from the root of the nnUNet repository.${NC}"
    echo "Expected to find 'nnunetv2/' directory and 'setup.py' file."
    echo "Current directory: $(pwd)"
    exit 1
fi
echo "✓ Found nnUNet repository structure"

# 1. Check if conda/mamba is installed
echo ""
echo -e "${YELLOW}[2/5] Checking for Conda/Mamba...${NC}"
if command -v mamba &> /dev/null; then
    CONDA_CMD="mamba"
    echo "✓ Mamba found - using mamba (faster)"
elif command -v conda &> /dev/null; then
    CONDA_CMD="conda"
    echo "✓ Conda found - using conda"
else
    echo -e "${RED}Error: Neither conda nor mamba found. Please install Miniconda or Mambaforge first.${NC}"
    echo "Visit: https://github.com/conda-forge/miniforge#mambaforge"
    exit 1
fi

# 2. Create environment from environment.yml
echo ""
echo -e "${YELLOW}[3/5] Creating conda environment from environment.yml...${NC}"
if conda env list | grep -q "^nnunet-dev "; then
    echo -e "${YELLOW}Warning: nnunet-dev environment already exists.${NC}"
    read -p "Do you want to remove and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        conda env remove -n nnunet-dev -y
        $CONDA_CMD env create -f environment.yml
    else
        echo "Skipping environment creation. Using existing environment."
    fi
else
    $CONDA_CMD env create -f environment.yml
fi

# 3. Get the conda base path
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh"

# 4. Activate environment
echo ""
echo -e "${YELLOW}[4/5] Activating nnunet-dev environment...${NC}"
conda activate nnunet-dev

# 5. Install nnUNet in editable mode from current directory
echo ""
echo -e "${YELLOW}[5/5] Installing nnUNet in editable mode...${NC}"
# Remove the placeholder nnunetv2 if it was installed from environment.yml
pip uninstall -y nnunetv2 2>/dev/null || true
# Install in editable mode from current directory
pip install -e .

# Optional: Export environment for reproducibility
# Uncomment the following lines to export environment specifications:
# echo ""
# echo -e "${YELLOW}[6/5] Exporting environment specifications...${NC}"
# conda env export > environment-lock.yml
# conda list --explicit > environment-explicit.txt
# pip freeze > requirements-pip.txt

echo ""
echo -e "${GREEN}======================================"
echo "Setup Complete! ✓"
echo "======================================"
echo ""
echo "To activate the environment, run:"
echo "  conda activate nnunet-dev"
echo ""
# echo "To verify the installation, run:"
# echo "  python test_installation.py"
# echo ""
