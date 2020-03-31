from slimit.parser import Parser
from slimit.visitors.nodevisitor import ASTVisitor
from slimit.lexer import Lexer
from slimit import ast
from slimit.visitors import nodevisitor
import ast as astReader


class MyVisitor(ASTVisitor):
    def visit_Object(self, node):
        """Visit object literal."""
        pairs = {}
        for prop in node:
            left, right = prop.left, astReader.literal_eval(prop.right.value)
            pairs[left.value] = astReader.literal_eval(right)
            self.visit(prop)
        return pairs


def generateConfigFile(file):
    with open(file, 'r') as content_file:
        content = content_file.read()

    parser = Parser()
    tree = parser.parse(content)
    visitor = MyVisitor()
    found = False
    pairs = {}

    for node in nodevisitor.visit(tree):
        if isinstance(node, ast.Identifier) and node.value == 'groundTruth':
            found = True
        if isinstance(node, ast.Object):
            pairs = visitor.visit(node)
            break

    return pairs


generateConfigFile("test-suite/aliasing/alias2.js")
