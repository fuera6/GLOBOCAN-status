'''
==short term ASIR 구하는 코드==
- Last update: 2024.07.09
- You need: CI5plus_Detailed_Legacy, CI5plus_Summary_Legacy datasets
- Steps
  1. 순서대로 detailed dataset, summary dataset 폴더를 지정하고, 끝으로 결과물을 저장할 위치를 지정한다.
  2. Questions에 연구 목적에 맞게 적절히 답을 한다.
    Q1. Which type of dataset do you require?
    >> incidence를 보고자 하는 Cases 파일의 위치를 선택 (1: detailed / 2: summary)
    Q2. Which sex are you interested in?
    >> 보고싶은 sex를 선택 (1: male / 2: female / 3: both)
    Q3. Which types of cancer are you interested in? Please write the corresponding numbers. If you are interested in more than one type, separate the numbers with spaces.
    >> 보고싶은 cancer의 번호들을 입력. 여러 개일 경우, 공백으로 구분하여 입력 (e.g., 24 25 26). 번호는 "CI5 Plus trend 참고자료.xlsx"에서 확인 가능.
    Q4. Please set a threshold for the analysis for each country and sex.
    >> 각 국가 및 성별마다 분석을 진행하는 모든 시기 통합 최소 건수 설정 (default: 100)
    Q5. Please set a range of years for the analysis.
    >> 보고싶은 기간 설정 (default: 15)
  3. 마지막으로 입력한 정보를 확인 후 y를 입력하여 분석을 시작한다.
  4. 저장된 파일을 확인한다.
'''

import numpy as np
import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

def upload_files():
    root = Tk()
    root.withdraw()
    detailed_directory_path = askdirectory(title="CI5plus_Detailed_Legacy")
    root.destroy()

    root = Tk()
    root.withdraw()
    summary_directory_path = askdirectory(title="CI5plus_Summary_Legacy")
    root.destroy()

    detailed_incidence_dict = {}
    if detailed_directory_path:
        for file in os.listdir(detailed_directory_path):
            if file in ["Africa_Cases.csv", "Americas_Cases.csv", "Asia_Cases.csv", "Europe_Cases.csv", "Oceania_Cases.csv"]:
                file_name = file[:-10]
                file_path = os.path.join(detailed_directory_path, file)
                df = pd.read_csv(file_path)
                detailed_incidence_dict[file_name] = df
            elif file in ["cancer_detailed.csv"]:
                file_path = os.path.join(detailed_directory_path, file)
                df = pd.read_csv(file_path, header=None)
                cancer_detailed = df
    
    summary_incidence_dict = {}
    population_dict = {}
    if summary_directory_path:
        for file in os.listdir(summary_directory_path):
            if file in ["Africa_Cases.csv", "Americas_Cases.csv", "Asia_Cases.csv", "Europe_Cases.csv", "Oceania_Cases.csv"]:
                file_name = file[:-10]
                file_path = os.path.join(summary_directory_path, file)
                df = pd.read_csv(file_path)
                summary_incidence_dict[file_name] = df
            elif file in ["Africa_Pops.csv", "Americas_Pops.csv", "Asia_Pops.csv", "Europe_Pops.csv", "Oceania_Pops.csv"]:
                file_name = file[:-9]
                file_path = os.path.join(summary_directory_path, file)
                df = pd.read_csv(file_path)
                population_dict[file_name] = df
            elif file in ["cancer_summary.csv"]:
                file_path = os.path.join(summary_directory_path, file)
                df = pd.read_csv(file_path, header=None)
                cancer_summary = df
        return detailed_incidence_dict, cancer_detailed, summary_incidence_dict, population_dict, cancer_summary

    else:
        print("directory가 선택되지 않았습니다.")
        exit(1)

