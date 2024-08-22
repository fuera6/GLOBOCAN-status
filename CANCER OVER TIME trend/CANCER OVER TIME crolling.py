'''
==long term age-standardized rate와 age-specific rate 구하는 코드==
- Last update: 2024.07.18
- You need: internet
- Steps
  1. 결과물을 저장할 위치를 지정한다.
  2. Questions에 연구 목적에 맞게 적절히 답을 한다.
    Which site of cancer are you looking for? Write ID.
    >> 보고자 하는 cancer site의 ID를 적는다. 해당 ID는 'CANCER OVER TIME 참고자료.xlsx'에 기입되어 있다.
  3. 원하는 cancer site가 맞는지 확인 후 y를 입력하여 분석을 시작한다.
  4. 저장된 파일을 확인한다.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
from tkinter import Tk
from tkinter.filedialog import askdirectory

FIRST_YEAR = 1943
LAST_YEAR = 2020

def saving_directory():
    root = Tk()
    root.withdraw()
    directory_path = askdirectory(title="Where to save")
    root.destroy()

    if directory_path:
        return directory_path
    else:
        print("directory가 선택되지 않았습니다.")
        exit(1)

def ID_to_name(ID):
    ID_to_name_dict = {
        1 : "All sites excl. non-melanoma skin cancer", 
        2 : "Lip, oral cavity and pharynx", 
        3 : "Oesophagus", 
        4 : "Stomach", 
        5 : "Colon", 
        6 : "Colorectum", 
        7 : "Rectum and anus", 
        8 : "Liver", 
        9 : "Gallbladder etc.", 
        10 : "Pancreas", 
        11 : "Larynx", 
        12 : "Lung", 
        13 : "Melanoma of skin", 
        14 : "Kaposi sarcoma", 
        15 : "Breast", 
        16 : "Cervix uteri", 
        17 : "Uterus", 
        18 : "Corpus uteri", 
        19 : "Ovary", 
        20 : "Prostate", 
        21 : "Testis", 
        22 : "Kidney", 
        23 : "Bladder", 
        24 : "Brain and central nervous system", 
        25 : "Thyroid", 
        26 : "Hodgkin lymphoma", 
        27 : "Non-Hodgkin lymphoma", 
        28 : "Multiple myeloma", 
        29 : "Leukaemia"
    }
    return ID_to_name_dict[ID]

def ID_to_num(ID):
    ID_to_num_dict = {
        1 : 0,
        2 : 1, 
        3 : 2, 
        4 : 3, 
        5 : 5, 
        6 : 106, 
        7 : 6, 
        8 : 7, 
        9 : 8, 
        10 : 9, 
        11 : 10, 
        12 : 11, 
        13 : 12, 
        14 : 13, 
        15 : 14, 
        16 : 16, 
        17 : 15, 
        18 : 17, 
        19 : 18, 
        20 : 19, 
        21 : 20, 
        22 : 21, 
        23 : 22, 
        24 : 23, 
        25 : 24, 
        26 : 25, 
        27 : 26, 
        28 : 27, 
        29 : 28
    }
    return ID_to_num_dict[ID]

def sex_string(sex):
    if sex == 1:
        return 'Male'
    else:
        return 'Female'

def type_string(type):
    if type == 0:
        return 'Incidence'
    else:
        return 'Mortality'

def ID_search():
    while True:
        ID = input("Which site of cancer are you looking for? Write ID. ")
        if not ID.isdigit():
            print("Available only 1-29.\n")
        elif int(ID) not in range(1, 30):
            print("Available only 1-29.\n")
        else:
            print()
            ID = int(ID)
            cancer_name = ID_to_name(ID)
            while True:
                flag = input(f"Are you looking for cancer in '{cancer_name}'? (y/n) ")
                if flag not in ('y', 'n'):
                    print("Available only 'y' or 'n'.\n")
                elif flag == 'y':
                    return ID
                else:
                    print()
                    break

def crolling(type, sex, cancer_ID):
    cancer_num = ID_to_num(cancer_ID)
    cancer_name = ID_to_name(cancer_ID)
    rates = pd.DataFrame(columns=['Country', 'Sex', 'Type', 'Year', 'Numbers', 'Coverage', 'Age-Adjusted Rate', 'Crude rate', 'Cumulative Risk [0-74]'])
    asr = pd.DataFrame(columns=['Country', 'Sex', 'Type', 'Year', 'Crude rate', 'R0-4', 'R5-9', 'R10-14', 'R15-19', 'R20-24', 'R25-29', 'R30-34', 'R35-39', 'R40-44', 'R45-49', 'R50-54', 'R55-59', 'R60-64', 'R65-69', 'R70-74', 'R75-79', 'R80-84', 'R85+'])
    pop = pd.DataFrame(columns=['Country', 'Sex', 'Type', 'Year', 'Number', 'Coverage', 'P0-4', 'P5-9', 'P10-14', 'P15-19', 'P20-24', 'P25-29', 'P30-34', 'P35-39', 'P40-44', 'P45-49', 'P50-54', 'P55-59', 'P60-64', 'P65-69', 'P70-74', 'P75-79', 'P80-84', 'P85+'])

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    driver.get(f"https://gco.iarc.fr/overtime/en/dataviz/tables?hide_tab_age_specific_numbers=1&types={type}&sexes={sex}&cancers={cancer_num}")
    WebDriverWait(driver, 180).until(
        EC.visibility_of_element_located((By.ID, "rates"))
    )

    table = driver.find_element(By.ID, "rates")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if not rows:
        if type == 0 and sex == 1:
            print(f"{cancer_name}의 Male Incidence data는 존재하지 않습니다.")
        elif type == 1 and sex == 1:
            print(f"{cancer_name}의 Male Mortality data는 존재하지 않습니다.")
        elif type == 0 and sex == 2:
            print(f"{cancer_name}의 Female Incidence data는 존재하지 않습니다.")
        elif type == 1 and sex == 21:
            print(f"{cancer_name}의 Female Mortality data는 존재하지 않습니다.")
        driver.close()
        return None, None, None
    else:
        if type == 0 and sex == 1:
            print(f"{cancer_name}의 Male Incidence data가 존재합니다.")
            print("데이터 수집을 시작합니다.")
        elif type == 1 and sex == 1:
            print(f"{cancer_name}의 Male Mortality data는 존재합니다.")
            print("데이터 수집을 시작합니다.")
        elif type == 0 and sex == 2:
            print(f"{cancer_name}의 Female Incidence data는 존재합니다.")
            print("데이터 수집을 시작합니다.")
        elif type == 1 and sex == 21:
            print(f"{cancer_name}의 Female Mortality data는 존재합니다.")
            print("데이터 수집을 시작합니다.")

    year = FIRST_YEAR

    while year <= LAST_YEAR:
        try:
            print(f"{year}년 데이터 수집 중...")
            driver.get(f"https://gco.iarc.fr/overtime/en/dataviz/tables?hide_tab_age_specific_numbers=1&types={type}&sexes={sex}&cancers={cancer_num}&years={year}")
            WebDriverWait(driver, 180).until(
                EC.visibility_of_element_located((By.ID, "rates"))
            )

            rates_table = driver.find_element(By.ID, "rates")
            rates_tbody = rates_table.find_element(By.TAG_NAME, 'tbody')
            rates_rows = rates_tbody.find_elements(By.TAG_NAME, 'tr')
            rates_data = []

            if not rates_rows:
                year += 1
                continue

            for row in rates_rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                cells_text = [cell.text for cell in cells]
                if cells_text:
                    rates_data.append(cells_text)

            rates_df = pd.DataFrame(rates_data, columns=['Country', 'Numbers', 'Coverage', 'Age-Adjusted Rate', 'Crude rate', 'Cumulative Risk [0-74]'])
            rates_df['Sex'] = sex_string(sex)
            rates_df['Type'] = type_string(type)
            rates_df['Year'] = year
            
            button1 = driver.find_element(By.ID, '__BVID__76___BV_tab_button__')
            button1.click()
            WebDriverWait(driver, 180).until(
                EC.visibility_of_element_located((By.ID, "age-specific-rates"))
            )

            asr_table = driver.find_element(By.ID, "age-specific-rates")
            asr_rows = asr_table.find_elements(By.TAG_NAME, 'tr')
            asr_data = []

            for row in asr_rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                cells_text = [cell.text for cell in cells]
                if cells_text:
                    asr_data.append(cells_text)
            
            asr_df = pd.DataFrame(asr_data, columns=['Country', 'Crude rate', 'R0-4', 'R5-9', 'R10-14', 'R15-19', 'R20-24', 'R25-29', 'R30-34', 'R35-39', 'R40-44', 'R45-49', 'R50-54', 'R55-59', 'R60-64', 'R65-69', 'R70-74', 'R75-79', 'R80-84', 'R85+'])
            asr_df['Sex'] = sex_string(sex)
            asr_df['Type'] = type_string(type)
            asr_df['Year'] = year

            button2 = driver.find_element(By.ID, '__BVID__78___BV_tab_button__')
            button2.click()
            WebDriverWait(driver, 180).until(
                EC.visibility_of_element_located((By.ID, "populations"))
            )

            pop_table = driver.find_element(By.ID, "populations")
            pop_rows = pop_table.find_elements(By.TAG_NAME, 'tr')
            pop_data = []

            for row in pop_rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                cells_text = [cell.text for cell in cells]
                if cells_text:
                    pop_data.append(cells_text)
            
            pop_df = pd.DataFrame(pop_data, columns=['Country', 'Number', 'Coverage', 'P0-4', 'P5-9', 'P10-14', 'P15-19', 'P20-24', 'P25-29', 'P30-34', 'P35-39', 'P40-44', 'P45-49', 'P50-54', 'P55-59', 'P60-64', 'P65-69', 'P70-74', 'P75-79', 'P80-84', 'P85+'])
            pop_df['Sex'] = sex_string(sex)
            pop_df['Type'] = type_string(type)
            pop_df['Year'] = year

        except:
            continue

        rates = pd.concat([rates, rates_df])
        asr = pd.concat([asr, asr_df])
        pop = pd.concat([pop, pop_df])
        year += 1
    
    if type == 0 and sex == 1:
        print(f"{cancer_name}의 Male Incidence data 수집이 완료되었습니다.")
    elif type == 1 and sex == 1:
        print(f"{cancer_name}의 Male Mortality data 수집이 완료되었습니다.")
    elif type == 0 and sex == 2:
        print(f"{cancer_name}의 Female Incidence data 수집이 완료되었습니다.")
    elif type == 1 and sex == 21:
        print(f"{cancer_name}의 Female Mortality data 수집이 완료되었습니다.")
    driver.close()
    rates['Country'] = rates['Country'].str.replace(",", "")
    rates['Country'] = rates['Country'].str.replace(":", "")
    rates['Country'] = rates['Country'].str.replace("*", "")
    asr['Country'] = asr['Country'].str.replace(",", "")
    asr['Country'] = asr['Country'].str.replace(":", "")
    asr['Country'] = asr['Country'].str.replace("*", "")
    asr = asr.fillna("0.00")
    pop['Country'] = pop['Country'].str.replace(",", "")
    pop['Country'] = pop['Country'].str.replace(":", "")
    pop['Country'] = pop['Country'].str.replace("*", "")
    return rates, asr, pop

def dataframe1(rates, asr, pop):
    df1 = rates.loc[:, ['Country', 'Sex', 'Type', 'Year', 'Age-Adjusted Rate']]

    asr_sub = asr.loc[:, ['Country', 'Sex', 'Type', 'Year', 'R0-4', 'R5-9', 'R10-14', 'R15-19', 'R20-24', 'R25-29', 'R30-34', 'R35-39', 'R40-44', 'R45-49', 'R50-54', 'R55-59', 'R60-64', 'R65-69', 'R70-74', 'R75-79', 'R80-84', 'R85+']]
    pop_sub = pop.loc[:, ['Country', 'Sex', 'Type', 'Year', 'P0-4', 'P5-9', 'P10-14', 'P15-19', 'P20-24', 'P25-29', 'P30-34', 'P35-39', 'P40-44', 'P45-49', 'P50-54', 'P55-59', 'P60-64', 'P65-69', 'P70-74', 'P75-79', 'P80-84', 'P85+']]

    merged_df = pd.merge(asr_sub, pop_sub, on=['Country', 'Sex', 'Type', 'Year'])
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
    Segi_pop = [12000, 10000, 9000, 9000, 8000, 8000, 6000, 6000, 6000, 6000, 5000, 4000, 4000, 3000, 2000, 1000, 500, 500]
    SEs = []
    for index, row in merged_df.iterrows():
        variance=0
        for i in range(len(age_groups)):
            age_rate_label = 'R' + age_groups[i]
            age_pop_label = 'P' + age_groups[i]
            age_rate = float(row[age_rate_label])
            age_pop = float(row[age_pop_label])
            age_case = age_rate*age_pop/100000
            if age_pop != 0:
                variance += age_case * ((Segi_pop[i]/age_pop)**2)
            else:
                variance += 0
        SEs.append((variance)**(1/2))
    df1['Standard Error'] = SEs
    df1 = df1.sort_values(by=['Country', 'Sex', 'Type', 'Year'])
    return df1

def dataframe2(asr, pop):
    asr_sub_key = asr.loc[:, ['Country', 'Sex', 'Type', 'Year']]
    age_groups = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
    duplicated_rows = []
    for index, row in asr_sub_key.iterrows():
        for age_group in age_groups:
            new_row = {
                'Country': row['Country'],
                'Sex': row['Sex'],
                'Type': row['Type'],
                'Age Group': age_group, 
                'Year': row['Year']
            }
            duplicated_rows.append(new_row)

    df2 = pd.DataFrame(duplicated_rows)

    asr_sub = asr.loc[:, ['Country', 'Sex', 'Type', 'Year', 'R0-4', 'R5-9', 'R10-14', 'R15-19', 'R20-24', 'R25-29', 'R30-34', 'R35-39', 'R40-44', 'R45-49', 'R50-54', 'R55-59', 'R60-64', 'R65-69', 'R70-74', 'R75-79', 'R80-84', 'R85+']]
    pop_sub = pop.loc[:, ['Country', 'Sex', 'Type', 'Year', 'P0-4', 'P5-9', 'P10-14', 'P15-19', 'P20-24', 'P25-29', 'P30-34', 'P35-39', 'P40-44', 'P45-49', 'P50-54', 'P55-59', 'P60-64', 'P65-69', 'P70-74', 'P75-79', 'P80-84', 'P85+']]
    merged_df = pd.merge(asr_sub, pop_sub, on=['Country', 'Sex', 'Type', 'Year'])
    SEs = []
    age_specific_rates = []
    for index, row in merged_df.iterrows():
        for age_group in age_groups:
            age_rate_label = 'R' + age_group
            age_pop_label = 'P' + age_group
            age_rate = float(row[age_rate_label])
            age_pop = float(row[age_pop_label])
            age_case = age_rate*age_pop/100000
            if age_pop != 0:
                SEs.append(((age_case)**(1/2) / age_pop)*100000)
            else:
                SEs.append(0)
            age_specific_rates.append(age_rate)
    
    df2['Age-Specific Rate'] = age_specific_rates
    df2['Standard Error'] = SEs
    df2['Age Group sorting'] = df2['Age Group'].apply(lambda x: int(re.split(r'[-+]', x)[0]))
    df2 = df2.sort_values(by=['Country', 'Sex', 'Type', 'Age Group sorting', 'Year'])
    df2.drop(columns=['Age Group sorting'], inplace=True)
    return df2

def main():
    print("===GLOBOCAN CANCER OVER TIME crolling by SK===\n")
    directory = saving_directory()
    ID = ID_search()
    male_incidence_rates, male_incidence_asr, male_incidence_pop = crolling(0, 1, ID)
    male_mortality_rates, male_mortality_asr, male_mortality_pop = crolling(1, 1, ID)
    female_incidence_rates, female_incidence_asr, female_incidence_pop = crolling(0, 2, ID)
    female_mortality_rates, female_mortality_asr, female_mortality_pop = crolling(1, 2, ID)

    valid_rates = [rates for rates in [male_incidence_rates, male_mortality_rates, female_incidence_rates, female_mortality_rates] if rates is not None]
    valid_asr = [asr for asr in [male_incidence_asr, male_mortality_asr, female_incidence_asr, female_mortality_asr] if asr is not None]
    valid_pop = [pop for pop in [male_incidence_pop, male_mortality_pop, female_incidence_pop, female_mortality_pop] if pop is not None]

    rates = pd.concat(valid_rates)
    asr = pd.concat(valid_asr)
    pop = pd.concat(valid_pop)

    df1 = dataframe1(rates, asr, pop)
    df2 = dataframe2(asr, pop)

    df1.to_csv(directory + f"/{ID_to_name(ID)}_age-standardized rate_trend.csv", index=False)
    df2.to_csv(directory + f"/{ID_to_name(ID)}_age-specific rate_trend.csv", index=False)

    print("\n분석 완료")
    print(f"{directory}의 {ID_to_name(ID)}_age-standardized rate_trend.csv와 {ID_to_name(ID)}_age-specific rate_trend.csv를 확인하세요.\n")

if __name__ == "__main__":
    main()
