# from pinterest_automation_script import run, sync_playwright as playwright
from helper import get_img_src_and_alts
import streamlit as st
from PIL import Image
import os

with st.sidebar:
    text= st.text_input(label="Enter the query")
    n= st.number_input(label="#images to consider", min_value=1)
    btn= st.button(label="Generate")
    



if btn:
    os.system(
        f'''python3 pinterest_automation_script.py q "{text}" '''
    )

    with open("temp.html") as f:
        html= f.read()
        zipped_tuple= get_img_src_and_alts(html, n)
        for i in zipped_tuple:
            # print(i)
            st.title("Image")
            data= {
                "blip_caption": i[0],
                "inner_page_alt_text": i[1],
                "outer_page_alt_text": i[2],
                "image_url": i[3],
            }
            st.image(data["image_url"])
            st.json(data)
    