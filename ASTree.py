import ast

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
        t = type(tree)
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