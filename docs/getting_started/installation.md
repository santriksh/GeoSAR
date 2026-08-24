# Installing GeoSAR

This guide explains how to install GeoSAR and verify that it is working correctly.

GeoSAR is developed using Python and relies on several geospatial libraries, including GDAL, Rasterio, and PROJ. The recommended installation method is through a Conda environment.

---

# System Requirements

GeoSAR has been tested with the following configuration:

| Component | Recommended Version |
|-----------|---------------------|
| Python | 3.10 or later |
| Operating System | Linux (Ubuntu 22.04 or later) |
| Package Manager | Conda / Miniconda |
| GDAL | 3.10+ |
| PROJ | 9+ |

Although GeoSAR may work on Windows and macOS, the primary development environment is Linux.

---

# Create a Conda Environment

Create a new virtual environment.

```bash
conda create -n geosar python=3.10
```

Activate the environment.

```bash
conda activate geosar
```

Verify the Python version.

```bash
python --version
```

Example output:

```text
Python 3.10.20
```

---

# Clone the Repository

Clone the GeoSAR repository.

```bash
git clone https://github.com/santriksh/GeoSAR.git
```

Move into the project directory.

```bash
cd GeoSAR
```

---

# Install GeoSAR

Install GeoSAR in editable mode.

```bash
pip install -e .
```

Editable mode allows changes made to the source code to become immediately available without reinstalling the package.

---

# Install Development Dependencies

If you plan to contribute to GeoSAR or run the test suite, install the development dependencies.

```bash
pip install -e ".[dev]"
```

This installs additional packages used for:

- pytest
- ruff
- documentation generation
- development tools

---

# Verify the Installation

Start Python.

```bash
python
```

Import GeoSAR.

```python
import sar

print(sar.__version__)
```

Expected output:

```text
1.0.0
```

Verify that the package can load correctly.

```python
import sar

print(sar.load_sar)
print(sar.refined_lee)
print(sar.ratio_change)
```

If these functions are displayed without errors, the installation has completed successfully.

---

# Running the Test Suite

To verify that your installation is functioning correctly, execute the automated test suite.
Back in the terminal, execute:

```bash
pytest
```

A successful installation should report all tests passing.

---

# Common Installation Issues

## ImportError: No module named 'sar'

Cause:

The current directory is not on the Python path, or GeoSAR has not been installed.

Solution:

```bash
pip install -e .
```

---

## GDAL / PROJ Errors

Example:

```text
PROJ database version mismatch
```

Cause:

Multiple GDAL or PROJ installations are being used simultaneously.

Solution:

- Use a dedicated Conda environment.
- Install GDAL, Rasterio, and PyProj from the same Conda channel.
- Ensure that Jupyter uses the same Python environment as the terminal.

---

## Jupyter Uses the Wrong Environment

Symptoms:

GeoSAR imports correctly in the terminal but fails inside Jupyter Notebook.

Solution:

Verify the active Python executable.

```python
import sys

print(sys.executable)
```

The reported executable should belong to the GeoSAR Conda environment.

---

# Next Steps

GeoSAR has now been installed successfully.

Continue with the next guide:

**Quick Start**

The Quick Start tutorial introduces the GeoSAR workflow by loading Sentinel-1 imagery, applying speckle filtering, detecting flooded regions, and visualizing the resulting flood map.