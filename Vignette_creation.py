import pandas as pd
import numpy as np


##############################################
# Create Master file for Context 1 (Football)
##############################################

# Create lists for each info block
c1_agent = ["Professional football player",
            "Pre-programmed AI"]
c1_outcome1 = ["A goal is scored for the Agent's team",
               "A goal is not scored for the Agent's team"]
c1_outcome2 = ["win",
               "lose"]
c1_Action = ["Agent shoots to score",
             "Agent passes"]
c1_Incentives = ["the number of goals scored",
                 "whether the team wins or loses"]

c1_Pivot = ["The winning team won by 1 goal",
            "The winning team won by 3 goals"]

# Transform the lists into 1x2 dataframes
df1 = pd.DataFrame(c1_agent, columns=['Agent'])
df2 = pd.DataFrame(c1_outcome1, columns=['Outcome1'])
df3 = pd.DataFrame(c1_outcome2, columns=['Outcome2'])
df4 = pd.DataFrame(c1_Action, columns=['Action'])
df5 = pd.DataFrame(c1_Incentives, columns=['Incentive'])
df6 = pd.DataFrame(c1_Pivot, columns=['Pivotality'])

# Create cartesion products by joining on a constant (0)
df1['key'] = 0
df2['key'] = 0
df3['key'] = 0
df4['key'] = 0
df5['key'] = 0
df6['key'] = 0

df_combined = ((((df1.merge(df2, on='key', how='outer')).merge(
    df3, on='key', how='outer')).merge(
    df4, on='key', how='outer')).merge(
    df5, on='key', how='outer')).merge(
    df6, on='key', how='outer').drop(columns='key')

# Randomly split the cartesion product into 4 equally sized samples (16 vignettes); (Repeat this 15 times)
# Creates a balanced distribution at both an individual and population level
# Creates 16 vignettes for each of the 60 participants, each option is repeated exactly 15 times
for i in range (15):
    df_temp = df_combined.sample(frac=1)
    Sample1 = df_temp[:16]
    Sample1['Subject'] = 1 + (i*4)
    Sample2 = df_temp[16:32]
    Sample2['Subject'] = 2 + (i*4)
    Sample3 = df_temp[32:48]
    Sample3['Subject'] = 3 + (i*4)
    Sample4 = df_temp[48:]
    Sample4['Subject'] = 4 + (i*4)
    if i == 0:
        DF_Output_Football = ((Sample1.append(Sample2)).append(Sample3)).append(Sample4)
    if i > 0:
        DF_Output_Football = DF_Output_Football.append(((Sample1.append(Sample2)).append(Sample3)).append(Sample4))

DF_Output_Football['Context'] = 'Football'
###################################################################################

##############################################
# Create Master file for Context 2 (Business)
##############################################

# Create lists for each info block
c2_agent = ["Senior business executive",
            "Pre-programmed AI"]
c2_outcome1 = ["Company profits increase",
               "Company profits decrease"]
c2_outcome2 = ["improve",
               "worsen"]
c2_Action = ["Agent votes to adopt new strategy",
             "Agent votes to keep existing strategy"]
c2_Incentives = ["company profits",
                 "environmental footprint"]
c2_Pivot = ["Motion passes by 1 vote",
            "Motion passes by 3 votes"]

# Transform the lists into 1x2 dataframes
df1 = pd.DataFrame(c2_agent, columns=['Agent'])
df2 = pd.DataFrame(c2_outcome1, columns=['Outcome1'])
df3 = pd.DataFrame(c2_outcome2, columns=['Outcome2'])
df4 = pd.DataFrame(c2_Action, columns=['Action'])
df5 = pd.DataFrame(c2_Incentives, columns=['Incentive'])
df6 = pd.DataFrame(c2_Pivot, columns=['Pivotality'])

# Create cartesion products by joining on a constant (0)
df1['key'] = 0
df2['key'] = 0
df3['key'] = 0
df4['key'] = 0
df5['key'] = 0
df6['key'] = 0

df_combined = ((((df1.merge(df2, on='key', how='outer')).merge(
    df3, on='key', how='outer')).merge(
    df4, on='key', how='outer')).merge(
    df5, on='key', how='outer')).merge(
    df6, on='key', how='outer').drop(columns='key')

# Randomly split the cartesion product into 4 equally sized samples (16 vignettes); (Repeat this 15 times)
# Creates a balanced distribution at both an individual and population level
# Creates 16 vignettes for each of the 60 participants, each option is repeated exactly 15 times
for i in range (15):
    df_temp = df_combined.sample(frac=1)
    Sample1 = df_temp[:16]
    Sample1['Subject'] = 1 + (i*4)
    Sample2 = df_temp[16:32]
    Sample2['Subject'] = 2 + (i*4)
    Sample3 = df_temp[32:48]
    Sample3['Subject'] = 3 + (i*4)
    Sample4 = df_temp[48:]
    Sample4['Subject'] = 4 + (i*4)
    if i == 0:
        DF_Output_Business = ((Sample1.append(Sample2)).append(Sample3)).append(Sample4)
    if i > 0:
        DF_Output_Business = DF_Output_Business.append(((Sample1.append(Sample2)).append(Sample3)).append(Sample4))

DF_Output_Business['Context'] = 'Business'
###################################################################################

# Combine the vignette templates
DF_Output_Final = DF_Output_Football.append(DF_Output_Business)

# Add a random column so as to shuffle the contexts between rounds
DF_Output_Final['Randomizer'] = np.random.randint(1, 1000, DF_Output_Final.shape[0])

DF_Output_Final = DF_Output_Final.sort_values(['Subject', 'Randomizer'], ascending=[True, False])

DF_Output_Final['RoundNum'] = DF_Output_Final.groupby(['Subject']).cumcount()+1

DF_Output_Final = DF_Output_Final.drop(columns=['Randomizer'])

DF_Output_Final.to_csv('Vignettes.csv', index=False)

