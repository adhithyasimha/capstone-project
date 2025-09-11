import ast
import re

# === Utility to remove comments and docstrings ===
def remove_comments_and_docstrings(code):
    # Remove docstrings using regex
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)

    # Remove inline and block comments
    code = re.sub(r'#.*', '', code)
    return code

# === AST transformer to blank out variable names ===
class VariableRemover(ast.NodeTransformer):
    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            return ast.copy_location(ast.Name(id=' ', ctx=node.ctx), node)
        return node

# === Rewriter to apply the AST blanking ===
def strip_variable_names(code):
    try:
        tree = ast.parse(code)
        tree = VariableRemover().visit(tree)
        ast.fix_missing_locations(tree)
        return ast.unparse(tree)
    except Exception:
        return code  # fallback if parsing fails

# === Main preprocessing pipeline ===
def preprocess(code: str) -> str:
    code = remove_comments_and_docstrings(code)
    code = strip_variable_names(code)
    return code