def ASIR(df, df_pop, country_name, registries, cancer, cancer_name, sex, threshold, term):
    index1 = ["N0_4", "N5_9", "N10_14", "N15_19", "N20_24", "N25_29", "N30_34", "N35_39", "N40_44", "N45_49", "N50_54", "N55_59", "N60_64", "N65_69", "N70_74", "N75_79", "N80_84", "N85+"]
    index2 = ["P0_4", "P5_9", "P10_14", "P15_19", "P20_24", "P25_29", "P30_34", "P35_39", "P40_44", "P45_49", "P50_54", "P55_59", "P60_64", "P65_69", "P70_74", "P75_79", "P80_84", "P85+"]

    years_group = []
    for registry in registries:
        years = df[(df['CANCER'] == cancer) & (df['REGISTRY'] == registry) & (df['SEX'] == sex)]['YEAR'].unique().tolist()
        years_group.append(years)
    
    result = set(years_group[0])
    if len(years_group) > 1:
        for lst in years_group[1:]:
            result.update(lst)
    years = sorted(list(result), reverse=True)
    years = years[:term]
    years = sorted(list(years))
    if years[-1] != 2017:
        if sex == 1:
            print(f"{cancer_name}의 {country_name}이며 Male인 데이터는 2017년 최신 데이터가 없어 제외되었습니다.")
        elif sex == 2:
            print(f"{cancer_name}의 {country_name}이며 Female인 데이터는 2017년 최신 데이터가 없어 제외되었습니다.")
        return

    df_sub = np.zeros((len(years), len(index1)))
    df_pop_sub = np.zeros((len(years), len(index2)))

    year_index_map = {year: idx for idx, year in enumerate(years)}

    for registry in registries:
        _df_sub = df[(df['CANCER'] == cancer) & (df['REGISTRY'] == registry) & (df['SEX'] == sex)]
        _df_pop_sub = df_pop[(df_pop['REGISTRY'] == registry) & (df_pop['SEX'] == sex)]

        for year in years:
            if year in _df_sub['YEAR'].values:
                year_data = _df_sub[_df_sub['YEAR'] == year][index1].to_numpy().squeeze()
            else:
                year_data = np.zeros((1, len(index1))).squeeze()

            if year in _df_pop_sub['YEAR'].values:
                year_pop_data = _df_pop_sub[_df_pop_sub['YEAR'] == year][index2].to_numpy().squeeze()
            else:
                year_pop_data = np.zeros((1, len(index2))).squeeze()
            df_sub[year_index_map[year]] += year_data.tolist()
            df_pop_sub[year_index_map[year]] += year_pop_data

    if sex == 1:
        sex = 'Male'
    elif sex == 2:
        sex = 'Female'

    if np.sum(df_sub) < threshold:
        print(f"{cancer_name}의 {country_name}이며 {sex}인 데이터는 최소 cancer 수 {threshold}건을 넘기지 못해 제외되었습니다.")
        return
    
    df_sub = pd.DataFrame(df_sub, columns=index1)
    df_pop_sub = pd.DataFrame(df_pop_sub, columns=index2)

    df_year = pd.DataFrame({'YEAR' : years})

    df_sub = pd.concat([df_year, df_sub], axis=1)
    df_pop_sub = pd.concat([df_year, df_pop_sub], axis=1)

    Segi_pop = [12000, 10000, 9000, 9000, 8000, 8000, 6000, 6000, 6000, 6000, 5000, 4000, 4000, 3000, 2000, 1000, 500, 500]
    
    years = df_sub['YEAR'].to_list()
    ASIRs = []
    SEs = []
    for year in years:
        incidences = (df_sub.loc[df_sub['YEAR'] == year, index1]).iloc[0].to_list()
        populations = (df_pop_sub.loc[df_pop_sub['YEAR'] == year, index2]).iloc[0].to_list()

        ASIR = 0
        variance = 0
        for i in range(len(incidences)):
            if populations[i] != 0:
                ASIR += Segi_pop[i]*incidences[i]/populations[i]
                variance += incidences[i]*((Segi_pop[i]/populations[i])**2)
            else:
                ASIR += 0
                variance += 0
        
        ASIRs.append(ASIR)
        SEs.append((variance)**(1/2))
    replaced_cancer_name = cancer_name.replace(":", " -").replace("/", " without ").replace(", ", " & ").replace(",", " & ")
    data = pd.DataFrame({'Cancer' : [replaced_cancer_name for i in range(len(years))], 
                         'Country' : [country_name for i in range(len(years))], 
                         'Sex' : [sex for i in range(len(years))], 
                         'Year' : years, 
                         'Age-Adjusted Rate' : ASIRs, 
                         'Standard Error' : SEs})

    return data

