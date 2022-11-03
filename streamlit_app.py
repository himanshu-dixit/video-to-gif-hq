import pathlib
import subprocess
import os

import ffmpeg
import streamlit as st

# global variables
uploaded_mp4_file = None
uploaded_mp4_file_length = 0
filename = None
downloadfile = None

def save_uploaded_file(uploadedfile):
  with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
     f.write(uploadedfile.getbuffer())
  return st.success("Saved file :{} in tempDir".format(uploadedfile.name))

@st.experimental_memo
def convert_mp3_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    """
    It converts mp3 to wav using ffmpeg
    :param input_data: bytes object of a mp3 file
    :return: A bytes object of a wav file.
    """
    # print('convert_mp3_to_wav_ffmpeg_bytes2bytes')
    args = (ffmpeg
            .input('pipe:', format='mp3')
            .output('pipe:', format='wav')
            .global_args('-loglevel', 'error')
            .get_args()
            )
    # print(args)
    proc = subprocess.Popen(
        ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(input=input_data)[0]


@st.experimental_memo
def on_file_change(uploaded_mp4_file):
    print(uploaded_mp4_file)
    # with open("tmp/uploaded_mp4_file.mp4", "w") as f:   # Opens file and casts as f 
    #     f.write("Hello World form " + f.name) 

    save_uploaded_file(uploaded_mp4_file)
    output = subprocess.getoutput("ls -l")
    # return convert_mp3_to_wav_ffmpeg_bytes2bytes(uploaded_mp4_file.getvalue())


def on_change_callback():
    """
    It prints a message to the console. Just for testing of callbacks.
    """
    print(f'on_change_callback: {uploaded_mp4_file}')


# The below code is a simple streamlit web app that allows you to upload an mp3 file
# and then download the converted wav file.
if __name__ == '__main__':
    st.title('HQ Video to gif')
    st.markdown("""Convert video to gif with custom palette. Generally high quality""")

    uploaded_mp4_file = st.file_uploader('Upload Your MP4 File', type=['mp4'], on_change=on_change_callback, accept_multiple_files=0)

    if uploaded_mp4_file:
        uploaded_mp4_file_length = len(uploaded_mp4_file.getvalue())
        filename = pathlib.Path(uploaded_mp4_file.name).stem
        if uploaded_mp4_file_length > 0:
            st.text(f'"{uploaded_mp4_file.name}": {round(uploaded_mp4_file_length/(1000 * 1000),2)} Mb')
            downloadfile = on_file_change(uploaded_mp4_file)

    st.markdown("""---""")
    if downloadfile:
        length = len(downloadfile)
        if length > 0:
            st.subheader('After conversion to WAV you can download it below')
            button = st.download_button(label="Download .wav file",
                            data=downloadfile,
                            file_name=f'{filename}.wav',
                            mime='audio/wav')
            st.text(f'Size of "{filename}.wav" file to download: {length} bytes')
    st.markdown("""---""")