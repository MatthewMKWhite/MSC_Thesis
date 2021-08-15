function [ExBS_start, ExBS_end] = ExampleBusiness()
cla
hold on 
ExBS_start = datestr(now);

IncentiveText = sprintf('Incentives are paid based\non the company profits');
AgentText = sprintf('Agent is a senior business executive');
ActionText = sprintf('Agent votes to adopt new strategy');
Outcome1Text = sprintf("Company profits increase");
Outcome2Text = sprintf("The company's environmental footprint worsens");
DummyText = sprintf('Company works in insurance');
PivotText = sprintf('Motion passes by 1 vote');
ExplainText = sprintf('From the above, you should see that the human agent, who receives bonuses based on company profits, voted to adopt a new strategy at his insurance firm. This decision passed by exactly one vote.\nIn the months that followed, the company saw an increase in profits, and a worsening of their environmental footprint.');
ReminderText = sprintf('Remember: you would then be asked to answer to what extent you feel the agent caused the change in environmental footprint.');

TitleText = sprintf("Example Round: Business");
text(-0.15,1.05,TitleText,'FontSize',17)

text(0.1,0.9,AgentText,'FontSize',17)
text(0.7,0.9,ActionText,'FontSize',17)
text(-0.1,0.6,IncentiveText,'FontSize',17)
text(0.80,0.6,PivotText,'FontSize',17)
text(0.1,0.3,Outcome1Text,'FontSize',17)
text(0.7,0.3,DummyText,'FontSize',17)
text(0.35,0.1,Outcome2Text,'FontSize',17)
text(-0.15,0.0,ExplainText,'FontSize',14,'Color','r')
text(-0.15,-0.05,ReminderText,'FontSize',14,'Color','r') 

pause


ExBS_end = datestr(now);