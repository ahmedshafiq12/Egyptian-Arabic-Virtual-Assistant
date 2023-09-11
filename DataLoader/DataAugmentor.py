import pandas as pd
import numpy as np
import librosa


class DataAugmentor:
    def __init__(self, data_dir, output_path):
        self.output_path = output_path
        self.data_dir = data_dir
        self.df = pd.read_csv(self.data_dir)
        self.file_list = self.df["path"]
        self.labels = self.df["label"]

    def save_csv(self, paths, labels):
        dict = {'path': paths, 'label': labels}
        df = pd.DataFrame(dict)
        df.to_csv(f'{self.output_path}/dataset.csv')

    def generate(self):
        new_paths = []
        new_labels = []
        noises = [0.005, 0.009, 0.02]
        shift_list = [10, 15, 20]
        factors = [1.2, 0.4, 0.8]
        n_steps_list = [-3, -5, -7]
        for i, wav_file_path in enumerate(self.file_list):
            label = self.labels[i]
            file_name = str(wav_file_path).split('/')[-1].split('.')[0]
            wav, sample_rate = librosa.load(wav_file_path, sr=None)

            # tfms 1: Noise addition:
            wav_n = wav + np.random.choice(noises) * np.random.normal(0, 1, len(wav))

            # tfms 2: Shifting Sound wave:
            shift = np.random.choice(shift_list)
            wav_roll = np.roll(wav, int(sample_rate / shift))

            # tfms 3: Time - stretching
            factor = np.random.choice(factors)
            wav_time_stch = librosa.effects.time_stretch(wav, factor)

            # tfms 4: Pitch - Shifting
            n_steps = np.random.choice(n_steps_list)
            wav_pitch_sf = librosa.effects.pitch_shift(wav, sample_rate, n_steps=n_steps)

            wav_tfms = [wav, wav_n, wav_roll, wav_time_stch, wav_pitch_sf]

            for j, op in enumerate(wav_tfms):
                new_paths.append(f'{file_name}_{j}.wav')
                new_labels.append(label)
                librosa.output.write_wav(f'{self.output_path}/{file_name}_{j}.wav', op, sample_rate)

        self.save_csv(new_paths, new_labels)


