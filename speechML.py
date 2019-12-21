import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

"""
    Author: Ali Afzal
    Last Updated: Friday Dec 19th
    Python3
"""


class Speech:

    # mL model
    model = None
    ml_accuracy = -1

    # Emotions in the RAVDESS dataset
    emotions={
    '01':'neutral',
    '02':'calm',
    '03':'happy',
    '04':'sad',
    '05':'angry',
    '06':'fearful',
    '07':'disgust',
    '08':'surprised'
    }

    # Emotions to observe
    observed_emotions=['calm', 'happy', 'fearful', 'disgust']
    
    def __init__(self):
        x_train,x_test,y_train,y_test=self.load_data(test_size=0.25)

        temp_model=MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)

        temp_model.fit(x_train,y_train)

        y_pred=temp_model.predict(x_test)

        accuracy=accuracy_score(y_true=y_test, y_pred=y_pred)

        print("Accuracy: {:.2f}%".format(accuracy*100))

        self.model = temp_model
        self.ml_accuracy = accuracy

    def extract_feature(self, file_name, mfcc, chroma, mel):
        with soundfile.SoundFile(file_name) as sound_file:
            X = sound_file.read(dtype="float32")
            sample_rate=sound_file.samplerate
            if chroma:
                stft=np.abs(librosa.stft(X))
            result=np.array([])
            if mfcc:
                mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
                result=np.hstack((result, mfccs))
            if chroma:
                chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
                result=np.hstack((result, chroma))
            if mel:
                mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
                result=np.hstack((result, mel))
            return result

    def load_data(self, test_size=0.2):
        x,y=[],[]
        for file in glob.glob("/Users/aliafzal/Desktop/speech/data/Actor_*/*.wav"):
            file_name=os.path.basename(file)
            emotion=self.emotions[file_name.split("-")[2]]
            if emotion not in self.observed_emotions:
                continue
            feature=self.extract_feature(file, mfcc=True, chroma=True, mel=True)
            x.append(feature)
            y.append(emotion)
        return train_test_split(np.array(x), y, test_size=test_size, random_state=9)

    def get_prediction(self, file):
        feature=self.extract_feature(file, mfcc=True, chroma=True, mel=True)
        x_pred = feature
        prediction = self.model.predict([np.array(x_pred)])
        return prediction
        
    def get_accuracy(self):
        return self.ml_accuracy


