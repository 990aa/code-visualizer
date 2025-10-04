<template>
    <div id="app">
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-import { python } from '@codemirror/lang-python';
import { java as javaLanguage } from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';port { java as javaLang } from '@codemirror/lang-java';mport { java as javaLanguage } from '@codemirror/lang-java';mport { java as javaLang } from '@codemirror/lang-java';mport { java as javaLang } from '@codemirror/lang-java';de"></i> Code Visualizer</h1>
                <p>Upload your code and see beautiful visualizations of algorithms and data structures</p>
            </div>

            <div class="app-container">
                <!-- Code Input Section -->
                <div class="card">
                    <h2><i class="fas fa-edit"></i> Code Editor</h2>
                    <div class="controls">
                        <select v-model="selectedLanguage" @change="loadExamples" class="language-select">
                            <option value="python">Python</option>
                            <option value="java">Java</option>
                            <option value="cpp">C++</option>
                        </select>
                        
                        <div class="examples-dropdown">
                            <button class="btn btn-secondary">
                                <i class="fas fa-download"></i> Load Example
                            </button>
                            <div class="examples-menu">
                                <div v-for="(code, name) in examples" 
                                     :key="name"
                                     class="example-item"
                                     @click="loadExample(code)">
                                    {{ name.replace('_', ' ').toUpperCase() }}
                                </div>
                            </div>
                        </div>
                        
                        <button class="btn btn-primary" @click="analyzeCode" :disabled="loading">
                            <i class="fas fa-play"></i> Visualize Code
                        </button>
                        
                        <button class="btn btn-secondary" @click="clearCode">
                            <i class="fas fa-trash"></i> Clear
                        </button>
                    </div>
                    
                    <codemirror
                        v-model="code"
                        placeholder="Enter your code here..."
                        :style="{ height: '400px' }"
                        :autofocus="true"
                        :indent-with-tab="true"
                        :tab-size="2"
                        :extensions="extensions"
                    />
                </div>

                <!-- Visualization Section -->
                <div class="card">
                    <h2><i class="fas fa-project-diagram"></i> Visualization</h2>
                    
                    <div class="visualization-area">
                        <div class="visualization-tabs">
                            <button 
                                v-for="tab in tabs" 
                                :key="tab.id"
                                :class="['tab', { active: activeTab === tab.id }]"
                                @click="activeTab = tab.id"
                            >
                                <i :class="tab.icon"></i> {{ tab.label }}
                            </button>
                        </div>

                        <div class="visualization-content">
                            <div v-if="loading" class="loading">
                                <div class="spinner"></div>
                                <p>Analyzing your code...</p>
                            </div>

                            <div v-else-if="error" class="error">
                                <i class="fas fa-exclamation-triangle"></i> {{ error }}
                            </div>

                            <div v-else-if="!visualizationData" class="loading">
                                <i class="fas fa-code" style="font-size: 3rem; opacity: 0.5;"></i>
                                <p>Your visualization will appear here</p>
                            </div>

                            <div v-else>
                                <!-- Control Flow Graph -->
                                <div v-if="activeTab === 'control_flow' && visualizationData.control_flow">
                                    <img :src="visualizationData.control_flow" class="graph-image" alt="Control Flow Graph">
                                </div>

                                <!-- Call Graph -->
                                <div v-if="activeTab === 'call_graph' && visualizationData.call_graph">
                                    <img :src="visualizationData.call_graph" class="graph-image" alt="Call Graph">
                                </div>

                                <!-- Data Structures -->
                                <div v-if="activeTab === 'data_structures' && visualizationData.data_structures" class="data-structures">
                                    <div v-for="ds in visualizationData.data_structures" :key="ds.name" class="ds-item">
                                        <h4>{{ ds.name }}</h4>
                                        <p>{{ ds.type }}</p>
                                        <small>{{ ds.visualization }}</small>
                                    </div>
                                </div>

                                <!-- Execution Steps -->
                                <div v-if="activeTab === 'execution_steps' && visualizationData.execution_steps" class="execution-steps">
                                    <div v-for="step in visualizationData.execution_steps" :key="step.step" class="step">
                                        <span class="step-number">Step {{ step.step }}:</span>
                                        {{ step.description }}
                                        <div v-if="step.state" style="margin-top: 5px; font-family: monospace; color: #666;">
                                            State: {{ step.state }}
                                        </div>
                                    </div>
                                </div>

                                <!-- Code Structure -->
                                <div v-if="activeTab === 'code_structure' && visualizationData.code_structure">
                                    <img :src="visualizationData.code_structure" class="graph-image" alt="Code Structure">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { Codemirror } from 'vue-codemirror';
