# Installation Issues

> Solutions for common installation and environment setup problems

## Table of Contents

- [Overview](#overview)
- [Conda Environment Issues](#conda-environment-issues)
- [Python Package Issues](#python-package-issues)
- [GPU/CUDA Issues](#gpucuda-issues)
- [Dependency Conflicts](#dependency-conflicts)
- [Path and Import Issues](#path-and-import-issues)
- [Workspace Setup Issues](#workspace-setup-issues)
- [See Also](#see-also)

## Overview

Installation issues typically fall into these categories:

| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| Conda | Environment creation fails | Dependency conflicts, channel issues |
| Packages | Import errors | Missing packages, version mismatches |
| GPU | CUDA errors, slow performance | Driver issues, PyTorch configuration |
| Paths | Module not found | PYTHONPATH, working directory |
| Workspace | Permission errors | Directory permissions, missing folders |

## Conda Environment Issues

### Environment Creation Fails

**Symptom:**
```
ResolvePackageNotFound: 
  - package_name=version
```

**Solutions:**

1. **Update conda:**
   ```bash
   conda update -n base conda
   ```

2. **Clear cache and retry:**
   ```bash
   conda clean --all
   conda env create -f environment.yml
   ```

3. **Use mamba for faster resolution:**
   ```bash
   conda install -n base mamba
   mamba env create -f environment.yml
   ```

4. **Create minimal environment and install manually:**
   ```bash
   conda create -n OHMind python=3.10
   conda activate OHMind
   pip install -r requirements.txt  # If available
   ```

### Environment Activation Fails

**Symptom:**
```
EnvironmentNameNotFound: Could not find conda environment: OHMind
```

**Solutions:**

1. **List available environments:**
   ```bash
   conda env list
   ```

2. **Check if environment was created:**
   ```bash
   conda info --envs
   ```

3. **Recreate if missing:**
   ```bash
   conda env create -f environment.yml
   ```

### Slow Environment Creation

**Symptom:** Environment creation takes very long (>30 minutes)

**Solutions:**

1. **Use mamba:**
   ```bash
   conda install -n base mamba
   mamba env create -f environment.yml
   ```

2. **Use libmamba solver:**
   ```bash
   conda install -n base conda-libmamba-solver
   conda config --set solver libmamba
   conda env create -f environment.yml
   ```

## Python Package Issues

### Import Errors

**Symptom:**
```python
ModuleNotFoundError: No module named 'langchain'
```

**Solutions:**

1. **Verify environment is activated:**
   ```bash
   conda activate OHMind
   which python  # Should point to OHMind env
   ```

2. **Install missing package:**
   ```bash
   pip install langchain langchain-core langgraph
   ```

3. **Check package is installed:**
   ```bash
   pip show langchain
   ```

### RDKit Import Fails

**Symptom:**
```python
ImportError: cannot import name 'Chem' from 'rdkit'
```

**Solutions:**

1. **Install RDKit via conda:**
   ```bash
   conda install -c conda-forge rdkit
   ```

2. **Verify installation:**
   ```bash
   python -c "from rdkit import Chem; print('RDKit OK')"
   ```

### PyTorch Import Fails

**Symptom:**
```python
ImportError: libcudart.so.XX.X: cannot open shared object file
```

**Solutions:**

1. **Install CPU-only PyTorch:**
   ```bash
   pip install torch --index-url https://download.pytorch.org/whl/cpu
   ```

2. **Install CUDA-compatible PyTorch:**
   ```bash
   # For CUDA 11.8
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   
   # For CUDA 12.1
   pip install torch --index-url https://download.pytorch.org/whl/cu121
   ```

### Version Mismatch Errors

**Symptom:**
```
TypeError: __init__() got an unexpected keyword argument 'xxx'
```

**Solutions:**

1. **Check package versions:**
   ```bash
   pip show langchain langchain-core langgraph
   ```

2. **Install specific versions:**
   ```bash
   pip install langchain==0.2.0 langchain-core==0.2.0 langgraph==0.1.0
   ```

3. **Upgrade all related packages:**
   ```bash
   pip install --upgrade langchain langchain-core langgraph langchain-openai
   ```

## GPU/CUDA Issues

### CUDA Not Available

**Symptom:**
```python
>>> import torch
>>> torch.cuda.is_available()
False
```

**Solutions:**

1. **Check NVIDIA driver:**
   ```bash
   nvidia-smi
   ```

2. **Check CUDA version:**
   ```bash
   nvcc --version
   ```

3. **Install matching PyTorch:**
   ```bash
   # Check your CUDA version first
   nvidia-smi | grep "CUDA Version"
   
   # Install matching PyTorch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

### Out of Memory (OOM)

**Symptom:**
```
RuntimeError: CUDA out of memory
```

**Solutions:**

1. **Reduce batch size in VAE operations**

2. **Clear GPU cache:**
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

3. **Use CPU for inference:**
   ```python
   device = "cpu"  # Instead of "cuda"
   ```

### Wrong GPU Selected

**Symptom:** Using wrong GPU or GPU 0 when another is preferred

**Solutions:**

1. **Set CUDA_VISIBLE_DEVICES:**
   ```bash
   export CUDA_VISIBLE_DEVICES=1  # Use GPU 1
   ```

2. **Set in Python:**
   ```python
   import os
   os.environ["CUDA_VISIBLE_DEVICES"] = "1"
   ```

## Dependency Conflicts

### Conflicting Package Versions

**Symptom:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solutions:**

1. **Create fresh environment:**
   ```bash
   conda deactivate
   conda env remove -n OHMind
   conda env create -f environment.yml
   ```

2. **Use pip-tools for resolution:**
   ```bash
   pip install pip-tools
   pip-compile requirements.in
   pip-sync requirements.txt
   ```

### Pydantic Version Issues

**Symptom:**
```
pydantic.errors.PydanticUserError: `xxx` is not a valid Pydantic field type
```

**Solutions:**

1. **Check Pydantic version:**
   ```bash
   pip show pydantic
   ```

2. **Install compatible version:**
   ```bash
   pip install "pydantic>=2.0,<3.0"
   ```

### LangChain Compatibility

**Symptom:** Various LangChain-related errors after upgrade

**Solutions:**

1. **Pin compatible versions:**
   ```bash
   pip install langchain==0.2.16 langchain-core==0.2.38 langgraph==0.2.28
   ```

2. **Check migration guide:**
   - LangChain has breaking changes between major versions
   - Consult the LangChain migration documentation

## Path and Import Issues

### Module Not Found

**Symptom:**
```python
ModuleNotFoundError: No module named 'OHMind'
```

**Solutions:**

1. **Set PYTHONPATH:**
   ```bash
   export PYTHONPATH="/path/to/OHMind:$PYTHONPATH"
   ```

2. **Add to .env file:**
   ```
   PYTHONPATH=/path/to/OHMind
   ```

3. **Install in development mode:**
   ```bash
   cd /path/to/OHMind
   pip install -e .
   ```

### Wrong Python Interpreter

**Symptom:** Commands work in terminal but not in scripts

**Solutions:**

1. **Check which Python:**
   ```bash
   which python
   # Should show: /path/to/anaconda3/envs/OHMind/bin/python
   ```

2. **Use full path in scripts:**
   ```bash
   /path/to/anaconda3/envs/OHMind/bin/python script.py
   ```

3. **Activate environment in script:**
   ```bash
   #!/bin/bash
   source /path/to/anaconda3/etc/profile.d/conda.sh
   conda activate OHMind
   python script.py
   ```

### Import Order Issues

**Symptom:** Import works sometimes but not always

**Solutions:**

1. **Check for circular imports**

2. **Ensure proper package structure:**
   ```
   OHMind/
   ├── __init__.py
   ├── OHVAE/
   │   └── __init__.py
   └── OHPSO/
       └── __init__.py
   ```

## Workspace Setup Issues

### Permission Denied

**Symptom:**
```
PermissionError: [Errno 13] Permission denied: '/OHMind_workspace/HEM'
```

**Solutions:**

1. **Create workspace with correct permissions:**
   ```bash
   mkdir -p "$OHMind_workspace"
   chmod 755 "$OHMind_workspace"
   ```

2. **Create subdirectories:**
   ```bash
   mkdir -p "$OHMind_workspace"/{HEM,QM,MD,Multiwfn}
   chmod 755 "$OHMind_workspace"/{HEM,QM,MD,Multiwfn}
   ```

3. **Check ownership:**
   ```bash
   ls -la "$OHMind_workspace"
   # Change owner if needed
   sudo chown -R $USER:$USER "$OHMind_workspace"
   ```

### Directory Not Found

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: '/OHMind_workspace/HEM'
```

**Solutions:**

1. **Set environment variable:**
   ```bash
   export OHMind_workspace="/path/to/workspace"
   ```

2. **Create directories:**
   ```bash
   mkdir -p "$OHMind_workspace"/{HEM,QM,MD,Multiwfn}
   ```

3. **Add to .env:**
   ```
   OHMind_workspace=/path/to/workspace
   HEM_SAVE_PATH=${OHMind_workspace}/HEM
   QM_WORK_DIR=${OHMind_workspace}/QM
   MD_WORK_DIR=${OHMind_workspace}/MD
   MULTIWFN_WORK_DIR=${OHMind_workspace}/Multiwfn
   ```

### Disk Space Issues

**Symptom:**
```
OSError: [Errno 28] No space left on device
```

**Solutions:**

1. **Check disk space:**
   ```bash
   df -h "$OHMind_workspace"
   ```

2. **Clean old results:**
   ```bash
   # Remove old QM temp files
   find "$QM_WORK_DIR" -name "temp_*" -mtime +7 -exec rm -rf {} \;
   
   # Remove old MD trajectories
   find "$MD_WORK_DIR" -name "*.xtc" -mtime +30 -exec rm {} \;
   ```

3. **Move workspace to larger disk:**
   ```bash
   export OHMind_workspace="/mnt/large_disk/OHMind_workspace"
   ```

## Quick Verification Script

```bash
#!/bin/bash
# verify_installation.sh

echo "=== OHMind Installation Verification ==="

# Check conda environment
echo -n "Conda environment: "
if [ "$CONDA_DEFAULT_ENV" = "OHMind" ]; then
    echo "✅ OHMind"
else
    echo "❌ Not in OHMind environment (current: $CONDA_DEFAULT_ENV)"
fi

# Check Python version
echo -n "Python version: "
python_version=$(python --version 2>&1)
if [[ "$python_version" == *"3.10"* ]] || [[ "$python_version" == *"3.11"* ]]; then
    echo "✅ $python_version"
else
    echo "⚠️  $python_version (recommended: 3.10+)"
fi

# Check key packages
echo "Key packages:"
for pkg in langchain langgraph rdkit torch pydantic fastapi; do
    if python -c "import $pkg" 2>/dev/null; then
        version=$(pip show $pkg 2>/dev/null | grep Version | cut -d' ' -f2)
        echo "  ✅ $pkg ($version)"
    else
        echo "  ❌ $pkg (not installed)"
    fi
done

# Check PYTHONPATH
echo -n "PYTHONPATH includes OHMind: "
if python -c "import OHMind" 2>/dev/null; then
    echo "✅"
else
    echo "❌ (set PYTHONPATH or install OHMind)"
fi

# Check workspace
echo -n "Workspace: "
if [ -d "$OHMind_workspace" ] && [ -w "$OHMind_workspace" ]; then
    echo "✅ $OHMind_workspace"
else
    echo "❌ Not configured or not writable"
fi

echo "=== Verification Complete ==="
```

## See Also

- [Troubleshooting Overview](./index.md) - Main troubleshooting guide
- [MCP Issues](./mcp-issues.md) - Server connection problems
- [Quick Start Guide](../getting-started/quick-start.md) - Initial setup
- [Installation Guide](../getting-started/installation.md) - Detailed installation

---

*Last updated: 2025-12-23 | OHMind v0.1.0*
