import pandas as pd
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

API_DELAY_TERM = 10


def web_driver():
    driver = webdriver.Chrome('chromedriver')
    driver.maximize_window()
    return driver


def replace_pd(df):
    mapping = {'-': 0}
    replace_dict = {}

    for column in df.columns:
        replace_dict[column] = mapping

    return df.replace(replace_dict)


def is_ready(driver):
    return driver.execute_script(r"""
        return document.readyState === 'complete'
    """)


def get_text_strip(element):
    if element:
        return element.text.strip()
    return 'No Element'


def crawling_stat(team_url):
    team_driver = web_driver()
    team_driver.get(team_url)
    time.sleep(API_DELAY_TERM)
    WebDriverWait(team_driver, 20).until(is_ready)

    # make pandas dataframe
    summary_columns = ['Team', '# Pl', 'Age', 'Poss', 'Gls', 'Ast', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR',
                       'xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP']

    opponent_columns = ['Team', 'Gls_Conceded', 'Ast_Conceded', 'G-PK_Conceded', 'PK_Conceded', 'PKatt_Conceded',\
                        'CrdY_Conceded', 'CrdR_Conceded', 'xG_Conceded', 'npxG_Conceded', 'xAG_Conceded',\
                        'npxG+xAG_Conceded', 'PrgC_Conceded', 'PrgP_Conceded']

    team_df_summary = pd.DataFrame(columns=summary_columns)
    team_df_opponent = pd.DataFrame(columns=opponent_columns)



    # team_summary_stats
    summary_elements = team_driver.find_element(By.ID, 'stats_squads_standard_for')\
        .find_element(By.CSS_SELECTOR, "tbody")\
        .find_elements(By.CSS_SELECTOR, "tr")

    print(summary_elements)
    for i, element in enumerate(summary_elements):
        print(i)
        team_dict = {'Team': get_text_strip(element.find_element(By.CSS_SELECTOR, "th"))}

        td_elements = element.find_elements(By.CSS_SELECTOR, "td")

        team_dict['# Pl'] = get_text_strip(td_elements[0])
        team_dict['Age'] = get_text_strip(td_elements[1])
        team_dict['Poss'] = get_text_strip(td_elements[2])
        team_dict['Gls'] = get_text_strip(td_elements[7])
        team_dict['Ast'] = get_text_strip(td_elements[8])
        team_dict['G-PK'] = get_text_strip(td_elements[10])
        team_dict['PK'] = get_text_strip(td_elements[11])
        team_dict['PKatt'] = get_text_strip(td_elements[12])
        team_dict['CrdY'] = get_text_strip(td_elements[13])
        team_dict['CrdR'] = get_text_strip(td_elements[14])
        team_dict['xG'] = get_text_strip(td_elements[15])
        team_dict['npxG'] = get_text_strip(td_elements[16])
        team_dict['xAG'] = get_text_strip(td_elements[17])
        team_dict['npxG+xAG'] = get_text_strip(td_elements[18])
        team_dict['PrgC'] = get_text_strip(td_elements[19])
        team_dict['PrgP'] = get_text_strip(td_elements[20])

        print(team_dict)
        # add disctionary date to dataframe
        team_df_summary.loc[len(team_df_summary)] = team_dict

    # to get opponent's stats
    # opponent_info = team_driver.find_element(By.XPATH, "/html/body/div[2]/div[6]/div[2]/div[3]/div[2]")
    # opponent_link = opponent_info.find_element(By.CSS_SELECTOR, "a")
    opponent_link = team_driver.find_element(By.XPATH, "/html/body/div[2]/div[6]/div[2]/div[3]/div[2]/a")
    print(opponent_link)
    opponent_link.click()
    time.sleep(API_DELAY_TERM)

    opponent_elements = team_driver.find_element(By.ID, 'stats_squads_standard_against')\
        .find_element(By.CSS_SELECTOR, "tbody")\
        .find_elements(By.CSS_SELECTOR, "tr")

    for i, element in enumerate(opponent_elements):
        print(i)
        team_dict = {'Team': get_text_strip(element.find_element(By.CSS_SELECTOR, "th"))[3:]}

        td_elements = element.find_elements(By.CSS_SELECTOR, "td")

        team_dict['Gls_Conceded'] = get_text_strip(td_elements[7])
        team_dict['Ast_Conceded'] = get_text_strip(td_elements[8])
        team_dict['G-PK_Conceded'] = get_text_strip(td_elements[10])
        team_dict['PK_Conceded'] = get_text_strip(td_elements[11])
        team_dict['PKatt_Conceded'] = get_text_strip(td_elements[12])
        team_dict['CrdY_Conceded'] = get_text_strip(td_elements[13])
        team_dict['CrdR_Conceded'] = get_text_strip(td_elements[14])
        team_dict['xG_Conceded'] = get_text_strip(td_elements[15])
        team_dict['npxG_Conceded'] = get_text_strip(td_elements[16])
        team_dict['xAG_Conceded'] = get_text_strip(td_elements[17])
        team_dict['npxG+xAG_Conceded'] = get_text_strip(td_elements[18])
        team_dict['PrgC_Conceded'] = get_text_strip(td_elements[19])
        team_dict['PrgP_Conceded'] = get_text_strip(td_elements[20])

        print(team_dict)
        # add disctionary date to dataframe
        team_df_opponent.loc[len(team_df_opponent)] = team_dict

    print('summary', team_df_summary)
    print('opponent', team_df_opponent)
    team_df = team_df_summary.merge(team_df_opponent, on='Team')

    print('team', team_df)

    # close webdriver
    team_driver.close()

    return replace_pd(team_df)


def save_team(league):
    """
    make player data and save

    prameter  -----------------------------------------------------
    league : you want to save league name of players

    """

    years = ['2019-2020', '2020-2021', '2021-2022']

    # years = ['2016-2017']
    # get team dataframe function
    def get_team_df(year):
        stat_url = f'https://fbref.com/en/comps/9/{year}/stats/{year}-Premier-League-Stats'
        stat_df = crawling_stat(stat_url)
        return stat_df

    for year in years:
        print(f"--- start collecting data : {year}")
        data = get_team_df(year)
        data.to_csv(f"../datasets/raw/unsupervised_learning/teams/fbref.com/team_stats_{year}.csv")
        print(f"--- finished data collection for {year} -" * 35)


if __name__ == "__main__":
    print('start runscript...')
    save_team('EnglishPremierLeague')
