# Automated Chess Game Analyzer

Welcome to the Chess Game Analyzer project! This repository contains over 3800 chess games collected from chess.com and analyzed using various techniques. The results of the analysis are presented in a Streamlit web application for easy exploration and visualization.

## Overview

Chess is a game of strategy and tactics, and analyzing games played by skilled players can provide valuable insights into different opening strategies, tactical patterns, and endgame techniques. In this project, I have collected a large dataset of chess games from chess.com and performed detailed analysis on them.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chesscom.streamlit.app/)

## Features

- **Large Dataset**: The dataset consists of over 3800 chess games played by players of varying skill levels.
- **Analysis**: The games are analyzed using state-of-the-art techniques to extract valuable information such as opening moves, common tactics, and endgame patterns.
- **Streamlit Web Application**: The results of the analysis are presented in an interactive web application built with Streamlit, allowing users to explore the data easily.
- **Up-to-date data**: The dataset is updated everyday at midnight through Github Actions.
- **Analyze your own games**: Conveniently insert your username and get your own analysis.

## How to Use locally

1. **Clone the Repository**: Clone this repository to your local machine using the following command:

    ``` bash
    git clone https://github.com/GermanPaul12/My-Chess-Com-Games-Analyzed-and-presented-on-Streamlit
    ```

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies:

    ``` bash
    cd My-Chess-Com-Games-Analyzed-and-presented-on-Streamlit
    pip install -r requirements.txt
    ```

3. **Change username**: Insert your own username under `/scripts` in the `get_names.py`:

    - Replace `codinggambit` with your own username
    - Alternatively you can skip this part completely and use the page Analysis by Username for that you can proceed with step 4

4. **Run the Web Application**: Start the Streamlit web application by running the following command:

    ``` bash
    streamlit run 🏠_Home.py
    ```

This will launch the web application in your default web browser, allowing you to interactively explore the analyzed chess games.

## Contributors

- [German Paul](https://github.com/GermanPaul12)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

We would like to thank chess.com for providing access to their API for collecting the chess game data used in this project. Additionally, we acknowledge the contributions of the open-source community, whose tools and libraries have been instrumental in the analysis and visualization of the chess games.

Feel free to explore the repository, contribute improvements, or use the analysis results for your own research or projects. Happy analyzing!
