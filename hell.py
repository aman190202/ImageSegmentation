import tempfile
 
# We create a temporary file using tempfile.TemporaryFile()
temp = tempfile.TemporaryFile()
 
# Temporary files are stored here
temp_dir = tempfile.gettempdir()
 
print(f"Temporary files are stored at: {temp_dir}")
 
print(f"Created a tempfile object: {temp}")
print(f"The name of the temp file is: {temp.name}")
 
# This will clean up the file and delete it automatically
temp.close()