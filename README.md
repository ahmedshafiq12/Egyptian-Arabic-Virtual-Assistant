# **Wise Man "حكيم" your Virtual Assistant**
Emotion Classification and Automatic Speech Recognition (ASR) with HuBERT Model

## **Introduction**

Wise Man is an AI project that focuses on two AI models: Emotion Classification and Automatic Speech Recognition (ASR). The Emotion Classification model is designed to classify facial images into seven emotion categories using the FER2013 dataset. The ASR model utilizes the HuBERT Model for Arabic speech recognition. The project's ultimate goal is to develop an AI assistant that can interact with users through video and text inputs.

**Emotion Classification**

The Emotion Classification model in Wise Man is trained on the FER2013 dataset, which contains facial images labeled with seven emotion categories. The model is capable of accurately classifying unseen facial images into the following emotions: Anger, Disgust, Fear, Happiness, Sadness, Surprise, and Neutral.

**Automatic Speech Recognition (ASR)**

Wise Man employs the HuBERT Model for Arabic speech recognition. The ASR model is trained to transcribe spoken Arabic language into text. It undergoes a two-stage training process, starting with pre-training on a large corpus of Egyptian Arabic text data to learn language patterns and nuances. It is then fine-tuned on a smaller dataset specific to the ASR task.

## **Project Architecture:**

**Overview of the assistant's architecture:**

The virtual assistant architecture consists of three main components: emotion recognition, speech-to-text recognition, and chatbot. The speech-to-text recognition module utilizes the HuBERT model, which is a large Arabic Egyptian language model trained specifically for understanding Egyptian Arabic accents. The chatbot component generates responses based on user queries using the HugChat API, which leverages Google Translate API for translation. The emotion recognition module employs the VGG19 model to analyze video inputs and detect facial expressions associated with various emotions. The user interface allows users to interact with the assistant through video, audio, and chat "text" inputs.

![WiseMan PipeLine](https://github.com/theonlyshafiq/NTI-FinalProject/assets/91796651/9b90ddee-85d2-4601-9f55-10ab02963731)












