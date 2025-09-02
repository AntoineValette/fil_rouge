import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Use the model Flan-T5-small
model_name = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Determine the device: for model.to(), use torch.device("cuda:0") if available, otherwise "cpu"
if torch.cuda.is_available():
    device_id = 0  # for the pipeline
    device = torch.device("cuda:0")
else:
    device_id = -1  # for the pipeline (CPU)
    device = torch.device("cpu")

model.to(device)

# Create the pipeline (device parameter expects -1 for CPU and 0 for GPU)
generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=device_id)

# Define the abstract (long text)
abstract = (
    "Automated melanoma recognition in dermoscopy images is a very challenging task due to the low contrast of skin lesions, "
    "the huge intraclass variation of melanomas, the high degree of visual similarity between melanoma and non-melanoma lesions, "
    "and the existence of many artifacts in the image. In order to meet these challenges, we propose a novel method for melanoma "
    "recognition by leveraging very deep convolutional neural networks (CNNs). Compared with existing methods employing either "
    "low-level hand-crafted features or CNNs with shallower architectures, our substantially deeper networks (more than 50 layers) "
    "can acquire richer and more discriminative features for more accurate recognition. To take full advantage of very deep networks, "
    "we propose a set of schemes to ensure effective training and learning under limited training data. First, we apply the residual "
    "learning to cope with the degradation and overfitting problems when a network goes deeper. This technique can ensure that our "
    "networks benefit from the performance gains achieved by increasing network depth. Then, we construct a fully convolutional "
    "residual network (FCRN) for accurate skin lesion segmentation, and further enhance its capability by incorporating a multi-scale "
    "contextual information integration scheme. Finally, we seamlessly integrate the proposed FCRN (for segmentation) and other very deep "
    "residual networks (for classification) to form a two-stage framework. This framework enables the classification network to extract "
    "more representative and specific features based on segmented results instead of the whole dermoscopy images, further alleviating the "
    "insufficiency of training data. The proposed framework is extensively evaluated on ISBI 2016 Skin Lesion Analysis Towards Melanoma "
    "Detection Challenge dataset. Experimental results demonstrate the significant performance gains of the proposed framework, ranking the "
    "first in classification and the second in segmentation among 25 teams and 28 teams, respectively. This study corroborates that very "
    "deep CNNs with effective training mechanisms can be employed to solve complicated medical image analysis tasks, even with limited training data."
)

# Set maximum prompt tokens
max_prompt_length = 512

# Define prompt parts: instructions are kept intact, only the abstract is subject to truncation
prompt_prefix = (
    "Extract 2 to 5 key keywords from the following abstract. Provide only a comma-separated list of keywords. "
    "Do not generate any additional text or explanations. Your answer should start with 'Keywords:' followed by the list.\n\n"
    "Abstract: \""
)
prompt_suffix = "\"\n\nKeywords:"

# Compute token lengths for prefix and suffix
prefix_tokens = tokenizer(prompt_prefix, add_special_tokens=False)['input_ids']
suffix_tokens = tokenizer(prompt_suffix, add_special_tokens=False)['input_ids']
available_tokens = max_prompt_length - len(prefix_tokens) - len(suffix_tokens)

# Tokenize the abstract and truncate if needed
abstract_tokens = tokenizer(abstract, add_special_tokens=False)['input_ids']
if len(abstract_tokens) > available_tokens:
    abstract_tokens = abstract_tokens[:available_tokens]
abstract_truncated = tokenizer.decode(abstract_tokens, skip_special_tokens=True)

# Build the final prompt
final_prompt = prompt_prefix + abstract_truncated + prompt_suffix

# Tokenize final prompt ensuring it is within max_prompt_length
inputs = tokenizer(final_prompt, return_tensors="pt", truncation=True, max_length=max_prompt_length)
inputs = inputs.to(device)

# Generate output with sampling enabled
outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=True,
    temperature=0.4,
    top_p=0.9
)
output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Post-processing: extract the text after the last occurrence of "Keywords:"
if "Keywords:" in output_text:
    matches = re.findall(r'Keywords:\s*(.*)', output_text, re.IGNORECASE)
    final_text = matches[-1].strip()
else:
    final_text = output_text.strip()

# Split by comma and remove duplicates while preserving order
keywords = [kw.strip() for kw in final_text.split(',') if kw.strip()]
seen = set()
unique_keywords = []
for kw in keywords:
    lower_kw = kw.lower()
    if lower_kw not in seen:
        seen.add(lower_kw)
        unique_keywords.append(kw)

print("Extracted Keywords:", unique_keywords)
print("\nFull Generated Text:\n", output_text)