import re
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Choose a model
model_name = "EleutherAI/gpt-neo-1.3B"
# model_name = "EleutherAI/gpt-neo-125M"

# Load the tokenizer and model explicitly using PyTorch
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create the pipeline (using GPU if available, device=0)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, framework="pt", device=0)

def extract_keywords(abstract):
    """
    Given an abstract, returns the extracted keywords as a list.
    """
    prompt = (
        "I want to get the keywords from an abstract. Here is an example.\n"
        "Example:\n"
        "Abstract: \"Natural language processing enables computers to understand human language.\"\n"
        "Keywords: natural language processing, computers, human language\n\n"
        "Now, based on the example above, extract 2 to 5 key keywords from the following abstract. "
        "Provide only a comma-separated list of keywords. Do not generate any additional examples, abstract, text, or explanations. "
        "I only want the final list of 2 to 5 keywords.\n\n"
        f"Abstract: \"{abstract}\"\n\n"
        "Keywords:"
    )

    result = generator(prompt, max_new_tokens=50, num_return_sequences=1, temperature=0.4, top_p=0.9)
    output_text = result[0]['generated_text']

    # Post-processing: extract text after the last occurrence of "Keywords:"
    matches = re.findall(r'Keywords:\s*(.*)', output_text, re.IGNORECASE)
    if matches:
        keywords_str = matches[-1].strip().split("\n")[0]
        # Split the comma-separated list and remove duplicates while preserving order
        keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
        seen = set()
        unique_keywords = []
        for kw in keywords:
            lower_kw = kw.lower()
            if lower_kw not in seen:
                seen.add(lower_kw)
                unique_keywords.append(lower_kw)
        return unique_keywords
    else:
        return []