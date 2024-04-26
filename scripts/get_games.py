import streamlit as st
from chessdotcom import get_player_game_archives, get_player_games_by_month
from chessdotcom import Client as ChessClient
import csv

def get_monthly_archives(username="codinggambit"):
    ChessClient.request_config["headers"]["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
    return [url.strip().replace("'", "")[-7:].split("/") for url in str(get_player_game_archives(username))[30:-2].split(",")]


def get_games_by_month(username="codinggambit"):
    ChessClient.request_config["headers"]["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3"
    id = 0
    games = {}
    for date_ in get_monthly_archives():
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
      
    with open('data/data.csv', 'w') as f:  # You will need 'wb' mode in Python 2.x  
        w = csv.DictWriter(f, games[0].keys())
        w.writeheader()
        for game in games.values():
            w = csv.DictWriter(f, game.keys())
            w.writerow(game)
    return games
    
if __name__ == '__main__':
    get_games_by_month()