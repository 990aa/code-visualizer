import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List, Any
import ast

class CodeVisualizer:
    def generate_visualization(self, analysis: Dict[str, Any], language: str) -> Dict[str, Any]:
        visualizations = {}
        
        # Control flow graph
        visualizations['control_flow'] = self._generate_control_flow(analysis)
        
        # Call graph
        visualizations['call_graph'] = self._generate_call_graph(analysis)
        
        # Data structures visualization
        visualizations['data_structures'] = self._visualize_data_structures(analysis)
        
        # Execution steps for algorithms
        visualizations['execution_steps'] = self._generate_execution_steps(analysis, language)
        
        # Code structure tree
        visualizations['code_structure'] = self._generate_code_structure(analysis)
        
        return visualizations

    def _generate_control_flow(self, analysis: Dict[str, Any]) -> str:
        G = nx.DiGraph()
        
        # Add nodes for functions, loops, conditionals
        for func in analysis.get('functions', []):
            G.add_node(f"func_{func['name']}", type='function', label=func['name'])
        
        for loop in analysis.get('loops', []):
            G.add_node(f"loop_{loop['line']}", type='loop', label=f"Loop L{loop['line']}")
        
        for conditional in analysis.get('conditionals', []):
            G.add_node(f"cond_{conditional['line']}", type='conditional', 
                      label=f"If L{conditional['line']}")
        
        # Create simple connections (this would be more sophisticated in production)
        nodes = list(G.nodes())
        for i in range(len(nodes) - 1):
            G.add_edge(nodes[i], nodes[i + 1])
        
        return self._graph_to_base64(G)

    def _generate_call_graph(self, analysis: Dict[str, Any]) -> str:
        G = nx.DiGraph()
        
        # Add function nodes
        for func in analysis.get('functions', []):
            G.add_node(func['name'], type='function')
        
        # Add method calls
        for call in analysis.get('calls', []):
            if 'function' in call:
                caller = self._find_caller(call['line'], analysis)
                if caller:
                    G.add_edge(caller, call['function'])
        
        return self._graph_to_base64(G)

    def _visualize_data_structures(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        structures = []
        
        # Detect arrays/lists
        variables = analysis.get('variables', [])
        for var in variables:
            if '[]' in str(var.get('type', '')) or 'list' in str(var.get('type', '')):
                structures.append({
                    'type': 'array',
                    'name': var['name'],
                    'visualization': self._create_array_visualization(var)
                })
        
        # Detect linked lists
        for cls in analysis.get('classes', []):
            if any('next' in method.lower() for method in cls.get('methods', [])):
                structures.append({
                    'type': 'linked_list',
                    'name': cls['name'],
                    'visualization': self._create_linked_list_visualization()
                })
        
        return structures

    def _generate_execution_steps(self, analysis: Dict[str, Any], language: str) -> List[Dict[str, Any]]:
        steps = []
        
        # For sorting algorithms
        if any('sort' in func.get('name', '').lower() for func in analysis.get('functions', [])):
            steps = self._simulate_sorting_steps()
        
        # For search algorithms
        elif any('search' in func.get('name', '').lower() for func in analysis.get('functions', [])):
            steps = self._simulate_search_steps()
        
        return steps

    def _generate_code_structure(self, analysis: Dict[str, Any]) -> str:
        G = nx.DiGraph()
        
        if 'code_structure' in analysis:
            for item in analysis['code_structure']:
                node_id = f"{item['type']}_{item['line']}"
                G.add_node(node_id, label=item['type'], line=item['line'])
        
        return self._graph_to_base64(G)

    def _graph_to_base64(self, G: nx.Graph) -> str:
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        
        # Color nodes by type
        node_colors = []
        for node in G.nodes():
            node_type = G.nodes[node].get('type', 'default')
            colors = {
                'function': 'lightblue',
                'loop': 'lightgreen',
                'conditional': 'lightcoral',
                'default': 'lightgray'
            }
            node_colors.append(colors.get(node_type, 'lightgray'))
        
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                node_size=2000, font_size=10, font_weight='bold',
                arrows=True)
        
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"

    def _find_caller(self, line_number: int, analysis: Dict[str, Any]) -> str:
        for func in analysis.get('functions', []):
            if func['line'] <= line_number:
                # Simple heuristic: last function before the call
                return func['name']
        return 'main'

    def _create_array_visualization(self, variable: Dict[str, Any]) -> str:
        # Create a simple array visualization
        return f"Array: {variable['name']} with dynamic size"

    def _create_linked_list_visualization(self) -> str:
        return "Linked list with node connections"

    def _simulate_sorting_steps(self) -> List[Dict[str, Any]]:
        return [
            {'step': 1, 'description': 'Initialize array', 'state': [5, 2, 8, 1, 9]},
            {'step': 2, 'description': 'Compare elements', 'state': [2, 5, 8, 1, 9]},
            {'step': 3, 'description': 'Swap if needed', 'state': [1, 2, 5, 8, 9]},
            {'step': 4, 'description': 'Sorted array', 'state': [1, 2, 5, 8, 9]}
        ]

    def _simulate_search_steps(self) -> List[Dict[str, Any]]:
        return [
            {'step': 1, 'description': 'Initialize search', 'state': 'low=0, high=4'},
            {'step': 2, 'description': 'Calculate mid', 'state': 'mid=2'},
            {'step': 3, 'description': 'Compare with target', 'state': 'found at index 2'}
        ]