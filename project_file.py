<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Analysis Tool</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
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
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
            width: 100%;
            max-width: 800px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
        }

        .header h1 {
            color: #2d3748;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: #718096;
            font-size: 1.1rem;
        }

        .step {
            margin-bottom: 30px;
            opacity: 0.5;
            transition: all 0.3s ease;
        }

        .step.active {
            opacity: 1;
            transform: translateY(-2px);
        }

        .step-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }

        .step-number {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
            font-size: 0.9rem;
        }

        .step-title {
            color: #2d3748;
            font-size: 1.2rem;
            font-weight: 600;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: #4a5568;
            font-weight: 500;
        }

        .input-group input[type="text"],
        .input-group input[type="file"],
        .input-group textarea {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }

        .input-group input[type="text"]:focus,
        .input-group textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .input-group textarea {
            resize: vertical;
            min-height: 100px;
        }

        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .status {
            padding: 12px 16px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-weight: 500;
        }

        .status.success {
            background: #f0fff4;
            color: #22543d;
            border: 1px solid #9ae6b4;
        }

        .status.error {
            background: #fed7d7;
            color: #742a2a;
            border: 1px solid #fc8181;
        }

        .status.info {
            background: #bee3f8;
            color: #2a4365;
            border: 1px solid #63b3ed;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .file-info {
            background: #f7fafc;
            padding: 15px;
            border-radius: 12px;
            margin-top: 10px;
            border: 1px solid #e2e8f0;
        }

        .answer-box {
            background: #f7fafc;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            margin-top: 20px;
        }

        .answer-box h3 {
            color: #2d3748;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        .answer-box p {
            color: #4a5568;
            line-height: 1.6;
            font-size: 1rem;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📄 PDF Analysis Tool</h1>
            <p>Analyze your PDF documents with AI-powered question answering</p>
        </div>

        <!-- Step 1: API Configuration -->
        <div class="step active" id="step1">
            <div class="step-header">
                <div class="step-number">1</div>
                <div class="step-title">Configure AI Models</div>
            </div>
            
            <!-- Model Selection -->
            <div class="input-group">
                <label for="modelSelect">Choose AI Model:</label>
                <select id="modelSelect" onchange="toggleApiInputs()" style="width: 100%; padding: 12px 16px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; background: white;">
                    <option value="huggingface">Hugging Face (RoBERTa)</option>
                    <option value="ibm">IBM Granite (watsonx.ai)</option>
                    <option value="both">Both Models (Compare Results)</option>
                </select>
            </div>

            <!-- Hugging Face API Key -->
            <div class="input-group" id="hfGroup">
                <label for="apiKey">Hugging Face API Key:</label>
                <input type="text" id="apiKey" placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx">
            </div>

            <!-- IBM watsonx.ai Credentials -->
            <div class="input-group hidden" id="ibmGroup">
                <label for="ibmApiKey">IBM Cloud API Key:</label>
                <input type="text" id="ibmApiKey" placeholder="Your IBM Cloud API Key">
                <label for="ibmProjectId" style="margin-top: 10px;">IBM watsonx.ai Project ID:</label>
                <input type="text" id="ibmProjectId" placeholder="Your watsonx.ai Project ID">
                <label for="ibmModel" style="margin-top: 10px;">IBM Model:</label>
                <select id="ibmModel" style="width: 100%; padding: 8px 12px; border: 2px solid #e2e8f0; border-radius: 8px;">
                    <option value="ibm/granite-13b-chat-v2">IBM Granite 13B Chat v2</option>
                    <option value="ibm/granite-13b-instruct-v2">IBM Granite 13B Instruct v2</option>
                    <option value="ibm/granite-20b-multilingual">IBM Granite 20B Multilingual</option>
                </select>
            </div>

            <button class="btn" onclick="verifyApiKeys()">Verify API Configuration</button>
            <div id="apiStatus"></div>
        </div>

        <!-- Step 2: PDF Upload -->
        <div class="step" id="step2">
            <div class="step-header">
                <div class="step-number">2</div>
                <div class="step-title">Upload PDF Document</div>
            </div>
            <div class="input-group">
                <label for="pdfFile">Select PDF File:</label>
                <input type="file" id="pdfFile" accept=".pdf" onchange="handleFileUpload(event)">
            </div>
            <div id="fileInfo"></div>
        </div>

        <!-- Step 3: Question Input -->
        <div class="step" id="step3">
            <div class="step-header">
                <div class="step-number">3</div>
                <div class="step-title">Ask Your Question</div>
            </div>
            <div class="input-group">
                <label for="question">What would you like to know about the document?</label>
                <textarea id="question" placeholder="Enter your question about the PDF content..."></textarea>
            </div>
            <button class="btn" onclick="analyzeDocument()" id="analyzeBtn">Analyze Document</button>
        </div>

        <!-- Step 4: Results -->
        <div class="step" id="step4">
            <div class="step-header">
                <div class="step-number">4</div>
                <div class="step-title">Analysis Results</div>
            </div>
            <div id="analysisResults"></div>
        </div>
    </div>

    <script>
        let apiKey = '';
        let ibmApiKey = '';
        let ibmProjectId = '';
        let ibmModel = 'ibm/granite-13b-chat-v2';
        let ibmAccessToken = '';
        let selectedModel = 'huggingface';
        let pdfText = '';
        let fileName = '';

        // Set up PDF.js worker
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

        function toggleApiInputs() {
            const modelSelect = document.getElementById('modelSelect');
            const hfGroup = document.getElementById('hfGroup');
            const ibmGroup = document.getElementById('ibmGroup');
            selectedModel = modelSelect.value;

            switch(selectedModel) {
                case 'huggingface':
                    hfGroup.classList.remove('hidden');
                    ibmGroup.classList.add('hidden');
                    break;
                case 'ibm':
                    hfGroup.classList.add('hidden');
                    ibmGroup.classList.remove('hidden');
                    break;
                case 'both':
                    hfGroup.classList.remove('hidden');
                    ibmGroup.classList.remove('hidden');
                    break;
            }
        }

        async function verifyApiKeys() {
            const apiStatus = document.getElementById('apiStatus');
            const modelSelect = document.getElementById('modelSelect');
            selectedModel = modelSelect.value;

            let hfValid = false;
            let ibmValid = false;

            // Verify Hugging Face if needed
            if (selectedModel === 'huggingface' || selectedModel === 'both') {
                const apiKeyInput = document.getElementById('apiKey');
                const enteredKey = apiKeyInput.value.trim();

                if (!enteredKey) {
                    showStatus(apiStatus, 'Please enter your Hugging Face API key', 'error');
                    return;
                }

                showStatus(apiStatus, 'Verifying Hugging Face API key...', 'info', true);

                try {
                    const response = await fetch('https://huggingface.co/api/whoami', {
                        headers: {
                            'Authorization': Bearer ${enteredKey}
                        }
                    });

                    if (response.ok) {
                        const data = await response.json();
                        apiKey = enteredKey;
                        hfValid = true;
                        showStatus(apiStatus, ✅ Hugging Face API verified! Welcome, ${data.name || 'User'}, 'success');
                    } else {
                        showStatus(apiStatus, '❌ Invalid Hugging Face API key. Please check and try again.', 'error');
                        return;
                    }
                } catch (error) {
                    showStatus(apiStatus, '❌ Error verifying Hugging Face API key.', 'error');
                    return;
                }
            }

            // Verify IBM watsonx.ai if needed
            if (selectedModel === 'ibm' || selectedModel === 'both') {
                const ibmApiKeyInput = document.getElementById('ibmApiKey');
                const ibmProjectIdInput = document.getElementById('ibmProjectId');
                const ibmModelSelect = document.getElementById('ibmModel');

                const enteredIbmKey = ibmApiKeyInput.value.trim();
                const enteredProjectId = ibmProjectIdInput.value.trim();
                const selectedIbmModel = ibmModelSelect.value;

                if (!enteredIbmKey || !enteredProjectId) {
                    showStatus(apiStatus, 'Please enter IBM Cloud API Key and Project ID', 'error');
                    return;
                }

                showStatus(apiStatus, 'Verifying IBM watsonx.ai credentials...', 'info', true);

                try {
                    // Get IBM Cloud IAM token
                    const tokenResponse = await fetch('https://iam.cloud.ibm.com/identity/token', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: grant_type=urn:iam:grant-type:apikey&apikey=${enteredIbmKey}
                    });

                    if (tokenResponse.ok) {
                        const tokenData = await tokenResponse.json();
                        ibmAccessToken = tokenData.access_token;
                        ibmApiKey = enteredIbmKey;
                        ibmProjectId = enteredProjectId;
                        ibmModel = selectedIbmModel;
                        ibmValid = true;

                        const currentStatus = hfValid ? 
                            'Hugging Face ✅ | IBM Granite ✅ Configuration ready!' : 
                            '✅ IBM watsonx.ai configuration ready!';
                        showStatus(apiStatus, currentStatus, 'success');
                    } else {
                        showStatus(apiStatus, '❌ Invalid IBM Cloud API key. Please check and try again.', 'error');
                        return;
                    }
                } catch (error) {
                    showStatus(apiStatus, '❌ Error verifying IBM credentials.', 'error');
                    return;
                }
            }

            // Proceed to next step if at least one model is configured
            if (hfValid || ibmValid) {
                activateStep('step2');
            }
        }

        async function handleFileUpload(event) {
            const file = event.target.files[0];
            const fileInfo = document.getElementById('fileInfo');

            if (!file) return;

            if (file.type !== 'application/pdf') {
                showStatus(fileInfo, '❌ Please select a PDF file', 'error');
                return;
            }

            fileName = file.name;
            showStatus(fileInfo, 'Extracting text from PDF...', 'info', true);

            try {
                const arrayBuffer = await file.arrayBuffer();
                const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
                let fullText = '';

                for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                    const page = await pdf.getPage(pageNum);
                    const textContent = await page.getTextContent();
                    const pageText = textContent.items.map(item => item.str).join(' ');
                    fullText += pageText + '\n';
                }

                pdfText = fullText.trim();
                
                if (pdfText.length === 0) {
                    showStatus(fileInfo, '❌ No text found in PDF. The document might be image-based.', 'error');
                    return;
                }

                const wordCount = pdfText.split(/\s+/).length;
                showStatus(fileInfo, `✅ PDF processed successfully! 
                    <div class="file-info">
                        <strong>File:</strong> ${fileName}<br>
                        <strong>Pages:</strong> ${pdf.numPages}<br>
                        <strong>Words:</strong> ${wordCount.toLocaleString()}
                    </div>`, 'success');
                
                activateStep('step3');
            } catch (error) {
                showStatus(fileInfo, '❌ Error processing PDF. Please try another file.', 'error');
            }
        }

        async function analyzeDocument() {
            const question = document.getElementById('question').value.trim();
            const analysisResults = document.getElementById('analysisResults');
            const analyzeBtn = document.getElementById('analyzeBtn');

            if (!question) {
                alert('Please enter a question about the document.');
                return;
            }

            analyzeBtn.disabled = true;
            showStatus(analysisResults, 'Analyzing document with selected AI model(s)...', 'info', true);
            activateStep('step4');

            let results = [];

            try {
                // Analyze with Hugging Face if selected
                if ((selectedModel === 'huggingface' || selectedModel === 'both') && apiKey) {
                    const hfResult = await analyzeWithHuggingFace(question);
                    results.push({
                        model: 'Hugging Face (RoBERTa)',
                        ...hfResult
                    });
                }

                // Analyze with IBM Granite if selected
                if ((selectedModel === 'ibm' || selectedModel === 'both') && ibmAccessToken) {
                    const ibmResult = await analyzeWithIBMGranite(question);
                    results.push({
                        model: IBM ${ibmModel.split('/')[1]} (watsonx.ai),
                        ...ibmResult
                    });
                }

                // Display results
                displayResults(results, question);

            } catch (error) {
                console.error('Analysis error:', error);
                showStatus(analysisResults, ❌ Error during analysis: ${error.message}. Please try again., 'error');
            } finally {
                analyzeBtn.disabled = false;
            }
        }

        async function analyzeWithHuggingFace(question) {
            try {
                const response = await fetch('https://api-inference.huggingface.co/models/deepset/roberta-base-squad2', {
                    method: 'POST',
                    headers: {
                        'Authorization': Bearer ${apiKey},
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        inputs: {
                            question: question,
                            context: pdfText.substring(0, 10000) // Limit context due to model constraints
                        }
                    })
                });

                if (!response.ok) {
                    throw new Error(Hugging Face API request failed: ${response.status});
                }

                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }

                return {
                    answer: result.answer || 'No specific answer found in the document.',
                    confidence: result.score ? (result.score * 100).toFixed(1) : 'N/A',
                    success: true
                };
            } catch (error) {
                return {
                    answer: Error: ${error.message},
                    confidence: '0',
                    success: false
                };
            }
        }

        async function analyzeWithIBMGranite(question) {
            try {
                // Prepare the document context (limit to prevent token overflow)
                const contextLimit = 4000; // Adjust based on model's context window
                const documentContext = pdfText.substring(0, contextLimit);
                
                // Create a comprehensive prompt for the IBM Granite model
                const prompt = `Based on the following document content, please answer the question accurately and concisely.

Document Content:
${documentContext}

Question: ${question}

Please provide a detailed answer based only on the information in the document. If the answer is not in the document, please state that clearly.

Answer:`;

                // Call IBM watsonx.ai API
                const response = await fetch('https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'Authorization': Bearer ${ibmAccessToken}
                    },
                    body: JSON.stringify({
                        input: prompt,
                        parameters: {
                            decoding_method: "greedy",
                            max_new_tokens: 500,
                            min_new_tokens: 10,
                            stop_sequences: [],
                            repetition_penalty: 1.05
                        },
                        model_id: ibmModel,
                        project_id: ibmProjectId
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(IBM API request failed: ${response.status} - ${errorData.message || 'Unknown error'});
                }

                const result = await response.json();
                
                if (result.results && result.results[0] && result.results[0].generated_text) {
                    const generatedText = result.results[0].generated_text.trim();
                    
                    // Calculate confidence based on response quality
                    let confidence = 75; // Base confidence for IBM Granite
                    if (generatedText.length > 50) confidence += 10;
                    if (generatedText.toLowerCase().includes('based on the document')) confidence += 10;
                    if (!generatedText.toLowerCase().includes('not in the document')) confidence += 5;
                    
                    return {
                        answer: generatedText,
                        confidence: Math.min(confidence, 95).toString(),
                        success: true,
                        tokens_used: result.results[0].input_token_count + result.results[0].generated_token_count
                    };
                } else {
                    throw new Error('No generated text in response');
                }

            } catch (error) {
                console.error('IBM Granite analysis error:', error);
                return {
                    answer: Error: ${error.message},
                    confidence: '0',
                    success: false
                };
            }
        }

        function displayResults(results, question) {
            const analysisResults = document.getElementById('analysisResults');
            
            let html = `<div class="answer-box">
                <h3>📋 Analysis Results</h3>
                <p><strong>Question:</strong> ${question}</p>
                <p><strong>Source:</strong> ${fileName}</p>
                <hr style="margin: 20px 0; border: none; border-top: 1px solid #e2e8f0;">
            `;

            results.forEach((result, index) => {
                const statusIcon = result.success ? '✅' : '❌';
                const modelColor = result.model.includes('Hugging Face') ? '#ff6b6b' : '#1f77b4';
                
                html += `
                    <div style="margin-bottom: 25px; padding: 15px; border-left: 4px solid ${modelColor}; background: #f8f9fa;">
                        <h4 style="color: ${modelColor}; margin-bottom: 10px;">${statusIcon} ${result.model}</h4>
                        <p><strong>Answer:</strong> ${result.answer}</p>
                        <p><strong>Confidence:</strong> ${result.confidence}%</p>
                        ${result.tokens_used ? <p><strong>Tokens Used:</strong> ${result.tokens_used}</p> : ''}
                        ${result.note ? <p><em>${result.note}</em></p> : ''}
                    </div>
                `;
            });

            if (results.length > 1) {
                const avgConfidence = results.reduce((sum, r) => sum + parseFloat(r.confidence || 0), 0) / results.length;
                html += `
                    <div style="text-align: center; padding: 15px; background: #e8f4f8; border-radius: 8px; margin-top: 20px;">
                        <strong>🤖 Model Comparison Complete</strong><br>
                        Average Confidence: ${avgConfidence.toFixed(1)}%
                    </div>
                `;
            }

            html += '</div>';
            analysisResults.innerHTML = html;
        }

        function showStatus(element, message, type, loading = false) {
            const loadingSpinner = loading ? '<span class="loading"></span>' : '';
            element.innerHTML = <div class="status ${type}">${loadingSpinner}${message}</div>;
        }

        function activateStep(stepId) {
            document.querySelectorAll('.step').forEach(step => {
                step.classList.remove('active');
            });
            document.getElementById(stepId).classList.add('active');
        }
    </script>
</body>
</html>
















