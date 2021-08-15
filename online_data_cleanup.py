# -*- coding: utf-8 -*-
"""
Spyder Editor

Import and format results data
"""


import pandas as pd

#Import raw data
results1 = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results session 1.csv')
results2 = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results session 2.csv')
results3 = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results session 3.csv')
results4 = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results session 4.csv')
results4 = results4.drop(9) #duplicated trial. Removed due to imbalance

#Append into a single dataset
results_appended = ((results1.append(results2)).append(results3)).append(results4)

#Only include completed trials
resultscompleted = results_appended[results_appended['CausalDetermine.32.player.CausalScore'].notna()]



###

Participtant_info = resultscompleted[['participant.id_in_session',
                                      'CausalDetermine.1.player.InfoOrderGroup',
                                      'CausalDetermine.32.player.Numeracy_Answer',
                                      'CausalDetermine.32.player.Age',
                                      'CausalDetermine.32.player.Nationality','CausalDetermine.32.player.Education',
                                      'CausalDetermine.32.player.Employment']]
Participtant_info.rename(columns={"participant.id_in_session": "ParticipantID", 
                                                      "CausalDetermine.1.player.InfoOrderGroup": "InfoOrderGroup", 
                                                      "CausalDetermine.32.player.Numeracy_Answer": "NumeracyAns", 
                                                      "CausalDetermine.32.player.Age": "Age",
                                                      "CausalDetermine.32.player.Nationality": "Nationality",
                                                      "CausalDetermine.32.player.Education" : "Education",
                                                      "CausalDetermine.32.player.Employment":"Employment"}, inplace=True)

Contact_info = resultscompleted[["CausalDetermine.32.player.Email_Address", "CausalDetermine.32.player.KeepPosted"]]
Contact_info = Contact_info.rename(columns={"CausalDetermine.32.player.Email_Address": "Email_Address",
                                            "CausalDetermine.32.player.KeepPosted": "KeepPosted"})

