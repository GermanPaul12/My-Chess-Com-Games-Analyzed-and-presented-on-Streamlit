from datetime import datetime as dt
import streamlit as st
import pandas as pd
import plotly.express as px

class Analysis:
    def __init__(self):
        self.data = pd.read_csv("data/data.csv", index_col=0)
    
    def total_games(self):
        return self.data.shape[0]   
    
    def percent_rated(self):
        return len(self.data[self.data.rated == True]) / self.total_games() * 100

    def games_won(self):
        return (len(self.data[(self.data.white_username == "CodingGambit") & (self.data.white_result == "win")]) + len(self.data[(self.data.black_username == "CodingGambit") & (self.data.black_result == "win")])) / self.total_games() * 100
    
    def games_lost(self):
        return 100 - self.games_won() 
    
    def games_with_white(self):
        return (len(self.data[(self.data.white_username == "CodingGambit")])) / self.total_games() * 100
    
    def games_with_black(self):
        return 100 - self.games_with_white()
    
    def most_played_time_format(self):
        for time_format, count in self.data.time_class.value_counts().items(): return time_format, count
        
    def most_played_time_control(self):
        for time_control, count in self.data.time_control.value_counts().items():
            return self.get_cleaned_time_control(time_control, count)
            
    def get_cleaned_time_control(self, time_control, count):
        if "+" in time_control:
            times = time_control.split("+")
            mins = int(times[0]) // 60
            secs = int(times[1])
            return f"{mins} minutes + {secs} {'seconds' if secs > 1 else 'second'} increment", count
        elif "/" in time_control:
            days = int(time_control.split("/")[1]) // 60 // 60 //24
            return f"{days} {'days' if days > 1 else 'day'} per turn", count
        else:
            return f"{int(time_control) // 60} minutes", count  
                

    def peak_rating(self):
        return max(max(self.data[self.data.white_username == "CodingGambit"]["white_rating"]),max(self.data[self.data.black_username == "CodingGambit"]["black_rating"]))

    def get_top_five_opponents(self):
        opps = self.data.white_username.value_counts()
        for name,val in self.data.black_username.value_counts().items():
            if name in opps:
                opps[name] += val
            else: opps[name] = val    
        return opps[1:6]
    
    def get_top_five_time_controls(self):
        data = self.data.time_control.value_counts()[:5]
        indexes = []
        for i in range(5):
            indexes.append(self.get_cleaned_time_control(data.index[i], data.iloc[i])[0])
        data = data.set_axis(indexes)    
        return data
    
    def highest_white_opp_win(self):
        data = self.data[(self.data["white_username"] == "CodingGambit") & (self.data['white_result'] == "win")]
        return data[data.black_rating == max(data.black_rating)][["black_rating", "black_username"]]
    
    def highest_black_opp_win(self):
        data = self.data[(self.data["black_username"] == "CodingGambit") & (self.data['black_result'] == "win")]
        return data[data.white_rating == max(data.white_rating)][["white_rating", "white_username"]]
    
    def add_column_my_rating(self) -> list:
        rating = []
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            if row.white_username == "CodingGambit":
                rating.append(row.white_rating)
            else:
                rating.append(row.black_rating)
        self.data["my_rating"] = rating
        return rating
    
    def add_column_date(self):
        dates = []
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            date = dt(year=row.year, month=row.month, day=1)
            dates.append(date)
        self.data["dates"] = dates
        return dates    
        
    def add_created_columns(self):
        self.add_column_my_rating()
        self.add_column_date()
        return None    
    
st.set_page_config(page_title='Analysis',page_icon='📊', layout="wide")
st.title("Chess.com Games Analysis")
a = Analysis()

with st.container(border=True):
    st.markdown("### :blue[A few facts] ♟")
    st.markdown(f"##### At the current moment I have played :green[{a.total_games()} games] on chess.com of which :green[{a.percent_rated():.2f}% were rated]")
    st.markdown(f"##### I won :green[{a.games_won():.2f}%] and lost :red[{a.games_lost():.2f}%] of the games I played")
    st.markdown(f"##### I played :blue[{a.games_with_white():.2f}%] of the games with the :blue[white pieces] and :blue[{a.games_with_black():.2f}%] with the :blue[black pieces]")
    st.markdown(f"##### Most games I had in the time format :blue[{a.most_played_time_format()[0]}] with :blue[{a.most_played_time_format()[1]}] games")
    st.markdown(f"##### Most played time control is :blue[{a.most_played_time_control()[0]}] with :blue[{a.most_played_time_control()[1]}] games")
    st.markdown(f"##### My peak rating is :green[{a.peak_rating()}] elo")
    st.markdown(f"##### With white my highest rated opponent against whom I won is :blue[{a.highest_white_opp_win()['black_username'].values[0]}] and the opponent's elo was :blue[{a.highest_white_opp_win()['black_rating'].values[0]}]")
    st.markdown(f"##### With black it is :blue[{a.highest_black_opp_win()['white_username'].values[0]}] and the opponent's elo was :blue[{a.highest_black_opp_win()['white_rating'].values[0]}]")


with st.container(border=True):
    st.markdown("### :blue[Visualizations] 📈")
    opps = a.get_top_five_opponents()
    st.plotly_chart(px.bar(x=opps.index, y=opps.values, title="Top five opponents I had most games with", labels={'x': 'Usernames', 'y':'Match count'}))
    time_control = a.get_top_five_time_controls()
    st.plotly_chart(px.bar(x=time_control.index, y=time_control.values, title="Top five time controls I most played", labels={'x': 'Time control', 'y':'Match count'}))
    st.markdown("My rating charts for different time controls. Last rating in the chart corresponds to the latest game played in that time control.")
    a.add_created_columns()
    for t_class in set(a.data.time_class):  
        ratings = a.data[a.data.time_class == t_class][["dates", "my_rating"]]
        st.plotly_chart(px.line(x=ratings.dates, y=ratings.my_rating, title=t_class, labels={'x': 'Date', 'y':'Elo'}))