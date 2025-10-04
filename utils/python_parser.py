import ast
import javalang
import re
from typing import Dict, List, Any

class PythonCodeParser:
    def parse_code(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            return self._analyze_ast(tree, code)
        except SyntaxError as e:
            return {'error': f'Syntax error: {e}'}

    def _analyze_ast(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        analysis = {
            'functions': [],
            'classes': [],
            'variables': [],
            'loops': [],
            'conditionals': [],
            'calls': [],
            'imports': [],
            'code_structure': []
        }
        
        lines = code.split('\n')
        
        for node in ast.walk(tree):
            # Functions
            if isinstance(node, ast.FunctionDef):
                analysis['functions'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'body': self._get_node_code(node, lines)
                })
            
            # Classes
            elif isinstance(node, ast.ClassDef):
                analysis['classes'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            
            # Variables
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        analysis['variables'].append({
                            'name': target.id,
                            'line': node.lineno,
                            'value': ast.unparse(node.value) if hasattr(ast, 'unparse') else 'N/A'
                        })
            
            # Loops
            elif isinstance(node, (ast.For, ast.While)):
                analysis['loops'].append({
                    'type': 'for' if isinstance(node, ast.For) else 'while',
                    'line': node.lineno,
                    'body': self._get_node_code(node, lines)
                })
            
            # Conditionals
            elif isinstance(node, ast.If):
                analysis['conditionals'].append({
                    'line': node.lineno,
                    'test': ast.unparse(node.test) if hasattr(ast, 'unparse') else 'N/A',
                    'body': self._get_node_code(node, lines)
                })
            
            # Function calls
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                analysis['calls'].append({
                    'function': node.func.id,
                    'line': node.lineno
                })
            
            # Imports
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                analysis['imports'].append({
                    'module': node.module if isinstance(node, ast.ImportFrom) else '',
                    'names': [alias.name for alias in node.names],
                    'line': node.lineno
                })
        
        # Build code structure
        analysis['code_structure'] = self._build_structure(tree, lines)
        return analysis

    def _get_node_code(self, node: ast.AST, lines: List[str]) -> str:
        try:
            return '\n'.join(lines[node.lineno-1:node.end_lineno])
        except:
            return ''

    def _build_structure(self, tree: ast.AST, lines: List[str]) -> List[Dict[str, Any]]:
        structure = []
        
        def traverse(node, depth=0):
            node_type = type(node).__name__
            structure.append({
                'type': node_type,
                'depth': depth,
                'line': getattr(node, 'lineno', 0),
                'code': self._get_node_code(node, lines) if hasattr(node, 'lineno') else ''
            })
            
            for child in ast.iter_child_nodes(node):
                traverse(child, depth + 1)
        
        traverse(tree)
        return structure