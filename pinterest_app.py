# from pinterest_automation_script import run, sync_playwright as playwright
from scripts.helper import get_img_src_and_alts
from scripts.llm_helper import generate_response
import streamlit as st
from PIL import Image
import os
from uuid import uuid4

with st.sidebar:
    text= st.text_input(label="Enter the query")
    n= st.number_input(label="#images to consider", min_value=1)
    btn= st.button(label="Generate")
    



if btn:
    uid= uuid4().__str__()
    filename= f"media/{uid}.html"
    os.system(
        f'''python3 pinterest_automation_script.py  "{text}"  "{filename}"'''
    )

    with open(filename) as f:
        html= f.read()
        results= get_img_src_and_alts(html, n, uid)
        llm_response= generate_response(text, results=results)
        st.title("LLM_RESPONSE")
        st.json(llm_response)
        for data in results:
            # print(i)
            st.title("Image")
            
            st.image(data["image_source"])
            st.json(data)
            
      
    os.system(
        f"sudo rm media/{uid}.*"
    )
    