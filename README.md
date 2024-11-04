# Pairs Trading Research Repository
Authored by Andrew Hall and Seth Peterson

## Getting Started

### 1. Create virtual environment
```bash
python -m venv .venv # Windows/Conda

python3 -m venv .venv #MacOS/Linux
```

### 2. Activate virtual environment
```bash
.venv/Scripts/activate # Windows

source .venv/bin/activate #MacOS/Linus/Conda
```

### 3. Upgrade pip
```bash
pip install --upgrade pip
```

### 4. Install requirements
```bash
pip install -r requirements.txt
```

## Development

### Jupyter Notebooks
Jupyter Notebooks have access to all research modules when placed in the root directory (outside of the research directory). Ideally Jupyter Notebooks are turned into single python files in the research directory.

### Python Files
To execute a python file from the command line that can still access the research modules execute the following. Note that there should be no back-slashes or .py file extensions.

```bash
python -m path.to.file
```