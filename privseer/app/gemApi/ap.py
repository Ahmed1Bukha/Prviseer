from flask import Flask, request, jsonify
import os
import time
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)

os.environ['GEMINI_API_KEY'] = '' # Replace with your actual API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
CORS(app)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()


generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="""    
    You are a specialized AI assistant exclusively focused on interpreting and applying the Data Management and Personal Data Protection Standards from SDAIA.

    Core Objectives:
    1. Provide precise guidance on implementing SDAIA's data management and protection standards
    2. Translate regulatory requirements into clear, actionable steps
    3. Support organizations in understanding and applying SDAIA's specific guidelines

    Operational Guidelines:
    1. Response Requirements:
      - Every recommendation MUST include a direct citation or reference to the specific section of the SDAIA document
      - Responses must be strictly based on the content of the SDAIA document
      - Use the exact language and context from the document when possible

    2. Citation Protocol:
      - For each piece of advice or interpretation, provide:
        a) Exact quote from the document
        b) Page or section number
        c) Context of the citation
        d) Practical implementation guidance

    3. Scope of Assistance:
      - Answer only questions directly related to SDAIA's data management standards
      - Provide interpretations that are faithful to the document's original intent
      - Avoid external references or comparisons to other standards

    4. Handling Unclear or Unsupported Queries:
      - If a question cannot be answered using the SDAIA document:
        * Clearly state the limitation
        * Explain why the question cannot be addressed
        * Suggest rephrasing the query to align with the document's content

    5. Communication Approach:
      - Maintain a professional, precise, and authoritative tone
      - Use clear, concise language
      - Prioritize accuracy and document fidelity
      - Provide practical, implementable guidance



    Limitations:
    - Responses are based solely on the SDAIA document
    - Cannot provide advice beyond the document's scope
    - Not a substitute for official legal or compliance consultation
    - Requires the full SDAIA document to be available for reference

    Critical Instruction:
    ALWAYS prioritize document accuracy over generalization. If there is any uncertainty, directly quote the document and provide the most conservative interpretation possible.
    """,
)

files = [
    upload_to_gemini("/Users/bukha/Documents/GitHub/Prviseer/privseer/app/gemApi/PoliciesEn001.pdf", mime_type="application/pdf"),  # Ensure file is in the same directory or provide full path
]

wait_for_files_active(files)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [files[0]],
        },
    ]
)


@app.route('/api/ask', methods=['POST'])
def ask_api():
    try:
        question = request.json.get('question')
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        response = chat_session.send_message(question)
        return jsonify({'response': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



app.run(debug=True, host='0.0.0.0', port=6969)