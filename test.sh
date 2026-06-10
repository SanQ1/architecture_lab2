#!/bin/bash

source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.

echo "=== Unit-тести домену ==="
pytest tests/domain

echo "=== Unit-тести Application layer ==="
pytest tests/application

echo "=== Integraion тести ==="
pytest tests/integration