#We restructure the data in a function so as not to flood our variable explorer
def Restructure(ResultsTable):
    #We first create a seperate, standardised table for each round
    for i in range(1,33):
        ThisRound = pd.DataFrame()
        #Create string-variables, to call column names in the loop
        CausalScore = "CausalDetermine."+str(i)+".player.CausalScore"
        BonusScore = "CausalDetermine."+str(i)+".player.BonusScore"
        Timeb1 = "CausalDetermine."+str(i)+".player.Timeb1"
        Timeb2 = "CausalDetermine."+str(i)+".player.Timeb2"
        Timeb3 = "CausalDetermine."+str(i)+".player.Timeb3"
        Timeb4 = "CausalDetermine."+str(i)+".player.Timeb4"
        Timeb5 = "CausalDetermine."+str(i)+".player.Timeb5"
        Timeb6 = "CausalDetermine."+str(i)+".player.Timeb6"
        Timeb7 = "CausalDetermine."+str(i)+".player.Timeb7"
        Viewsb1 = "CausalDetermine."+str(i)+".player.Viewsb1"
        Viewsb2 = "CausalDetermine."+str(i)+".player.Viewsb2"
        Viewsb3 = "CausalDetermine."+str(i)+".player.Viewsb3"
        Viewsb4 = "CausalDetermine."+str(i)+".player.Viewsb4"
        Viewsb5 = "CausalDetermine."+str(i)+".player.Viewsb5"
        Viewsb6 = "CausalDetermine."+str(i)+".player.Viewsb6"
        Viewsb7 = "CausalDetermine."+str(i)+".player.Viewsb7"
        InfoOrderGroup = "CausalDetermine."+str(i)+".player.InfoOrderGroup"
        Participant_order = "CausalDetermine."+str(i)+".player.Participant_order"
        Agent = "CausalDetermine."+str(i)+".player.Agent"
        Outcome1 = "CausalDetermine."+str(i)+".player.Outcome1"
        Outcome2 = "CausalDetermine."+str(i)+".player.Outcome2"
        Action = "CausalDetermine."+str(i)+".player.Action"
        Incentive = "CausalDetermine."+str(i)+".player.Incentive"
        Pivotality = "CausalDetermine."+str(i)+".player.Pivotality"
        Context = "CausalDetermine."+str(i)+".player.Context"
        DummyText = "CausalDetermine."+str(i)+".player.Dummy1"
        
        #Add the appropriate columns to this round
        ThisRound["Participant_ID"]=ResultsTable[Participant_order]
        ThisRound["Round"]=i
        ThisRound["InfoOrderGroup"]=ResultsTable[InfoOrderGroup]
        ThisRound["Context"]=ResultsTable[Context]
        ThisRound["CausalScore"]=ResultsTable[CausalScore]
        ThisRound["BonusScore"]=ResultsTable[BonusScore]
        ThisRound["Agent"]=ResultsTable[Agent]
        ThisRound["Outcome1"]=ResultsTable[Outcome1]
        ThisRound["Outcome2"]=ResultsTable[Outcome2]
        ThisRound["Action"]=ResultsTable[Action]
        ThisRound["Incentive"]=ResultsTable[Incentive]
        ThisRound["Pivotality"]=ResultsTable[Pivotality]
        ThisRound["DummyText"]=ResultsTable[DummyText]
        ThisRound["Timeb1"]=ResultsTable[Timeb1]
        ThisRound["Timeb2"]=ResultsTable[Timeb2]
        ThisRound["Timeb3"]=ResultsTable[Timeb3]
        ThisRound["Timeb4"]=ResultsTable[Timeb4]
        ThisRound["Timeb5"]=ResultsTable[Timeb5]
        ThisRound["Timeb6"]=ResultsTable[Timeb6]
        ThisRound["Timeb7"]=ResultsTable[Timeb7]
        ThisRound["Viewsb1"]=ResultsTable[Viewsb1]
        ThisRound["Viewsb2"]=ResultsTable[Viewsb2]
        ThisRound["Viewsb3"]=ResultsTable[Viewsb3]
        ThisRound["Viewsb4"]=ResultsTable[Viewsb4]
        ThisRound["Viewsb5"]=ResultsTable[Viewsb5]
        ThisRound["Viewsb6"]=ResultsTable[Viewsb6]
        ThisRound["Viewsb7"]=ResultsTable[Viewsb7]
    
        # We can now easily append them into a single structured table
        if i==1:
            All_Rounds = ThisRound
        elif i>1: 
            All_Rounds = All_Rounds.append(ThisRound)
        
    return All_Rounds
#Call the function
All_Rounds = Restructure(resultscompleted)

#Replace the text values with their numeric equivalents 
All_Rounds['Agent'] = All_Rounds['Agent'].replace(['Senior business executive','Professional football player','Pre-programmed AI'],[1,1,0])
All_Rounds['Outcome1'] = All_Rounds['Outcome1'].replace(['Company profits decrease','Company profits increase',"A goal is not scored for the Agent's team","A goal is scored for the Agent's team"],[0,1,0,1])
All_Rounds['Outcome2'] = All_Rounds['Outcome2'].replace(['worsen','improve',"lose","win"],[0,1,0,1])
All_Rounds['Action'] = All_Rounds['Action'].replace(['Agent votes to keep existing strategy','Agent votes to adopt new strategy',"Agent passes","Agent shoots to score"],[0,1,0,1])
All_Rounds['Incentive'] = All_Rounds['Incentive'].replace(['company profits','environmental footprint',"the number of goals scored","whether the team wins or loses"],[0,1,0,1])
All_Rounds['Pivotality'] = All_Rounds['Pivotality'].replace(['Motion passes by 3 votes','Motion passes by 1 vote',"The winning team won by 3 goals","The winning team won by 1 goal"],[0,1,0,1])
All_Rounds['DummyText'] = All_Rounds['DummyText'].replace(['A','B'],[0,1])
All_Rounds['CausalScore'] = All_Rounds['CausalScore'].replace(['Not at all', 'Very Slightly', 'Slightly', 'Neutral', 'Moderately', 'Very much','Almost Entirely'],[1,2,3,4,5,6,7])
#All_Rounds['BonusScore'] = All_Rounds['BonusScore'].replace([-10, -1, 0, 1, 10],[1,2,3,4,5])


