import re
from typing import Dict, List, Any

class CppCodeParser:
    def parse_code(self, code: str) -> Dict[str, Any]:
        return self._analyze_with_regex(code)

    def _analyze_with_regex(self, code: str) -> Dict[str, Any]:
        analysis = {
            'functions': [],
            'classes': [],
            'variables': [],
            'loops': [],
            'conditionals': [],
            'calls': [],
            'includes': [],
            'code_structure': []
        }
        
        lines = code.split('\n')
        
        # Parse includes
        analysis['includes'] = [
            {'line': i+1, 'header': match.group(1)}
            for i, line in enumerate(lines)
            for match in [re.match(r'#include\s*[<"]([^>"]+)[>"]', line.strip())]
            if match
        ]
        
        # Parse functions
        function_pattern = r'(\w+)\s+(\w+)\s*\(([^)]*)\)\s*\{'
        for i, line in enumerate(lines):
            match = re.search(function_pattern, line)
            if match:
                analysis['functions'].append({
                    'return_type': match.group(1),
                    'name': match.group(2),
                    'parameters': match.group(3),
                    'line': i+1
                })
        
        # Parse classes
        class_pattern = r'class\s+(\w+)'
        for i, line in enumerate(lines):
            match = re.search(class_pattern, line)
            if match:
                analysis['classes'].append({
                    'name': match.group(1),
                    'line': i+1
                })
        
        # Parse loops
        for i, line in enumerate(lines):
            if re.search(r'\b(for|while)\s*\(', line):
                analysis['loops'].append({
                    'type': 'for' if 'for' in line else 'while',
                    'line': i+1
                })
        
        # Parse conditionals
        for i, line in enumerate(lines):
            if re.search(r'\bif\s*\(', line):
                analysis['conditionals'].append({
                    'line': i+1
                })
        
        return analysis