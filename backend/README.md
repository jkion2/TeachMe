# Backend

## Set up

### 1. Install Build Dependencies

```bash
# Required for manim to work
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y ffmpeg libcairo2-dev libpango1.0-dev pkg-config
sudo apt install texlive-latex-base texlive-latex-extra

# Required for the python environment
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Python Packages

```bash
uv venv # creates a virtual environment
source .venv/bin/activate # activates the virtual environment
uv sync # installs the packages
```

### 3. Run Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

or

```bash
uv run main.py
```