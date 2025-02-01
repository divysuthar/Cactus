import spacy
from transformers import BartForConditionalGeneration, BartTokenizer
from pdfminer.high_level import extract_text
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
from ..views import summaries, prompts, filtered_prompts


nlp = spacy.load("en_core_web_sm")

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


# Function to summarize text using a transformer model
def summarize_text(text, max_input_length=1024, max_output_length=150):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=max_input_length,
        truncation=True,
        padding=True,
    )
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_output_length,
        num_beams=4,
        early_stopping=True,
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


# Function to extract key sections from the paper
def extract_sections_from_text(text):
    sections = {
        "abstract": "",
        "introduction": "",
        "methodology": "",
        "results": "",
    }

    lower_text = text.lower()

    abstract_start = lower_text.find("abstract")
    introduction_start = lower_text.find("introduction")
    methodology_start = lower_text.find("methodology")
    results_start = lower_text.find("results")
    conclusion_start = lower_text.find("conclusion")

    if abstract_start != -1:
        abstract_end = introduction_start if introduction_start != -1 else len(text)
        sections["abstract"] = text[abstract_start:abstract_end].strip()

    if introduction_start != -1:
        introduction_end = methodology_start if methodology_start != -1 else len(text)
        sections["introduction"] = text[introduction_start:introduction_end].strip()

    if methodology_start != -1:
        methodology_end = results_start if results_start != -1 else len(text)
        sections["methodology"] = text[methodology_start:methodology_end].strip()

    if results_start != -1:
        results_end = conclusion_start if conclusion_start != -1 else len(text)
        sections["results"] = text[results_start:results_end].strip()

    return sections


def extract_numerical_metrics(text):
    doc = nlp(text)
    metrics = []

    # Extract numerical entities from the text
    for ent in doc.ents:
        if ent.label_ == "CARDINAL" or ent.label_ == "PERCENT":
            metrics.append(ent.text)

    return metrics


def create_prompts_from_summary(summary):
    # Split summary by period and strip leading/trailing whitespace from each sentence
    sentences = [
        sentence.strip() for sentence in summary.split(".") if sentence.strip()
    ]
    # Return the sentences as individual prompts in an array
    return sentences


# Main function to process the research paper and generate summaries
def process_research_paper_without_metrics(pdf_path):
    paper_text = extract_text_from_pdf(pdf_path)

    # Extract sections from the paper dynamically
    sections = extract_sections_from_text(paper_text)

    summaries = {}
    prompts = []  # List to store individual sentence prompts

    # Summarize each section if present
    for section, text in sections.items():
        if text:
            section_summary = summarize_text(text)
            summaries[f"{section}_summary"] = section_summary
            section_prompts = create_prompts_from_summary(section_summary)
            prompts.extend(section_prompts)
        else:
            summaries[f"{section}_summary"] = f"No {section} found."

    combined_text = sections["results"] + " " + sections["methodology"]
    numerical_metrics = extract_numerical_metrics(combined_text)

    if numerical_metrics:
        summaries["results_summary"] = summaries["results_summary"].replace(
            f" Key metrics extracted: {', '.join(numerical_metrics)}.", ""
        )
    else:
        summaries["results_summary"] = "No numerical metrics detected."

    summaries["numerical_metrics"] = (
        numerical_metrics if numerical_metrics else "No numerical metrics found."
    )

    return summaries, prompts


# Function to filter prompts based on length
def filter_short_prompts(prompts, min_length=5):
    filtered_prompts = [
        prompt for prompt in prompts if len(prompt.split()) >= min_length
    ]
    return filtered_prompts

print("Abstract Summary:", summaries["abstract_summary"])
print("Introduction Summary:", summaries["introduction_summary"])
print("Methodology Summary:", summaries["methodology_summary"])
print("Results Summary:", summaries["results_summary"])
print("Extracted Numerical Metrics:", summaries["numerical_metrics"])


# Print the generated prompts
print("\nGenerated Prompts:")
print(filtered_prompts)


from diffusers import StableDiffusionPipeline, AutoPipelineForText2Image
import torch
import os


def generate_images(prompts, folder_name="generated_images"):
    """Generate multiple im_ages from a list of text prompts and save them in a folder."""
    model_id = "runwayml/stable-diffusion-v1-5"  # Smaller model for faster generation
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    # Create folder to store images
    os.makedirs(folder_name, exist_ok=True)

    # Generate and save images
    for i, prompt in enumerate(prompts):
        image = pipe(prompt).images[0]
        image_path = os.path.join(folder_name, f"image_{i+1}.png")
        image.save(image_path)
        print(f"Saved: {image_path}")


def create_text_images(
    prompts,
    font_path="../Arial.ttf",
    font_size=60,
    output_folder="generated_images2",
):
    """Generate images from a list of text prompts with customizable font and size."""
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i, prompt in enumerate(prompts):
        # Create a new image with white background
        image = Image.new("RGB", (800, 600), color="white")
        draw = ImageDraw.Draw(image)

        # Load the specified font and size
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            print(f"Font at {font_path} not found. Using default font.")
            font = ImageFont.load_default()

        # Wrap the text to fit within the image width
        max_width = image.width - 40 
        wrapped_text = textwrap.fill(prompt, width=max_width // (font_size // 2))

        # Calculate text size and position to center the text
        lines = wrapped_text.split("\n")
        text_height = sum([font.getsize(line)[1] for line in lines])
        y_offset = (image.height - text_height) // 2

        # Add wrapped text to the image
        for line in lines:
            text_width, text_height = draw.textsize(line, font=font)
            x_offset = (image.width - text_width) // 2
            draw.text((x_offset, y_offset), line, font=font, fill="black")
            y_offset += text_height

        # Save the image
        image_path = os.path.join(output_folder, f"slide_{i+1}.png")
        image.save(image_path)
        print(f"Saved: {image_path}")


if __name__ == "__main__":
    prompts_img = filtered_prompts  # Use the filtered
    generate_images(prompts_img)
    create_text_images(
        prompts_img,
        font_path="../Arial.ttf",
        font_size=60,
        output_folder="generated_images2",
    )
