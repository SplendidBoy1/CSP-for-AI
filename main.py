from FileProcessor import *
from ASTree import AST
from CSP import *
from datetime import datetime


def main():
    file_path = 'test.txt'
    # Tạo object FileProcessor
    file_processor = FileProcessor()
    
    file_content = file_processor.read_file(file_path)
    if file_content is not None:
        print("File content:")
        print(file_content) # check thử thoi nha :))

    operand, result = file_processor.split_string(file_content)
    ast_obj = AST(operand, result)
    csp = CSP(ast_obj)
    print(''.join(sorted(csp.vars)))
    start=datetime.now()
    result = csp.backtracking_search()
    print(datetime.now() - start)
    print(result)
    print(ast_obj.get_names_as_lists())
    file_processor = FileProcessor()
    if result == False:
        file_processor.append_to_file("NO SOLUTION")
    else:
        file_processor.append_to_file(result)
      
if __name__ == "__main__":
    main()