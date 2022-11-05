import pathlib
import subprocess
import os
import random

import ffmpeg
import streamlit as st

# global variables
uploaded_mp4_file = None
uploaded_mp4_file_length = 0
filename = None
downloadfile = None

def save_uploaded_file(uploadedfile):
  random_string = str(random.randint(0, 9999999)) + "-"
  tmp_file_name = random_string + uploadedfile.name
  if not os.path.exists("tmp"):
    os.makedirs("tmp")
  with open(os.path.join("tmp",tmp_file_name),"wb") as f:
     f.write(uploadedfile.getbuffer())
  return tmp_file_name

@st.experimental_memo
def on_file_change(uploaded_mp4_file):
    print(uploaded_mp4_file)
    file_name = save_uploaded_file(uploaded_mp4_file)

    output = subprocess.getoutput("./convert_mp4_to_gif.sh ./tmp/"+file_name)
    gif_file_name = "./tmp/"+file_name+".gif"

    return gif_file_name


def on_change_callback():
    """
    It prints a message to the console. Just for testing of callbacks.
    """
    print(f'on_change_callback: {uploaded_mp4_file}')


# The below code is a simple streamlit web app that allows you to upload an mp3 file
# and then download the converted wav file.
if __name__ == '__main__':
    st.title('HQ Video to gif')
    st.markdown("""📺 Gif from video with custom rgb palette with floyd steinberg dithering""")
    uploaded_mp4_file = st.file_uploader('Upload Your MP4 File', type=['mp4'], on_change=on_change_callback, accept_multiple_files=0)

    if uploaded_mp4_file:
        uploaded_mp4_file_length = len(uploaded_mp4_file.getvalue())
        filename = pathlib.Path(uploaded_mp4_file.name).stem
        if uploaded_mp4_file_length > 0:
            st.text(f'📺 Generating gif from video "{uploaded_mp4_file.name}": {round(uploaded_mp4_file_length/(1000 * 1000),2)} Mb')
            downloadfile = on_file_change(uploaded_mp4_file)

    st.markdown("""---""")
    if downloadfile:
        data = open(downloadfile,'rb')
        length = 1
        if length > 0:
            st.subheader('Download gif from below')
            button = st.download_button(label="Download your HQ .gif file",
                            data=data,
                            file_name=f'{filename}.gif')
            st.text(f'Size of "{filename}.gif" file to download')
    st.markdown("""---""")