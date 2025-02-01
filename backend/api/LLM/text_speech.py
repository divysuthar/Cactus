from .image_generator import filtered_prompts  # Make sure the relative import is valid

from gtts import gTTS
import os

# Function to generate voiceover
def generate_voiceover(text, lang='en', accent='com', slow=False, file_path='voiceover.mp3'):
    tts = gTTS(text=text, lang=lang, slow=slow, tld=accent)
    tts.save(file_path)
    print(f"Voiceover saved as {file_path}")


def run_voiceover_generation(language='en', accent_type='com', slow_speed=False):
    # List of prompts
    prompts = filtered_prompts
    
    # Input preferences
    language = input("Enter language code (default: 'en'): ") or 'en'
    accent_type = input("Enter accent type (com for common, us for US, uk for UK): ") or 'com'
    speed = input("Should the speech be slow (yes/no)? ").strip().lower()
    
    # Convert 'yes' to True, 'no' to False
    slow_speed = speed == 'yes'
    
    # Define the output folder
    output_folder = 'voiceovers2'
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Loop through each prompt and generate a voiceover individually
    for i, prompt in enumerate(prompts, start=1):
        file_name = f"voiceover_{i}.mp3"
        file_path = os.path.join(output_folder, file_name)
        generate_voiceover(prompt, lang=language, accent=accent_type, slow=slow_speed, file_path=file_path)