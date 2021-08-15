# Individuals' decision trees

import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster import hierarchy
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as sm

# Set seed for replicability
np.random.seed(282)

# Import data
results_cleaned = pd.read_csv('C:\\Users\\Matt\\PycharmProjects\\MSCThesis\\Results_Cleaned.csv')

# We train a tree for each participant
ParticipantList = list(dict.fromkeys(results_cleaned['Participant_ID'])) # dictionary used to remove duplicates
ParticipantList.sort()
for i in ParticipantList:
    globals()[f'Participant_{i}'] = results_cleaned[results_cleaned['Participant_ID']==i]
    # Define the tree
    MyTreeModel = tree.DecisionTreeRegressor(max_depth=4)
    # Define the inputs and target
    MyX = globals()[f'Participant_{i}'][["Is_Human","ST_Outcome","End_Outcome","TakesAction","MotivatedByEndOutcome","Is_Pivotal","DummyText","ContextIsFootball"]]
    MyY = globals()[f'Participant_{i}']['CausalScore']
    # Fit the model
    MyTreeModel = MyTreeModel.fit(MyX,MyY)
    # Get MDI feature importances and save into a combined dataframe
    Feature_importances = MyTreeModel.feature_importances_
    DF_importances = pd.DataFrame([Feature_importances])
    DF_importances.columns = ["Is_Human","ST_Outcome","End_Outcome","TakesAction","MotivatedByEndOutcome","Is_Pivotal","DummyText","ContextIsFootball"]
    DF_importances["Participant"] = i
    if i == 1:
        ALL_Participants_FI = DF_importances
    else:
        ALL_Participants_FI = ALL_Participants_FI.append(DF_importances)

# Example tree for appendix
plt.figure(figsize=(22,12))  # set plot size (denoted in inches)
tree.plot_tree(MyTreeModel, fontsize=10, feature_names=["Is_Human","ST_Outcome","End_Outcome","TakesAction","MotivatedByEndOutcome","Is_Pivotal","DummyText","ContextIsFootball"])
plt.show()

# Cluster similar trees
ALL_Participants_clustering = ALL_Participants_FI
ALL_Participants_clustering = ALL_Participants_clustering.drop(columns=['Participant']) # Exclude participant number from inputs
Clustermodel = AgglomerativeClustering(distance_threshold=None, n_clusters=5)
Clustermodel.fit(ALL_Participants_clustering)
Z = hierarchy.linkage(Clustermodel.children_, 'ward')
# Hierachy map
plt.figure(figsize=(20,10))
dn = hierarchy.dendrogram(Z)
print(Clustermodel.get_params())

# Fit the clusters
Clusters = Clustermodel.fit_predict(ALL_Participants_clustering)

# Add clusters to the Feature importances dataset
ALL_Participants_FI["Cluster"] = Clusters

# Export to csv for visual analysis
ALL_Participants_FI.to_csv("Individual_FI.csv")

## M2 between clusters

# Standardization of time variables
TimeVars = ['Time_Action_md','Time_Agent_md','Time_Incentive_md','Time_Pivotal_md', 'Time_ST_Outcome_md', 'Time_Dummy_md','Time_EndOutcome_md']
Scalar = StandardScaler()
Newtime = pd.DataFrame(Scalar.fit_transform(results_cleaned[TimeVars]))
Newtime = Newtime.set_axis(TimeVars, axis=1)
results_standardized = results_cleaned.join(Newtime, rsuffix='_Z')

# Join Clusters to primary dataset
Clusters_DF = ALL_Participants_FI[['Participant', "Cluster"]]
Clustered_standardized = results_standardized.merge(Clusters_DF, left_on='Participant_ID', right_on='Participant', how='left')

# Create a dataset for all records for all people within each cluster
CLustered_data_1 = Clustered_standardized[Clustered_standardized["Cluster"]==0]
CLustered_data_2 = Clustered_standardized[Clustered_standardized["Cluster"]==1]
CLustered_data_3 = Clustered_standardized[Clustered_standardized["Cluster"]==2]
CLustered_data_4 = Clustered_standardized[Clustered_standardized["Cluster"]==3]
CLustered_data_5 = Clustered_standardized[Clustered_standardized["Cluster"]==4]

# Train M2 for each cluster
M2_cluster1 = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=CLustered_data_1).fit()
print("Cluster 1")
print(M2_cluster1.summary())

M2_cluster2 = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=CLustered_data_2).fit()
print("Cluster 2")
print(M2_cluster2.summary())

M2_cluster3 = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=CLustered_data_3).fit()
print("Cluster 3")
print(M2_cluster3.summary())

M2_cluster4 = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=CLustered_data_4).fit()
print("Cluster 4")
print(M2_cluster4.summary())

M2_cluster5 = sm.gls(formula="CausalScore ~ Is_Human + ST_Outcome + End_Outcome + TakesAction + MotivatedByEndOutcome + Is_Pivotal + DummyText + Context + InfoOrderGroup + Is_SouthAfrican + CorrectNumeracy + PostGraduateDegree", data=CLustered_data_5).fit()
print("Cluster 5")
print(M2_cluster5.summary())