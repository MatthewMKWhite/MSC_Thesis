function [round_start, round_end] = plotpoints(Agent,Action,Incentive,Pivotality,Outcome1,Dummy,Outcome2, Context, Round)
cla
hold on 
round_start = datestr(now);

 
IncentiveText = sprintf('Incentives are paid based\non %s',Incentive);
AgentText = sprintf('Agent is a %s',Agent);
ActionText = sprintf('%s', Action);
Outcome1Text = sprintf('%s', Outcome1);
PivotText = sprintf('%s', Pivotality);
TitleText = sprintf("Information Round: %i",Round);
text(-0.15,1.05,TitleText,'FontSize',17)

if (strcmpi(Context, "Football"))  
    Outcome2Text = sprintf("Agent's team %ss",Outcome2);
    position_outc2 = 0.45;
    posistion_pivotal = 0.80;
    if (strcmpi(Dummy, "A")) 
        DummyText = sprintf('Agent was playing on home ground');
    else
        DummyText = sprintf('Agent was playing on away ground');
    end
else
    Outcome2Text = sprintf("The company's environmental footprint %ss",Outcome2);
    position_outc2 = 0.35;
    posistion_pivotal = 0.85;
    if (strcmpi(Dummy, "A")) 
        DummyText = sprintf('Company works in insurance');
    else
        DummyText = sprintf('Company works in banking');
    end
end



text(0.1,0.9,AgentText,'FontSize',17)
text(0.7,0.9,ActionText,'FontSize',17)
text(-0.1,0.6,IncentiveText,'FontSize',17)
text(posistion_pivotal,0.6,PivotText,'FontSize',17)
text(0.1,0.3,Outcome1Text,'FontSize',17)
text(0.7,0.3,DummyText,'FontSize',17)
text(position_outc2,0.1,Outcome2Text,'FontSize',17)
text(-0.15,-0.05,"Press any key to continue",'FontSize',14,'Color','r') 

pause


round_end = datestr(now);