.PHONY: all setup run clean

# Default to creating a venv
VENV_DIR ?= .venv
PYTHON = $(VENV_DIR)/bin/python

# --- GPU Acceleration ---
# Uncomment the line below to build with NVIDIA CUDA support.
# Requires NVIDIA CUDA Toolkit to be installed.
# CMAKE_ARGS="-DGGML_CUDA=on"

# For Apple Silicon, Metal support is enabled by default if the library detects it.
# You can force it with: CMAKE_ARGS="-DLLAMA_METAL=on"

all: setup

setup: $(VENV_DIR)/touchfile

$(VENV_DIR)/touchfile: requirements.txt
	@echo "--> Creating virtual environment in $(VENV_DIR)..."
	python3 -m venv $(VENV_DIR)
	@echo "--> Installing dependencies from requirements.txt..."
	$(PYTHON) -m pip install --upgrade pip
# If CMAKE_ARGS is set, force a reinstall of llama-cpp-python
ifdef CMAKE_ARGS
	@echo "--> Installing with GPU acceleration: $(CMAKE_ARGS)"
	CMAKE_ARGS=$(CMAKE_ARGS) FORCE_CMAKE=1 $(PYTHON) -m pip install --upgrade --force-reinstall --no-cache-dir -r requirements.txt
else
	@echo "--> Installing with standard CPU support..."
	$(PYTHON) -m pip install -r requirements.txt
endif
	@echo "--> Setup complete. You can now run 'make run'"
	touch $@

run:
	@echo "--> Starting AI server and Telegram bot..."
	@$(PYTHON) -m honcho start

clean:
	@echo "--> Cleaning up..."
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "--> Cleanup complete." 