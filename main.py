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
    start=datetime.now()
    ast_obj = AST(operand, result)
    csp = CSP(ast_obj)
    print(''.join(sorted(csp.vars)))
    csp.backtracking_search()
    print(datetime.now() - start)
    print(csp.list_solve)
    file_processor = FileProcessor()
    if len(csp.list_solve) == 0:
        file_processor.append_to_file("NO SOLUTION")
    else:
        for i in csp.list_solve:
            file_processor.append_to_file(i)
      
if __name__ == "__main__":
    main()