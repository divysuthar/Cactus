import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


def create_video():
    # Define folders
    folder1 = "generated_images"
    folder2 = "generated_images2"
    audio_folder = "voiceovers"

    # Get sorted list of images
    images1 = sorted([os.path.join(folder1, f) for f in os.listdir(folder1) if f.endswith(".png")])
    images2 = sorted([os.path.join(folder2, f) for f in os.listdir(folder2) if f.endswith(".png")])
    # Select images based on odd/even rule
    selected_images = []
    for i in range(max(len(images1), len(images2))):
        if i % 2 == 0 and i < len(images2):
            selected_images.append(images2[i])  # Even index -> folder2
        elif i % 2 == 1 and i < len(images1):
            selected_images.append(images1[i])  # Odd index -> folder1

    # Ensure the number of selected images matches the number of audio files
    audio_files = sorted([os.path.join(audio_folder, f) for f in os.listdir(audio_folder) if f.endswith(".mp3")])
    if len(selected_images) != len(audio_files):
        raise ValueError("The number of selected images and audio files must be the same.")

    # Create a list to hold the video clips
    video_clips = []

    # Process each image and its corresponding audio file
    for image_path, audio_path in zip(selected_images, audio_files):
        # Load audio file
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration

        # Load image and set its duration to match the audio
        image_clip = ImageClip(image_path).set_duration(audio_duration)

        # Set the audio of the image clip
        image_clip = image_clip.set_audio(audio_clip)

        # Append the image clip to the list
        video_clips.append(image_clip)

    # Concatenate all the image clips into a single video
    final_video = concatenate_videoclips(video_clips, method="compose")

    # Output path for the final video
    output_path = "final_output.mp4"

    # Write the final video file
    final_video.write_videofile(output_path, codec="libx264",fps=24)

    print(f"Video saved at: {output_path}")
    