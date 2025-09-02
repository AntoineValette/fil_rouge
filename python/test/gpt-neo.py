import re
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Choose a model
model_name = "EleutherAI/gpt-neo-1.3B"
#model_name = "EleutherAI/gpt-neo-125M"

# Load the tokenizer and model explicitly using PyTorch
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create the pipeline (using the GPU if available, device=0)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, framework="pt", device=0)

# Define your abstract
abstract = (
    "Automated melanoma recognition in dermoscopy images is a very challenging task due to the low contrast "
    "of skin lesions, the huge intraclass variation of melanomas, the high degree of visual similarity between "
    "melanoma and non-melanoma lesions, and the existence of many artifacts in the image. In order to meet these "
    "challenges, we propose a novel method for melanoma recognition by leveraging very deep convolutional neural "
    "networks (CNNs). Compared with existing methods employing either low-level hand-crafted features or CNNs with "
    "shallower architectures, our substantially deeper networks (more than 50 layers) can acquire richer and more "
    "discriminative features for more accurate recognition. To take full advantage of very deep networks, we propose a "
    "set of schemes to ensure effective training and learning under limited training data. First, we apply the residual "
    "learning to cope with the degradation and overfitting problems when a network goes deeper. This technique can ensure "
    "that our networks benefit from the performance gains achieved by increasing network depth. Then, we construct a "
    "fully convolutional residual network (FCRN) for accurate skin lesion segmentation, and further enhance its capability "
    "by incorporating a multi-scale contextual information integration scheme. Finally, we seamlessly integrate the proposed "
    "FCRN (for segmentation) and other very deep residual networks (for classification) to form a two-stage framework. This "
    "framework enables the classification network to extract more representative and specific features based on segmented "
    "results instead of the whole dermoscopy images, further alleviating the insufficiency of training data. The proposed "
    "framework is extensively evaluated on ISBI 2016 Skin Lesion Analysis Towards Melanoma Detection Challenge dataset. "
    "Experimental results demonstrate the significant performance gains of the proposed framework, ranking the first in "
    "classification and the second in segmentation among 25 teams and 28 teams, respectively. This study corroborates that "
    "very deep CNNs with effective training mechanisms can be employed to solve complicated medical image analysis tasks, "
    "even with limited training data."
)

# Improved prompt with clear examples and explicit instructions to return 2-5 keywords.
prompt = (
    "I want to get the keywords from an abstract. Here is an example.\n"
    "Example:\n"
    "Abstract: \"Natural language processing enables computers to understand human language.\"\n"
    "Keywords: natural language processing, computers, human language\n\n"
    "Now, based on the example above, extract 2 to 5 key keywords from the following abstract. Provide only a comma-separated list of keywords. Do not generate any additional examples, abstract, text, or explanations. I only want the final list of 2 to 5 keywords.\n\n"
    f"Abstract: \"{abstract}\"\n\n"
    "Keywords:"
)

# Generate output using adjusted parameters
result = generator(prompt, max_new_tokens=50, num_return_sequences=1, temperature=0.4, top_p=0.9)
output_text = result[0]['generated_text']

# Post-processing: extract text after the last occurrence of the "Keywords:" marker
matches = re.findall(r'Keywords:\s*(.*)', output_text, re.IGNORECASE)
if matches:
    keywords_str = matches[-1].strip()  # Take the last match as the final answer
    # If the model generates extra text after the keywords, split at the first newline
    keywords_str = keywords_str.split("\n")[0]
    # Split the comma-separated list and remove duplicates while preserving order
    keywords = [kw.strip() for kw in keywords_str.split(',') if kw.strip()]
    seen = set()
    unique_keywords = []
    for kw in keywords:
        lower_kw = kw.lower()
        if lower_kw not in seen:
            seen.add(lower_kw)
            unique_keywords.append(kw)
    print("Extracted Keywords:", unique_keywords)
else:
    print("Could not extract keywords from the output.")

#print("\nFull Generated Text:\n", output_text)