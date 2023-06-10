# !/usr/bin/env python
import glob

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
    raw_team_csv_path = f'teams/fbref.com'

    for year in ['2016-2017', '2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']:
        df1 = pd.read_csv(f'{root_path}/{raw_team_csv_path}/{year}_PPM.csv')
        df2 = pd.read_csv(f'{root_path}/{raw_team_csv_path}/team_stats_{year}.csv')
        df_merged = df1.merge(df2, on="Team", how='inner')
        df_merged.to_csv(f"{root_path}/{raw_team_csv_path}/merged/{year}_merged.csv")

    team_cols = ['Team', '# Pl', 'Age', 'Poss', 'Gls', 'Ast', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR', 'Gls_Conceded',
                 'Ast_Conceded', 'G-PK_Conceded', 'PK_Conceded', 'PKatt_Conceded', 'CrdY_Conceded', 'CrdR_Conceded', 'Pts/MP']
    team_concatenated_df = concatenate_csv_files(f'{root_path}/{raw_team_csv_path}/merged')
    merged_team_df = select_columns(team_concatenated_df, team_cols)

    cols_to_norm = team_cols[1:]
    merged_team_df[cols_to_norm] = merged_team_df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    merged_team_df.to_csv("ul_team_final.csv", index=False)


def get_player_data(root_path: str) -> None:
    raw_player_csv_path = 'players/EnglishPremierLeague/'
    player_cols = ['Unnamed: 0', 'team_x', 'tournament', 'assists', 'intercepts', 'team_y', 'Shirt Number',
                   'Nationality', 'Positions']
    player_concatenated_df = concatenate_csv_files(f'{root_path}/{raw_player_csv_path}')
    merged_player_df = select_columns(player_concatenated_df, player_cols, drop=True)
    cols_to_norm = ['mins','goals','yels','reds','shoots_per_game','pass_success','overall_ratings','tackles','fouls',
                    'offsides_won','clear','drb','blocks','key_pass','drb_won','fouls_given','offsides_given',
                    'dispossessed','turnover','total_pass','crosses','long_pass','rating_1','rating_2','rating_3',
                    'rating_4','rating_5','rating_6','rating_7','rating_8','rating_9','rating_10']
    merged_player_df[cols_to_norm] = merged_player_df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    merged_player_df.to_csv("ul_player_final.csv", index=False)


if __name__ == "__main__":
    """
     For unsupervised learning, EPL team datasets (2016-2022) should be combined into one. EPL player's performance 
     datasets should be concatenated based on their team. 
     Raw datasets can be crawled from https://1xbet.whoscored.com.
    """
    root_path = 'C:/your_home_dir/workspace/SIADS-Milestone-II/datasets/raw/unsupervised_learning'
    get_team_data(root_path)
    get_player_data(root_path)


