# NOTE: whitespace in front of commands are Tabs!
# Install the package with development dependencies
# alternative to `pip install -r requirements`
install:
	pip install .[dev] && pip uninstall EPICcoder -y

# Clean up build artifacts
clean:
	rm -rf build/ dist/ *.egg-info

