import ast

from itertools import chain, permutations
from string import digits
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

    def parse_math_equation(self,equation):
        equation = equation.replace(" ", "")  # Remove spaces from the equation
        parts = equation.split("=")

        left_side = parts[0]
        right_side = parts[1]

        # operands = []  # List to store the operands
        # operators = []  # List to store the operators
        # current_operand = ""  # Temporary variable to build the current operand
        # parenthese_position = []
        # countCol = 0
        # countRow = 0

        # for char in left_side:
        #     if char in ('+', '*'):  # If the character is an operator
        #         if current_operand:
        #             operands.append(current_operand)
        #             current_operand = ""
        #         operators.append(char)
        #     elif char in ('('):
        #         temp = len(operators)  # dấu ngoặc mở bằng lấy phần tử thứ đó
        #         countCol += 1
        #     elif char in (')'):
        #         parenthese_position.append([temp,len(operators)  ])#dấu ngoặc đóng lấy phần tử tới đó
            
        #     else:  # If the character is a digit or a variable
        #         current_operand += char

        # if current_operand:  # Process the last operand (if any)
        #     operands.append(current_operand)

        return left_side, right_side
            

class AST:
    def __init__(self, operand_str: str, result: str):
        self.tree = ast.parse(operand_str)
        
        self.result = result

    def get_result(self, assignments: dict) -> int:
        sum = 0
        temp = 1
        
        for char in reversed(self.result):
            sum += assignments[char]*temp
            temp *= 10
        return sum

    def get_tree_result_util(self, tree, assignments: dict) -> int:
        t = type(tree) # xác định mỗi node là operand hay là operator hay la parenthese
        
        if (t == ast.Module):
            
            return self.get_tree_result_util(tree.body, assignments)
        elif (t == list):
            return self.get_tree_result_util(tree[0], assignments)
        elif t == ast.Expr:
            return self.get_tree_result_util(tree.value, assignments)
        elif (t == ast.BinOp):
            o = type(tree.op)
            if (o == ast.Add):
                return self.get_tree_result_util(tree.left, assignments) + self.get_tree_result_util(tree.right, assignments)
            elif (o == ast.Sub):
                return self.get_tree_result_util(tree.left, assignments) - self.get_tree_result_util(tree.right, assignments)
            elif (o == ast.Mult):
                return self.get_tree_result_util(tree.left, assignments) * self.get_tree_result_util(tree.right, assignments)
        elif (t == ast.Name):
            sum = 0
            temp = 1
            for char in reversed(tree.id):
                sum += assignments[char]*temp
                temp *= 10
            return sum

    def get_tree_result(self, assignments : dict) -> int:
        # đệ quy vô cây ast -> sử dụng bảng gán giá trị tìm kết quả phép toán
        return self.get_tree_result_util(self.tree, assignments)
    def get_names_as_lists(self):
        names_list = []

        def extract_names(node):
            if isinstance(node, ast.Module):
                for item in node.body:
                    extract_names(item)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names_list.append(target.id)
            elif isinstance(node, ast.Expr):
                extract_names(node.value)
            elif isinstance(node, ast.BinOp):
                extract_names(node.left)
                extract_names(node.right)
            elif isinstance(node, ast.Name):
                names_list.append(node.id)
        
        extract_names(self.tree)
        

        # Tách phần tử cuối cùng thành một phần tử riêng
        

        return names_list
    
def solve_cryptarithm(addends, result):
    
    letters = ''.join(sorted(set(chain(result, *addends)))) #những chữ cái tồn tại
    # equal = "="
    # result = f"{letters} {equal}"
    print(letters, end=' = ')
    initial_letters = ''.join(set(chain(result[0], (a[0] for a in addends)))) #chữ cái đầu
    
    results = set()
    for perm in permutations(digits, len(digits)): #perm: những khả năng
        
        integer_list = list(map(int, perm))
        pairs = zip(letters, integer_list)
        value_dict = dict(pairs)
        
        if (ast_obj.get_tree_result(value_dict)) == ast_obj.get_result(value_dict):
            numeric_values = [str(value) for value in value_dict.values() if isinstance(value, (int, str)) and str(value).isdigit()]
            current_result = ''.join(numeric_values)
            results.add(current_result)

    print(', '.join(results))
            

            
            
if __name__ == '__main__':
    file_path = "test.txt"
    # Tạo object FileProcessor
    file_processor = FileProcessor()
    
    file_content = file_processor.read_file(file_path)
    print(file_content)
    operands_list, result_operand= file_processor.parse_math_equation(file_content)

   # ast_obj = AST("SO+MANY+MORE+MEN+SEEM+TO+SAY+THAT+THEY+MAY+SOON+TRY+TO+STAY+AT+HOME+SO+AS+TO+SEE+OR+HEAR+THE+SAME+ONE+MAN+TRY+TO+MEET+THE+TEAM+ON+THE+MOON+AS+HE+HAS+AT+THE+OTHER+TEN", "TESTS")
    ast_obj = AST(operands_list,result_operand)
    addends = ast_obj.get_names_as_lists()
    
    # value_dict = {'D' : 7, 'E' : 5, 'M' : 1, 'N' : 6, 'O' : 0, 'R' : 8, 'S' : 9, 'Y' : 2}
    # print(ast_obj.get_tree_result(value_dict))
    # print(ast_obj.get_result(value_dict))
    results = solve_cryptarithm(addends,ast_obj.result)
    print(results)