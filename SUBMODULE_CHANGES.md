# Submodule Changes Summary

## Overview
This repository contains fixes for compilation issues in DPVO. Some of these fixes affect the git submodules (Pangolin and DBoW2).

## Handling Submodule Changes

### For Pangolin Submodule

The Pangolin submodule has compilation fixes that are documented in `pangolin-compilation-fixes.patch`.

**To apply these fixes in a fresh clone:**

```bash
cd Pangolin
git apply ../pangolin-compilation-fixes.patch
cd ..
```

Or include them in your Pangolin build:

```bash
cd Pangolin/build
cmake ..
make -j8
sudo make install
cd ../..
```

### For DBoW2 Submodule

The DBoW2 submodule has been included but may have modifications. If you encounter build issues, you can:

1. Check the current state:
```bash
cd DBoW2
git status
cd ..
```

2. Reset to original if needed:
```bash
cd DBoW2
git checkout .
cd ..
git submodule update
```

## Complete Setup from Scratch

```bash
# Clone with submodules
git clone --recursive https://github.com/Roboticistprogrammer/DPVO_Custom.git
cd DPVO_Custom

# Setup conda environment
conda env create -f environment.yml
conda activate dpvo

# Install Eigen
wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip
unzip eigen-3.4.0.zip -d thirdparty

# Install DPVO core (uses the fixed setup.py)
pip install --no-build-isolation .

# Download models and data
./download_models_and_data.sh

# [Optional] Install Pangolin Viewer
./Pangolin/scripts/install_prerequisites.sh recommended
mkdir -p Pangolin/build && cd Pangolin/build
cmake ..
make -j8
sudo make install
cd ../..

# Apply Pangolin compilation fixes if needed
cd Pangolin
git apply ../pangolin-compilation-fixes.patch
cd ..

# Install DPViewer
pip install ./DPViewer
```

## Changes Made

### Main Repository Changes
- **setup.py**: Fixed torch import handling for pip build isolation
- **BUILD_FIXES.md**: Comprehensive documentation of all fixes
- **pangolin-compilation-fixes.patch**: Patch file for Pangolin compilation issues

### Submodule Modifications (in Pangolin)

These changes fix compilation issues with modern toolchains:

1. **packetstream_tags.h**: Added `#include <cstdint>`
2. **image_io_jpg.cpp**: Added `#include <cstdint>`
3. **image_io_bmp.cpp**: Added `#include <cstdint>`
4. **ffmpeg_common.h**: Removed deprecated XVMC pixel format entries

## Testing the Installation

```bash
# Without visualization
python demo.py --imagedir=<path> --calib=<calib_file> --stride=5 --plot

# With visualization (requires DPViewer)
python demo.py --imagedir=<path> --calib=<calib_file> --stride=5 --plot --viz
```

## Troubleshooting

If you encounter issues with Pangolin compilation:

```bash
cd Pangolin
git status  # Check what's modified
git apply ../pangolin-compilation-fixes.patch  # Apply fixes
cd ../Pangolin/build
cmake ..
make clean
make -j8
sudo make install
```

## Verified Configurations

- **OS**: Ubuntu 22.04 (Linux)
- **Compiler**: GCC 13.3.0
- **Python**: 3.10
- **CUDA**: 12.1
- **CuDNN**: Installed
- **FFmpeg**: 7.x
- **PyTorch**: 2.3.1
- **CMake**: 3.22+
