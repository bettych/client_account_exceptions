import pandas as pd
import numpy as np

# Read in tableau export
df = pd.read_csv('working files/current week.csv', 
                    na_filter=False,
                    encoding = "ISO-8859-1",
                    dtype={'EmpID': 'str'})
                    # TODO: set Account Number as index

# Column: Team Name
# Add team name by EmpID
team_name = pd.read_csv('working files/Team Name.csv', 
                        na_filter=False,
                        dtype={'EmpID': 'str'})
df = pd.merge(left=df, right=team_name, how='left')
df.loc[(df['Team Name'].isna()), "Team Name"] = "#N/A"


# Column: Round
# Update blank Round to "Done" where Team Name is NOT null
df.loc[(df['Team Name']!="#N/A") & (df['Round']==""), "Round"] = "Done"


# Column: New Household Name
#         New Owner ID
#         New Owner Name
# Add new info by Account Number
new = pd.read_csv('working files/account_and_household.csv', 
                        na_filter=False,
                        encoding = "ISO-8859-1",
                        dtype={'Owner ID': 'str'},
                        usecols=['Account Number',
                                 'Household',
                                 'Owner ID',
                                 'Owner Name'])
new = new.drop_duplicates(subset=['Account Number'])
df = pd.merge(left=df, right=new, how='left')
df.loc[(df['Household'].isna()), "Household"] = "#N/A"
df.loc[(df['Household']==""), "Household"] = "0"
df.loc[(df['New Owner ID'].isna()), "New Owner ID"] = "#N/A"
df.loc[(df['New Owner Name'].isna()), "New Owner Name"] = "#N/A"


# Column: New in DB
# Is the owner in current database?
# Leave #N/A as is for Sales Team
df['New in DB'] = np.where(df['New Owner ID']=="#N/A", "#N/A",
                    np.where(df['New Owner ID']==df['DBID'], "Yes", "No"))
# TODO: multiple replace?

# Column: Added?
df['Added?'] = np.where(df['Household']=="", "Yes", "No")

# Column: GenX Owner Name
# Add GenX info by Account Number
genXsys = pd.read_csv('working files/genxsys.csv', na_filter=False)
genXsys = genXsys.drop_duplicates(subset=['genx_name'])
df = pd.merge(df, genXsys['genx_name'], 
                left_on="Account Number", 
                right_on=[genXsys["ACCOUNT_NUMBER"]], 
                how='left')

# TODO: get last report's status and comments
# TODO: sort

# Export dataframe to csv file
df.to_csv("current week - updated.csv", index=False)