#Rename as appropriate
All_Rounds.rename(columns={ "Agent": "Is_Human",
                            "Outcome1": "ST_Outcome",
                            "Action":"TakesAction",
                           "Outcome2": "End_Outcome",
                           "Pivotality": "Is_Pivotal",
                           "Incentive": "MotivatedByEndOutcome",
                           
                           
                           }, inplace=True)

#Relate time and num views from button back to information shown (based on context and infoordergroup)
All_Rounds = All_Rounds.reset_index()    
for index, row in All_Rounds.iterrows():
    if (row['InfoOrderGroup'] == 'A') or (row['InfoOrderGroup'] == 'B' and row['Context'] == 'Football'):
        Time_Agent = row['Timeb1']
        Time_Action = row['Timeb2']
        Time_Incentive = row['Timeb3']
        Time_Pivotal = row['Timeb4']
        Time_ST_Outcome = row['Timeb5']
        Time_Dummy = row['Timeb6']
        Time_EndOutcome = row['Timeb7']      
        Views_Agent = row['Viewsb1']
        Views_Action = row['Viewsb2']
        Views_Incentive = row['Viewsb3']
        Views_Pivotal = row['Viewsb4']
        Views_ST_Outcome = row['Viewsb5']
        Views_Dummy = row['Viewsb6']
        Views_EndOutcome = row['Viewsb7']
    elif row['Context']=='Business':
        Time_Agent = row['Timeb4']
        Time_Action = row['Timeb1']
        Time_Incentive = row['Timeb2']
        Time_Pivotal = row['Timeb7']
        Time_ST_Outcome = row['Timeb3']
        Time_Dummy = row['Timeb5']
        Time_EndOutcome = row['Timeb6']
        Views_Agent = row['Viewsb4']
        Views_Action = row['Viewsb1']
        Views_Incentive = row['Viewsb2']
        Views_Pivotal = row['Viewsb7']
        Views_ST_Outcome = row['Viewsb3']
        Views_Dummy = row['Viewsb5']
        Views_EndOutcome = row['Viewsb6']
    elif (row['InfoOrderGroup'] == "C") and (row['Context']=="Football"):
        Time_Agent = row['Timeb3']
        Time_Action = row['Timeb7']
        Time_Incentive = row['Timeb4']
        Time_Pivotal = row['Timeb6']
        Time_ST_Outcome = row['Timeb1']
        Time_Dummy = row['Timeb2']
        Time_EndOutcome = row['Timeb5']
        Views_Agent = row['Viewsb3']
        Views_Action = row['Viewsb7']
        Views_Incentive = row['Viewsb4']
        Views_Pivotal = row['Viewsb6']
        Views_ST_Outcome = row['Viewsb1']
        Views_Dummy = row['Viewsb2']
        Views_EndOutcome = row['Viewsb5']   
    All_Rounds.at[index,'Time_Agent'] = Time_Agent
    All_Rounds.at[index,'Time_Action'] = Time_Action
    All_Rounds.at[index,'Time_Incentive'] = Time_Incentive
    All_Rounds.at[index,'Time_Pivotal'] = Time_Pivotal
    All_Rounds.at[index,'Time_ST_Outcome'] = Time_ST_Outcome
    All_Rounds.at[index,'Time_Dummy'] = Time_Dummy
    All_Rounds.at[index,'Time_EndOutcome'] = Time_EndOutcome
    All_Rounds.at[index,'Views_Agent'] = Views_Agent
    All_Rounds.at[index,'Views_Action'] = Views_Action
    All_Rounds.at[index,'Views_Incentive'] = Views_Incentive
    All_Rounds.at[index,'Views_Pivotal'] = Views_Pivotal
    All_Rounds.at[index,'Views_ST_Outcome'] = Views_ST_Outcome
    All_Rounds.at[index,'Views_Dummy'] = Views_Dummy
    All_Rounds.at[index,'Views_EndOutcome'] = Views_EndOutcome
    if row['Context'] == 'Football':
        All_Rounds.at[index,'ContextIsFootball'] = 1
    else:
        All_Rounds.at[index,'ContextIsFootball'] = 0
    if row['InfoOrderGroup'] == 'B':
        All_Rounds.at[index,'InfoOrderB'] = 1
        All_Rounds.at[index,'InfoOrderC'] = 0
    elif row['InfoOrderGroup'] == 'C':
        All_Rounds.at[index,'InfoOrderB'] = 0
        All_Rounds.at[index,'InfoOrderC'] = 1
    else:
        All_Rounds.at[index,'InfoOrderB'] = 0
        All_Rounds.at[index,'InfoOrderC'] = 0
    
