# import os
# from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


# def create_video():
#     # Define folders
#     folder1 = "generated_images"
#     folder2 = "generated_images2"
#     audio_folder = "voiceovers"

#     # Get sorted list of images
#     images1 = sorted([os.path.join(folder1, f) for f in os.listdir(folder1) if f.endswith(".png")])
#     images2 = sorted([os.path.join(folder2, f) for f in os.listdir(folder2) if f.endswith(".png")])
#     # Select images based on odd/even rule
#     selected_images = []
#     for i in range(max(len(images1), len(images2))):
#         if i % 2 == 0 and i < len(images2):
#             selected_images.append(images2[i])  # Even index -> folder2
#         elif i % 2 == 1 and i < len(images1):
#             selected_images.append(images1[i])  # Odd index -> folder1

#     # Ensure the number of selected images matches the number of audio files
#     audio_files = sorted([os.path.join(audio_folder, f) for f in os.listdir(audio_folder) if f.endswith(".mp3")])
#     if len(selected_images) != len(audio_files):
#         raise ValueError("The number of selected images and audio files must be the same.")

#     # Create a list to hold the video clips
#     video_clips = []

#     # Process each image and its corresponding audio file
#     for image_path, audio_path in zip(selected_images, audio_files):
#         # Load audio file
#         audio_clip = AudioFileClip(audio_path)
#         audio_duration = audio_clip.duration

#         # Load image and set its duration to match the audio
#         image_clip = ImageClip(image_path).set_duration(audio_duration)

#         # Set the audio of the image clip
#         image_clip = image_clip.set_audio(audio_clip)

#         # Append the image clip to the list
#         video_clips.append(image_clip)

#     # Concatenate all the image clips into a single video
#     final_video = concatenate_videoclips(video_clips, method="compose")

#     # Output path for the final video
#     output_path = "final_output.mp4"

#     # Write the final video file
#     final_video.write_videofile(output_path, codec="libx264",fps=24)

#     print(f"Video saved at: {output_path}")


import os
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeAudioClip,
)


def create_video():
    # Define folders
    folder1 = "generated_images"
    folder2 = "generated_images2"
    audio_folder = "voiceovers2"
    songs_folder = "Songs"  # Folder where background music is stored
    
    # Get sorted list of images
    images1 = sorted(
        [os.path.join(folder1, f) for f in os.listdir(folder1) if f.endswith(".png")]
    )
    images2 = sorted(
        [os.path.join(folder2, f) for f in os.listdir(folder2) if f.endswith(".png")]
    )
    
    # Select images based on odd/even rule
    selected_images = []
    for i in range(max(len(images1), len(images2))):
        if i % 2 == 0 and i < len(images2):
            selected_images.append(images2[i])  # Even index -> folder2
        elif i % 2 == 1 and i < len(images1):
            selected_images.append(images1[i])  # Odd index -> folder1
    
    # Ensure the number of selected images matches the number of audio files
    audio_files = sorted(
        [
            os.path.join(audio_folder, f)
            for f in os.listdir(audio_folder)
            if f.endswith(".mp3")
        ]
    )
    if len(selected_images) != len(audio_files):
        print(
            f"Warning: Images ({len(selected_images)}) and voiceovers ({len(audio_files)}) do not match!"
        )
        min_length = min(len(selected_images), len(audio_files))
        selected_images = selected_images[:min_length]
        audio_files = audio_files[:min_length]
    
    # Get the list of background music files from the "songs" folder
    background_music_files = sorted(
        [
            os.path.join(songs_folder, f)
            for f in os.listdir(songs_folder)
            if f.endswith(".mp3")
        ]
    )
    
    # Ask the user to select the background music (for simplicity, choose the first file as an example here)
    if len(background_music_files) > 0:
        print("Available background music files:")
        for idx, song in enumerate(background_music_files, start=1):
            print(f"{idx}. {os.path.basename(song)}")
    
        while True:
            try:
                choice = int(input("Select a background music track (1-6): "))
                if 1 <= choice <= len(background_music_files):
                    background_music_path = background_music_files[choice - 1]
                    break
                else:
                    print("Invalid choice. Please select a number between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6.")
    else:
        raise ValueError("No background music files found.")
    # Load the background music
    background_music = AudioFileClip(background_music_path)
    
    # Create a list to hold the video clips
    video_clips = []
    
    # Process each image and its corresponding audio file
    for image_path, audio_path in zip(selected_images, audio_files):
        # Load the individual audio file (voiceover)
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration
    
        # Load the image and set its duration to match the audio
        image_clip = ImageClip(image_path).set_duration(audio_duration)
    
        # Set the voiceover audio for the image clip
        image_clip = image_clip.set_audio(audio_clip)
    
        # Append the image clip to the list
        video_clips.append(image_clip)
    
    # Concatenate all the image clips into a single video
    final_video = concatenate_videoclips(video_clips, method="compose")
    
    # Sync background music with the video
    background_music = background_music.set_duration(
        final_video.duration
    )  # Make background music the same length as the video
    background_music = background_music.volumex(
        0.3
    )  # Adjust the volume of background music if needed
    
    # Combine the background music with the video audio
    final_audio = CompositeAudioClip([final_video.audio, background_music])
    
    # Set the final audio to the video clip
    final_video = final_video.set_audio(final_audio)
    
    # Output path for the final video
    output_path = "final_output.mp4"
    
    # Write the final video file
    final_video.write_videofile(output_path, codec="libx264", fps=24)
    
    print(f"Video saved at: {output_path}")
    