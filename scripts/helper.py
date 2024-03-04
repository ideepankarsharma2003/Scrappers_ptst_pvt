from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
import os
from keys import HF_API_KEY

def find_comments(soup_html: BeautifulSoup):
    comments_target_class= "lH1 dyH iFc H2s bwj X8m zDA IZT".split()
    for h2 in soup_html.find_all("h2"):
        cls= h2.get("class", "")
        if cls==comments_target_class:
            return h2.text
    return 0
        
        
def find_followers(soup_html:BeautifulSoup):
    followers_target_class= "tBJ dyH iFc j1A X8m zDA IZT swG".split()
    for div in soup_html.find_all("div"):
        cls= div.get("class", "")
        if cls==followers_target_class:
            return div.text
    return 0


def get_internal_alt_text(
    pinterest_page: str,
    base_file: str
):
    alt_internal= None
    try:
        soup_internal= BeautifulSoup(requests.get(pinterest_page).content, features="html.parser")
        followers= find_followers(soup_internal)
        comments= find_comments(soup_internal)
        
        all_imgs= soup_internal.find_all("img")
        for img in all_imgs:
            src= img.get("src", "none")
            if os.path.basename(src)==base_file:
                alt_internal= img.get("alt", None)
                break
    except Exception as e:
        print(e)
    finally:
        return {
                "internal_alt_text": alt_internal,
                "followers": followers,
                "comments": comments, 
                "pinterest": pinterest_page
                }
    



import json
import requests
import time
headers = {"Authorization": f"Bearer {HF_API_KEY}"}
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"



def query(filename, tries=0):
    if tries==3:
        return 
    
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    response= json.loads(response.content.decode("utf-8"))
    
    try:
        alt_text= response[0]['generated_text']
    except:
        print("""
              [Model is Loading, Going for Sleep of 20 seconds]
              """)
        time.sleep(20)
        query(filename=filename, tries=tries+1)
        alt_text= response
    
    finally:
        return alt_text
        






def get_img_src_and_alts(
    soup_content:str,
    n: int,
    uid:str="temp"
):
    soup= BeautifulSoup(markup=soup_content, features="html.parser")
    all_anchors= soup.find_all("a")[::2] # because the anchors are in image and labels both, use only one
    top_n_anchors= all_anchors[:n]
    # top_n_images= soup.find_all("img")[:n]
    
    results= []

    for anchor in tqdm(top_n_anchors):
        img= anchor.find("img")        
        alt= img.get("alt", "None")
        src= img.get("src", "None")
        base_file= os.path.basename(src)
        
        link= f"https://pinterest.com{anchor['href']}"        
        page_data= get_internal_alt_text(link, base_file)
        
        
        
        
        
        filename= f"media/{uid}.jpeg"
        with open(filename, "wb") as f:
            f.write(requests.get(url=src).content)
        
        alt_text= query(filename)
        
        
        
        page_data["image_source"]=src            
        page_data["image_outer_alt_text"]= alt
        page_data["blip_alt_text"]= alt_text
        
        
        results.append(page_data)
    return results
    
    
    
    
    