def analysis(cancers, cancer_names, sexes, threshold, term, df_Africa, df_Americas, df_Asia, df_Europe, df_Oceania, df_Africa_pop, df_Americas_pop, df_Asia_pop, df_Europe_pop, df_Oceania_pop):
    data = pd.DataFrame(columns=['Cancer', 'Country', 'Sex', 'Year', 'Age-Adjusted Rate', 'Standard Error'])
    for i in range(len(cancers)):
        for sex in sexes:
            data = pd.concat([data, ASIR(df_Africa, df_Africa_pop, "Uganda", [80000299], cancers[i], cancer_names[i], sex, threshold, term)])

            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Argentina", [3200799], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Chile", [15200199], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Colombia", [17000199, 17000299, 17000399, 17000499], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Costa Rica", [18800099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Ecuador", [21800199], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Puerto Rico", [63000099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "Canada", [12400099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "USA (White people)", [84002010], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Americas, df_Americas_pop, "USA (Black people)", [84002030], cancers[i], cancer_names[i], sex, threshold, term)])

            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Bahrain", [4800046], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "China", [15600199, 15600299, 15600399, 15600799, 15600999, 15601499, 15601599, 15601899], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "India", [35600399, 35600499, 35600799, 35601199], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Israel", [37600099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Japan", [39200299, 39200499], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Republic of Korea", [41000099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Kuwait", [41400025], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Philippines", [60800299], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Qatar", [63400068], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Thailand", [76400199, 76400299, 76400499, 76400599], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Asia, df_Asia_pop, "Turkiye", [79200199, 79200299], cancers[i], cancer_names[i], sex, threshold, term)])

            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Austria", [4000099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Belarus", [11200099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Croatia", [19100099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Cyprus", [19600099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Czech Republic", [20300099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Denmark", [20800099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Estonia", [23300099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "France", [25000199, 25000299, 25000399, 25000499, 25000599, 25000699, 25000899, 25001499, 25001699, 25001799], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Germany", [27600299, 27601299, 27601699, 27603099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Iceland", [35200099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Ireland", [37200099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Italy", [38001499, 38001999, 38002999, 38003399, 38003499], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Latvia", [42800099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Lithuania", [44000099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Malta", [47000099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "The Netherlands", [52800099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Norway", [57800099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Poland", [61600799], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Slovenia", [70500099], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Spain", [72400199, 72400299, 72400399, 72400499, 72400699, 72401099, 72401199, 72401499], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "Switzerland", [75600299, 75600599, 75600899, 75601099, 75601199], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Europe, df_Europe_pop, "UK", [82600199, 82602099, 82603099, 82604099], cancers[i], cancer_names[i], sex, threshold, term)])

            data = pd.concat([data, ASIR(df_Oceania, df_Oceania_pop, "Austrailia", [3600299, 3600399, 3600499, 3600599, 3600699, 3600799, 3600899], cancers[i], cancer_names[i], sex, threshold, term)])
            data = pd.concat([data, ASIR(df_Oceania, df_Oceania_pop, "New Zealand", [55400099], cancers[i], cancer_names[i], sex, threshold, term)])
            
    return data

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

def main():
    detailed_incidence_dict, cancer_detailed, summary_incidence_dict, population_dict, cancer_summary = upload_files()
    directory = saving_directory()
    while True:
        num = input("Q1. Which type of dataset do you require? 1: detailed / 2: summary\nA1. ")
        if not num.isdigit():
            print("1과 2중에 선택해주세요.\n")
        elif int(num) not in (1, 2):
            print("1과 2중에 선택해주세요.\n")
        else:
            num = int(num)
            print()
            break

    while True:    
        sex = input("Q2. Which sex are you interested in? 1: male / 2: female / 3: both\nA2. ")
        if not sex.isdigit():
            print("1, 2, 3중에 선택해주세요.\n")
        elif int(sex) not in (1, 2, 3):
            print("1, 2, 3중에 선택해주세요.\n")
        else:
            sex = int(sex)
            print()
            break
    
    while True:
        cancers = input("Q3. Which types of cancer are you interested in? Please write the corresponding numbers. If you are interested in more than one type, separate the numbers with spaces.\nA3. ")
        cancer_list = cancers.split(" ")
        if all(c.isdigit() for c in cancer_list):
            cancer_list = [int(c)-1 for c in cancer_list]
            print()
            break
        else:
            print("입력값 중에 정수가 아닌 값이 있습니다. 다시 입력해주세요.\n")
    
    while True:
        threshold = input("Q4. Please set a threshold for the analysis for each country and sex.\nA4. ")
        if not threshold.isdigit():
            print("자연수 중에 선택해주세요.\n")
        else:
            threshold = int(threshold)
            print()
            break
    
    while True:
        term = input("Q5. Please set a range of years for the analysis.\nA5. ")
        if not term.isdigit():
            print("자연수 중에 선택해주세요.\n")
        else:
            term = int(term)
            print()
            break
  
    print("---검색 결과---\n")
    if sex == 1:
        print("sex: male only")
    elif sex == 2:
        print("sex: female only")
    else:
        print("sex: both sex")
    print(f"\nthreshold: {threshold} cases")
    print(f"\nperiod: {2018-term}-2017 ({term} years)")
    print("\ncancers:")
    if num == 1:
        cancers = cancer_detailed.iloc[cancer_list].iloc[:, 1].tolist()
        for cancer in cancers:
            print(f"- {cancer.strip()}")
    elif num == 2:
        cancers = cancer_summary.iloc[cancer_list].iloc[:, 1].tolist()
        for cancer in cancers:
            print(f"- {cancer.strip()}")
    print("\n------------\n")
    
    while True:
        ans = input("해당 정보가 맞는지 확인해주세요. (y/n) ")
        if ans not in ("y", "n"):
            print("다시 입력해주세요.\n")
        elif ans == "n":
            print("다시 시작해주세요.\n")
            exit()
        else:
            print()
            break
       
    if sex == 1:
        sexes = [1]
    elif sex == 2:
        sexes = [2]
    else:
        sexes = [1, 2]

    cancer_list = [c+1 for c in cancer_list]
    data = analysis(cancer_list, cancers, sexes, threshold, term, detailed_incidence_dict['Africa'], detailed_incidence_dict['Americas'], detailed_incidence_dict['Asia'], detailed_incidence_dict['Europe'], detailed_incidence_dict['Oceania'], population_dict['Africa'], population_dict['Americas'], population_dict['Asia'], population_dict['Europe'], population_dict['Oceania'])
    
    data.to_csv(directory + "/shortterm_trend.csv", index=False)
    print("\n분석 완료")
    print(f"{directory}/shortterm_trend.csv 를 확인하세요.\n")

if __name__ == "__main__":
    main()
