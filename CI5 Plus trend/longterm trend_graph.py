'''
==long term ASIR trend graph 그리는 코드==
- Last update: 2024.07.05
- You need: longterm_trend.py를 실행시켜 얻은 longterm_trend.csv 파일
- Steps
  1. longterm_trend.csv 파일을 업로드하고, 결과물을 저장할 위치를 지정한다.
  2. Questions에 연구 목적에 맞게 적절히 답을 한다.
    Q1. General maximum value for y-axis
    >> 일반적인 y-max 값을 입력한다.
    Q2. Write the country and the maximum value for the y-axis, if it is an exception. No exception, then write 'end'
    >> 특이하게 incidence가 낮거나 높은 국가만 선별해서 따로 y-max 값 처리를 해준다. 이때 Country는 longterm_trend.csv에 있는 국가 이름을 가져다 쓴다. 다 끝났으면 "Country: " 질문에서 'end'를 입력한다.
  3. 각 cancer type 별로 2를 반복한다.
  4. 저장된 그림을 확인한다.
- Tips
  1. 우선 한 번 대충 돌려보고, y-max 값을 어떻게 잡아야 할 지 감을 잡는다.
  2. dpi를 300으로 해도 해상도 꽤 괜찮다. 1200으로 하면 메모리 이슈 때문인지 안 돌아간다.
'''

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.ndimage import gaussian_filter1d
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def upload_file():
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(title="Upload longterm_trend.csv", filetypes=[("csv", "*.csv")])
    root.destroy()

    if file_path:
        df = pd.read_csv(file_path)
        return df
    else:
        print("file이 선택되지 않았습니다.")
        exit(1)

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

def sub_dataframe(data, by, country, sex):
    df_sub = data[(data['Country'] == country) & (data['Sex'] == sex)]
    df_sub = df_sub.sort_values(by=[by], ascending=True)
    return df_sub

def generate_decade_years(first_year, last_year):
    start_year = (first_year // 10) * 10
    if start_year < first_year:
        start_year += 10

    end_year = (last_year // 10) * 10
    if end_year > last_year:
        end_year -= 10

    decade_years = list(range(start_year, end_year + 1, 10))
    return decade_years

def trend_plot(df, cancer_name, countries, exceptions_dict, first_year, last_year, y_max, directory_path):
    num_countries = len(countries)
    num_cols = 4
    num_rows = math.ceil(num_countries / num_cols)
    final_four_idx = [num_countries-4, num_countries-3, num_countries-2, num_countries-1]

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 5 * num_rows), dpi=300, constrained_layout=True)
    axes = axes.flatten()

    for idx, country in enumerate(countries):
        if country in list(exceptions_dict.keys()):
            ylim = exceptions_dict[country]
        else:
            ylim = y_max
        
        df_m = sub_dataframe(df, 'Year', country, 'Male')
        df_f = sub_dataframe(df, 'Year', country, 'Female')

        index_m = df_m['Year'].values
        index_f = df_f['Year'].values

        ax = axes[idx]

        years = generate_decade_years(first_year, last_year)
        if idx in final_four_idx:
            ax.set_xticks(years)
            ax.set_xticklabels([str(y) for y in years], rotation=45, fontsize=15)
            for label in ax.get_xticklabels():
                label.set_fontfamily("Arial")
            ax.set_xlabel('Year', fontsize=20, fontfamily="Arial")
        else:
            ax.set_xticklabels([])
        if idx%4 == 0:
            ax.set_ylabel('ASR (per 100,000 people)', fontsize=20, fontfamily="Arial")
        
        ax.tick_params(axis='y', labelsize=15)
        for label in ax.get_yticklabels():
            label.set_fontfamily("Arial")

        ax.scatter(index_m, df_m['Age-Adjusted Rate'], color='#009FC3', s=10, label='Male')
        ax.scatter(index_f, df_f['Age-Adjusted Rate'], color='#B30437', s=10, label='Female')

        val_m = gaussian_filter1d(df_m['Age-Adjusted Rate'], sigma=5)
        val_f = gaussian_filter1d(df_f['Age-Adjusted Rate'], sigma=5)

        ax.plot(index_m, val_m, color='#009FC3', linewidth=4, label='Male Rate', solid_capstyle='projecting')
        ax.plot(index_f, val_f, color='#B30437', linewidth=4, label='Female Rate', solid_capstyle='projecting')

        ax.yaxis.set_major_locator(MaxNLocator(nbins=4))

        ax.set_xlim([first_year-1, last_year+1])
        ax.set_ylim([0, ylim])
        ax.set_title(country, fontsize=30, fontfamily="Arial")

    for i in range(num_countries, len(axes)):
        fig.delaxes(axes[i])

    plt.savefig(f"{directory_path}/{cancer_name}_trend.png", format='png')
    plt.close()
    print(f"\n완료되었습니다. {directory_path}/{cancer_name}_trend.png 를 확인하세요.")

def main():
    longterm_trend = upload_file()
    directory_path = saving_directory()
    first_year = min(longterm_trend['Year'].unique().tolist())
    last_year = max(longterm_trend['Year'].unique().tolist())

    for cancer in list(longterm_trend['Cancer'].unique()):
        print(f"=={cancer} trend graph==")
        df_sub = longterm_trend[longterm_trend['Cancer'] == cancer]
        countries = sorted(df_sub['Country'].unique().tolist())
        while True:
            y_max = input("Q1. General maximum value for y-axis:\nA1. ")
            if not y_max.isdigit():
                print("자연수 중에 선택해주세요.\n")
            else:
                y_max = int(y_max)
                print()
                break
        print("Q2. Write the country and the maximum value for the y-axis, if it is an exception. No exception, then write 'end':")
        flag = True
        exceptions = {}
        while flag:
            while flag:
                country_exception = input("Country: ")
                if country_exception == "end":
                    flag = False
                    break
                elif country_exception not in countries:
                    print("업로드한 csv 파일에 있는 국가 이름으로 작성해주세요.\n")
                    continue
                else:
                    break
            while flag:        
                y_max_exception = input("y max: ")
                if not y_max_exception.isdigit():
                    print("자연수 중에 선택해주세요.\n")
                    continue
                else:
                    y_max_exception = int(y_max_exception)
                    exceptions[country_exception] = y_max_exception
                    print()
                    break

        trend_plot(df_sub, cancer, countries, exceptions, first_year, last_year, y_max, directory_path)
        print("========================\n")

if __name__ == "__main__":
    main()
