from pydub import AudioSegment
import subprocess
import os

def convert_flac_to_mp3(input_file, output_file, bitrate="320k"):
    try:
        # Step 1: Use pydub to load the FLAC file (only for audio content)
        audio = AudioSegment.from_file(input_file, format="flac")

        # Step 2: Export a temporary MP3 file with the specified bitrate
        temp_mp3_file = "temp_audio.mp3"
        audio.export(temp_mp3_file, format="mp3", bitrate=bitrate)

        # Step 3: Use ffmpeg to copy metadata (including artwork) from FLAC to the MP3 file
        cmd = [
            "ffmpeg",
            "-i", input_file,            # Input FLAC file (metadata + artwork)
            "-i", temp_mp3_file,         # Input MP3 file (audio stream only)
            "-map", "1:a",               # Map only the audio from the MP3 (audio stream)
            "-map_metadata", "0",        # Copy metadata from the FLAC file
            "-map_metadata:s:v", "0:s:v", # Copy attached pictures (album artwork) from FLAC
            "-c:a", "copy",              # Avoid re-encoding the audio to preserve quality
            "-id3v2_version", "3",       # Ensure MP3 ID3v2 metadata compatibility
            output_file                  # Output MP3 file
        ]
        
        # Step 4: Run the ffmpeg command to finalize the conversion with metadata
        subprocess.run(cmd, check=True)
        print(f"Conversion successful: {output_file}")

        # Step 5: Clean up the temporary MP3 file
        if os.path.exists(temp_mp3_file):
            os.remove(temp_mp3_file)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred with ffmpeg: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_flac_file = "input/01. Slowdive - Alison.flac"  # Replace with your input FLAC file path
    output_mp3_file = "output/01. Slowdive - Alison.mp3"  # Replace with your desired output MP3 file path
    
    # Ensure the input file exists
    if os.path.exists(input_flac_file):
        convert_flac_to_mp3(input_flac_file, output_mp3_file, bitrate="320k")
    else:
        print("Input file does not exist.")
