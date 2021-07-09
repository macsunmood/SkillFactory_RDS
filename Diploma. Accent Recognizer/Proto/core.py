import streamlit as st

from utils import *

import os
import joblib
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model

import speech_recognition as sr


###
### APP CORE
###


TF_HASH_FUNCS = {
    tf.compat.v1.Session: id
}


BATCH_SIZE = 64
ACCENTS_DICT = {0: 'england', 1: 'us'}


###==============================================


def recognize_GSR(recognizer, audio):
    '''recognize speech using Google Speech Recognition'''
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand speech')
    except sr.RequestError as e:
        print(f'Could not request results from Google Speech Recognition service; {e}')


###==============================================


def get_models_list(dir_name, exts=('h5', 'joblib')):
    return [dir_name + f for f in os.listdir(dir_name) 
            if os.path.isfile(os.path.join(dir_name, f)) 
            and f.split('.')[-1] in exts]

class Info(tf.keras.layers.Layer):
    def __init__(self, accents_dict):
        self.accents_dict = accents_dict
        super().__init__()
    def get_config(self):
        return {'accents_dict': self.accents_dict}

class AccentsInfo(Info):
	pass

def get_acc_dict(model):
    d = next(l.accents_dict for l in model.layers 
             if hasattr(l, 'accents_dict'))
    return {int(k): v for k, v in d.items()}


@st.cache(allow_output_mutation=True, hash_funcs=TF_HASH_FUNCS)
def load_models(models_dir='models/'):
	'''Load pretrained models'''
	# Open a new TensorFlow session
	config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
	session = tf.compat.v1.Session(config=config)
	with session.as_default():
		models = {}
		for m in get_models_list(models_dir):
			if m.split('.')[-1] == 'joblib':
				model = joblib.load(m)
			elif m.split('.')[-1] == 'h5':
				try:
					model = load_model(m, custom_objects={'Info': Info, 
														  'AccentsInfo': AccentsInfo})
				except:
					model = load_model(m)

			if not hasattr(model, 'accents_dict'):
				try:
					model.accents_dict = get_acc_dict(model)
				except:
					model.accents_dict = ACCENTS_DICT

			models.update({model.name: model})
	return session, models


def make_prediction(model, features, batch_size):
    # predict = model.predict(features, batch_size)
    pred_proba = model.predict_proba(features, 1)
    # pred_proba = model.predict_proba(features)
    pred = np.argmax(pred_proba, axis=-1)
    return pred_proba, pred

def recognize_accent(model, features):
	# features = np.expand_dims(features, 0)
	pred_proba, pred = make_prediction(model, features, BATCH_SIZE)
	# pred = make_prediction(model, features, 1)[0]
	return pred_proba[0], model.accents_dict[pred[0]]