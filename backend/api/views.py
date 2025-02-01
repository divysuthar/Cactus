# from rest_framework.response import Response
# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser

# # from rest_framework import status
# from .serializers import *
# # from PyPDF2 import PdfReader

# # # Create your views here.


# # @api_view(["POST"])
# # @parser_classes([MultiPartParser, FormParser])
# # def FileUpload(request):
# #     if request.method == "POST":
# #         file = request.FILES["file"]
# #         file_type = file.content_type
# #         try:
# #             file_content = None

# #             if file_type == "text/plain":
# #                 file_content = file.read().decode("utf-8")

# #             elif file_type == "application/pdf":
# #                 reader = PdfReader(file)
# #                 file_content = "\n".join(
# #                     [
# #                         page.extract_text()
# #                         for page in reader.pages
# #                         if page.extract_text()
# #                     ]
# #                 )

# #             else:
# #                 return Response(
# #                     {"error": "Unsupported file type"},
# #                     status=status.HTTP_400_BAD_REQUEST,
# #                 )
# #             file_content = file_content.split("\n")
# #             print("File Content:\n", file_content)

# #             file_serializer = FileSerializer(data={"file": file})
# #             if file_serializer.is_valid():
# #                 file_serializer.save()
# #                 return Response(
# #                     {"message": "File uploaded successfully", "content": file_content},
# #                     status=status.HTTP_201_CREATED,
# #                 )
# #             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #         except UnicodeDecodeError:
# #             return Response("Invalid file type", status=status.HTTP_400_BAD_REQUEST)


# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from PyPDF2 import PdfReader
# import fitz  # PyMuPDF
# from io import BytesIO
# from PIL import Image
# from .serializers import FileSerializer
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser


# @api_view(["POST"])
# @parser_classes([MultiPartParser, FormParser])
# def FileUpload(request):
#     if request.method == "POST":
#         file = request.FILES.get("file")
#         if not file:
#             return Response(
#                 {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         file_type = file.content_type
#         file_content = None
#         images = []  # List to store extracted images
#         file_data = file.read()  # Read the file content once to reuse

#         try:
#             if file_type == "text/plain":
#                 # Handling plain text file
#                 file_content = file_data.decode("utf-8")

#             elif file_type == "application/pdf":
#                 # Handling PDF files
#                 # Extract text from PDF using PyPDF2
#                 reader = PdfReader(BytesIO(file_data))  # Using the byte stream
#                 text = []
#                 for page in reader.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         text.append(page_text)
#                 file_content = "\n".join(text)  # Combine text from all pages

#                 # Extract images from PDF using PyMuPDF (fitz)
#                 pdf_document = fitz.open(
#                     stream=BytesIO(file_data), filetype="pdf"
#                 )  # Use the stream argument to read from BytesIO
#                 for page_num in range(pdf_document.page_count):
#                     page = pdf_document.load_page(page_num)
#                     for img in page.get_images(full=True):
#                         xref = img[0]
#                         base_image = pdf_document.extract_image(xref)
#                         image_bytes = base_image["image"]  # Get the image in bytes

#                         # Open the image using Pillow
#                         image = Image.open(BytesIO(image_bytes))
#                         image_content = f"Image {page_num + 1} - {image.format} ({image.size[0]}x{image.size[1]})"
#                         images.append(image_content)  # Save image info

#             else:
#                 return Response(
#                     {"error": "Unsupported file type"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             # If there were images, return image info
#             # if images:
#             #     print("Extracted Images: ", images)

#             # Return the content (text and images info)
#             print(file_content.split("\n") if file_content else None)
#             return Response(
#                 {
#                     "message": "File uploaded successfully",
#                     "content": file_content.split("\n") if file_content else None,
#                     "images": images,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# @api_view(["GET"])
# def TestAPI(request):
#     import subprocess
#     subprocess.run([r'C:\Users\divys\OneDrive\Desktop\MINeD\.venv\Scripts\python.exe', r'C:\Users\divys\OneDrive\Desktop\MINeD\backend\LLM\Image_video.py'], check=True)

#     return Response({"message": "API is working!"})


# views.py
# import requests
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import DocumentFileSerializer

# @api_view(['POST'])
# def summarize_document(request):
#     # Validate the file input using the serializer
#     serializer = DocumentFileSerializer(data=request.data)

#     if serializer.is_valid():
#         # Get the uploaded file from the request
#         uploaded_file = serializer.validated_data['file']

#         # Define the API endpoint and token
#         url = 'https://api.apyhub.com/ai/summarize-documents/file'
#         token = 'APY0szeCFi1TfheASNtYbNMivFQAYBCV1p2A2x8zYbMZ0CkdbXpFOAno4zF3JIx3gclgqhPDs'  # Replace with your actual API token

#         # Prepare the headers for the request
#         headers = {
#             'apy-token': token,
#             'Content-Type': 'application/json',
#         }

#         # Prepare the file to be sent in the POST request
#         files = {
#             'file': uploaded_file
#         }

#         # Send the POST request to the external API
#         response = requests.post(url, headers=headers, files=files)

#         # Check if the request was successful
#         if response.status_code == 200:
#             # If the response is JSON, return it
#             return Response(response.json(), status=status.HTTP_200_OK)
#         else:
#             # Handle error
#             return Response({'error': 'Failed to summarize document'}, status=response.status_code)
#     else:
#         # Return validation error if the file is invalid
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# research/views.py
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings

# Import your processing functions
from .LLM.image_generator import (
    process_research_paper_without_metrics,
    generate_images,
    create_text_images,
)
from .LLM.text_speech import run_voiceover_generation
from .LLM.merge_making_video import create_video


@api_view(["POST"])
def research_paper_upload(request):
    """
    API endpoint that accepts a PDF file upload, processes the research paper,
    and returns summaries and prompts.
    """
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

    # Save the uploaded file to a designated folder (e.g., MEDIA_ROOT/uploads)
    upload_path = os.path.join("uploads", pdf_file.name)
    file_path = default_storage.save(upload_path, pdf_file)
    absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    # Process the research paper
    summaries, prompts = process_research_paper_without_metrics(absolute_file_path)

    # Filter prompts that have at least 5 words
    filtered_prompts = [prompt for prompt in prompts if len(prompt.split()) >= 5]

    # Generate images (you can adjust output folders as needed)
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
