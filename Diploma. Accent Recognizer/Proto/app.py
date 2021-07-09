import streamlit as st

from core import *
from examples import EXAMPLES

import numpy as np
import pandas as pd

from youtube_dl import YoutubeDL
import ffmpeg

import speech_recognition as sr


###
### APP UI
###


st.set_page_config('English Accent Recognizer 🌎', '🗣️')

# Load pretrained models and start new tensorflow session
session, MODELS = load_models()

sndsrc_help = '''
Select the **Sound Source** and then
- post a `video URL`
- or speak into the `microphone`
'''  # has to be moved outside of function for markdown to work


def ui_main():
    '''Draw main UI layout'''
    st.title('[proto] English Accent Recognizer 🌎')

    SOURCE_OPTIONS = {
        '🎞️ YouTube': page_youtube, 
        '🎤 Microphone': page_mic
    }
    option_source = st.sidebar.selectbox('Sound Source:', [*SOURCE_OPTIONS], 
                                         help=sndsrc_help)
    global option_model  # will be used in `ui_recognition()`
    option_model = st.sidebar.radio('Predictor Model:', [*MODELS])

    mdl = MODELS[option_model]  # get current selected model

    global examples_filtered  # will be used in `page_youtube()`
    examples_filtered = {k: v for k, v in EXAMPLES.items() 
                         if v['accent'] in mdl.accents_dict.values()}

    SOURCE_OPTIONS[option_source]()  # access page UI for the selected source

    # Show accents supported by the selected model
    show_accents(mdl)
    # Show summary of the selected model
    show_summary(mdl)
    

def show_accents(mdl):
    '''Display model accents'''
    st.sidebar.markdown('---')
    st.sidebar.text('Supported Accents:')
    accents_df = pd.DataFrame.from_dict(mdl.accents_dict, 
                                        orient='index', columns=['Accent'])
    st.sidebar.dataframe(accents_df, width=500)

def show_summary(mdl):
    '''Display model summary'''
    set_sb_width = lambda width: st.markdown(
        f"""
            <style>
            [data-testid="stSidebar"][aria-expanded="true"] > 
            div:first-child {{
                width: {width}px;
            }}
            [data-testid="stSidebar"][aria-expanded="false"] > 
            div:first-child {{
                width: {width}px;
                margin-left: -{width}px;
            }}
            </style>
        """,
        unsafe_allow_html=True,
    )
    if hasattr(mdl, 'summary'):
        model_struct = []
        mdl.summary(print_fn=lambda x: model_struct.append(x))
        model_summary = '\n'.join(model_struct)
        with st.sidebar.beta_expander('Model Summary'):
            set_sb_width(600)
            st.code(model_summary)


def page_youtube():
    '''Obtain audio from YouTube video'''
    with st.beta_expander('Choose Example Preset'):
        example = EXAMPLES[st.selectbox('Example:', [*examples_filtered], index=1)]

    col_url, col_start_from = st.beta_columns([5, 2])
    url = col_url.text_input('YouTube video URL:', example['url'])
    start_from = col_start_from.number_input(
        'Start From:', 
        min_value=0.0, step=0.5, format='%f', value=example['start'], 
        help='Time shift from the beginning (in seconds)'
    )
    
    if url:
        try:
            with YoutubeDL({'format': 'best+bestaudio'}) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception as e:
            st.error(e)
        else:
            str_title = f"<div style='float: left; text-align: left; width=50%'>\
            **Title:** [{info['title']}]({url})</div>"
            str_duration = f"<div style='float: right; text-align: right; width=50%'>\
            **Overall Duration:** {info['duration']} sec.</div>"
            st.write(f"<small>{str_title + str_duration}</small>", 
                     unsafe_allow_html=True)

            video_url = info['requested_formats'][0]['url']
            audio_url = info['requested_formats'][1]['url']

            out, err = (
                ffmpeg
                .input(video_url, ss=start_from, t=5)
                .output('temp.mp4', vcodec='copy')
                .overwrite_output()
                .run()
            )
            st.video('temp.mp4')

            audio_data, err = (
                ffmpeg
                .input(audio_url, ss=start_from, t=6)
                .output('pipe:', format='wav')#, acodec='pcm_s16le')
                .run(capture_stdout=True)
            )
            audio_wav, audio_np = proc_raw_audio(audio_data)

            ui_processed_sound(audio_wav, audio_np)

def page_mic():
    '''Obtain audio from the microphone'''
    MIC_OPTIONS = {
        f'{v:02} - {k}': v for v, k in 
        enumerate(sr.Microphone.list_microphone_names())
    }  # list of all available mic devices

    expander_src = st.beta_expander('Choose source device')
    option_mic = expander_src.selectbox('Mic Source:', [*MIC_OPTIONS], index=1, 
                                        help='List of your available input devices')

    expander = st.beta_expander('Doubt what to say?')
    expander.write('Read the following: `Hello, my name is Random Tomato`')
    st.write('')

    r = sr.Recognizer()

    if st.button('⭕ Start speaking'):
        with sr.Microphone(device_index=MIC_OPTIONS[option_mic], 
                           sample_rate=SAMPLE_RATE) as source:
            with st.spinner('< ..speak now.. >'):
                audio = r.listen(source)

        recognized = recognize_GSR(r, audio)
        # recognized = recognize_GCS(r, audio)
        if recognized:
            st.info(recognized.capitalize())

        audio_data = audio.get_wav_data()
        audio_wav, audio_np = proc_raw_audio(audio_data)

        ui_processed_sound(audio_wav, audio_np, show_button=False)

def ui_processed_sound(audio_wav, audio_np, show_button=True):
    '''UI to show sound processing results'''
    _, center_h, _ = st.beta_columns([1, 1, 1])
    center_h.header('Processed Audio')

    st.audio(audio_wav)
    features = get_features(audio_np)
    
    if show_button:
        _, center, _ = st.beta_columns([1, 1, 1])
        if center.button('🔮 Recognize accent'):
            ui_recognition(features)
    else:
        ui_recognition(features)

def ui_recognition(features):
    '''Recognition UI interface'''
    with st.spinner('Predicting..'):
        probs, accent = recognize_accent(MODELS[option_model], features)

    st.success(f'💬 Accent: **`{accent.upper()}`**')
    
    # Compute and display prediction probabilities
    probs_df = pd.DataFrame.from_dict(MODELS[option_model].accents_dict, 
                                      orient='index', columns={'Accent'})
    probs_df['Probability'] = [f'{x:.4f}%' for x in probs]
    probs_df.set_index('Accent', inplace=True)
    probs_df.sort_values('Probability', ascending=False, inplace=True)
    
    st.write('🎲 Prediction Probabilities:')

    get_tone = lambda c: hex(int(255 - 255 * c))[2:]
    make_color = lambda c: f'#FFFF{get_tone(c)}'.ljust(7, '0')
    highlight_max = lambda cells: [
        f'background-color: {make_color(float(c[:-1]))}'
        for c in cells
    ]
    st.dataframe(probs_df.style.apply(highlight_max))


if __name__ == "__main__":
    ui_main()