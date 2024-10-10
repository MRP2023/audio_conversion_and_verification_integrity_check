import librosa
import numpy as np
import matplotlib.pyplot as plt
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

def plot_spectrogram(y, sr, file_name):
    """Plot and save the spectrogram."""
    plt.figure(figsize=(12, 8))
    S = np.abs(librosa.stft(y))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title(f"Spectrogram of {file_name}")
    new_name=file_name.replace("input/", "")
    spectrogram_image = f"flac_verification_report/{new_name}_spectrogram.png"
    plt.savefig(spectrogram_image, dpi=500)
    plt.close()
    return spectrogram_image

def check_high_frequency_content(y, sr, threshold_hz=20000):
    """Check for significant high-frequency content above the threshold."""
    S = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    
    # Find the index of the threshold frequency (e.g., 20kHz)
    idx = np.where(freqs > threshold_hz)[0][0]
    
    # Analyze energy content above the threshold frequency
    high_freq_energy = np.mean(S[idx:, :])
    total_energy = np.mean(S)
    
    return high_freq_energy / total_energy

def generate_pdf_report(file_name, conclusion, details, spectrogram_image):
    """Generate a PDF report summarizing the FLAC authenticity analysis."""
    new_name=file_name.replace("input/", "")
    pdf_file = f"flac_verification_report/{new_name}_authenticity_report.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    
    c.setFont("Helvetica", 16)
    c.drawString(100, 750, "FLAC Authenticity Analysis Report")
    
    # Draw conclusion
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"File: {file_name}")
    c.drawString(100, 680, f"Conclusion: {conclusion}")
    
    # Draw additional details
    text = c.beginText(100, 650)
    text.setFont("Helvetica", 12)
    text.textLines(details)
    c.drawText(text)
    
    # Add spectrogram image
    if os.path.exists(spectrogram_image):
        c.drawImage(spectrogram_image, 100, 350, width=400, height=300)
    
    # Save PDF
    c.showPage()
    c.save()

def save_csv_report(file_name, spectral_features):
    """Save spectral features in a CSV file."""
    new_name=file_name.replace("input/", "")
    csv_file = f"flac_verification_report/{new_name}_authenticity_analysis.csv"
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Feature", "Value"])
        for key, value in spectral_features.items():
            writer.writerow([key, value])
    return csv_file

def verify_flac_authenticity(audio_file, threshold_hz=20000, cutoff_ratio=0.001):
    """Main function to verify FLAC authenticity and generate a report."""
    y, sr = librosa.load(audio_file, sr=None)
    
    # Plot and save spectrogram for visual inspection
    spectrogram_image = plot_spectrogram(y, sr, audio_file)
    
    # Check for high-frequency content
    high_freq_ratio = check_high_frequency_content(y, sr, threshold_hz)
    
    # Analyze results
    conclusion = ""
    details = ""
    if high_freq_ratio > cutoff_ratio:
        conclusion = "The file seems authentic. Significant content above 20 kHz detected."
        details = (f"Based on spectral analysis, the file has a high-frequency content ratio of {high_freq_ratio:.4f}. "
                   "This suggests that the file retains energy in the upper frequency range (above 20 kHz), "
                   "which is typical for authentic FLAC files. Therefore, it is likely that this file was not converted from a lossy format.")
    else:
        conclusion = "The file might be a fake FLAC. Limited content above 20 kHz."
        details = (f"Based on spectral analysis, the file has a high-frequency content ratio of {high_freq_ratio:.4f}. "
                   "This indicates a lack of significant energy in the upper frequency range, which is a characteristic of lossy formats such as MP3. "
                   "This suggests that the FLAC file may have been created by converting from a lossy source.")
    
    # Create a dictionary of spectral features for reporting
    spectral_features = {
        "High Frequency Content Ratio": f"{high_freq_ratio:.4f}",
        "Authenticity Conclusion": conclusion
    }
    
    # Generate reports
    generate_pdf_report(audio_file, conclusion, details, spectrogram_image)
    save_csv_report(audio_file, spectral_features)
    
    # Return results for console output
    print(f"PDF and CSV reports generated for {audio_file}.")
    print(f"Conclusion: {conclusion}")
    print(f"Details: {details}")

if __name__ == "__main__":
    audio_file = "input/08. Slowdive - Altogether.flac"  # Replace with your FLAC file path
    verify_flac_authenticity(audio_file)
