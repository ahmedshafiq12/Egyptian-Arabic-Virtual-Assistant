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


**In the project architecture, the following pipeline is incorporated:**

**Input Processing:**

1. The project takes a video as input.
2. The video is split into separate frames for further processing.

Face Detection:

1. The frames extracted from the video undergo face detection.
2. A face detection algorithm is employed to identify and locate faces within each frame.

speech-to-Text Conversion:

1. The audio track of the video is extracted.
2. The extracted audio is passed through the HuBERT pre-trained model for speech-to-text conversion.
3. HuBERT converts the spoken Arabic language in the audio to text.

Face Emotion Recognition:

1. The frames with detected faces are fed into the VGG19 model.
2. The VGG19 model, trained on the FER2013 dataset, performs face emotion recognition.
3. Each face in the frames is classified into one of the predefined emotion categories.

HugChat API:

1. The recognized emotion and extracted text from the speech are sent to the HugChat API.
2. The HugChat API processes the input and generates an appropriate response in English.

Translation:

1. The English response from the HugChat API is passed through the Google Translate API.
2. The Google Translate API translates the response from English to Arabic.

Finally the output

## **Data Collection**

In this project, we collected videos from YouTube featuring Egyptian Arabic speakers from various channels and diverse content. These videos were selected to ensure a wide range of speech patterns, accents, and topics. Importantly, each video was accompanied by subtitles or closed captions.

In this project, we collected videos from YouTube featuring Egyptian Arabic speakers from various channels and diverse content. These videos were selected to ensure a wide range of speech patterns, accents, and topics. Importantly, each video was accompanied by subtitles or closed captions.

Video Extraction:

1. We extracted the audio track from each video using appropriate tools.
2. This allowed us to isolate the spoken content while disregarding the visual aspects.

Subtitles as Labels:

1. The subtitles or closed captions provided with the videos were utilized as the ground truth labels.
2. These subtitles accurately represented the speech content in written form.

By separating the audio from the video and utilizing the subtitles as labels, we were able to create a dataset suitable for training and evaluating our speech-to-text models. This approach facilitated the inclusion of diverse spoken content, ensuring that our models are capable of accurately transcribing Egyptian Arabic speech across various topics and contexts.

The collected dataset serves as a valuable resource for training and evaluating our models, enabling them to achieve high accuracy and robustness in converting spoken Arabic language into written text.

## **Data Preprocessing**

Gathered the FER2013 dataset, which contains facial images labeled with seven emotion categories. In this project, we have performed various preprocessing steps on the FER2013 dataset. These steps include rescaling, zooming, and data cleansing to ensure the data is suitable for further analysis and modeling. Preprocessed the dataset by resizing the images to a standard size and normalizing pixel values to improve model performance.
Split the dataset into training, validation, and testing sets to ensure an unbiased evaluation of the model's accuracy.

Rescaling

We have applied rescaling techniques to normalize the pixel values of the images in the dataset. This helps in reducing the influence of varying pixel intensity ranges and brings all the images to a consistent scale.

Data Cleansing

To ensure the quality of the dataset, we have performed data cleansing operations. This involves removing any irrelevant or noisy data points that could potentially affect the model's performance. By eliminating such instances, we aim to enhance the overall accuracy and reliability of the dataset.

These preprocessing steps are crucial in preparing the FER2013 dataset for subsequent analysis and model training. The resulting dataset is now ready to be used for tasks such as emotion recognition or facial expression classification.

```python
from tensorflow.keras.layers.preprocessing import TextVectorization

# Create a TextVectorization layer

```









