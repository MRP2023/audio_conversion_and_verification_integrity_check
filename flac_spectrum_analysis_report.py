import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def plot_waveform(audio_file, ax):
    y, sr = librosa.load(audio_file, sr=None)
    librosa.display.waveshow(y, sr=sr, ax=ax)
    ax.set_title('Waveform')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')

def plot_spectrogram(audio_file, ax):
    y, sr = librosa.load(audio_file, sr=None)
    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_db, sr=sr, ax=ax, x_axis='time', y_axis='linear')
    ax.set_title('Spectrogram')
    plt.colorbar(img, ax=ax, format="%+2.0f dB")

def compute_spectral_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    
    # Compute spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
    
    return {
        'Spectral Centroid': np.mean(spectral_centroid),
        'Spectral Bandwidth': np.mean(spectral_bandwidth),
        'Spectral Rolloff (85%)': np.mean(spectral_rolloff),
    }

def generate_report(audio_file, features):
    report = pd.DataFrame(features, index=[0])
    report.to_csv('flac_spectrum_report/audio_analysis_report.csv', index=False)

    with PdfPages('flac_spectrum_report/audio_analysis_report.pdf') as pdf:
        # Plotting waveform and spectrogram
        fig, axs = plt.subplots(2, 1, figsize=(10, 10))
        plot_waveform(audio_file, axs[0])
        plot_spectrogram(audio_file, axs[1])
        plt.tight_layout()
        
        # Save the figure to PDF
        pdf.savefig(fig)
        plt.close(fig)
        
        # Create a new figure for the report
        fig = plt.figure(figsize=(10, 4))
        plt.axis('off')  # Turn off the axis
        plt.title('Spectral Features Summary', fontsize=16)
        
        # Display the features
        for feature, value in features.items():
            plt.text(0.1, 0.8 - 0.1 * list(features.keys()).index(feature), 
                     f"{feature}: {value:.2f}", fontsize=14)
        
        # Save the features summary to PDF
        pdf.savefig(fig)
        plt.close(fig)

def analyze_audio_file(audio_file):
    # Create subplots
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot waveform
    plot_waveform(audio_file, axs[0])
    
    # Plot spectrogram
    plot_spectrogram(audio_file, axs[1])
    
    plt.tight_layout()
    plt.savefig('flac_spectrum_report/audio_analysis_visuals.png', dpi=500)  # Save visuals as PNG
    plt.show()
    
    # Compute spectral features
    features = compute_spectral_features(audio_file)
    
    # Generate report
    generate_report(audio_file, features)

# Example usage
if __name__ == "__main__":
    audio_file = "input/08. Slowdive - Altogether.flac"  # Replace with your FLAC file
    analyze_audio_file(audio_file)
