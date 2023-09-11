from DataLoader.Preprocessor import Preprocessor

p = Preprocessor("D:/NTI-FinalProject/dataset_raw", "Dataset")
p.read_audio("D:\\NTI-FinalProject\\dataset_raw\\1.wav", "D:\\NTI-FinalProject\\dataset_raw\\wave_files\\1.wav")
# p.prepare_data()