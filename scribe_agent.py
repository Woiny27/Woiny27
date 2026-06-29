import ollama

# Tool definition for medical dictionary lookup
def medical_lookup(term):
    # Simulates an offline Wikipedia/Medical DB lookup
    medical_db = {
        "dyspnea": "Difficult or labored breathing; shortness of breath.",
        "tachycardia": "Abnormally rapid heart rate, typically over 100 bpm.",
        "hypertension": "Persistently elevated blood pressure in the arteries.",
        "bradycardia": "Abnormally slow heart rate, typically below 60 bpm.",
        "edema": "Swelling caused by excess fluid trapped in body tissues.",
    }
    return medical_db.get(term.lower(), f"Definition for {term}: [Retrieved from local medical database]")

# Agentic tool registry
tools = {
    "medical_lookup": medical_lookup,
}

# Agent loop using Gemma 4 Thinking Mode logic
def run_agent(prompt):
    print(f"\n🚀 Agent received task: {prompt}\n")

    # Step 1: Identify medical terms to look up
    terms_response = ollama.chat(model='gemma4:e4b', messages=[
        {'role': 'system', 'content': 'You are a medical AI agent. Extract key medical terms from the prompt that need definition. Return only a comma-separated list of terms.'},
        {'role': 'user', 'content': prompt}
    ])
    
    raw_content = terms_response['message']['content']
    terms = raw_content.split(',')
    print(f"🔍 Terms identified: {terms}")

    # Step 2: Execute tool calls for each term
    context = ""
    for term in terms:
        term = term.strip()
        if term: # Ensure it's not an empty string
            definition = medical_lookup(term)
            context += f"\n- {term}: {definition}"
            print(f"⚙️ Looked up '{term}': {definition}")

    # Step 3: Generate final enriched summary
    final_response = ollama.chat(model='gemma4:e4b', messages=[
        {'role': 'system', 'content': 'You are a professional medical scribe with access to a medical dictionary.'},
        {'role': 'user', 'content': f'{prompt}\n\nUse these definitions as context:{context}\n\nGenerate a complete SOAP note.'}
    ])
    return final_response['message']['content']

# Example usage
if __name__ == "__main__":
    prompt = "Analyze the term 'Dyspnea' and include its definition in the patient's summary."
    result = run_agent(prompt)
    print(f"\n📋 Final SOAP Note:\n{result}")
