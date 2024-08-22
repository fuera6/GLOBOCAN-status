'''
==long term ASIR trend table 구하는 코드==
- Last update: 2024.07.09
- You need: *.Export.APC.csv, *.Export.AAPC.csv
- Steps
  1. *.Export.APC.csv, *.Export.AAPC.csv 파일을 업로드하고, 결과물을 저장할 위치를 지정한다.
  2. 저장된 테이블을 확인한다.
'''

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

def upload_file():
    root = Tk()
    root.withdraw()
    file_path_APC = askopenfilename(title="Upload *.Export.APC.csv", filetypes=[("csv", "*.csv")])
    root.destroy()

    if file_path_APC:
        df_APC = pd.read_csv(file_path_APC)
    else:
        print("*.Export.APC.csv file이 선택되지 않았습니다.")
        exit(1)
    
    root = Tk()
    root.withdraw()
    file_path_AAPC = askopenfilename(title="Upload *.Export.AAPC.csv", filetypes=[("csv", "*.csv")])
    root.destroy()

    if file_path_AAPC:
        df_AAPC = pd.read_csv(file_path_AAPC)
    else:
        print("*.Export.AAPC.csv file이 선택되지 않았습니다.")
        exit(1)
    
    return df_APC, df_AAPC

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

def registries():
    df_registries = pd.DataFrame({
        "Country" : ["Argentina", "Austrailia", "Austria", "Bahrain", "Belarus", "Canada", "Chile", "China", "Colombia", "Costa Rica", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Ecuador", "Estonia", "France", "Germany", "Iceland", "India", "Ireland", "Israel", "Italy", "Japan", "Kuwait", "Latvia", "Lithuania", "Malta", "New Zealand", "Norway", "Philippines", "Poland", "Puerto Rico", "Qatar", "Republic of Korea", "Slovenia", "Spain", "Switzerland", "Thailand", "The Netherlands", "Turkiye", "Uganda", "UK", "USA (Black people)", "USA (White people)"], 
        "Registry" : ["Mendoza", "New South Wales & Australian Capital Territory, Northern Territory, Queensland, South Australia, Tasmania, Victoria, and Western Australia", "National", "National (Bahraini)", "National", "Alberta, British Columbia, Manitoba, Newfoundland, Nova Scotia, Ontario, Prince Edward Island, and Saskatchewan", "Valdivia", "Beijing City, Harbin City, Jiashan County, Qidong City, Shanghai City, Wuhan City, Yanting County, and Zhongshan City", "Bucaramanga, Cali, Manizales, and Pasto", "National", "National", "National", "National", "National", "Quito", "National", "Bas-Rhin, Calvados, Doubs, Haut-Rhin, Herault, Isere, Loire-Atlantique, Manche, Somme, and Vendee", "Bremen, Hamburg, Saarland, and Schleswig-Holstein", "National", "Barshi, Chennai, Dindigul Ambilikkai, and Mumbai", "National", "National", "Palermo, South Tyrol, Syracuse, Trento, and Perugia", "Miyagi Prefecture and Osaka", "National (Kuwaiti)", "National", "National", "National", "National", "National", "Manila", "Kielce", "National", "National (Qatari)", "National", "National", "Basque Country, Canary Islands, Girona, Granada, La Rioja, Murcia, Navarra, and Tarragona", "Geneva, Graubunden and Glarus, Ticino, Valais, and Vaud", "Chiang Mai, Khon Kaen, Lampang, and Songkhla", "National", "Antalya and Izmir", "Kyadondo County", "England, Northern Ireland, Scotland, and Wales", "SEER (9 Registries): Atlanta, Connecticut, Detroit, Hawaii, Iowa, New Mexico, San Francisco-Oakland, Seattle-Puget Sound, and Utah", "SEER (9 Registries): Atlanta, Connecticut, Detroit, Hawaii, Iowa, New Mexico, San Francisco-Oakland, Seattle-Puget Sound, and Utah"]
    })

    return df_registries

def get_tables(df_APC, df_AAPC, df_registries, directory_path):
    for cancer in df_AAPC['Cancer'].unique():
        Countries = []
        Registries = []
        Male_period = []
        Male_APC = []
        Male_APC_significant = []
        Male_AAPC = []
        Male_AAPC_significant = []
        Female_period = []
        Female_APC = []
        Female_APC_significant = []
        Female_AAPC = []
        Female_AAPC_significant = []
        df_AAPC_sub_1 = df_AAPC[df_AAPC['Cancer'] == cancer]
        for country in sorted(df_AAPC_sub_1['Country'].unique()):
            df_AAPC_sub_2 = df_AAPC_sub_1[df_AAPC_sub_1['Country'] == country]
            Countries.append(country)
            print(df_registries.loc[df_registries['Country'] == country, 'Registry'])
            Registries.append(df_registries.loc[df_registries['Country'] == country, 'Registry'].values[0])
            
            if len(df_AAPC_sub_2) == 1:
                if df_AAPC_sub_2['Sex'].values[0] == 'Male':
                    if df_AAPC_sub_2['Joinpoint Model'].values[0] == 0:
                        Male_period.append(str(df_AAPC_sub_2['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2['End Obs'].values[0]))
                        Male_APC.append("")
                        Male_APC_significant.append("")
                        Male_AAPC.append(str(round(df_AAPC_sub_2['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2['AAPC C.I. High'].values[0], 2)) + ")")
                        Male_AAPC_significant.append(df_AAPC_sub_2['Statistically Significant (0=No  1=Yes)'].values[0])
                        Female_period.append("")
                        Female_APC.append("")
                        Female_APC_significant.append("")
                        Female_AAPC.append("")
                        Female_AAPC_significant.append("")
                    else:
                        df_APC_sub = df_APC[(df_APC['Cancer'] == cancer) & (df_APC['Country'] == country) & (df_APC['Sex'] == 'Male')]
                        for index, row in df_APC_sub.iterrows():
                            Countries.append("")
                            Registries.append("")
                            Male_period.append(str(row['Segment Start']) + "-" + str(row['Segment End']))
                            Male_APC.append(str(round(row['APC'], 2)) + " (" + str(round(row['APC 95% LCL'], 2)) + " to " + str(round(row['APC 95% UCL'], 2)) + ")")
                            Male_APC_significant.append(row['APC Significant'])
                            Male_AAPC.append("")
                            Male_AAPC_significant.append("")
                            Female_period.append("")
                            Female_APC.append("")
                            Female_APC_significant.append("")
                            Female_AAPC.append("")
                            Female_AAPC_significant.append("")
                        Male_period.append(str(df_AAPC_sub_2['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2['End Obs'].values[0]))
                        Male_APC.append("")
                        Male_APC_significant.append("")
                        Male_AAPC.append(str(round(df_AAPC_sub_2['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2['AAPC C.I. High'].values[0], 2)) + ")")
                        Male_AAPC_significant.append(df_AAPC_sub_2['Statistically Significant (0=No  1=Yes)'].values[0])
                        Female_period.append("")
                        Female_APC.append("")
                        Female_APC_significant.append("")
                        Female_AAPC.append("")
                        Female_AAPC_significant.append("")
                elif df_AAPC_sub_2['Sex'].values[0] == 'Female':
                    if df_AAPC_sub_2['Joinpoint Model'].values[0] == 0:
                        Male_period.append("")
                        Male_APC.append("")
                        Male_APC_significant.append("")
                        Male_AAPC.append("")
                        Male_AAPC_significant.append("")
                        Female_period.append(str(df_AAPC_sub_2['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2['End Obs'].values[0]))
                        Female_APC.append("")
                        Female_APC_significant.append("")
                        Female_AAPC.append(str(round(df_AAPC_sub_2['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2['AAPC C.I. High'].values[0], 2)) + ")")
                        Female_AAPC_significant.append(df_AAPC_sub_2['Statistically Significant (0=No  1=Yes)'].values[0])
                    else:
                        df_APC_sub = df_APC[(df_APC['Cancer'] == cancer) & (df_APC['Country'] == country) & (df_APC['Sex'] == 'Female')]
                        for index, row in df_APC_sub.iterrows():
                            Countries.append("")
                            Registries.append("")
                            Male_period.append("")
                            Male_APC.append("")
                            Male_APC_significant.append("")
                            Male_AAPC.append("")
                            Male_AAPC_significant.append("")
                            Female_period.append(str(row['Segment Start']) + "-" + str(row['Segment End']))
                            Female_APC.append(str(round(row['APC'], 2)) + " (" + str(round(row['APC 95% LCL'], 2)) + " to " + str(round(row['APC 95% UCL'], 2)) + ")")
                            Female_APC_significant.append(row['APC Significant'])
                            Female_AAPC.append("")
                            Female_AAPC_significant.append("")
                        Male_period.append("")
                        Male_APC.append("")
                        Male_APC_significant.append("")
                        Male_AAPC.append("")
                        Male_AAPC_significant.append("")
                        Female_period.append(str(df_AAPC_sub_2['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2['End Obs'].values[0]))
                        Female_APC.append("")
                        Female_APC_significant.append("")
                        Female_AAPC.append(str(round(df_AAPC_sub_2['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2['AAPC C.I. High'].values[0], 2)) + ")")
                        Female_AAPC_significant.append(df_AAPC_sub_2['Statistically Significant (0=No  1=Yes)'].values[0])
            else:
                df_APC_sub_male = df_APC[(df_APC['Cancer'] == cancer) & (df_APC['Country'] == country) & (df_APC['Sex'] == 'Male')]
                df_APC_sub_female = df_APC[(df_APC['Cancer'] == cancer) & (df_APC['Country'] == country) & (df_APC['Sex'] == 'Female')]
                df_AAPC_sub_2_male = df_AAPC_sub_2[df_AAPC_sub_2['Sex'] == 'Male']
                df_AAPC_sub_2_female = df_AAPC_sub_2[df_AAPC_sub_2['Sex'] == 'Female']

                male_joinpoint = df_AAPC_sub_2_male['Joinpoint Model'].values[0]
                female_joinpoint = df_AAPC_sub_2_female['Joinpoint Model'].values[0]
                if male_joinpoint == 0 and female_joinpoint == 0:
                    Male_period.append(str(df_AAPC_sub_2_male['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_male['End Obs'].values[0]))
                    Male_APC.append("")
                    Male_APC_significant.append("")
                    Male_AAPC.append(str(round(df_AAPC_sub_2_male['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_male['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_male['AAPC C.I. High'].values[0], 2)) + ")")
                    Male_AAPC_significant.append(df_AAPC_sub_2_male['Statistically Significant (0=No  1=Yes)'].values[0])
                    Female_period.append(str(df_AAPC_sub_2_female['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_female['End Obs'].values[0]))
                    Female_APC.append("")
                    Female_APC_significant.append("")
                    Female_AAPC.append(str(round(df_AAPC_sub_2_female['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_female['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_female['AAPC C.I. High'].values[0], 2)) + ")")
                    Female_AAPC_significant.append(df_AAPC_sub_2_female['Statistically Significant (0=No  1=Yes)'].values[0])
                elif male_joinpoint == 0 and female_joinpoint > 0:
                    for index, row in df_APC_sub_female.iterrows():
                        Countries.append("")
                        Registries.append("")
                        Male_period.append("")
                        Male_APC.append("")
                        Male_APC_significant.append("")
                        Male_AAPC.append("")
                        Male_AAPC_significant.append("")
                        Female_period.append(str(row['Segment Start']) + "-" + str(row['Segment End']))
                        Female_APC.append(str(round(row['APC'], 2)) + " (" + str(round(row['APC 95% LCL'], 2)) + " to " + str(round(row['APC 95% UCL'], 2)) + ")")
                        Female_APC_significant.append(row['APC Significant'])
                        Female_AAPC.append("")
                        Female_AAPC_significant.append("")
                    Male_period.append(str(df_AAPC_sub_2_male['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_male['End Obs'].values[0]))
                    Male_APC.append("")
                    Male_APC_significant.append("")
                    Male_AAPC.append(str(round(df_AAPC_sub_2_male['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_male['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_male['AAPC C.I. High'].values[0], 2)) + ")")
                    Male_AAPC_significant.append(df_AAPC_sub_2_male['Statistically Significant (0=No  1=Yes)'].values[0])
                    Female_period.append(str(df_AAPC_sub_2_female['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_female['End Obs'].values[0]))
                    Female_APC.append("")
                    Female_APC_significant.append("")
                    Female_AAPC.append(str(round(df_AAPC_sub_2_female['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_female['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_female['AAPC C.I. High'].values[0], 2)) + ")")
                    Female_AAPC_significant.append(df_AAPC_sub_2_female['Statistically Significant (0=No  1=Yes)'].values[0])
                elif male_joinpoint > 0 and female_joinpoint == 0:
                    for index, row in df_APC_sub_male.iterrows():
                        Countries.append("")
                        Registries.append("")
                        Male_period.append(str(row['Segment Start']) + "-" + str(row['Segment End']))
                        Male_APC.append(str(round(row['APC'], 2)) + " (" + str(round(row['APC 95% LCL'], 2)) + " to " + str(round(row['APC 95% UCL'], 2)) + ")")
                        Male_APC_significant.append(row['APC Significant'])
                        Male_AAPC.append("")
                        Male_AAPC_significant.append("")
                        Female_period.append("")
                        Female_APC.append("")
                        Female_APC_significant.append("")
                        Female_AAPC.append("")
                        Female_AAPC_significant.append("")
                    Male_period.append(str(df_AAPC_sub_2_male['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_male['End Obs'].values[0]))
                    Male_APC.append("")
                    Male_APC_significant.append("")
                    Male_AAPC.append(str(round(df_AAPC_sub_2_male['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_male['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_male['AAPC C.I. High'].values[0], 2)) + ")")
                    Male_AAPC_significant.append(df_AAPC_sub_2_male['Statistically Significant (0=No  1=Yes)'].values[0])
                    Female_period.append(str(df_AAPC_sub_2_female['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_female['End Obs'].values[0]))
                    Female_APC.append("")
                    Female_APC_significant.append("")
                    Female_AAPC.append(str(round(df_AAPC_sub_2_female['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_female['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_female['AAPC C.I. High'].values[0], 2)) + ")")
                    Female_AAPC_significant.append(df_AAPC_sub_2_female['Statistically Significant (0=No  1=Yes)'].values[0])
                else:
                    male_more = 0
                    female_more = 0
                    if male_joinpoint > female_joinpoint:
                        female_more = male_joinpoint - female_joinpoint
                    elif male_joinpoint < female_joinpoint:
                        male_more = female_joinpoint - male_joinpoint
                    
                    for i in range(max(male_joinpoint, female_joinpoint) + 1):
                        Countries.append("")
                        Registries.append("")

                    for index, row in df_APC_sub_male.iterrows():
                        Male_period.append(str(row['Segment Start']) + "-" + str(row['Segment End']))
                        Male_APC.append(str(round(row['APC'], 2)) + " (" + str(round(row['APC 95% LCL'], 2)) + " to " + str(round(row['APC 95% UCL'], 2)) + ")")
                        Male_APC_significant.append(row['APC Significant'])
                        Male_AAPC.append("")
                        Male_AAPC_significant.append("")
                    
                    for index, row in df_APC_sub_female.iterrows():
                        Female_period.append(str(row['Segment Start']) + "-" + str(row['Segment End']))
                        Female_APC.append(str(round(row['APC'], 2)) + " (" + str(round(row['APC 95% LCL'], 2)) + " to " + str(round(row['APC 95% UCL'], 2)) + ")")
                        Female_APC_significant.append(row['APC Significant'])
                        Female_AAPC.append("")
                        Female_AAPC_significant.append("")
                    
                    for m in range(male_more):
                        Male_period.append("")
                        Male_APC.append("")
                        Male_APC_significant.append("")
                        Male_AAPC.append("")
                        Male_AAPC_significant.append("")
                    
                    for f in range(female_more):
                        Female_period.append("")
                        Female_APC.append("")
                        Female_APC_significant.append("")
                        Female_AAPC.append("")
                        Female_AAPC_significant.append("")
                    
                    Male_period.append(str(df_AAPC_sub_2_male['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_male['End Obs'].values[0]))
                    Male_APC.append("")
                    Male_APC_significant.append("")
                    Male_AAPC.append(str(round(df_AAPC_sub_2_male['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_male['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_male['AAPC C.I. High'].values[0], 2)) + ")")
                    Male_AAPC_significant.append(df_AAPC_sub_2_male['Statistically Significant (0=No  1=Yes)'].values[0])
                    Female_period.append(str(df_AAPC_sub_2_female['Start Obs'].values[0]) + "-" + str(df_AAPC_sub_2_female['End Obs'].values[0]))
                    Female_APC.append("")
                    Female_APC_significant.append("")
                    Female_AAPC.append(str(round(df_AAPC_sub_2_female['AAPC'].values[0], 2)) + " (" + str(round(df_AAPC_sub_2_female['AAPC C.I. Low'].values[0], 2)) + " to " + str(round(df_AAPC_sub_2_female['AAPC C.I. High'].values[0], 2)) + ")")
                    Female_AAPC_significant.append(df_AAPC_sub_2_female['Statistically Significant (0=No  1=Yes)'].values[0])

        df_table = pd.DataFrame({
            "Countries" : Countries, 
            "Registries" : Registries, 
            "Male period" : Male_period, 
            "Male APC, % (95% CI)" : Male_APC, 
            "Male APC significant" : Male_APC_significant, 
            "Male AAPC, % (95% CI)" : Male_AAPC, 
            "Male AAPC significant" : Male_AAPC_significant, 
            "Female period" : Female_period, 
            "Female APC, % (95% CI)" : Female_APC, 
            "Female APC significant" : Female_APC_significant, 
            "Female AAPC, % (95% CI)" : Female_AAPC, 
            "Female AAPC significant" : Female_AAPC_significant
        })
        
        df_table.to_csv(directory_path + "/" + cancer + ".csv", index=False)
        print(f"{cancer} 완료.")
    
def main():
    df_APC, df_AAPC = upload_file()
    directory_path = saving_directory()

    df_registries = registries()

    get_tables(df_APC, df_AAPC, df_registries, directory_path)
    print(f"\n모두 완료되었습니다. {directory_path}를 확인하세요.")
    
if __name__ == "__main__":
    main()
