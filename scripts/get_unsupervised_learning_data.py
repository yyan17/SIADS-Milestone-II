# !/usr/bin/env python
import glob
import os

import pandas as pd


def concatenate_csv_files(file_dir_path: str) -> pd.DataFrame:
    csv_files = glob.glob(f'{file_dir_path}/*.csv')
    return pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)


def select_columns(df: pd.DataFrame, selected_columns: list, drop=False) -> pd.DataFrame:
    """
    Team = Team name,
    # Pl = number of players,
    Age = Age,
    Poss = Possession,
    Gls = Goals,
    Ast = Assists,
    G-PK = Goals - Penalty Kicks,
    PK = Penalty Kicks,
    PKatt = Penalty Kicks Attempted,
    CrdY = Cautions - Yellow Cards,
    CrdR = Cautions - Red Cards
    """
    if drop:
        df.drop(selected_columns, axis=1, inplace=True)
    else:
        df = df[selected_columns]

    return df.dropna().reset_index(drop=True)


def get_team_data(root_path: str) -> None:
    raw_team_csv_path = 'teams/fbref.com'
    team_cols = ['Team', '# Pl', 'Age', 'Poss', 'Gls', 'Ast', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'Gls_Conceded',
                 'Ast_Conceded', 'G-PK_Conceded', 'PK_Conceded', 'PKatt_Conceded', 'CrdY_Conceded', 'CrdR_Conceded']
    team_concatenated_df = concatenate_csv_files(os.path.join(root_path, raw_team_csv_path))
    normalized_team_df = select_columns(team_concatenated_df, team_cols)
    normalized_team_df.to_csv("ul_team_final.csv", index=False)


def get_player_data(root_path: str) -> None:
    raw_player_csv_path = 'players/EnglishPremierLeague/'
    player_cols = ['Unnamed: 0', 'team_x', 'tournament', 'assists', 'intercepts', 'team_y', 'Shirt Number',
                   'Nationality', 'Positions']
    player_concatenated_df = concatenate_csv_files(os.path.join(root_path, raw_player_csv_path))
    normalized_player_df = select_columns(player_concatenated_df, player_cols, drop=True)
    normalized_player_df.to_csv("ul_player_final.csv", index=False)


if __name__ == "__main__":
    """
     For unsupervised learning, EPL team datasets (2016-2022) should be combined into one. EPL player's performance 
     datasets should be concatenated based on their team. 
     Raw datasets can be crawled from https://1xbet.whoscored.com.
    """
    root_path = 'C:/your_home_dir/workspace/SIADS-Milestone-II/datasets/raw/unsupervised_learning'
    get_team_data(root_path)
    get_player_data(root_path)


