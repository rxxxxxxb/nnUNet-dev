# nnUNetv2 Commands Cheatsheet

Quick reference for common commands.

## Environment Management

```bash
# Activate environment
conda activate nnunet-dev

# Deactivate environment
conda deactivate

# Verify installation
python /home/racoon/project_gca/nnUNet-dev/test_installation.py

# Check GPU
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"

# Monitor GPU usage
watch -n 1 nvidia-smi
```

## nnUNet Workflow

### 1. Prepare Dataset
```bash
# Dataset structure
~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_raw/DatasetXXX_Name/
├── dataset.json
├── imagesTr/
└── labelsTr/
```

### 2. Verify Dataset Integrity
```bash
nnUNetv2_plan_and_preprocess -d DATASET_ID --verify_dataset_integrity
```

### 3. Plan and Preprocess
```bash
# Single dataset
nnUNetv2_plan_and_preprocess -d DATASET_ID

# Multiple datasets
nnUNetv2_plan_and_preprocess -d 1 2 3

# Custom plans
nnUNetv2_plan_and_preprocess -d DATASET_ID -pl ExperimentPlanner
```

### 4. Training
```bash
# Basic training (single fold)
nnUNetv2_train DATASET_ID CONFIG FOLD

# Examples:
nnUNetv2_train 1 2d 0
nnUNetv2_train 1 3d_fullres 0
nnUNetv2_train 1 3d_lowres 0
nnUNetv2_train 1 3d_cascade_fullres 0

# All folds (5-fold cross-validation)
nnUNetv2_train 1 3d_fullres 0
nnUNetv2_train 1 3d_fullres 1
nnUNetv2_train 1 3d_fullres 2
nnUNetv2_train 1 3d_fullres 3
nnUNetv2_train 1 3d_fullres 4

# Continue interrupted training
nnUNetv2_train DATASET_ID CONFIG FOLD --c

# Use specific GPU
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 1 3d_fullres 0

# Multi-GPU training
nnUNetv2_train DATASET_ID CONFIG FOLD --device cuda:0,1
```

### 5. Find Best Configuration
```bash
nnUNetv2_find_best_configuration DATASET_ID -c 2d 3d_fullres
```

### 6. Inference
```bash
# Single fold
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIG -f FOLD

# Example:
nnUNetv2_predict -i ~/data/test_images -o ~/data/predictions -d 1 -c 3d_fullres -f 0

# Ensemble (all folds)
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIG -f all

# Multiple configurations
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c 2d 3d_fullres -f all

# Checkpoint
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIG -f FOLD --chk checkpoint_best.pth

# Disable test-time augmentation (faster)
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIG -f FOLD --disable_tta

# Save probabilities
nnUNetv2_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -d DATASET_ID -c CONFIG -f FOLD --save_probabilities
```

### 7. Ensemble Predictions
```bash
nnUNetv2_ensemble -i FOLDER1 FOLDER2 -o OUTPUT_FOLDER
```

### 8. Evaluation
```bash
nnUNetv2_evaluate_folder GT_FOLDER PRED_FOLDER -djfile DATASET_JSON -pfile PLANS_FILE
```

## GPU Control

```bash
# Use specific GPU
export CUDA_VISIBLE_DEVICES=0

# Use multiple GPUs
export CUDA_VISIBLE_DEVICES=0,1

# CPU only (no GPU)
export CUDA_VISIBLE_DEVICES=-1

# Check which GPUs are available
nvidia-smi

# Monitor GPU in real-time
watch -n 1 nvidia-smi

# GPU stats (install gpustat first: pip install gpustat)
gpustat -i 1
```

## Development

```bash
# Navigate to project
cd /home/racoon/project_gca/nnUNet-dev

# Edit code (example)
nano nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py

# Changes are live immediately - no reinstall needed!

# Run custom script
python my_custom_script.py

# Check for updates from GitHub
git fetch origin
git pull origin master

# Create branch for your changes
git checkout -b my-feature

# View your changes
git diff
```

## Debugging

