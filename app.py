import matplotlib
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from utils.python_parser import PythonCodeParser
from utils.java_parser import JavaCodeParser
from utils.cpp_parser import CppCodeParser
from utils.visualizer import CodeVisualizer

matplotlib.use('Agg')

app = Flask(__name__, static_folder='frontend/dist', static_url_path='/')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route('/analyze', methods=['POST'])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Parse code based on language
        if language == 'python':
            parser = PythonCodeParser()
        elif language == 'java':
            parser = JavaCodeParser()
        elif language == 'cpp':
            parser = CppCodeParser()
        else:
            return jsonify({'error': 'Unsupported language'}), 400
        
        # Parse the code
        analysis_result = parser.parse_code(code)
        
        # Generate visualization data
        visualizer = CodeVisualizer()
        visualization_data = visualizer.generate_visualization(analysis_result, language)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'visualization': visualization_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/examples/<language>', methods=['GET'])
def get_examples(language):
    examples = {
        'python': {
            'bubble_sort': '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
''',
            'binary_search': '''
def binary_search(arr, target):
    low, high = 0, len(arr)-1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
''',
            'linked_list': '''
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
'''
        },
        'java': {
            'quick_sort': '''
public class QuickSort {
    public void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = (low - 1);
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;
        return i + 1;
    }
}
''',
            'binary_tree': '''
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}

class BinaryTree {
    TreeNode root;
    
    public void insert(int val) {
        root = insertRec(root, val);
    }
    
    private TreeNode insertRec(TreeNode root, int val) {
        if (root == null) {
            root = new TreeNode(val);
            return root;
        }
        if (val < root.val) {
            root.left = insertRec(root.left, val);
        } else if (val > root.val) {
            root.right = insertRec(root.right, val);
        }
        return root;
    }
}
'''
        }
    }
    
    return jsonify(examples.get(language, {}))

if __name__ == '__main__':
    app.run(debug=True)