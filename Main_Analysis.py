# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 12:39:46 2021

@author: Matthew White

Thesis Primary Analysis

Last updated 15 August 2021
"""
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge

from sklearn.tree import export_graphviz
import numpy as np
import statsmodels.formula.api as sm
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt
from subprocess import call

# Set seed for replicability (282 chosen by google random number generator)
np.random.seed(282)

# Import (online) data
results_cleaned = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results_Cleaned.csv')

# Standardization of time variables
TimeVars = ['Time_Action_md','Time_Agent_md','Time_Incentive_md','Time_Pivotal_md', 'Time_ST_Outcome_md', 'Time_Dummy_md','Time_EndOutcome_md']
Scalar = StandardScaler()
Newtime = pd.DataFrame(Scalar.fit_transform(results_cleaned[TimeVars]))
Newtime = Newtime.set_axis(TimeVars, axis=1)
results_standardized = results_cleaned.join(Newtime, rsuffix='_Z')

# Seperate by context
results_business_only = results_standardized[results_standardized['Context'] == 'Business']
results_football_only = results_standardized[results_standardized['Context'] == 'Football']

# Base regression: Causality is a function of the 7 inputs, and the context
BaseRegress = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context", data=results_standardized).fit()
print(BaseRegress.summary())

# Single context base regressions
Football_base = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context", data=results_football_only).fit()
Business_base = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context", data=results_business_only).fit()
print(Football_base.summary())
print(Business_base.summary())

# Add controls participant fixed effects & info order
FixedEffectRegress = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=results_standardized).fit()
print(FixedEffectRegress.summary())


# Add time interactions
FullModel = sm.gls(formula="CausalScore ~ Is_Human*Time_Agent_md_Z + ST_Outcome*Time_ST_Outcome_md_Z + End_Outcome*Time_EndOutcome_md_Z + TakesAction*Time_Action_md_Z + MotivatedByEndOutcome*Time_Incentive_md_Z + Is_Pivotal*Time_Pivotal_md_Z + DummyText*Time_Dummy_md_Z + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=results_standardized).fit()
print(FullModel.summary())

# Single context full regressions
Football_Full = sm.gls(formula="CausalScore ~ Is_Human*Time_Agent_md_Z + ST_Outcome*Time_ST_Outcome_md_Z + End_Outcome*Time_EndOutcome_md_Z + TakesAction*Time_Action_md_Z + MotivatedByEndOutcome*Time_Incentive_md_Z + Is_Pivotal*Time_Pivotal_md_Z + DummyText*Time_Dummy_md_Z  + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=results_football_only).fit()
Business_Full = sm.gls(formula="CausalScore ~ Is_Human*Time_Agent_md_Z + ST_Outcome*Time_ST_Outcome_md_Z + End_Outcome*Time_EndOutcome_md_Z + TakesAction*Time_Action_md_Z + MotivatedByEndOutcome*Time_Incentive_md_Z + Is_Pivotal*Time_Pivotal_md_Z + DummyText*Time_Dummy_md_Z + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=results_business_only).fit()
print(Football_Full.summary())
print(Business_Full.summary())

# Out of sample testing 1: Random samples

#80-20 training and testing split
Randomsplitter = np.random.rand(len(results_standardized)) < 0.8
train = results_standardized[Randomsplitter]
test = results_standardized[~Randomsplitter]

print("Training set: " + str(len(train)))
print("Testing set: " + str(len(test)))

Y_Train = train['CausalScore']
Y_Test = test['CausalScore']
X_TrainRF1 = train[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]
X_TestRF1 = test[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]

## Random Forest (RF1)
# Train the model
RF_Model1 = RandomForestRegressor(max_depth=7, n_estimators=50).fit(X_TrainRF1,Y_Train)

# Test the model
Prediction_RF1 = RF_Model1.predict(X_TestRF1)
R2_RF1 = r2_score(Y_Test, Prediction_RF1)
RMSE_RF1 = sqrt(mean_squared_error(Y_Test, Prediction_RF1))
MAE_RF1 = mean_absolute_error(Y_Test, Prediction_RF1)
parameters = RF_Model1.get_params()
print("TEST RF1 R2 = " + str(R2_RF1))
print("RF1 RMSE = " + str(RMSE_RF1))
print("RF1 MAE = " + str(MAE_RF1))
print(parameters)

# Calculate MDI feature importance
Feature_importance_RF1 = RF_Model1.feature_importances_
StandardError = np.std([tree.feature_importances_ for tree in RF_Model1.estimators_], axis=0)
featurenames = ["Is Human","Z_Species","ST_Outcome","Z_ST_Outcome","End Outcome","Z_End_Outcome","Takes Action","Z_Action","Motivated By End Outcome","Z Incentives","Is Pivotal","Z_Pivotal" ,"Dummy","Z_Dummy","Context (Football)", "Nationality","Correct Numeracy", "Postgraduate Degree", "InfoOrder (B)", "InfoOrder (C)"]
forest_importances = pd.Series(Feature_importance_RF1, index=featurenames)
forest_importances = forest_importances.sort_values(ascending=False)

# Plot MDI feature importance
fig, ax = plt.subplots()
forest_importances.plot.bar(yerr=StandardError, ax=ax)
ax.set_title("Feature Importance using MDI")
ax.set_ylabel("Mean decrease in impurity")
fig.tight_layout()
plt.show()


## Out of sample Ridge Regression
# Fit the model
Ridge_Model = Ridge(alpha=1.0).fit(X_TrainRF1,Y_Train)
# Make a prediction
Prediction_Ridge = Ridge_Model.predict(X_TestRF1)

#Test the accuracy
R2_Ridge = r2_score(Y_Test, Prediction_Ridge)
RMSE_Ridge = sqrt(mean_squared_error(Y_Test, Prediction_Ridge))
MAE_Ridge = mean_absolute_error(Y_Test, Prediction_Ridge)
parameters_ridge = RF_Model1.get_params()
print("Ridge R2 = " + str(R2_Ridge))
print("Ridge RMSE = " + str(RMSE_Ridge))
print("Ridge MAE = " + str(MAE_Ridge))
print(parameters_ridge)

## Out of sample GLS

# M2 out of sample: Train
OOSModel = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree ", data=train).fit()
print(OOSModel.summary())

# M2 Test
OOS_prediction = OOSModel.predict(test)
R2_GLS = r2_score(Y_Test, OOS_prediction)
RMSE_GLS = sqrt(mean_squared_error(Y_Test, OOS_prediction))
MAE_GLS = mean_absolute_error(Y_Test, OOS_prediction)
print("GLS R2 = " + str(R2_GLS))
print("GLS RMSE = " + str(RMSE_GLS))
print("GLS MAE = " + str(MAE_GLS))

# + interactions, accuracy drops
# M3 out of sample: Train
OOSModel_w_interaction = sm.gls(formula="CausalScore ~ Is_Human*Time_Agent_md_Z + ST_Outcome*Time_ST_Outcome_md_Z + End_Outcome*Time_EndOutcome_md_Z + TakesAction*Time_Action_md_Z + MotivatedByEndOutcome*Time_Incentive_md_Z + Is_Pivotal*Time_Pivotal_md_Z + DummyText*Time_Dummy_md_Z + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=train).fit()
# M3 Test
OOS_wInt_prediction = OOSModel_w_interaction.predict(test)
R2_GLS = r2_score(Y_Test, OOS_wInt_prediction)
RMSE_GLS = sqrt(mean_squared_error(Y_Test, OOS_wInt_prediction))
MAE_GLS = mean_absolute_error(Y_Test, OOS_wInt_prediction)
print("GLS2 R2 = " + str(R2_GLS))
print("GLS2 RMSE = " + str(RMSE_GLS))
print("GLS2 MAE = " + str(MAE_GLS))

# Out of sample testing 2: Separate models accross contexts
RandomsplitterBus = np.random.rand(len(results_business_only)) < 0.8
RandomsplitterFoot = np.random.rand(len(results_football_only)) < 0.8

trainBus = results_business_only[RandomsplitterBus]
testBus = results_business_only[~RandomsplitterBus]

trainFoot = results_football_only[RandomsplitterFoot]
testFoot = results_football_only[~RandomsplitterFoot]

print("business set: " + str(len(results_business_only)))
print("football set: " + str(len(results_football_only)))

# Football RF model
Y_Train_Foot = trainFoot['CausalScore']
Y_Test_Foot = testFoot['CausalScore']
X_Train_Foot = trainFoot[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]
X_Test_Foot = testFoot[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]

RF_ModelFoot = RandomForestRegressor(max_depth=7, n_estimators=50).fit(X_Train_Foot,Y_Train_Foot)
Prediction_RFFoot = RF_ModelFoot.predict(X_Test_Foot)

R2_foot = r2_score(Y_Test_Foot, Prediction_RFFoot)
RMSE_foot = sqrt(mean_squared_error(Y_Test_Foot, Prediction_RFFoot))
MAE_foot = mean_absolute_error(Y_Test_Foot, Prediction_RFFoot)
print("RF Football R2 = " + str(R2_foot))
print("RF Football RMSE = " + str(RMSE_foot))
print("RF Football MAE = " + str(MAE_foot))


# Business RF Model
Y_Train_Bus = trainBus['CausalScore']
Y_Test_Bus = testBus['CausalScore']
X_Train_Bus = trainBus[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]
X_Test_Bus = testBus[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]

RF_ModelBus = RandomForestRegressor(max_depth=7, n_estimators=50).fit(X_Train_Bus,Y_Train_Bus)
Prediction_RFBus = RF_ModelBus.predict(X_Test_Bus)

R2_Bus = r2_score(Y_Test_Bus, Prediction_RFBus)
RMSE_Bus = sqrt(mean_squared_error(Y_Test_Bus, Prediction_RFBus))
MAE_Bus = mean_absolute_error(Y_Test_Bus, Prediction_RFBus)
print("RF Business R2 = " + str(R2_Bus))
print("RF Business RMSE = " + str(RMSE_Bus))
print("RF Business MAE = " + str(MAE_Bus))

# Cross context prediction of RF
Prediction_RF_CC = RF_ModelBus.predict(X_Test_Foot)
R2_RF_CC = r2_score(Y_Test_Foot, Prediction_RF_CC)
RMSE_RF_CC = sqrt(mean_squared_error(Y_Test_Foot, Prediction_RF_CC))
MAE_RF_CC = mean_absolute_error(Y_Test_Foot, Prediction_RF_CC)
print("RF CC R2 = " + str(R2_RF_CC))
print("RF CC RMSE = " + str(RMSE_RF_CC))
print("RF CC MAE = " + str(MAE_RF_CC))


# Individual Regressions with each infoblock (robustness checks)
Reg0 = sm.gls(formula="CausalScore ~ Context", data=results_cleaned).fit()
Reg1 = sm.gls(formula="CausalScore ~ Is_Human + Context", data=results_cleaned).fit()
Reg2 = sm.gls(formula="CausalScore ~  ST_Outcome + Context", data=results_cleaned).fit()
Reg3 = sm.gls(formula="CausalScore ~ End_Outcome + Context", data=results_cleaned).fit()
Reg4 = sm.gls(formula="CausalScore ~ TakesAction + Context", data=results_cleaned).fit()
Reg5 = sm.gls(formula="CausalScore ~ MotivatedByEndOutcome +  Context", data=results_cleaned).fit()
Reg6 = sm.gls(formula="CausalScore ~ Is_Pivotal + Context", data=results_cleaned).fit()
Reg7 = sm.gls(formula="CausalScore ~ DummyText + Context", data=results_cleaned).fit()
print(Reg0.summary())
print(Reg1.summary())
print(Reg2.summary())
print(Reg3.summary())
print(Reg4.summary())
print(Reg5.summary())
print(Reg6.summary())
print(Reg7.summary())


# Bonus modelling
BonusRegress = sm.gls(formula="BonusScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=results_standardized).fit()
print(BonusRegress.summary())

# Create a sample tree from RF (11th tree)
estimator = RF_Model1.estimators_[10]

# Export as dot file
export_graphviz(estimator, out_file='tree.dot',
                feature_names = featurenames,
                class_names = "CausalScore",
                rounded = True, proportion = False,
                precision = 2, filled = True)

# Convert to png using system command (requires Graphviz)
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png'], shell=True)


####################
## Regress models on eye_tracking results
# Import eye tracking data
Eye_results = pd.read_csv("C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Eye_tracking_standardized.csv")

# Split X, Y
Eye_trackX = Eye_results[["Is_Human","Time_Agent_md_Z","ST_Outcome","Time_ST_Outcome_md_Z","End_Outcome","Time_EndOutcome_md_Z","TakesAction","Time_Action_md_Z","MotivatedByEndOutcome","Time_Incentive_md_Z","Is_Pivotal","Time_Pivotal_md_Z" ,"DummyText","Time_Dummy_md_Z","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]
Eye_trackY = Eye_results["Causal_Response"]

# RF cross experiment prediction
Prediction_RF_ET = RF_Model1.predict(Eye_trackX)

R2_RF_ET = r2_score(Eye_trackY, Prediction_RF_ET)
RMSE_RF_ET = sqrt(mean_squared_error(Eye_trackY, Prediction_RF_ET))
MAE_RF_ET = mean_absolute_error(Eye_trackY, Prediction_RF_ET)
print("ET RF1 R2 = " + str(R2_RF_ET))
print("ET RF1 RMSE = " + str(RMSE_RF_ET))
print("ET RF1 MAE = " + str(MAE_RF_ET))

# M2 cross experiment prediction
OOS_prediction = OOSModel.predict(Eye_results)
R2_GLS_ET = r2_score(Eye_trackY, OOS_prediction)
RMSE_GLS_ET = sqrt(mean_squared_error(Eye_trackY, OOS_prediction))
MAE_GLS_ET = mean_absolute_error(Eye_trackY, OOS_prediction)
print("GLS R2 ET = " + str(R2_GLS_ET))
print("GLS RMSE ET = " + str(RMSE_GLS_ET))
print("GLS MAE ET = " + str(MAE_GLS_ET))

# RF2 (exclude attention) cross experiment prediction

RF2X =  results_standardized[["Is_Human", "ST_Outcome", "End_Outcome", "TakesAction", "MotivatedByEndOutcome", "Is_Pivotal", "DummyText","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]
RF2Y = results_standardized['CausalScore']
Eye_trackX_2 = Eye_results[["Is_Human","ST_Outcome","End_Outcome","TakesAction","MotivatedByEndOutcome","Is_Pivotal","DummyText","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]

RF_Model2 = RandomForestRegressor(max_depth=5, n_estimators=50).fit(RF2X,RF2Y)
Prediction_RF2 = RF_Model2.predict(Eye_trackX_2)

R2_RF2 = r2_score(Eye_trackY, Prediction_RF2)
RMSE_RF2 = sqrt(mean_squared_error(Eye_trackY, Prediction_RF2))
MAE_RF2 = mean_absolute_error(Eye_trackY, Prediction_RF2)
parameters = RF_Model2.get_params()

print("RF2 R2 = " + str(R2_RF2))
print("RF2 RMSE = " + str(RMSE_RF2))
print("RF3 MAE = " + str(MAE_RF2))
print(parameters)


# RF2 (exclude attention) within experiment prediction

X_TrainRF2 = train[["Is_Human", "ST_Outcome", "End_Outcome", "TakesAction", "MotivatedByEndOutcome", "Is_Pivotal", "DummyText","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]
X_TestRF2 = test[["Is_Human", "ST_Outcome", "End_Outcome", "TakesAction", "MotivatedByEndOutcome", "Is_Pivotal", "DummyText","ContextIsFootball", "Is_SouthAfrican","CorrectNumeracy", "PostGraduateDegree", "InfoOrderB", "InfoOrderC"]]

RF_Model2 = RandomForestRegressor(max_depth=5, n_estimators=50).fit(X_TrainRF2,Y_Train)
Prediction_RF2 = RF_Model2.predict(X_TestRF2)

R2_RF2 = r2_score(Y_Test, Prediction_RF2)
RMSE_RF2= sqrt(mean_squared_error(Y_Test, Prediction_RF2))
MAE_RF2 = mean_absolute_error(Y_Test, Prediction_RF2)

print("RF2 R2 = " + str(R2_RF2))
print("RF2 RMSE = " + str(RMSE_RF2))
print("RF2 MAE = " + str(MAE_RF2))

# End
