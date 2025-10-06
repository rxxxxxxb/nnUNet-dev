#!/usr/bin/env python
"""
Test script to verify nnUNetv2 development environment installation.

Run this after setting up the environment to ensure everything is working correctly.

Usage:
    python test_installation.py
"""

import sys
from typing import Tuple


def test_python_version() -> Tuple[bool, str]:
    """Test if Python version is appropriate."""
    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    
    if version_info >= (3, 9):
        return True, f"✓ Python {version_str} (OK)"
    else:
        return False, f"✗ Python {version_str} (Required: >=3.9)"


def test_pytorch() -> Tuple[bool, str]:
    """Test PyTorch installation."""
    try:
        import torch
        return True, f"✓ PyTorch {torch.__version__}"
    except ImportError as e:
        return False, f"✗ PyTorch not found: {e}"


def test_cuda() -> Tuple[bool, str]:
    """Test CUDA availability."""
    try:
        import torch
        if torch.cuda.is_available():
            cuda_version = torch.version.cuda if hasattr(torch.version, 'cuda') else "unknown"
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0) if device_count > 0 else "N/A"
            return True, f"✓ CUDA {cuda_version} available ({device_count} GPU(s): {device_name})"
        else:
            return False, "✗ CUDA not available (CPU-only mode)"
    except Exception as e:
        return False, f"✗ Error checking CUDA: {e}"


def test_core_dependencies() -> list:
    """Test core scientific computing dependencies."""
    results = []
    
    packages = [
        "numpy",
        "scipy",
        "pandas",
        "sklearn",
        "skimage",
        "SimpleITK",
        "nibabel",
        "batchgenerators",
        "tqdm",
        "matplotlib",
    ]
    
    for package in packages:
        try:
            if package == "sklearn":
                import sklearn
                version = sklearn.__version__
            elif package == "skimage":
                import skimage
                version = skimage.__version__
            else:
                module = __import__(package)
                version = getattr(module, "__version__", "unknown")
            
            results.append((True, f"✓ {package} {version}"))
        except ImportError:
            results.append((False, f"✗ {package} not found"))
    
    return results


def test_nnunet() -> Tuple[bool, str]:
    """Test nnUNet installation."""
    try:
        import nnunetv2
        version = getattr(nnunetv2, "__version__", "unknown")
        return True, f"✓ nnunetv2 {version}"
    except ImportError as e:
        return False, f"✗ nnunetv2 not found: {e}"


def test_nnunet_imports() -> list:
    """Test important nnUNet module imports."""
    results = []
    
    modules = [
        "nnunetv2.training.nnUNetTrainer.nnUNetTrainer",
        "nnunetv2.utilities.plans_handling.plans_handler",
        "nnunetv2.preprocessing.preprocessors.default_preprocessor",
        "nnunetv2.inference.predict_from_raw_data",
    ]
    
    for module_path in modules:
        try:
            parts = module_path.rsplit(".", 1)
            module = __import__(parts[0], fromlist=[parts[1]] if len(parts) > 1 else [])
            if len(parts) > 1:
                getattr(module, parts[1])
            results.append((True, f"✓ {module_path}"))
        except ImportError as e:
            results.append((False, f"✗ {module_path}: {e}"))
        except AttributeError as e:
            results.append((False, f"✗ {module_path}: {e}"))
    
    return results


def test_environment_variables() -> list:
    """Test nnUNet environment variables."""
    import os
    
    results = []
    required_vars = ["nnUNet_raw", "nnUNet_preprocessed", "nnUNet_results"]
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            exists = "exists" if os.path.exists(value) else "not found"
            results.append((True, f"✓ {var}={value} ({exists})"))
        else:
            results.append((False, f"✗ {var} not set"))
    
    return results


def test_cuda_functionality() -> Tuple[bool, str]:
    """Test actual CUDA functionality with a simple tensor operation."""
    try:
        import torch
        if not torch.cuda.is_available():
            return False, "⚠ CUDA not available, skipping functionality test"
        
        # Create tensors and perform operation on GPU
        device = torch.device("cuda:0")
        x = torch.randn(100, 100, device=device)
        y = torch.randn(100, 100, device=device)
        z = torch.matmul(x, y)
        
        # Move back to CPU to verify
        z_cpu = z.cpu()
        
        return True, "✓ CUDA functionality test passed (matrix multiplication)"
    except Exception as e:
        return False, f"✗ CUDA functionality test failed: {e}"


def main():
    """Run all tests and display results."""
    print("=" * 70)
    print("nnUNetv2 Development Environment Installation Test")
    print("=" * 70)
    print()
    
    all_passed = True
    
    # Python version
    print("1. Python Version")
    print("-" * 70)
    passed, msg = test_python_version()
    print(f"   {msg}")
    all_passed = all_passed and passed
    print()
    
    # PyTorch
    print("2. PyTorch Installation")
    print("-" * 70)
    passed, msg = test_pytorch()
    print(f"   {msg}")
    all_passed = all_passed and passed
    print()
    
    # CUDA
    print("3. CUDA Availability")
    print("-" * 70)
    passed, msg = test_cuda()
    print(f"   {msg}")
    if not passed:
        print("   ⚠ Training will run on CPU (much slower)")
    print()
    
    # CUDA functionality
    print("4. CUDA Functionality")
    print("-" * 70)
    passed, msg = test_cuda_functionality()
    print(f"   {msg}")
    print()
    
    # Core dependencies
    print("5. Core Dependencies")
    print("-" * 70)
    results = test_core_dependencies()
    for passed, msg in results:
        print(f"   {msg}")
        all_passed = all_passed and passed
    print()
    
    # nnUNet main package
    print("6. nnUNet Package")
    print("-" * 70)
    passed, msg = test_nnunet()
    print(f"   {msg}")
    all_passed = all_passed and passed
    print()
    
    # nnUNet imports
    print("7. nnUNet Module Imports")
    print("-" * 70)
    results = test_nnunet_imports()
    for passed, msg in results:
        print(f"   {msg}")
        all_passed = all_passed and passed
    print()
    
    # Environment variables
    print("8. Environment Variables")
    print("-" * 70)
    results = test_environment_variables()
    for passed, msg in results:
        print(f"   {msg}")
        if not passed:
            all_passed = False
    print()
    
    # Summary
    print("=" * 70)
    if all_passed:
        print("✓ All tests passed! Your environment is ready for nnUNet development.")
    else:
        print("✗ Some tests failed. Please review the output above.")
        print()
        print("Common fixes:")
        print("  - CUDA not available: Check nvidia-smi and reinstall PyTorch")
        print("  - Missing packages: conda install or pip install the missing package")
        print("  - nnUNet not found: cd nnUNet && pip install -e .")
        print("  - Environment variables: Set nnUNet_raw, nnUNet_preprocessed, nnUNet_results")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