All_Rounds_Cleaned = All_Rounds.drop(columns=['Timeb1', 
                                              'Timeb2', 
                                              'Timeb3', 
                                              'Timeb4', 
                                              'Timeb5', 
                                              'Timeb6', 
                                              'Timeb7', 
                                              'Viewsb1', 
                                              'Viewsb2', 
                                              'Viewsb3', 
                                              'Viewsb4', 
                                              'Viewsb5', 
                                              'Viewsb6', 
                                              'Viewsb7'])

All_Rounds_Cleaned = All_Rounds_Cleaned.fillna(0)

#Add a column for each time variable, which is the deviation from the mean
TimeVars = ['Time_Action','Time_Agent','Time_Incentive','Time_Pivotal', 'Time_ST_Outcome', 'Time_Dummy','Time_EndOutcome']
All_Rounds_Cleaned1 = All_Rounds_Cleaned.join(All_Rounds_Cleaned[TimeVars].sub(All_Rounds_Cleaned.groupby('Context')[TimeVars].transform('mean')).add_suffix('_md'))



for index, row in Participtant_info.iterrows():
    if row['Nationality'] in ["South African","SA","Cypriot and South African","","RSA","South Africna"]:
        Is_SouthAfrican = 1
    else:
        Is_SouthAfrican = 0
    if row['NumeracyAns'] == 25:
        CorrectNumeracy = 1
    else:
        CorrectNumeracy = 0
    if row['Education'] in ["4) Postgraduate Diploma/Honours Degree","5) Master's Degree","6) PhD or Higher"]:
        PostGraduateDegree = 1
    else:
        PostGraduateDegree = 0
    Participtant_info.at[index,'Is_SouthAfrican'] = Is_SouthAfrican
    Participtant_info.at[index,'CorrectNumeracy'] = CorrectNumeracy
    Participtant_info.at[index,'PostGraduateDegree'] = PostGraduateDegree
    


#join fixed effects back onto the main dataset
FixedEffects = Participtant_info[['ParticipantID','Is_SouthAfrican','CorrectNumeracy','PostGraduateDegree']]  # df2 but only with columns x, a, and b

All_Rounds_Cleaned_Final = All_Rounds_Cleaned1.merge(FixedEffects,how='left',left_on='Participant_ID', right_on='ParticipantID')  
All_Rounds_Cleaned_Final = All_Rounds_Cleaned_Final.drop(columns=['ParticipantID'])

All_Rounds_Cleaned_Final.to_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results_Cleaned.csv', index=False)
Participtant_info.to_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Participant_Information.csv', index=False)

