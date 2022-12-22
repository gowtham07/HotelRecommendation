# import logging
# import logging.handlers
import queue
import threading
import time
import urllib.request
from collections import deque
from pathlib import Path
from typing import List
from hotels import search
#import av
import numpy as np
#import pydub
import streamlit as st
from streamlit.elements.utils import _shown_default_value_warning
_shown_default_value_warning = True
from streamlit_webrtc import WebRtcMode, webrtc_streamer

# HERE = Path(__file__).parent

# logger = logging.getLogger(__name__)


# This code is based on https://github.com/streamlit/demo-self-driving/blob/230245391f2dda0cb464008195a470751c01770b/streamlit_app.py#L48  # noqa: E501
def download_file(url, download_to: Path, expected_size=None):
    # Don't download the file twice.
    # (If possible, verify the download using the file length.)
    if download_to.exists():
        if expected_size:
            if download_to.stat().st_size == expected_size:
                return
        else:
            st.info(f"{url} is already downloaded.")
            if not st.button("Download again?"):
                return

    download_to.parent.mkdir(parents=True, exist_ok=True)

    # These are handles to two visual elements to animate.
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning("Downloading %s..." % url)
        progress_bar = st.progress(0)
        with open(download_to, "wb") as output_file:
            with urllib.request.urlopen(url) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    # We perform animation by overwriting the elements.
                    weights_warning.warning(
                        "Downloading %s... (%6.2f/%6.2f MB)"
                        % (url, counter / MEGABYTES, length / MEGABYTES)
                    )
                    progress_bar.progress(min(counter / length, 1.0))
    # Finally, we remove these visual elements by calling .empty().
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()

def give_best_hotel(query: str,option: str):
    review,hotel = search(query)
    
    if option == 'First':
        st.session_state.Reviews = review[0]
        st.session_state.hotel_name = hotel[0]
    if option == 'Second':
        st.session_state.Reviews = review[1]
        st.session_state.hotel_name = hotel[1]   
    if option == 'Third':
        st.session_state.Reviews = review[2]
        st.session_state.hotel_name = hotel[2] 
    if option == 'Fourth':
        st.session_state.Reviews = review[3]
        st.session_state.hotel_name = hotel[3]
    if option == 'Fifth':
        st.session_state.Reviews = review[4]
        st.session_state.hotel_name = hotel[4]            
    # with tab1:

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
        

        st.text_area(label ="Hotel Review",value=" ", height =200,on_change=give_best_hotel, key='Reviews')
        st.text_area(label ="Hotel Name",value=" ", height =50, on_change=give_best_hotel, key='hotel_name')
        # with tab5:
        
        #     panel3_1=st.empty()
            

        # with tab6:

        #     panel3_2=st.empty()
        
        cap_button = st.button("Give best hotels", on_click=give_best_hotel, args=(text_des,option,)) # Give button a variable name
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