```bash
# Verbose training
nnUNetv2_train DATASET_ID CONFIG FOLD --verbose

# Check preprocessed files
ls ~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_preprocessed/DatasetXXX_Name/

# Check results
ls ~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_results/DatasetXXX_Name/

# View tensorboard logs
tensorboard --logdir ~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_results/

# Check dataset integrity
nnUNetv2_plan_and_preprocess -d DATASET_ID --verify_dataset_integrity

# Test imports
python -c "from nnunetv2.training.nnUNetTrainer.nnUNetTrainer import nnUNetTrainer; print('OK')"

# Check environment variables
echo $nnUNet_raw
echo $nnUNet_preprocessed
echo $nnUNet_results
```

## Common Workflows

### Full Pipeline (Single Configuration)
```bash
# 1. Activate environment
conda activate nnunet-dev

# 2. Verify dataset and preprocess
nnUNetv2_plan_and_preprocess -d 1 --verify_dataset_integrity

# 3. Train all folds
for fold in {0..4}; do
    nnUNetv2_train 1 3d_fullres $fold
done

# 4. Find best configuration (if comparing multiple)
nnUNetv2_find_best_configuration 1 -c 3d_fullres

# 5. Run inference with ensemble
nnUNetv2_predict -i ~/test_images -o ~/predictions -d 1 -c 3d_fullres -f all

# 6. Evaluate
nnUNetv2_evaluate_folder ~/test_labels ~/predictions \
    -djfile ~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_preprocessed/Dataset001_Name/dataset.json \
    -pfile ~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_preprocessed/Dataset001_Name/nnUNetPlans.json
```

### Quick Test (Single Fold, No Ensemble)
```bash
conda activate nnunet-dev
nnUNetv2_plan_and_preprocess -d 1
nnUNetv2_train 1 3d_fullres 0
nnUNetv2_predict -i ~/test_images -o ~/predictions -d 1 -c 3d_fullres -f 0
```

### Multi-GPU Training
```bash
# Use GPUs 0 and 1
CUDA_VISIBLE_DEVICES=0,1 nnUNetv2_train 1 3d_fullres 0
```

## File Locations

```bash
# Raw data
~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_raw/

# Preprocessed data
~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_preprocessed/

# Training results
~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_results/

# Source code (editable)
/home/racoon/project_gca/nnUNet-dev/nnunetv2/

# Environment config
/home/racoon/project_gca/nnUNet-dev/environment.yml
```

## Troubleshooting

```bash
# Out of memory error
# Solution 1: Use smaller batch size (edit trainer)
# Solution 2: Use specific GPU
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train ...

# Import error
# Reinstall in editable mode
cd /home/racoon/project_gca/nnUNet-dev
pip install -e .

# Environment variable not set
export nnUNet_raw="$HOME/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_raw"
export nnUNet_preprocessed="$HOME/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_preprocessed"
export nnUNet_results="$HOME/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_results"

# CUDA not available
# Check driver
nvidia-smi
# Reinstall PyTorch
mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
```

## More Information

- **Full Documentation**: `/home/racoon/project_gca/nnUNet-dev/readme.md`
- **Quick Start**: `/home/racoon/project_gca/nnUNet-dev/QUICKSTART.md`
- **Data Setup**: `/home/racoon/project_gca/nnUNet-dev/DATA_SETUP.md`
- **Official Docs**: `/home/racoon/project_gca/nnUNet-dev/documentation/`
- **GitHub**: https://github.com/MIC-DKFZ/nnUNet

## Pro Tips

1. **Always use environment**: `conda activate nnunet-dev`
2. **Monitor GPU**: `watch -n 1 nvidia-smi`
3. **Use tmux for long jobs**: `tmux new -s training`
4. **Verify dataset first**: `--verify_dataset_integrity`
5. **Start with single fold**: Test with fold 0 before training all folds
6. **Backup results**: `~/project_gca/nnUNet-dev/dataset/nnunet/nnUNet_results/` contains trained models
7. **Editable install**: Changes to source code are immediate

---

Print this cheatsheet or keep it open for quick reference!

