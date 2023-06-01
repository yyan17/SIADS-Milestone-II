# !/usr/bin/env python
import glob

import pandas as pd


def concatenate_csv_files(file_dir_path: str) -> pd.DataFrame:
    csv_files = glob.glob(f'{file_dir_path}/*.csv')

    concat_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)
    concat_df['Date'] = pd.to_datetime(concat_df['Date'], dayfirst=True)
    concat_df.sort_values(by='Date', inplace=True, ascending=True)
    return concat_df


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    HomeTeam = Home Team
    Away team = Away Team
    FTHG and HG = Full Time Home Team Goals
    FTAG and AG = Full-Time Away Team Goals
    FTR and Res = Full-Time Result (H=Home Win, D=Draw, A=Away Win)
    HTHG = Half Time Home Team Goals
    HTAG = Half Time Away Team Goals
    HTR = Half Time Result (H=Home Win, D=Draw, A=Away Win)

    Referee = Match Referee
    HS = Home Team Shots
    AS = Away Team Shots
    HST = Home Team Shots on Target
    AST = Away Team Shots on Target
    HC = Home Team Corners
    AC = Away Team Corners
    HF = Home Team Fouls Committed
    AF = Away Team Fouls Committed
    HY = Home Team Yellow Cards
    AY = Away Team Yellow Cards
    HR = Home Team Red Cards
    AR = Away Team Red Cards
    """
    return df[["HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR", "Referee", "HS", "AS",
               "HST", "AST", "HF", "AF", "HC", "AC", "HY", "AY", "HR", "AR"]].dropna().reset_index(drop=True)


if __name__ == "__main__":
    """
     For supervised learning, EPL datasets (2009-2022) should be combined into one. Raw datasets downloaded from 
     https://www.kaggle.com/datasets/saife245/english-premier-league?select=Datasets.
    """
    raw_csv_root_path = 'C:/your_home_dir/workspace/SIADS-Milestone-II/datasets/raw/supervised_learning'
    concatenated_df = concatenate_csv_files(raw_csv_root_path)
    normalized_df = drop_columns(concatenated_df)
    normalized_df.to_csv("sl_final.csv", index=False)