import { python } from '@codemirror/lang-python';
import { java from '@codemirror/lang-java';
import { cpp } from '@codemirror/lang-cpp';
import { oneDark } from '@codemirror/theme-one-dark';

const code = ref('');
const selectedLanguage = ref('python');
const loading = ref(false);
const error = ref('');
const visualizationData = ref(null);
const activeTab = ref('control_flow');
const examples = ref({});

const extensions = computed(() => {
    const lang = selectedLanguage.value;
    const theme = oneDark;
    if (lang === 'python') return [python(), theme];
    if (lang === 'java') return [javaLanguage(), theme];
    if (lang === 'cpp') return [cpp(), theme];
    return [theme];
});

const tabs = [
    { id: 'control_flow', label: 'Control Flow', icon: 'fas fa-sitemap' },
    { id: 'call_graph', label: 'Call Graph', icon: 'fas fa-project-diagram' },
    { id: 'data_structures', label: 'Data Structures', icon: 'fas fa-cube' },
    { id: 'execution_steps', label: 'Execution Steps', icon: 'fas fa-play-circle' },
    { id: 'code_structure', label: 'Code Structure', icon: 'fas fa-code-branch' }
];

const analyzeCode = async () => {
    if (!code.value.trim()) {
        error.value = 'Please enter some code to visualize';
        return;
    }

    loading.value = true;
    error.value = '';
    visualizationData.value = null;

    try {
        const response = await axios.post('http://localhost:5000/analyze', {
            code: code.value,
            language: selectedLanguage.value
        });

        if (response.data.success) {
            visualizationData.value = response.data.visualization;
        } else {
            error.value = response.data.error || 'An error occurred during analysis';
        }
    } catch (err) {
        error.value = err.response?.data?.error || 'Failed to analyze code';
    } finally {
        loading.value = false;
    }
};

const clearCode = () => {
    code.value = '';
    visualizationData.value = null;
    error.value = '';
};

const loadExamples = async () => {
    try {
        const response = await axios.get(`http://localhost:5000/examples/${selectedLanguage.value}`);
        examples.value = response.data;
    } catch (err) {
        console.error('Failed to load examples:', err);
    }
};

const loadExample = (exampleCode) => {
    code.value = exampleCode;
};

onMounted(() => {
    loadExamples();
    // Load a default example
    code.value = `def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print("Sorted array:", sorted_numbers)`;
});
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    text-align: center;
    margin-bottom: 30px;
    color: white;
}

.header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.header p {
    font-size: 1.1rem;
    opacity: 0.9;
}

.app-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

@media (max-width: 1024px) {
    .app-container {
        grid-template-columns: 1fr;
    }
}

.card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

.card h2 {
    color: #4a5568;
    margin-bottom: 20px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 10px;
}

.code-input {
    width: 100%;
    min-height: 400px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    padding: 15px;
    resize: vertical;
    background: #f7fafc;
    transition: border-color 0.3s ease;
}

.code-input:focus {
    outline: none;
    border-color: #667eea;
}

.controls {
    display: flex;
    gap: 15px;
    margin: 20px 0;
    flex-wrap: wrap;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5a6fd8;
    transform: translateY(-2px);
}

.btn-secondary {
    background: #e2e8f0;
    color: #4a5568;
}

.btn-secondary:hover {
    background: #cbd5e0;
}

select.language-select {
    padding: 12px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 14px;
    background: white;
    color: #4a5568;
}

.visualization-area {
    min-height: 400px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.visualization-tabs {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.tab {
    padding: 10px 20px;
    background: #e2e8f0;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.tab.active {
    background: #667eea;
    color: white;
}

.visualization-content {
    flex: 1;
    border: 2px dashed #cbd5e0;
    border-radius: 8px;
    padding: 20px;
    background: #f7fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 300px;
}

.graph-image {
    max-width: 100%;
    max-height: 400px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.execution-steps {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.step {
    background: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #667eea;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.step-number {
    font-weight: bold;
    color: #667eea;
    margin-right: 10px;
}

.data-structures {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.ds-item {
    background: white;
    padding: 15px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    color: #667eea;
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e2e8f0;
    border-top: 4px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.error {
    background: #fed7d7;
    color: #c53030;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #fc8181;
}

.examples-dropdown {
    position: relative;
    display: inline-block;
}

.examples-menu {
    display: none;
    position: absolute;
    background: white;
    min-width: 200px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    border-radius: 8px;
    z-index: 1000;
    max-height: 300px;
    overflow-y: auto;
}

.examples-dropdown:hover .examples-menu {
    display: block;
}

.example-item {
    padding: 12px 15px;
    cursor: pointer;
    border-bottom: 1px solid #e2e8f0;
    transition: background 0.3s ease;
}

.example-item:hover {
    background: #f7fafc;
}

.example-item:last-child {
    border-bottom: none;
}
</style>
