import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings

from .LLM.image_generator import (
    process_research_paper_without_metrics,
    generate_images,
    create_text_images,
)
from .LLM.text_speech import run_voiceover_generation
from .LLM.merge_making_video import create_video


@api_view(["POST"])
def research_paper_upload(request):
    if "file" not in request.FILES:
        return Response(
            {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
        )

    pdf_file = request.FILES["file"]
    if not pdf_file.name.lower().endswith(".pdf"):
        return Response(
            {"error": "Invalid file type. Only PDF files are accepted."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    # Save the uploaded file to a designated folder
    upload_path = os.path.join(upload_dir, pdf_file.name)
    file_path = default_storage.save(upload_path, pdf_file)
    absolute_file_path = default_storage.path(file_path)

    # Process the research paper
    summaries, prompts = process_research_paper_without_metrics(absolute_file_path)

    # Filter prompts that have at least 5 words
    filtered_prompts = [prompt for prompt in prompts if len(prompt.split()) >= 5]

    # Generate images
    generate_images(filtered_prompts)
    create_text_images(
        filtered_prompts,
        font_path=r"..\Arial.ttf",
        font_size=60,
        output_folder="generated_images2",
    )

    response_data = {
        "summaries": summaries,
        "prompts": filtered_prompts,
        "message": "Processing complete!",
    }

    run_voiceover_generation(language='en', accent_type='com', slow_speed=False)
    create_video()

    return Response(response_data, status=status.HTTP_200_OK)
