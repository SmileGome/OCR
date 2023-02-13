import streamlit as st
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from st_functions import st_button
from PIL import Image

st.set_page_config(page_icon='🐻' ,layout="wide")

def main():
    st.title("GOME")
    # st.sidebar.markdown("# GOME")
    col1, col2, col3 = st.columns(3)
    img1 = Image.open('C://GOME//pix2tex//pix2tex//serving//front-end//pages//강지우.png')
    col1.image(img1.resize((300, 300)))
    col1.markdown("<h2 style='text-align: center;'>강지우</h2>", unsafe_allow_html=True)
    img2 = Image.open('C://GOME//pix2tex//pix2tex//serving//front-end//pages//곽지윤.png')
    col2.image(img2.resize((300, 300)))
    col2.markdown("<h2 style='text-align: center;'>곽지윤</h2>", unsafe_allow_html=True)
    img3 = Image.open('C://GOME//pix2tex//pix2tex//serving//front-end//pages//김윤혜.png')
    col3.image(img3.resize((300, 300)))
    col3.markdown("<h2 style='text-align: center;'>김윤혜</h2>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()