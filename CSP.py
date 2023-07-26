import copy
from abc import ABC, abstractmethod
from itertools import chain
from string import digits
import ASTree
from FileProcessor import *

    
class Constraint(ABC):
    @abstractmethod
    def consist(self, assignment):
        pass

#a + b = c
# class Series_equal(Constraint):
#     def __init__(self, ast, vars) -> None:
#         self.ast = ast
#         self.vars = vars
        
#     def consist(self, assignment : dict):
#         if len(assignment) < len(self.vars):
#             return True
#         else:
#             return self.ast.get_tree_result(assignment) == self.ast.get_result(assignment)
#         return False
            
class All_different(Constraint):
    def __init__(self, vars) -> None:
        self.vars = vars
    
    def consist(self, domain : dict, value):
        for i in domain:
            if value not in domain[i]:
                continue
            else:
                domain[i].remove(value)
            if len(domain[i]) == 0:
                return False
        return True
        
class CSP:
    def __init__(self, ast : ASTree):
        self.ast = ast
        self.vars = self.get_vars()
        self.domain = self.get_domain()
        self.constraints = self.add_constraint()
    
    def get_vars(self):
        result = ''.join(set(chain(self.ast.result, *self.ast.get_names_as_lists())))
        return result
                   
    def get_domain(self) -> dict:
        domain = {}
        first_char = list(set(i[0] for i in self.ast.get_names_as_lists()))#[S, M]
        first_char.append(self.ast.result[0])
        for i in self.vars:#[]
            if i in first_char:
                domain[i] = list(range(1, 10))
            else:
                domain[i] = list(range(0, 10))
        return domain
    
    #inference step
    def forward_checking_inference(self, var, value):
        #A
        self.domain.pop(var)
        #A
        #B C D
        flag = True
        for i in self.constraints:
            flag = i.consist(self.domain, value)
        return flag
        
    def add_constraint(self):
        cons_1 = All_different(self.vars)
        return [cons_1]
        
    def is_complete_assignment(self, assignment):
        if len(assignment) == len(self.vars):
            if (self.ast.get_tree_result(assignment) == self.ast.get_result(assignment)):
                return True
            return False
        return False
      
    def take_var_MRV(self):
        min_MRV = str()
        #{[1, 2]}
        min_value = 11
        for i in self.domain:
            min = len(self.domain[i])
            if min <= min_value:
                min_MRV = i
                min_value = min
        return min_MRV
        
    def backtracking_search(self, assignment = {}):
        if self.is_complete_assignment(assignment):
            temp_assignment = {key: val for key, val in sorted(assignment.items(), key = lambda ele: ele[0])}
            numeric_values = [str(value) for value in temp_assignment.values() if isinstance(value, (int, str)) and str(value).isdigit()]
            current_result = ''.join(numeric_values)
            return current_result
        #MRV
        if self.domain == {}:
            return False
        var = self.take_var_MRV()
        ####################
        for value in self.domain[var]:
            copy_domain = copy.deepcopy(self.domain)
            #send consistent to inference
            #{A: (1 -> 4), B: (1 -> 4), C: (1 -> 4), D: (1 -> 4)}
            copy_assignment = copy.deepcopy(assignment)
            copy_assignment[var] = value
            if self.forward_checking_inference(var, value):
                result = self.backtracking_search(copy_assignment)
                if result != False:
                    return result
            self.domain = copy_domain
        return False                              