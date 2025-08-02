import requests
import time

# 🔐 Replace this with your Hugging Face API Token
API_TOKEN = "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"
API_URL = "https://huggingface.co/bartowski/ibm-granite_granite-vision-3.2-2b-GGUF"



headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_answer(context, question):
    if not context or not question:
        return "⚠️ Missing context or question"
    
    # Truncate context if too long
    if len(context) > 2000:
        context = context[:2000] + "..."
    
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.3},
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 503:
            time.sleep(10)
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            return f"⚠️ API Error: {response.status_code}"
        
        result = response.json()
        
        if isinstance(result, list) and "generated_text" in result[0]:
            answer = result[0]["generated_text"].strip()
        elif isinstance(result, dict) and "generated_text" in result:
            answer = result["generated_text"].strip()
        elif "error" in (result[0] if isinstance(result, list) else result):
            return "⚠️ Model error"
        else:
            return "⚠️ Unexpected response"
        
        # Clean answer
        answer = answer.replace("Answer:", "").strip()
        return answer if len(answer) > 10 else "⚠️ No meaningful answer generated"
        
    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"



# import requests
# import time

# # 🔐 Replace this with your Hugging Face API Token
# API_TOKEN = "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"

# # Use a working model for text generation
# API_URL = "https://api-inference.huggingface.co/models/ibm-watsonx/mixtral-8x7b-instruct-v01-q"

# headers = {
#     "Authorization": f"Bearer {API_TOKEN}",
#     "Content-Type": "application/json"
# }

# def generate_answer(context, question):
#     if not context or not question:
#         return "⚠️ Missing context or question"
    
#     # Truncate context if too long
#     if len(context) > 1500:
#         context = context[:1500] + "..."
    
#     # Format prompt for T5 model
#     prompt = f"Answer the question based on the context.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 150,
#             "temperature": 0.3,
#             "do_sample": True
#         },
#         "options": {
#             "wait_for_model": True
#         }
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
#         # Handle model loading
#         if response.status_code == 503:
#             time.sleep(15)
#             response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
#         if response.status_code != 200:
#             return f"⚠️ API Error: {response.status_code}"
        
#         result = response.json()
        
#         # Handle response format
#         if isinstance(result, list) and len(result) > 0:
#             if "generated_text" in result[0]:
#                 answer = result[0]["generated_text"]
#             else:
#                 return "⚠️ Unexpected response format"
#         elif isinstance(result, dict) and "generated_text" in result:
#             answer = result["generated_text"]
#         else:
#             return "⚠️ No answer generated"
        
#         # Clean the answer
#         answer = answer.replace(prompt, "").strip()
#         answer = answer.replace("Answer:", "").strip()
        
#         return answer if len(answer) > 5 else "⚠️ Could not generate a meaningful answer"
        
#     except Exception as e:
#         return f"⚠️ Request failed: {str(e)}"

