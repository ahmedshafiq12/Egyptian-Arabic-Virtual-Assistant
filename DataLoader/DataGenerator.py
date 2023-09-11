import numpy as np
import librosa
import os


class AudioDataGenerator:
    def __init__(self, data_dir, sample_rate=44100, duration=5, batch_size=32):
        self.data_dir = data_dir
        self.df = pd.read_csv(self.data_dir)
        self.sample_rate = sample_rate
        self.duration = duration
        self.batch_size = batch_size
        self.file_list = self.df["path"]
        self.labels = self.df["label"]
        self.num_files = len(self.file_list)
        self.steps_per_epoch = int(np.ceil(self.num_files / batch_size))

    def load_audio(self, audio_file):
        audio, _ = librosa.load(audio_file, sr=self.sample_rate, duration=self.duration)
        return audio

    def generate(self):
        while True:
            np.random.shuffle(self.file_list)
            for i in range(self.steps_per_epoch):
                batch_files = self.file_list[i * self.batch_size:(i + 1) * self.batch_size]
                batch_labels = self.labels[i * self.batch_size:(i + 1) * self.batch_size]
                batch_audio = [self.load_audio(os.path.join(self.data_dir, file)) for file in batch_files]

                # Perform any additional audio processing on the batch of audio data

                yield np.array(batch_audio), np.array(batch_labels)  # Modify the labels as per your use case
