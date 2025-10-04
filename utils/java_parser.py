import javalang
from typing import Dict, List, Any

class JavaCodeParser:
    def parse_code(self, code: str) -> Dict[str, Any]:
        try:
            tree = javalang.parse.parse(code)
            return self._analyze_tree(tree, code)
        except Exception as e:
            return {'error': f'Parse error: {e}'}

    def _analyze_tree(self, tree, code: str) -> Dict[str, Any]:
        analysis = {
            'methods': [],
            'classes': [],
            'variables': [],
            'loops': [],
            'conditionals': [],
            'calls': [],
            'imports': [],
            'code_structure': []
        }
        
        lines = code.split('\n')
        
        for path, node in tree:
            # Classes
            if isinstance(node, javalang.tree.ClassDeclaration):
                analysis['classes'].append({
                    'name': node.name,
                    'line': node.position.line if node.position else 0,
                    'methods': [m.name for m in node.methods] if node.methods else []
                })
            
            # Methods
            elif isinstance(node, javalang.tree.MethodDeclaration):
                analysis['methods'].append({
                    'name': node.name,
                    'line': node.position.line if node.position else 0,
                    'return_type': node.return_type.name if node.return_type else 'void',
                    'parameters': [{'type': param.type.name, 'name': param.name} 
                                 for param in node.parameters] if node.parameters else []
                })
            
            # Variables
            elif isinstance(node, javalang.tree.VariableDeclaration):
                for declarator in node.declarators:
                    analysis['variables'].append({
                        'name': declarator.name,
                        'type': node.type.name,
                        'line': node.position.line if node.position else 0
                    })
            
            # Loops
            elif isinstance(node, (javalang.tree.ForStatement, javalang.tree.WhileStatement)):
                analysis['loops'].append({
                    'type': 'for' if isinstance(node, javalang.tree.ForStatement) else 'while',
                    'line': node.position.line if node.position else 0
                })
            
            # Conditionals
            elif isinstance(node, javalang.tree.IfStatement):
                analysis['conditionals'].append({
                    'line': node.position.line if node.position else 0
                })
            
            # Method calls
            elif isinstance(node, javalang.tree.MethodInvocation):
                analysis['calls'].append({
                    'method': node.member,
                    'line': node.position.line if node.position else 0
                })
        
        return analysis