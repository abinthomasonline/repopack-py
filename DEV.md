# Run tests
pytest --cov --verbose

# Install package locally for testing
pip install -e .

# Build package (update version.py first)
python -m build

# Upload package
twine upload dist/*

# Note: Make sure to install build and twine:
# pip install build twine

