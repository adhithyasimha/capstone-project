import ast
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === Utility to remove comments and docstrings ===
def remove_comments_and_docstrings(code):
    logger.info(f"Removing comments and docstrings from code of length {len(code)}")
    
    # Remove docstrings using regex
    code_before = code
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
    logger.info(f"After docstring removal: {len(code)} chars (removed {len(code_before) - len(code)} chars)")

    # Remove inline and block comments
    code_before = code
    code = re.sub(r'#.*', '', code)
    logger.info(f"After comment removal: {len(code)} chars (removed {len(code_before) - len(code)} chars)")
    
    return code

# === AST transformer to blank out variable names ===
class VariableRemover(ast.NodeTransformer):
    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Load)):
            logger.debug(f"Replacing variable name '{node.id}' with space")
            return ast.copy_location(ast.Name(id=' ', ctx=node.ctx), node)
        return node

# === Rewriter to apply the AST blanking ===
def strip_variable_names(code):
    logger.info(f"Stripping variable names from code of length {len(code)}")
    try:
        tree = ast.parse(code)
        logger.info("AST parsing successful, applying variable name removal")
        tree = VariableRemover().visit(tree)
        ast.fix_missing_locations(tree)
        result = ast.unparse(tree)
        logger.info(f"Variable names stripped, result length: {len(result)}")
        return result
    except Exception as e:
        logger.warning(f"AST parsing failed: {e}, returning original code")
        return code  # fallback if parsing fails

# === Main preprocessing pipeline ===
def preprocess(code: str) -> str:
    logger.info(f"Starting preprocessing for code: {code[:100]}...")
    
    code = remove_comments_and_docstrings(code)
    code = strip_variable_names(code)
    
    logger.info(f"Preprocessing complete. Final code: {code[:100]}...")
    return code
