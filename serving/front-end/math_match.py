import streamlit as st
from streamlit_cropper import st_cropper
import requests
from PIL import Image
import io
# from st_functions import st_button, load_css
# from streamlit_card import card
# from streamlit_option_menu import option_menu
import streamlit as st
from bokeh.models.widgets import Div
import webbrowser




backend_address = 'http://127.0.0.1:8502'


def load_image():
    image_data = st.file_uploader(label="Upload an image")
    if image_data is not None:
        return image_data
    else:
        return None


def OCR(image):
    files = {"file": image.getvalue()}
    response = requests.get(url = f"{backend_address}/OCR/", files=files)
    # pred = response.json()['pred'] # 이거 스게컴에서 보고 넣기
    return response

def DPR(latex_code):
    data = {"latex": latex_code}
    response = requests.get(url = f"{backend_address}/Search/", json=data)
    return response

def move_page(link):
        js = f"window.open({link})"  # New tab or window
        js = f"window.location.href = {link}"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)   

def main():
    st.title("MATH MATCH")
    st.write("### 수식 인식 및 검색 서비스")
  
    # st.write("### Formula Recognition & Search Service")
    header = "입력 이미지"
    image_file = load_image()
    if image_file == None:
        st.error("수식 이미지를 입력해주세요.")
    else:
        crop_flag = st.checkbox(label="Crop the image", value=False)
        if crop_flag:
            st.subheader("원본 이미지")
            image = Image.open(image_file)
            image = st_cropper(image, box_color='#595959', aspect_ratio=None)
            cropped_img_pth = 'C:\GOME\pix2tex\pix2tex\serving\cropped_imgs\cropped_img'
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            image_file = img_byte_arr
            header = "선택된 이미지"
        image = Image.open(image_file)
        st.subheader(header)
        st.image(image)
        st.write('---')
        if st.button('Convert'):
            with st.spinner('Converting...'):
                # 수식 인식
                ocr_res = OCR(image_file)
            if ocr_res.ok:
                latex = ocr_res.json()
                # if 'latex_code' not in st.session_state:
                st.session_state['latex_code'] = latex
                st.markdown("### LaTeX Code")
                st.markdown(f'$\\displaystyle {latex}$')
                st.code(latex, language='latex')
            else:
                st.error(ocr_res.text)

        if st.button('Search'):
            # 검색
            # st.write(st.session_state['latex_code'])
            latex = st.session_state['latex_code']
            st.subheader("LaTeX Code")
            st.markdown(f'$\\displaystyle {latex}$')
            st.code(latex, language='latex')
            search_res = DPR(st.session_state['latex_code'])
            st.write("---")
            if search_res.ok:
                result = search_res.json()
                st.subheader("검색 결과")
                exists = []
                rank, i = 1, 0
                while rank <= 5:
                    i += 1
                    idx = str(i)
                    title = result[idx]['title']
                    link = result[idx]['link']
                    summary = result[idx]['summary']
                    latex = result[idx]['latex']
                    if title in exists:
                        continue
                    exists.append(title)
                    # st.markdown(f"#### [{i}](f{link}). {title}")
                    # st.markdown(f'$\\displaystyle {latex}$')
                    form = st.form(key=idx)
                    with form:
                        if len(summary) > 200:
                            st.markdown(f"#### {rank}. {title}")
                            st.markdown(f'$\\displaystyle {latex}$')
                            st.write(summary[:200] + '...')
                            # st.info(summary[:200] + '...')
                        else:
                            st.markdown(f"#### {rank}. {title}")
                            st.markdown(f'$\\displaystyle {latex}$')
                            st.write(summary)
                            # st.info(summary)
                        move_link = st.form_submit_button('Web Page', on_click = move_page(link))
                        # if move_link:
                        #     js = "window.open('https://www.streamlit.io/')"  # New tab or window
                        #     js = "window.location.href = 'https://www.streamlit.io/'"  # Current tab
                        #     html = '<img src onerror="{}">'.format(js)
                        #     div = Div(text=html)
                        #     st.bokeh_chart(div)   
                    rank += 1
                    # if int(i) % 2 == 0:
                    #     col1.markdown("### title")
                    #     col1.info(summary)
                    # else:
                    #     col2.subheader(title)
                    #     col2.info(summary)
                    # st_button(link, summary, title)

            else:
                st.info(search_res.text)

if __name__=='__main__':
    # load_css()
    main()
