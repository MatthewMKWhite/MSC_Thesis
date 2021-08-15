function [ExFt_start, ExFt_end] =  ExampleFootball()
cla
hold on 
ExFt_start = datestr(now);

IncentiveText = sprintf('Incentives are paid based\non the number of goals scored');
AgentText = sprintf('Agent is a Professional football player');
ActionText = sprintf('Agent shoots to score');
Outcome1Text = sprintf("A goal is not scored for the Agent's team");
Outcome2Text = sprintf("Agent's team wins");
DummyText = sprintf('Agent was playing on home ground');
PivotText = sprintf('The winning team won by 3 goals');
ExplainText = sprintf('From the above, you should see that the human agent, who receives bonuses based on how many goals they score, was playing at home ground, tried to shoot for goal and missed, but the team still won the match by 3 points.');
ReminderText = sprintf('Remember: you would then be asked to answer to what extent you feel the agent caused the team to win/lose.');

TitleText = sprintf("Example Round: Football");
text(-0.15,1.05,TitleText,'FontSize',17)

text(0.1,0.9,AgentText,'FontSize',17)
text(0.7,0.9,ActionText,'FontSize',17)
text(-0.1,0.6,IncentiveText,'FontSize',17)
text(0.80,0.6,PivotText,'FontSize',17)
text(0.1,0.3,Outcome1Text,'FontSize',17)
text(0.7,0.3,DummyText,'FontSize',17)
text(0.45,0.1,Outcome2Text,'FontSize',17)
text(-0.15,0.0,ExplainText,'FontSize',14,'Color','r') 
text(-0.15,-0.05,ReminderText,'FontSize',14,'Color','r') 

pause


ExFt_end = datestr(now);