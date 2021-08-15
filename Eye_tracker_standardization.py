# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 12:39:06 2021

@author: Matt
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
# Import the data
Eye_track = pd.read_csv("C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Eye_tracking_results.csv")
Personal_Combined = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Eye_tracking_personal.csv')


# As discussed in the thesis, we exclude outlier p57
Eye_track = Eye_track[Eye_track["ParticipantNum"]>57]

# Standardize in the same way as done for online experiment (ie difference from mean, then divide by std dev)
TimeVars = ['Action_time','Agent_time','Incentive_time','Pivotality_time', 'ST_Outcome', 'Dummy_time','End_Outcome']
Eye_track1 = Eye_track.join(Eye_track[TimeVars].sub(Eye_track.groupby('Context')[TimeVars].transform('mean')).add_suffix('_md'))

# Rename so as to work with online regressions
Eye_track1.rename(columns={ "Action_time_md": "Time_Action_md",
                            "Agent_time_md": "Time_Agent_md",
                            "Incentive_time_md":"Time_Incentive_md",
                            "ST_Outcome_md" :"Time_ST_Outcome_md",
                           "Pivotality_time_md": "Time_Pivotal_md",
                           "Dummy_time_md": "Time_Dummy_md",
                           "End_Outcome_md": "Time_EndOutcome_md",
                           "Agent": "Is_Human",
                           "Outcome1": "ST_Outcome",
                           "Outcome2": "End_Outcome",
                           "Action":"TakesAction",
                           "Pivotality":"Is_Pivotal",
                           "Incentive": "MotivatedByEndOutcome"
                           
                           }, inplace=True)


# Replace null time-values with 0
Eye_track1 = Eye_track1.fillna(0)
Eye_track1.reset_index(inplace=True)
TimeVars = ['Time_Action_md','Time_Agent_md','Time_Incentive_md','Time_Pivotal_md', 'Time_ST_Outcome_md', 'Time_Dummy_md','Time_EndOutcome_md']

Scalar = StandardScaler()
Newtime = pd.DataFrame(Scalar.fit_transform(Eye_track1[TimeVars]))
Newtime = Newtime.set_axis(TimeVars, axis=1)
Eye_track_standardized = Eye_track1.join(Newtime, rsuffix='_Z')


# Restructure personal data
for index, row in Eye_track_standardized.iterrows():
    Eye_track_standardized.at[index,'Is_SouthAfrican'] = 0 # All participants were European in this run
    Eye_track_standardized.at[index,'PostGraduateDegree'] = 1 # All participants have MSc in Business Economics
    Eye_track_standardized.at[index,'InfoOrderGroup'] = "A" # All participants were in InfoOrderGroup A
    Eye_track_standardized.at[index,'InfoOrderB'] = 0
    Eye_track_standardized.at[index,'InfoOrderC'] = 0
    if row["Context"] == "Football":
        Isfootball = 1
    else:
        Isfootball = 0
    player = row["ParticipantNum"]
    player_pers = Personal_Combined[Personal_Combined["ParticipantNum"]==player]
    player_pers.reset_index(inplace=True)
    player_ans = player_pers.iloc[0,player_pers.columns.get_loc('Numeracy')]
    if float(player_ans) == 25.0:
        CorrectNumeracy = 1
    else:
        CorrectNumeracy = 0
    Eye_track_standardized.at[index,'CorrectNumeracy'] = CorrectNumeracy     
    Eye_track_standardized.at[index,'ContextIsFootball'] = Isfootball

# Export standardized data to csv
Eye_track_standardized.to_csv("C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Eye_tracking_standardized.csv", index=False)
