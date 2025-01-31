# from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

# from rest_framework import status
# from .serializer import FileSerializer
# from PyPDF2 import PdfReader

# # Create your views here.


# @api_view(["POST"])
# @parser_classes([MultiPartParser, FormParser])
# def FileUpload(request):
#     if request.method == "POST":
#         file = request.FILES["file"]
#         file_type = file.content_type
#         try:
#             file_content = None

#             if file_type == "text/plain":
#                 file_content = file.read().decode("utf-8")

#             elif file_type == "application/pdf":
#                 reader = PdfReader(file)
#                 file_content = "\n".join(
#                     [
#                         page.extract_text()
#                         for page in reader.pages
#                         if page.extract_text()
#                     ]
#                 )

#             else:
#                 return Response(
#                     {"error": "Unsupported file type"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             file_content = file_content.split("\n")
#             print("File Content:\n", file_content)

#             file_serializer = FileSerializer(data={"file": file})
#             if file_serializer.is_valid():
#                 file_serializer.save()
#                 return Response(
#                     {"message": "File uploaded successfully", "content": file_content},
#                     status=status.HTTP_201_CREATED,
#                 )
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except UnicodeDecodeError:
#             return Response("Invalid file type", status=status.HTTP_400_BAD_REQUEST)


from rest_framework.response import Response
from rest_framework.decorators import api_view
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image
from .serializers import FileSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def FileUpload(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )

        file_type = file.content_type
        file_content = None
        images = []  # List to store extracted images
        file_data = file.read()  # Read the file content once to reuse

        try:
            if file_type == "text/plain":
                # Handling plain text file
                file_content = file_data.decode("utf-8")

            elif file_type == "application/pdf":
                # Handling PDF files
                # Extract text from PDF using PyPDF2
                reader = PdfReader(BytesIO(file_data))  # Using the byte stream
                text = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
                file_content = "\n".join(text)  # Combine text from all pages

                # Extract images from PDF using PyMuPDF (fitz)
                pdf_document = fitz.open(
                    stream=BytesIO(file_data), filetype="pdf"
                )  # Use the stream argument to read from BytesIO
                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)
                    for img in page.get_images(full=True):
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]  # Get the image in bytes

                        # Open the image using Pillow
                        image = Image.open(BytesIO(image_bytes))
                        image_content = f"Image {page_num + 1} - {image.format} ({image.size[0]}x{image.size[1]})"
                        images.append(image_content)  # Save image info

            else:
                return Response(
                    {"error": "Unsupported file type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # If there were images, return image info
            # if images:
            #     print("Extracted Images: ", images)

            # Return the content (text and images info)
            print(file_content.split("\n") if file_content else None)
            return Response(
                {
                    "message": "File uploaded successfully",
                    "content": file_content.split("\n") if file_content else None,
                    "images": images,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
