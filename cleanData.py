import pandas as pd
import numpy as np

df = pd.DataFrame()

def getCleaned(DF,Target=False):
    df=DF

    #replace every cell containing '?' with NaN
    df.replace('?', np.NaN, inplace=True)                   

    #Obtain the headings of the dataframe
    columns = list(df.head(0))                                   

    #if last column is the target, remove the rows containing null
    if(Target==True):
        df.dropna(subset=[columns[-1]], axis=0, inplace=True)       
        df.reset_index(drop=True, inplace=True)      

    #Delete Rows that contain duplicates
    df.drop_duplicates(inplace=True)

    #Delete Columns thathave single values 
    for key, value in df.items():
        if len(df[key].unique())==1:
            del df[key]               

    return df




# #Describe a Dataframe using Dataframe.describe()
# desc = df.describe()

# #Describe the objects as well
# desc2 = df.describe(include="all")

# #obtaining specific columns only. and their description
# col_only = df[['symboling','make','body-style']]
# desc3 = df[['symboling','make','body-style']].describe(include="all")

# #Describe/Summarize using Dataframe.info()
# df.info()

# #a new path for the csv file to be saved
# path = r"C:\Users\vinee\Desktop\3rd_YEAR\Data_Analysis\automobile.csv"

# #save the dataframe as a new csv file.index=False means the index row(0,1,2,...) will not be included
# df.to_csv(path, index=False) 
