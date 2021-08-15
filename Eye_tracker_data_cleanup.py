import numpy as np
import pandas as pd
from datetime import datetime, date


# Import Personal Data
P57_Personal = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Personal_57.xlsx")
P58_Personal = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Personal_58.xlsx")
P59_Personal = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Personal_59.xlsx")
P60_Personal = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Personal_60.xlsx")

# Import Results Data
P57_Results = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Results_57.xlsx")
P58_Results  = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Results_58.xlsx")
P59_Results  = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Results_59.xlsx")
P60_Results  = pd.read_excel("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\Results_60.xlsx")

# Import Gazepoint Data
P57_EyeTrack = pd.read_csv("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\P57.csv")
P58_EyeTrack  = pd.read_csv("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\P58.csv")
P59_EyeTrack = pd.read_csv("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\P59.csv")
P60_EyeTrack  = pd.read_csv("C:\\Users\\Matt\\Desktop\\MATLAB\\Thesis\\Experiment Results\\P60.csv")

# Append Results datasets
Results_Combined = P57_Results.append(P58_Results.append(P59_Results.append(P60_Results)))
Personal_Combined = P57_Personal.append(P58_Personal.append(P59_Personal.append(P60_Personal)))
Personal_Combined.to_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Eye_tracking_personal.csv', index=False)


# Set values to duples
Results_Combined['Agent'] = Results_Combined['Agent'].replace(['Senior business executive','Professional football player','Pre-programmed AI'],[1,1,0])
Results_Combined['Outcome1'] = Results_Combined['Outcome1'].replace(['Company profits decrease','Company profits increase',"A goal is not scored for the Agent's team","A goal is scored for the Agent's team"],[0,1,0,1])
Results_Combined['Outcome2'] = Results_Combined['Outcome2'].replace(['worsen','improve',"lose","win"],[0,1,0,1])
Results_Combined['Action'] = Results_Combined['Action'].replace(['Agent votes to keep existing strategy','Agent votes to adopt new strategy',"Agent passes","Agent shoots to score"],[0,1,0,1])
Results_Combined['Incentive'] = Results_Combined['Incentive'].replace(['company profits','environmental footprint',"the number of goals scored","whether the team wins or loses"],[0,1,0,1])
Results_Combined['Pivotality'] = Results_Combined['Pivotality'].replace(['Motion passes by 3 votes','Motion passes by 1 vote',"The winning team won by 3 goals","The winning team won by 1 goal"],[0,1,0,1])
Results_Combined['DummyText'] = Results_Combined['Dummy'].replace(['A','B'],[0,1])


# Time analysis
for i in [57,58,59,60]:

    globals()[f'P{i}_Abridged'] = globals()[f'P{i}_EyeTrack'].iloc[:, [0,8,9]]
    globals()[f'P{i}_Abridged'].rename(columns={globals()[f'P{i}_Abridged'].columns[0]: "Time", globals()[f'P{i}_Abridged'].columns[1]: "BestX", globals()[f'P{i}_Abridged'].columns[2]: "BestY"}, inplace=True)

    MatlabConfStart = globals()[f'P{i}_Personal'].at[0, 'ConfStart']
    MatlabConfEnd = globals()[f'P{i}_Personal'].at[0, 'ConfEnd']
    GazepointRecordStart = globals()[f'P{i}_EyeTrack'].columns[0]

    MatlabConfStartTime = MatlabConfStart[-8:]
    MatlabConfEndTime = MatlabConfEnd[-8:]
    GazepointStart = GazepointRecordStart[-13:-5]

    MatlabConfStartTime1 = datetime.strptime(MatlabConfStartTime,'%H:%M:%S').time()
    MatlabConfEndtime1 = datetime.strptime(MatlabConfEndTime,'%H:%M:%S').time()
    GazepointStart = datetime.strptime(GazepointStart,'%H:%M:%S').time()
    TimeTrackToConf = (datetime.combine(date.today(), MatlabConfStartTime1) - datetime.combine(date.today(), GazepointStart)).total_seconds()
    
    #Round start and end times
    for roundnum in range(1,33):
        roundkey = roundnum-1
        RoundStart = globals()[f'P{i}_Results'].at[roundkey, 'StartTime']
        RoundEnd = globals()[f'P{i}_Results'].at[roundkey, 'EndTime']
        CleanStart = datetime.strptime(RoundStart[-8:],'%H:%M:%S').time()
        CleanEnd = datetime.strptime(RoundEnd[-8:],'%H:%M:%S').time()
        Round_LB = (datetime.combine(date.today(), CleanStart) - datetime.combine(date.today(), GazepointStart)).total_seconds()
        Round_UB = (datetime.combine(date.today(), CleanEnd) - datetime.combine(date.today(), GazepointStart)).total_seconds()
        for index, row in globals()[f'P{i}_Abridged'].iterrows():
            if (row["Time"] > Round_LB) & (row["Time"] < Round_UB):
                globals()[f'P{i}_Abridged'].at[index,'Round'] = roundnum
    
