# Test Impact Engine

A simple **Test Impact Analysis** application that identifies which tests are **added, removed, or modified** between Git commits by analyzing test files, without executing the test suite.

- **Backend Framework:** FastAPI  
- **Git Analysis:** Git CLI (`git show`)  
- **Test Detection:** Regex-based parsing  
- **Interface:** REST API + Node.js CLI  
- **Language:** Python  

---

## Features

- Analyze Git commits to detect impacted tests  
- Identify tests that are added, removed, or modified  
- Supports Jest / Vitest style tests (`test()` and `it()`)  
- Detects real modifications by comparing test bodies  
- Exposes a simple REST API for impact analysis  
- Includes a CLI to consume the API and display results  

---

## Tech Stack

- FastAPI
- Git CLI
- Python 3.12+
- Node.js (for CLI)

---
# Create and activate conda environment
conda create genenv
conda activate genenv

# Install dependencies
pip install fastapi uvicorn

# Run the API server
uvicorn api.main:app --reload

# Run the CLI
node cli/index.js --commit <commit-hash> --repo <absolute-path-to-repo>



