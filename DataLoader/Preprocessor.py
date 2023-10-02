from pydub import AudioSegment
import ffmpeg
import re
import wave
from tqdm import tqdm
import os
import pysrt


class Preprocessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        if not os.path.exists(f"{self.output_path}"):
            os.makedirs(f"{self.output_path}")
        if not os.path.exists(f"{self.input_path}/wave_files"):
            os.makedirs(f"{self.input_path}/wave_files")

    def read_transcript(self, transcript_path):
        transcript = pysrt.open(transcript_path)
        return transcript

    def extract_samples(self, transcript):
        times = []
        labels = []

        for i in range(len(transcript)):
            start_time = ([*transcript[i].start][0] * 3600) + ([*transcript[i].start][1] * 60) + [*transcript[i].start][
                2] + ([*transcript[i].start][3] / 1000)
            if i == len(transcript) - 1:
                end_time = ([*transcript[i].end][0] * 3600) + ([*transcript[i].end][1] * 60) + [*transcript[i].end][
                    2] + ([*transcript[i].end][3] / 1000)
            else:
                end_time = ([*transcript[i + 1].start][0] * 3600) + ([*transcript[i + 1].start][1] * 60) + \
                           [*transcript[i + 1].start][2] + ([*transcript[i + 1].start][3] / 1000)

            time = (start_time, end_time)
            times.append(time)

            labels.append(transcript[i].text)

        return times, labels

    def read_audio(self, input_audio_path, output_audio_path):
        ffmpeg.input(input_audio_path).output(output_audio_path).run()
        audio = AudioSegment.from_file(output_audio_path)
        return audio

    def crop_audio(self, audio, start_time, end_time):
        cropped_audio = audio[start_time * 1000: end_time * 1000]
        return cropped_audio

    def export_audio(self, cropped_audio, export_path):
        cropped_audio.export(export_path, format='wav')

    def prepare_data(self):
        all_paths = []
        all_labels = []

        transcript_paths = []
        for file in os.listdir(self.input_path):
            if file.endswith('.srt'):
                transcript_paths.append(file)

        audio_paths = []
        for file in os.listdir(self.input_path):
            if file.endswith('.wav'):
                audio_paths.append(file)

        print(transcript_paths)
        print(audio_paths)

        for transcript_path, audio_file_name in tqdm(zip(transcript_paths, audio_paths)):
            transcript = self.read_transcript(os.path.join(self.input_path, transcript_path))
            audio_path = os.path.join(self.input_path, audio_file_name)
            out_path = os.path.join(self.input_path, "wave_files", audio_file_name)
            audio = self.read_audio(audio_path, out_path)

            times, labels = self.extract_samples(transcript)
            all_labels.extend(labels)

            for i, (start_time, end_time) in enumerate(times):
                cropped_audio = self.crop_audio(audio, start_time, end_time)
                if cropped_audio.duration_seconds == 0.0:
                    all_labels.pop()
                    continue
                cropped_audio_path = (f'{self.output_path}/'
                                      + re.findall('\d+', audio_file_name)[0]
                                      + '_' + str(i) + '.wav')
                self.export_audio(cropped_audio, cropped_audio_path)
                all_paths.append(cropped_audio_path)