import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

def plot_spectrogram(audio_file, ax, title):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)
    
    # Compute the Short-Time Fourier Transform (STFT) to get the spectrogram
    S = np.abs(librosa.stft(y))
    
    # Convert the power spectrogram (amplitude squared) to decibel (dB) units
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    
    # enable below comment if you want to Display the spectrogram with Logarithmic  frequency Scale
    # img = librosa.display.specshow(S_db, sr=sr, ax=ax, x_axis='time', y_axis='log')

    img = librosa.display.specshow(S_db, sr=sr, ax=ax, x_axis='time', y_axis='linear')
    
    ax.set_title(title)
    plt.colorbar(img, ax=ax, format="%+2.0f dB")
    
def compare_audio_spectra(file1, file2):
    # Create a figure with two subplots (side by side)
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot the spectrogram for the first file (FLAC)
    plot_spectrogram(file1, axs[0], title='Original FLAC File')

    # Plot the spectrogram for the second file (MP3)
    plot_spectrogram(file2, axs[1], title='Converted MP3 File')
    
    # Show the comparison plot
    plt.tight_layout()
    plt.savefig('spectrum_images/spectrogram_comparison_1.png', dpi=500)  # Save as PNG
    plt.show()

def plot_difference(file1, file2):
    # Load both audio files
    y1, sr1 = librosa.load(file1, sr=None)
    y2, sr2 = librosa.load(file2, sr=None)
    
    # Compute STFT for both files
    S1 = np.abs(librosa.stft(y1))
    S2 = np.abs(librosa.stft(y2))
    
    # Convert to dB scale
    S1_db = librosa.amplitude_to_db(S1, ref=np.max)
    S2_db = librosa.amplitude_to_db(S2, ref=np.max)
    
    # Calculate the difference between spectrograms
    diff = S1_db - S2_db
    
    # Plot the difference
    fig, ax = plt.subplots(figsize=(10, 5))
    img = librosa.display.specshow(diff, sr=sr1, ax=ax, x_axis='time', y_axis='log')
    ax.set_title('Difference in Spectrogram (FLAC - MP3)')
    plt.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.tight_layout()
    plt.savefig('spectrum_images/spectrogram_difference_1.png', dpi=500)
    plt.show()

# Example usage
if __name__ == "__main__":
    original_flac = "input/08. Slowdive - Altogether.flac"  # Replace with your FLAC file
    converted_mp3 = "output/08. Slowdive - Altogether.mp3"  # Replace with your MP3 file
    
    # Plot the spectra of both files side by side
    compare_audio_spectra(original_flac, converted_mp3)
    
    # Plot the difference in the spectra
    plot_difference(original_flac, converted_mp3)
