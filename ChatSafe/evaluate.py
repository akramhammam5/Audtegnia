import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def plot_wav(file_path):

    sample_rate, data = wavfile.read(file_path)


    data = data / np.max(np.abs(data), axis=0)


    time = np.arange(0, len(data)) / sample_rate


    plt.figure(figsize=(10, 4))
    plt.plot(time, data, color='blue')
    plt.title('Audio Waveform')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    wav_file_path = '/home/elliot/Downloads/young.wav'
    plot_wav(wav_file_path)

