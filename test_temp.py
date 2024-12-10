import tempfile

# Get the system's temporary directory
temp_dir = tempfile.gettempdir()

print(temp_dir)

print(f"Temporary directory: {temp_dir}")