#Center points for each player's AOI
    for j in range(1,8):
        LowerBound = TimeTrackToConf + (3*(j-1))
        UpperBound = TimeTrackToConf + (3*j)
        globals()[f'attention_stim_{j}'] = globals()[f'P{i}_Abridged'][(globals()[f'P{i}_Abridged']['Time']>LowerBound) & (globals()[f'P{i}_Abridged']['Time']<=UpperBound)]
#        print(j)
#        print(globals()[f'attention_stim_{j}'])
        globals()[f'P_{i}_MeanX_stim_{j}'] = globals()[f'attention_stim_{j}']["BestX"].iloc[-1]
        globals()[f'P_{i}_MeanY_stim_{j}'] = globals()[f'attention_stim_{j}']["BestY"].iloc[-1]
    
    globals()[f'P_{i}_X_s'] = [None] * 7
    globals()[f'P_{i}_Y_s'] = [None] * 7
    for w in range(1,8):
        globals()[f'P_{i}_X_s'][w-1] = globals()[f'P_{i}_MeanX_stim_{w}']
        globals()[f'P_{i}_Y_s'][w-1] = globals()[f'P_{i}_MeanY_stim_{w}']
    
    #Classify each fixation into an AOI if applicable 
def ClassifyAOI(table, i):
    for index, row in table.iterrows():
        if (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_1']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_1']) < 0.15):
            Info="Agent"
        elif (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_2']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_2']) < 0.15):
            Info="Action"
        elif (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_3']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_3']) < 0.15):
            Info="Incentive"
        elif (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_4']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_4']) < 0.15):
            Info="Pivotality"
        elif (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_5']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_5']) < 0.15):
            Info="ST_Outcome"
        elif (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_6']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_6']) < 0.15):
            Info="Dummy"
        elif (abs(row["BestX"] - globals()[f'P_{i}_MeanX_stim_7']) < 0.15) & (abs(row["BestY"] - globals()[f'P_{i}_MeanY_stim_7']) < 0.15):
            Info="End_Outcome"
        else:
            Info="N/A"    
        table.at[index,'ViewedInfo'] = Info

# Run using the coordinates from the most successful participant's callibration (given that the others didn't work)
# Mention in limitations
ClassifyAOI(P57_Abridged,58)
ClassifyAOI(P58_Abridged,58)
ClassifyAOI(P59_Abridged,58)
ClassifyAOI(P60_Abridged,58)

# Now add durations
for i in [57,58,59,60]:
    for h in range(1,len(globals()[f'P{i}_Abridged'])):
        globals()[f'P{i}_Abridged'].loc[h,"Duration"] = (globals()[f'P{i}_Abridged'].loc[h,"Time"]- globals()[f'P{i}_Abridged'].loc[h-1,"Time"])*1000 #milliseconds
    globals()[f'P{i}_Abridged']["Participant"] = i

# Combine together
All_Together = P57_Abridged.append(P58_Abridged.append(P59_Abridged.append(P60_Abridged)))
# Only interested in attention during rounds
All_Together = All_Together[All_Together["Round"].between(1, 32, inclusive=True)]  

# Sum durations per stimuli per participant per round
Rolled_Together = All_Together.groupby(['Participant','Round','ViewedInfo']).sum()        
# Reshape to be one row per participant per round
Rolled_Pivot = Rolled_Together.pivot_table(index=['Participant','Round'], columns='ViewedInfo',values='Duration')

# Join to the main results table
Combined_Eye_Tracking_Results = Results_Combined.merge(Rolled_Pivot, left_on=['ParticipantNum','TrialNumber'],right_on=['Participant','Round'],suffixes=('','_time'))
# Export to csv
Combined_Eye_Tracking_Results.to_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Eye_tracking_results.csv', index=False)

