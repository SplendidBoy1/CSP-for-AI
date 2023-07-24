
class FileProcessor:
    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

    def split_string(self, equation_str):
        parts = equation_str.split('=')
        print("After split: ", parts)
        operand = parts[0]
        result = parts[1]
        return operand, result
    
    def append_to_file(self, content):
        self.file_path = "output.txt"
        try:
            with open(self.file_path, 'a') as file:
                file.write(content + "\n")
        except Exception as e:
            print("An error occurred while appending content to the file:", e)