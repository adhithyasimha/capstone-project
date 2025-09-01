import ast
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_functions(code_string):
    functions = []
    logger.info(f"Extracting functions from code string of length {len(code_string)}")
    
    try:
        # First try using AST for proper parsing
        logger.info("Attempting AST-based function extraction")
        tree = ast.parse(code_string)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get the source code for this function
                func_lines = code_string.splitlines()[node.lineno-1:node.end_lineno]
                func_code = '\n'.join(func_lines)
                
                # Generate a simple AST representation as string
                func_ast = ast.dump(node)
                
                logger.info(f"AST: Found function '{node.name}' at line {node.lineno}")
                logger.info(f"AST: Function code: {func_code}")
                
                functions.append({
                    "name": node.name,
                    "code": func_code,
                    "ast": func_ast,
                    "lineno": node.lineno
                })
        
    except SyntaxError as e:
        logger.warning(f"AST parsing failed: {e}. Trying regex fallback.")
        
        # Fallback to regex-based function extraction
        function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\):'
        matches = re.finditer(function_pattern, code_string)
        
        for match in matches:
            func_name = match.group(1)
            func_start = match.start()
            
            # Find function end by looking for next function or class
            next_func = re.search(r'def\s+[a-zA-Z_]', code_string[func_start + 1:])
            next_class = re.search(r'class\s+[a-zA-Z_]', code_string[func_start + 1:])
            
            if next_func:
                next_func_start = next_func.start() + func_start + 1
            else:
                next_func_start = len(code_string)
                
            if next_class:
                next_class_start = next_class.start() + func_start + 1
            else:
                next_class_start = len(code_string)
                
            func_end = min(next_func_start, next_class_start)
            func_code = code_string[func_start:func_end].strip()
            
            # Get line number (approximately)
            line_count = code_string[:func_start].count('\n') + 1
            
            logger.info(f"Regex: Found function '{func_name}' at line {line_count}")
            logger.info(f"Regex: Function code: {func_code}")
            
            functions.append({
                "name": func_name,
                "code": func_code,
                # Use simplified function signature as AST since we can't parse it
                "ast": f"Function({func_name}, args=[{match.group(2)}])",
                "lineno": line_count
            })
    
    logger.info(f"Successfully extracted {len(functions)} functions")
    for func in functions:
        logger.info(f"Found function: {func['name']} with {len(func['code'].splitlines())} lines")
    
    return functions
