from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import os
from keys import HF_API_KEY


def get_internal_alt_text(
    pinterest_page: str,
    base_file: str
):
    alt_internal= None
    try:
        soup_internal= BeautifulSoup(requests.get(pinterest_page).content, features="html.parser")
        all_imgs= soup_internal.find_all("img")
        for img in all_imgs:
            src= img.get("src", "none")
            if os.path.basename(src)==base_file:
                alt_internal= img.get("alt", None)
                break
    except Exception as e:
        print(e)
    finally:
        return alt_internal
    



import json
import requests
headers = {"Authorization": f"Bearer {HF_API_KEY}"}
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))



def get_img_src_and_alts(
    soup_content:str,
    n: int
):
    soup= BeautifulSoup(markup=soup_content, features="html.parser")
    all_anchors= soup.find_all("a")[::2] # because the anchors are in image and labels both, use only one
    top_n_anchors= all_anchors[:n]
    # top_n_images= soup.find_all("img")[:n]
    image_sources= []
    image_original_alt_texts= []
    image_original_alt_texts_internal= []
    image_alt_texts= []

    for anchor in tqdm(top_n_anchors):
        img= anchor.find("img")        
        alt= img.get("alt", "None")
        src= img.get("src", "None")
        base_file= os.path.basename(src)
        
        link= f"https://pinterest.com{anchor['href']}"        
        main_alt= get_internal_alt_text(link, base_file)
        
        image_original_alt_texts_internal.append(main_alt)
        image_sources.append(src)
        image_original_alt_texts.append(alt)
        
        filename= "temp.jpeg"
        with open(filename, "wb") as f:
            f.write(requests.get(url=src).content)
        try: 
            response= query(filename)
            alt_text= response[0]['generated_text']
        except:
            alt_text= response
        image_alt_texts.append(alt_text)
        

        
        
    return zip(image_alt_texts, image_original_alt_texts_internal, image_original_alt_texts, image_sources)
    
    
    
    
    
