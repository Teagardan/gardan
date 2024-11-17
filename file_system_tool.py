class FileSystemTool:
    def __init__(self):
        pass  # No initialization needed

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            return file_content

        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
            return "Sorry, I couldn't find the file."

        except Exception as e:
            print(f"Error reading file: {e}")
            return "Sorry, there was an error reading the file."

    def write_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return "File written successfully."

        except Exception as e:
            print(f"Error writing file: {e}")
            return "Sorry, there was an error writing the file."