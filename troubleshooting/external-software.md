---
title: External Software Issues
description: "Solutions for ORCA, GROMACS, and Multiwfn configuration and execution problems"
parent: Troubleshooting
nav_order: 4
---

# External Software Issues

> Solutions for ORCA, GROMACS, and Multiwfn configuration and execution problems

## Table of Contents

- [Overview](#overview)
- [ORCA Issues](#orca-issues)
- [GROMACS Issues](#gromacs-issues)
- [Multiwfn Issues](#multiwfn-issues)
- [Common Path Issues](#common-path-issues)
- [License and Installation](#license-and-installation)
- [See Also](#see-also)

## Overview

External software issues typically fall into these categories:

| Software | Common Issues | Environment Variables |
|----------|---------------|----------------------|
| ORCA | Path, MPI, license | `OHMind_ORCA`, `OHMind_MPI` |
| GROMACS | PATH, GPU, topology | `MD_WORK_DIR` |
| Multiwfn | Path, input files | `MULTIWFN_PATH`, `MULTIWFN_WORK_DIR` |

## ORCA Issues

### ORCA Binary Not Found

**Symptom:**
```
FileNotFoundError: ORCA executable not found
```

**Solutions:**

1. **Set ORCA path:**
   ```bash
   export OHMind_ORCA="/path/to/orca/orca"
   ```

2. **Verify path is correct:**
   ```bash
   ls -la "$OHMind_ORCA"
   # Should show the orca executable
   ```

3. **Add to .env:**
   ```
   OHMind_ORCA=/opt/orca/orca
   ```

4. **Test ORCA:**
   ```bash
   "$OHMind_ORCA" --version
   ```

### MPI Configuration Issues

**Symptom:**
```
Error: MPI not found or misconfigured
```

**Solutions:**

1. **Set MPI path:**
   ```bash
   export OHMind_MPI="/usr/lib/openmpi/bin"
   ```

2. **Verify MPI installation:**
   ```bash
   ls -la "$OHMind_MPI/mpirun"
   "$OHMind_MPI/mpirun" --version
   ```

3. **Check ORCA-MPI compatibility:**
   - ORCA requires specific OpenMPI versions
   - Check ORCA documentation for compatible versions

4. **Add MPI to PATH:**
   ```bash
   export PATH="$OHMind_MPI:$PATH"
   export LD_LIBRARY_PATH="/usr/lib/openmpi/lib:$LD_LIBRARY_PATH"
   ```

### ORCA Calculation Fails

**Symptom:**
```
ORCA finished with error code 1
```

**Solutions:**

1. **Check ORCA output file:**
   ```bash
   cat "$QM_WORK_DIR/job_name.out" | tail -50
   ```

2. **Common errors and fixes:**

   **Memory error:**
   ```
   # In ORCA input, increase memory
   %maxcore 4000  # 4GB per core
   ```

   **Convergence failure:**
   ```
   # Try different SCF settings
   %scf
     MaxIter 500
     DIISMaxEq 15
   end
   ```

   **Basis set not found:**
   ```bash
   # Check ORCA basis set library path
   ls "$ORCA_PATH/../share/orca/basis"
   ```

3. **Check disk space:**
   ```bash
   df -h "$QM_WORK_DIR"
   ```

### QM_WORK_DIR Issues

**Symptom:**
```
PermissionError: Cannot write to QM_WORK_DIR
```

**Solutions:**

1. **Create and set permissions:**
   ```bash
   mkdir -p "$QM_WORK_DIR"
   chmod 755 "$QM_WORK_DIR"
   ```

2. **Check disk space:**
   ```bash
   df -h "$QM_WORK_DIR"
   # ORCA can generate large temporary files
   ```

3. **Clean old files:**
   ```bash
   # Remove old temporary directories
   find "$QM_WORK_DIR" -name "temp_*" -mtime +7 -exec rm -rf {} \;
   ```

### ORCA License Issues

**Symptom:**
```
ORCA requires a valid license
```

**Solutions:**

1. **Register at ORCA forum:**
   - Visit: https://orcaforum.kofo.mpg.de/
   - Register for academic license

2. **Download correct version:**
   - Match your system architecture
   - Use version compatible with your MPI

## GROMACS Issues

### GROMACS Not in PATH

**Symptom:**
```
gmx: command not found
```

**Solutions:**

1. **Source GROMACS environment:**
   ```bash
   source /path/to/gromacs/bin/GMXRC
   ```

2. **Add to PATH manually:**
   ```bash
   export PATH="/path/to/gromacs/bin:$PATH"
   ```

3. **Verify installation:**
   ```bash
   which gmx
   gmx --version
   ```

4. **Add to .bashrc for persistence:**
   ```bash
   echo 'source /path/to/gromacs/bin/GMXRC' >> ~/.bashrc
   ```

### GPU/CUDA Issues

**Symptom:**
```
GROMACS was compiled without GPU support
```

**Solutions:**

1. **Check GROMACS GPU support:**
   ```bash
   gmx mdrun -version | grep GPU
   ```

2. **Install GPU-enabled GROMACS:**
   ```bash
   # Build with CUDA support
   cmake .. -DGMX_GPU=CUDA -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda
   make -j$(nproc)
   make install
   ```

3. **Check CUDA availability:**
   ```bash
   nvidia-smi
   nvcc --version
   ```

### Topology Errors

**Symptom:**
```
Fatal error: No such moleculetype XXX
```

**Solutions:**

1. **Check force field files:**
   ```bash
   ls /path/to/gromacs/share/gromacs/top/
   ```

2. **Verify topology includes:**
   ```
   ; In topology file
   #include "amber99sb.ff/forcefield.itp"
   ```

3. **Check molecule definitions:**
   ```bash
   grep "moleculetype" topology.top
   ```

### MD_WORK_DIR Issues

**Symptom:**
```
Cannot create output files in MD_WORK_DIR
```

**Solutions:**

1. **Create directory:**
   ```bash
   mkdir -p "$MD_WORK_DIR"
   chmod 755 "$MD_WORK_DIR"
   ```

2. **Check disk space:**
   ```bash
   df -h "$MD_WORK_DIR"
   # MD trajectories can be very large
   ```

3. **Clean old simulations:**
   ```bash
   # Remove old trajectory files
   find "$MD_WORK_DIR" -name "*.xtc" -mtime +30 -exec rm {} \;
   ```

### Simulation Crashes

**Symptom:**
```
Fatal error: Step XXX: The domain decomposition grid has shifted too much
```

**Solutions:**

1. **Check system setup:**
   - Verify box size is appropriate
   - Check for overlapping atoms

2. **Reduce time step:**
   ```
   ; In mdp file
   dt = 0.001  ; 1 fs instead of 2 fs
   ```

3. **Improve energy minimization:**
   ```bash
   gmx mdrun -v -deffnm em -nsteps 50000
   ```

4. **Check for bad contacts:**
   ```bash
   gmx grompp -f em.mdp -c system.gro -p topol.top -o em.tpr -maxwarn 1
   ```

## Multiwfn Issues

### Multiwfn Binary Not Found

**Symptom:**
```
FileNotFoundError: Multiwfn executable not found
```

**Solutions:**

1. **Set Multiwfn path:**
   ```bash
   export MULTIWFN_PATH="/path/to/Multiwfn/Multiwfn"
   ```

2. **Verify path:**
   ```bash
   ls -la "$MULTIWFN_PATH"
   "$MULTIWFN_PATH" << EOF
   q
   EOF
   ```

3. **Add to .env:**
   ```
   MULTIWFN_PATH=/opt/Multiwfn/Multiwfn
   ```

### Missing Input Files

**Symptom:**
```
Error: Cannot find wavefunction file
```

**Solutions:**

1. **Check file exists:**
   ```bash
   ls -la "$MULTIWFN_WORK_DIR"/*.wfn
   ls -la "$MULTIWFN_WORK_DIR"/*.molden
   ```

2. **Generate wavefunction from ORCA:**
   ```
   # In ORCA input
   %output
     Print[P_MOs] 1
     Print[P_Basis] 2
   end
   ```

3. **Convert formats if needed:**
   ```bash
   # Multiwfn can read: .wfn, .wfx, .molden, .fch, .gbw
   ```

### MULTIWFN_WORK_DIR Issues

**Symptom:**
```
Cannot write output to MULTIWFN_WORK_DIR
```

**Solutions:**

1. **Create directory:**
   ```bash
   mkdir -p "$MULTIWFN_WORK_DIR"
   chmod 755 "$MULTIWFN_WORK_DIR"
   ```

2. **Check permissions:**
   ```bash
   touch "$MULTIWFN_WORK_DIR/test" && rm "$MULTIWFN_WORK_DIR/test"
   ```

### Multiwfn Analysis Fails

**Symptom:**
```
Error in Multiwfn analysis
```

**Solutions:**

1. **Check Multiwfn output:**
   ```bash
   cat "$MULTIWFN_WORK_DIR/analysis.log"
   ```

2. **Run interactively to debug:**
   ```bash
   cd "$MULTIWFN_WORK_DIR"
   "$MULTIWFN_PATH" input.wfn
   # Follow prompts manually
   ```

3. **Check input file format:**
   - Ensure wavefunction file is complete
   - Verify file is not corrupted

### Display/GUI Issues

**Symptom:**
```
Error: Cannot open display
```

**Solutions:**

1. **Run in text mode:**
   ```bash
   # Multiwfn can run without GUI
   export DISPLAY=""
   ```

2. **Use X forwarding:**
   ```bash
   ssh -X user@server
   ```

3. **Install required libraries:**
   ```bash
   # For GUI support
   sudo apt-get install libgtk-3-0 libglu1-mesa
   ```

## Common Path Issues

### Environment Variables Not Set

**Symptom:** Various "not found" errors

**Solutions:**

1. **Check all required variables:**
   ```bash
   echo "OHMind_ORCA: $OHMind_ORCA"
   echo "OHMind_MPI: $OHMind_MPI"
   echo "MULTIWFN_PATH: $MULTIWFN_PATH"
   echo "QM_WORK_DIR: $QM_WORK_DIR"
   echo "MD_WORK_DIR: $MD_WORK_DIR"
   echo "MULTIWFN_WORK_DIR: $MULTIWFN_WORK_DIR"
   ```

2. **Set in .env file:**
   ```
   # External software paths
   OHMind_ORCA=/opt/orca/orca
   OHMind_MPI=/usr/lib/openmpi/bin
   MULTIWFN_PATH=/opt/Multiwfn/Multiwfn
   
   # Work directories
   QM_WORK_DIR=${OHMind_workspace}/QM
   MD_WORK_DIR=${OHMind_workspace}/MD
   MULTIWFN_WORK_DIR=${OHMind_workspace}/Multiwfn
   ```

3. **Source in startup script:**
   ```bash
   # In start_OHMind.sh
   source .env
   ```

### Library Path Issues

**Symptom:**
```
error while loading shared libraries: libXXX.so
```

**Solutions:**

1. **Add to LD_LIBRARY_PATH:**
   ```bash
   export LD_LIBRARY_PATH="/path/to/libs:$LD_LIBRARY_PATH"
   ```

2. **Install missing libraries:**
   ```bash
   # Find which package provides the library
   apt-file search libXXX.so
   sudo apt-get install package-name
   ```

3. **Use ldconfig:**
   ```bash
   sudo ldconfig
   ```

## License and Installation

### ORCA Installation

1. **Register at ORCA forum:**
   - https://orcaforum.kofo.mpg.de/

2. **Download and extract:**
   ```bash
   tar -xf orca_5_0_4_linux_x86-64_shared_openmpi411.tar.xz
   mv orca_5_0_4_linux_x86-64_shared_openmpi411 /opt/orca
   ```

3. **Set environment:**
   ```bash
   export OHMind_ORCA=/opt/orca/orca
   export PATH="/opt/orca:$PATH"
   export LD_LIBRARY_PATH="/opt/orca:$LD_LIBRARY_PATH"
   ```

### GROMACS Installation

1. **Install via package manager:**
   ```bash
   sudo apt-get install gromacs
   ```

2. **Or build from source:**
   ```bash
   wget https://ftp.gromacs.org/gromacs/gromacs-2023.tar.gz
   tar -xf gromacs-2023.tar.gz
   cd gromacs-2023
   mkdir build && cd build
   cmake .. -DGMX_BUILD_OWN_FFTW=ON
   make -j$(nproc)
   sudo make install
   source /usr/local/gromacs/bin/GMXRC
   ```

### Multiwfn Installation

1. **Download from:**
   - http://sobereva.com/multiwfn/

2. **Extract and set up:**
   ```bash
   unzip Multiwfn_3.8_bin_Linux.zip
   mv Multiwfn_3.8_bin_Linux /opt/Multiwfn
   chmod +x /opt/Multiwfn/Multiwfn
   export MULTIWFN_PATH=/opt/Multiwfn/Multiwfn
   ```

## Diagnostic Script

```bash
#!/bin/bash
# external_software_check.sh

echo "=== External Software Check ==="

# ORCA
echo ""
echo "1. ORCA:"
if [ -n "$OHMind_ORCA" ] && [ -x "$OHMind_ORCA" ]; then
    echo "   ✅ Path: $OHMind_ORCA"
    version=$("$OHMind_ORCA" --version 2>&1 | head -1)
    echo "   Version: $version"
else
    echo "   ❌ Not configured or not executable"
    echo "   OHMind_ORCA=$OHMind_ORCA"
fi

# MPI
echo ""
echo "2. MPI:"
if [ -n "$OHMind_MPI" ] && [ -x "$OHMind_MPI/mpirun" ]; then
    echo "   ✅ Path: $OHMind_MPI"
    version=$("$OHMind_MPI/mpirun" --version 2>&1 | head -1)
    echo "   Version: $version"
else
    echo "   ❌ Not configured or not executable"
    echo "   OHMind_MPI=$OHMind_MPI"
fi

# GROMACS
echo ""
echo "3. GROMACS:"
if command -v gmx &> /dev/null; then
    echo "   ✅ Path: $(which gmx)"
    version=$(gmx --version 2>&1 | grep "GROMACS version" | head -1)
    echo "   $version"
else
    echo "   ❌ Not found in PATH"
fi

# Multiwfn
echo ""
echo "4. Multiwfn:"
if [ -n "$MULTIWFN_PATH" ] && [ -x "$MULTIWFN_PATH" ]; then
    echo "   ✅ Path: $MULTIWFN_PATH"
else
    echo "   ❌ Not configured or not executable"
    echo "   MULTIWFN_PATH=$MULTIWFN_PATH"
fi

# Work directories
echo ""
echo "5. Work Directories:"
for dir in QM_WORK_DIR MD_WORK_DIR MULTIWFN_WORK_DIR; do
    path="${!dir}"
    if [ -d "$path" ] && [ -w "$path" ]; then
        echo "   ✅ $dir: $path"
    else
        echo "   ❌ $dir: $path (missing or not writable)"
    fi
done

echo ""
echo "=== Check Complete ==="
```

## See Also

- [Troubleshooting Overview](./index.md) - Main troubleshooting guide
- [Installation Issues](./installation-issues.md) - Setup problems
- [MCP Issues](./mcp-issues.md) - Server connection problems
- [Configuration Reference](../configuration/index.md) - Environment setup
- [ORCA Server](../mcp-servers/orca-server.md) - ORCA MCP documentation
- [GROMACS Server](../mcp-servers/gromacs-server.md) - GROMACS MCP documentation
- [Multiwfn Server](../mcp-servers/multiwfn-server.md) - Multiwfn MCP documentation

---

*Last updated: 2025-12-23 | OHMind v0.1.0*
