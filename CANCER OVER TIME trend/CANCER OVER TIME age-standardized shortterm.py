'''
==short term trend 구하는 코드==
- Last update: 2024.07.18
- You need: *_age-standardized rate_trend.csv (from 'CANCER OVER TIME crolling.py')
- Steps
  1. *_age-standardized rate_trend.csv 파일을 업로드하고, 결과물을 저장할 위치를 지정한다.
  2. 저장된 데이터를 확인한다.
'''

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
import os

def upload_file():
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(title="Upload *_age-standardized rate_trend.csv", filetypes=[("csv", "*.csv")])
    root.destroy()

    if file_path:
        file_name = os.path.basename(file_path)
        df = pd.read_csv(file_path)
    else:
        print("file이 선택되지 않았습니다.")
        exit(1)
        
    return df, file_name

def saving_directory():
    root = Tk()
    root.withdraw()
    directory_path = askdirectory(title="Select saving directory")
    root.destroy()

    if directory_path:
        return directory_path
    else:
        print("directory가 선택되지 않았습니다.")
        exit(1)

def shortterm(df_sub, term):
    df_new = pd.DataFrame(columns = ['Country', 'Sex', 'Type', 'Year', 'Age-Adjusted Rate', 'Standard Error'])
    if df_sub.empty:
        return df_new
    years = df_sub['Year'].values.tolist()
    re = max(years)-min(years)-term+2
    repeat = re if re > 0 else 0

    for i in range(repeat):
        start_year = max(years)-term+1-i
        end_year = max(years) - i
        new_years = list(range(start_year, end_year+1))

        if all(year in years for year in new_years):
            df_new = df_sub[df_sub['Year'].isin(new_years)]
            return df_new
        else:
            continue
    return df_new

def main():
    print("===GLOBOCAN CANCER OVER TIME shortterm by SK===\n")
    df, file_name = upload_file()
    directory = saving_directory()

    while True:
        term = input("How long term (years) do you want? ")
        if not term.isdigit():
            print("Available only natural number.\n")
        else:
            term = int(term)
            print()
            break
    
    countries = df['Country'].unique()
    sexes = df['Sex'].unique()
    types = df['Type'].unique()
    shortterm_df = pd.DataFrame(columns = ['Country', 'Sex', 'Type', 'Year', 'Age-Adjusted Rate', 'Standard Error'])
    for country in countries:
        for sex in sexes:
            for typ in types:
                df_sub = df[(df['Country'] == country) & (df['Sex'] == sex) & (df['Type'] == typ)]
                new_shortterm_df = shortterm(df_sub, term)
                if shortterm_df.empty:
                    shortterm_df = new_shortterm_df
                elif not new_shortterm_df.empty:
                    shortterm_df = pd.concat([shortterm_df, new_shortterm_df])
    new_file_name = file_name[:-4] + " (recent " + str(term) + " years).csv"
    shortterm_df.to_csv(directory + "/" + new_file_name, index=False)
    print("분석 완료")
    print(f"{directory}의 {new_file_name}를 확인하세요.\n")

if __name__ == "__main__":
    main()
