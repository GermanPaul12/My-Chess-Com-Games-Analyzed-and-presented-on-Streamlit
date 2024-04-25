import streamlit as st
import pandas as pd

class Analysis:
    def __init__(self):
        self.data = pd.read_csv("data/data.csv", index_col=0)
    
    def total_games(self):
        return self.data.shape[0]    


st.set_page_config(page_title='Analysis',page_icon='📊')
st.title("Chess.com Games Analysis")
a = Analysis()

st.write(f"At the current moment I have played {a.total_games()} on chess.com")