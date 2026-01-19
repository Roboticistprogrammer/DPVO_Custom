# DPVO Build Fixes and Compilation Issues

## Summary
This document describes all the fixes applied to make DPVO compile successfully with modern toolchains (GCC 13, FFmpeg 7.x, Python 3.10).

## Issues Fixed

### 1. PyTorch Import Error During pip install
**Problem:** `ModuleNotFoundError: No module named 'torch'` when running `pip install .`

**Root Cause:** The `setup.py` imported torch at the top level, but torch wasn't available in the isolated build environment created by pip.

**Solution:** Modified `setup.py` to defer torch imports until build time and use `--no-build-isolation` flag.

**Files Changed:**
- `setup.py` - Wrapped torch imports in functions that are called during setup

**How to Use:**
```bash
pip install --no-build-isolation .
```

### 2. Pangolin Compilation Fixes

#### Issue 2a: Missing `<cstdint>` Headers
**Problem:** Compilation errors like `'uint32_t' does not name a type` in multiple Pangolin source files.

**Root Cause:** Modern C++ compilers require explicit `#include <cstdint>` for integer types. Older headers were relying on implicit includes.

**Solution:** Added `#include <cstdint>` to affected files.

**Files Changed (in Pangolin submodule):**
- `components/pango_packetstream/include/pangolin/log/packetstream_tags.h`
- `components/pango_image/src/image_io_jpg.cpp`
- `components/pango_image/src/image_io_bmp.cpp`

#### Issue 2b: FFmpeg Compatibility (Deprecated API)
**Problem:** Compilation errors for `AV_PIX_FMT_XVMC_MPEG2_MC` and `AV_PIX_FMT_XVMC_MPEG2_IDCT` when building with FFmpeg 7.x.

**Root Cause:** These pixel formats were deprecated and removed in newer FFmpeg versions. The `FF_API_XVMC` macro was not being defined.

**Solution:** Removed the deprecated format entries from the switch statement.

**Files Changed (in Pangolin submodule):**
- `components/pango_video/include/pangolin/video/drivers/ffmpeg_common.h` - Removed deprecated XVMC format cases

**Patch File:** See `pangolin-compilation-fixes.patch`

## Installation Steps

### Step 1: Environment Setup
```bash
git clone https://github.com/princeton-vl/DPVO.git --recursive
cd DPVO
conda env create -f environment.yml
conda activate dpvo
```

### Step 2: Install Eigen
```bash
wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip
unzip eigen-3.4.0.zip -d thirdparty
```

### Step 3: Install DPVO Core
```bash
pip install --no-build-isolation .
```

### Step 4: Download Models and Data
```bash
./download_models_and_data.sh
```

### Step 5: Install Pangolin Viewer (Optional)
```bash
# Install prerequisites
./Pangolin/scripts/install_prerequisites.sh recommended

# Build Pangolin (applies fixes automatically)
mkdir -p Pangolin/build && cd Pangolin/build
cmake ..
make -j8
sudo make install
cd ../..

# Apply compilation fixes if needed
# cd Pangolin && git apply ../pangolin-compilation-fixes.patch && cd ..

# Install DPViewer
pip install ./DPViewer
```

## Testing

### Without Viewer
```bash
python demo.py --imagedir=calib/iphone.txt --calib=calib/iphone.txt --stride=5 --plot
```

### With Viewer
```bash
python demo.py --imagedir=calib/iphone.txt --calib=calib/iphone.txt --stride=5 --plot --viz
```

## Troubleshooting

### If Pangolin Compilation Fails
1. Check that all prerequisites are installed: `./Pangolin/scripts/install_prerequisites.sh recommended`
2. Apply the fixes manually:
   ```bash
   cd Pangolin
   git apply ../pangolin-compilation-fixes.patch
   cd ../Pangolin/build
   cmake ..
   make -j8
   sudo make install
   ```

### If DPViewer Import Fails
Ensure Pangolin was installed to system paths:
```bash
sudo ldconfig
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

## Platform Tested
- OS: Ubuntu 20/22 (Linux)
- GCC: 13.3.0
- Python: 3.10
- CUDA: 12.1
- FFmpeg: 7.x
- PyTorch: 2.3.1
