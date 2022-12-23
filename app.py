# import logging
# import logging.handlers
import queue
import threading
import time
import pandas as pd
from collections import deque
from pathlib import Path
from typing import List
from hotels import search
#import av
import numpy as np
#import pydub
import streamlit as st
import requests
from langdetect import detect, detect_langs



#create folium object

from streamlit.elements.utils import _shown_default_value_warning
_shown_default_value_warning = True


# HERE = Path(__file__).parent

# logger = logging.getLogger(__name__)
def trans(query,review):
    lang = detect(query)
    lang_r = detect(review) 
    
    

    reviews = review.split(".")
    rev = reviews[0:len(reviews)-1]
    if lang != 'en':
        trans_texts = ""
        for i in rev:
            url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" + lang_r + "&tl=" + lang + "&dt=t&q=" + i
            response = requests.get(url)
            result = response.text
            indexx = result.index('","')
            result = result[4:int(indexx)]
            trans_texts = trans_texts + result
    else:
           trans_texts = review
    return trans_texts   


def give_best_hotel(query: str,option: str):
    review,hotel,location,city= search(query)
    
    if option == 'First':
        review = trans(query,review[0])
        st.session_state.Reviews = review
        st.session_state.hotel_name = hotel[0] + " in" + " " + city[0]
        st.session_state.hotel_location = location[0]
        
    if option == 'Second':
        review = trans(query,review[1])
        st.session_state.Reviews = review
        st.session_state.hotel_name = hotel[1]  + " in" + " " + city[1]
        st.session_state.hotel_location = location[1]
    if option == 'Third':
        review = trans(query,review[2])
        st.session_state.Reviews = review
        st.session_state.hotel_name = hotel[2] + " in" + " " + city[2]
        st.session_state.hotel_location = location[2]
    if option == 'Fourth':
        review = trans(query,review[3])
        st.session_state.Reviews = review
        st.session_state.hotel_name = hotel[3] + " in" + " " + city[3]
        st.session_state.hotel_location = location[3]
    if option == 'Fifth':
        review = trans(query,review[4])
        st.session_state.Reviews = review
        st.session_state.hotel_name = hotel[4]  + " in" + " " + city[4]
        st.session_state.hotel_location = location[4]         
    # with tab1:
    return st.session_state.hotel_location 

def reset():

    st.session_state.hotel_name = " "
    st.session_state.Reviews = " "
    
       
    #  panel3_1=st.empty()
     
    #  panel3_1=st.write(review)      

    # with tab2:

    #  panel3_2=st.empty()
    #  panel3_2=st.write(hotel)  
    
    
 


def main():
    
    
        if "Reviews" not in st.session_state:
          st.session_state.Reviews = ""
        if "hotel_name" not in st.session_state:
          st.session_state.hotel_name = ""
        if "hotel_location" not in st.session_state:
           st.session_state.hotel_location = ""

        with st.sidebar:
            with st.expander('HotelRecommender'):
                st.image('nomad.jpeg')       
                st.markdown('HotelRecommender helps travellers to find best hotels along with some reviews by other customers according to their input description in a city using modern AI solutions. Users can type in English, German, Spanish languages etc..')
            
        st.header("HotelRecommender")
        st.markdown(
            """
            Making life easier for nomads!

            Recommends you the hotel with best reviews in city you want!!
    """
        )

    

        text_des= st.text_input(label = "Enter your description of hotel you need with in a city", placeholder = "A nice hotel in New York" )

        # tab5, tab6= st.tabs(["Best Reviews","Best Hotel Names"])

        option = st.selectbox('Which selection do you need to display from five matches',('First', 'Second', 'Third','Fourth','Fifth'))
        

        # st.text_area(label ="Hotel Review",value=" ", height =200,on_change=give_best_hotel, key='Reviews')
        # st.text_area(label ="Hotel Name",value=" ", height =1, on_change=give_best_hotel, key='hotel_name')
       #my_map= folium.Map(location=st.session_state.hotel_location)
        # with tab5:
        
        #     panel3_1=st.empty()
            

        # with tab6:

        #     panel3_2=st.empty()
        
        cap_button = st.button("Give best hotels", on_click=give_best_hotel, args=(text_des,option,)) # Give button a variable name
        if cap_button:
            map_data = pd.DataFrame({'lat': [st.session_state.hotel_location[0]], 'lon': [st.session_state.hotel_location[1]]})
            st.text_area(label ="Hotel Review",value=" ", height =200,on_change=give_best_hotel, key='Reviews')
            st.text_area(label ="Hotel Name",value=" ", height =1, on_change=give_best_hotel, key='hotel_name')
            st.map(map_data) 
            # m = folium.Map(location=st.session_state.hotel_location, zoom_start=30)
            # folium_static(m)
            # coordinates = tuple(st.session_state.hotel_location)
            # _map = gmaps.figure(center=coordinates, zoom_level=12)
            # snippet = embed.embed_snippet(views=_map)
            # html = embed.html_template.format(title="", snippet=snippet)
            # components.html(html, height=500,width=500)
        reset_button = st.button("Reset", on_click=reset)
    # if cap_button: # Make button a condition.
    #     # start_capture()
    #     st.text("Captured Successfully")
    
    






if __name__ == "__main__":
    import os

    # DEBUG = os.environ.get("DEBUG", "false").lower() not in ["false", "no", "0"]

    # logging.basicConfig(
    #     format="[%(asctime)s] %(levelname)7s from %(name)s in %(pathname)s:%(lineno)d: "
    #     "%(message)s",
    #     force=True,
    # )

    # logger.setLevel(level=logging.DEBUG if DEBUG else logging.INFO)

    # st_webrtc_logger = logging.getLogger("streamlit_webrtc")
    # st_webrtc_logger.setLevel(logging.DEBUG)

    # fsevents_logger = logging.getLogger("fsevents")
    # fsevents_logger.setLevel(logging.WARNING)
    main()