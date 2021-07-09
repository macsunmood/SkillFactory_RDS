import streamlit as st

import numpy as np
from io import BytesIO

from pydub import AudioSegment
from pydub.silence import detect_leading_silence
import librosa

import librosa.display as lbd
import matplotlib.pyplot as plt


###
###=== Audio Loading and Processing
###


SAMPLE_RATE = 22050
DURATION = 5

n_mfcc = 13  # number of MFCCs to extract from each sample
n_mels = 128

n_fft = 2048
hop_length = 512

delta_width = 9 # MFCC Delta parameter


def trim_silence(sound, s_thresh=-28.0):
    '''Trims silent chunks from beginning and end of the sound'''
    duration = len(sound)
    
    start_trim = detect_leading_silence(sound, s_thresh)
    end_trim = detect_leading_silence(sound.reverse(), s_thresh)
    
    start = start_trim if start_trim != duration else None
    end = duration - end_trim if end_trim != duration else None
    
    return sound[start:end]

def normalize_volume(sound, target_dBFS=-20.0):
    '''Normalizes sound and shifts to specified loudness'''
    sound = sound.normalize()
    difference = target_dBFS - sound.dBFS
    return sound.apply_gain(difference)

def proc_raw_audio(audio_data, start_from=0, duration=DURATION):
    '''Processes raw audio data and return wav and numpy arrays'''
    # Instanciate pydub AudioSegment object from raw audio
    audioObj = AudioSegment.from_file(BytesIO(audio_data))

    # Convert to mono mode with the desired sample rate
    audioObj = audioObj.set_frame_rate(SAMPLE_RATE).set_channels(1)
    # Normalize audio volume
    audioObj = normalize_volume(audioObj)
    # Trim by removing silence from beginning and end of the sound
    audioObj = trim_silence(audioObj)
    # Cut to the desired duration
    start = start_from * 1000
    end = start + duration * 1000
    audioObj = audioObj[start:end]

    # Convert AudioSegment to wav format instance
    buf = BytesIO()
    audioObj.export(buf, format='wav')
    audio_wav = buf.getvalue()

    # Convert the AudioSegment to signal in form of numpy.array
    arr = audioObj.get_array_of_samples()
    audio_np = np.array(arr, dtype='float')
    
    # Normalize if specified
    # if normalized:
        # audio_np = np.array(arr) / np.iinfo(arr.typecode).max
        # y /= np.linalg.norm(y)
    # return y, sample_rate

    return audio_wav, audio_np


###==============================================


def obtain_features(y, sr=22050, duration=5, delta_width=9):
    '''Extracts sound features from given signal and returns them as a numpy array'''
    # --- MFCC (returns M: np.ndarray [shape=(n_mfcc, t)])
    mfcc = librosa.feature.mfcc(y, sr, 
                                n_mfcc=n_mfcc, n_mels=n_mels, 
                                n_fft=n_fft, hop_length=hop_length)

    return mfcc

def create_features_array(mfcc):#, mfcc_delta1, mfcc_delta2, spectr_c, spectr_r):
    '''Creates wholistic numpy array of means and variances out of given features'''
    make_meanvar = lambda mean, var: [item for mv in zip(mean, var) for item in mv]

    mean_var_ops = [
        (mfcc.mean(axis=1), mfcc.var(axis=1))
    ]

    mfcc_meanvars = sum([make_meanvar(mean, var) 
                         for mean, var in mean_var_ops], [])

    # features_array = mfcc_meanvars + spectr_meanvars
    features_array = [mfcc_meanvars]

    return features_array

# def get_features(y, sr=22050, duration=5, delta_width=9):
#     'Returns numpy array of sound features obtained from signal'
#     return create_features_array(*obtain_features(y, sr, duration, delta_width))



pad_signal = lambda s, v: np.pad(s, 
    [(0, 0), (0, max(0, 216 - s.shape[1]))], 
    constant_values=v)

def get_features(y, duration=5, sr=SAMPLE_RATE):
    '''Returns numpy array of sound features obtained from signal'''

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # WAVE PLOT
    axes[0].set_title(f'Wave Plot for audio sample at {sr} hz')
    axes[0].set_facecolor('#B4E8CF')
    lbd.waveplot(y, sr, color='#4300FF', facecolor='#7B4CFF', ax=axes[0])

    # MELSPEC
    melspec = librosa.feature.melspectrogram(y, sr)
    melspec = librosa.power_to_db(np.abs(melspec), ref=np.max)
    axes[1].set_title(f'Mel Spectogram | shape: {melspec.shape}')
    lbd.specshow(melspec, cmap='viridis', y_axis='mel', x_axis='time', ax=axes[1])

    st.pyplot(fig)

    # Prepare melspec for use
    melspec = pad_signal(melspec, melspec.min())
    melspec = melspec.reshape(1, -1)

    # MFCC
    mfcc = create_features_array(obtain_features(y, sr, duration, delta_width))
    mfcc = np.array(mfcc).reshape(1, -1)

    return melspec
    # return mfcc