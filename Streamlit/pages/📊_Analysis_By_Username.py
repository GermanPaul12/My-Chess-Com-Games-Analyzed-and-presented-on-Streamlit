import csv
from datetime import datetime as dt
import streamlit as st
import pandas as pd
import plotly.express as px
from chessdotcom import get_player_game_archives, get_player_games_by_month
from chessdotcom import Client as ChessClient


class Analysis:
    def __init__(self, user):
        self.data = pd.read_csv("data/user.csv", index_col=0)
        self.user = user
    
    def total_games(self):
        return self.data.shape[0]   
    
    def percent_rated(self):
        return len(self.data[self.data.rated == True]) / self.total_games() * 100

    def games_won(self):
        return (len(self.data[(self.data.white_username == self.user) & (self.data.white_result == "win")]) + len(self.data[(self.data.black_username == self.user) & (self.data.black_result == "win")])) / self.total_games() * 100
    
    def games_lost(self):
        return 100 - self.games_won() 
    
    def games_with_white(self):
        return (len(self.data[(self.data.white_username == self.user)])) / self.total_games() * 100
    
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
        return max(max(self.data[self.data.white_username == self.user]["white_rating"]),max(self.data[self.data.black_username == self.user]["black_rating"]))

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
        data = self.data[(self.data["white_username"] == self.user) & (self.data['white_result'] == "win")]
        return data[data.black_rating == max(data.black_rating)][["black_rating", "black_username"]]
    
    def highest_black_opp_win(self):
        data = self.data[(self.data["black_username"] == self.user) & (self.data['black_result'] == "win")]
        return data[data.white_rating == max(data.white_rating)][["white_rating", "white_username"]]
    
    def add_column_my_rating(self) -> list:
        rating = []
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            if row.white_username == self.user:
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
    
def get_monthly_archives(username):
    ChessClient.request_config["headers"]["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
    return [url.strip().replace("'", "")[-7:].split("/") for url in str(get_player_game_archives(username))[30:-2].split(",")]


def get_games_by_month(username):
    ChessClient.request_config["headers"]["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
    id = 0
    games = {}
    for date_ in get_monthly_archives(username):
        year, month = date_
        for i, g in enumerate(get_player_games_by_month(username, year, month).json["games"]):
            try:
                data = {
                "id": id,
                "month": month,
                "year": year,
                "url": g["url"],
                "pgn": g["pgn"],
                "time_control": g["time_control"],
                "rated": g["rated"],
                "time_class": g["time_class"],
                "rules": g["rules"],
                "white_rating": g["white"]["rating"],
                "white_result": g["white"]["result"],
                "white_username": g["white"]["username"],
                "black_rating": g["black"]["rating"],
                "black_result": g["black"]["result"],
                "black_username": g["black"]["username"]
                }
                print("Inserting data:", data)  # Print out data for debugging
                games[id] = data
                id += 1
            except Exception as e:
                print("Error inserting data:", e)
                # Handle the exception here as per your requirement
    
    with open('data/user.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x  
        w = csv.DictWriter(f, games[0].keys())
        w.writeheader()
        for game in games.values():
            w = csv.DictWriter(f, game.keys())
            w.writerow(game)
    return games
    
st.set_page_config(page_title='Analysis',page_icon='📊', layout="wide")
st.title("Chess.com Games Analysis by Username")

text = st.text_input("Enter an username 👤")
if text and st.button("Collect data and start analysis"):
    st.warning("Data collection takes on average less than 1 minute it depends on the number of games of the player.")
    get_games_by_month(text)
    a = Analysis(text)
    with st.container(border=True):
        st.markdown("### :blue[A few facts] ♟")
        st.markdown(f"##### At the current moment {text} has played :green[{a.total_games()} games] on chess.com of which :green[{a.percent_rated():.2f}% were rated]")
        st.markdown(f"##### {text} won :green[{a.games_won():.2f}%] and lost :red[{a.games_lost():.2f}%] of the games he/she played")
        st.markdown(f"##### {text} played :blue[{a.games_with_white():.2f}%] of the games with the :blue[white pieces] and :blue[{a.games_with_black():.2f}%] with the :blue[black pieces]")
        st.markdown(f"##### Most games {text} had in the time format :blue[{a.most_played_time_format()[0]}] with :blue[{a.most_played_time_format()[1]}] games")
        st.markdown(f"##### Most played time control is :blue[{a.most_played_time_control()[0]}] with :blue[{a.most_played_time_control()[1]}] games")
        st.markdown(f"##### {text}'s peak rating is :green[{a.peak_rating()}] elo")
        st.markdown(f"##### With white {text}'s highest rated opponent against whom I won is :blue[{a.highest_white_opp_win()['black_username'].values[0]}] and the opponent's elo was :blue[{a.highest_white_opp_win()['black_rating'].values[0]}]")
        st.markdown(f"##### With black it is :blue[{a.highest_black_opp_win()['white_username'].values[0]}] and the opponent's elo was :blue[{a.highest_black_opp_win()['white_rating'].values[0]}]")


    with st.container(border=True):
        st.markdown("### :blue[Visualizations] 📈")
        opps = a.get_top_five_opponents()
        st.plotly_chart(px.bar(x=opps.index, y=opps.values, title=f"Top five opponents {text} had most games with", labels={'x': 'Usernames', 'y':'Match count'}))
        time_control = a.get_top_five_time_controls()
        st.plotly_chart(px.bar(x=time_control.index, y=time_control.values, title=f"Top five time controls {text} most played", labels={'x': 'Time control', 'y':'Match count'}))
        st.markdown(f"{text}'s rating charts for different time controls. Last rating in the chart corresponds to the latest game played in that time control.")
        a.add_created_columns()
        for t_class in set(a.data.time_class):  
            ratings = a.data[a.data.time_class == t_class][["dates", "my_rating"]]
            st.plotly_chart(px.line(x=ratings.dates, y=ratings.my_rating, title=t_class, labels={'x': 'Date', 'y':'Elo'}))