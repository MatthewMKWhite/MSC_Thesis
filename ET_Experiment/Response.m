function [Feedback_start_time, Feedback_end_time, Response_causal, Response_bonus] = Response(Outcome, Context, Round)
Feedback_start_time = datestr(now);

if (strcmpi(Context, "Football"))  
    OutcomeFormatted = sprintf("their team to %s", Outcome); 
else
    OutcomeFormatted = sprintf("the company's environmental footprint to %s", Outcome);
end

Causal_Text = sprintf('Based on the previous screen, to what extent do you feel the agent* caused %s?',OutcomeFormatted);
Bonus_text = sprintf("Assuming that the agent* is currently paid at a fair market rate, what bonus or malus (negative) would you recommend for this agent?\nRemember this independent of the agent’s personal incentives, and should be made using your own intuition.");
Caveat_text = sprintf("(In the case of a computerized agent, assume this refers to the developer of the agent.)");
TitleText = sprintf("Response Round: %i",Round);


cla
%% causal screen
text(-0.15,1.05,TitleText,'FontSize',17)
text(-0.1,0.95,Causal_Text,'FontSize',16)
hold on
text(-0.1,0.9,Caveat_text,'FontSize',13)
text(-0.05,0.8,"Where",'FontSize',16)
text(0.01,0.75,"1: Not at all",'FontSize',16)
text(0.01,0.65,"2: Very Slightly",'FontSize',16)
text(0.01,0.55,"3: Slightly",'FontSize',16)
text(0.01,0.45,"4: Neutral",'FontSize',16)
text(0.01,0.35,"5: Moderately",'FontSize',16)
text(0.01,0.25,"6: Very Much",'FontSize',16)
text(0.01,0.15,"7: Almost Entirely",'FontSize',16)
pause
Response_causal = get(gcf,'CurrentCharacter');

%input validity check
if str2double(Response_causal) >= 1 && str2double(Response_causal) <= 7
   causal_valid = 1;
else
   causal_valid = 0;
end
while causal_valid == 0
    cla
    text(-0.1,0.95,"Invalid response, please input a number between 1 and 7",'FontSize',17)
    pause
    Response_causal = get(gcf,'CurrentCharacter');
    if str2double(Response_causal) >= 1 && str2double(Response_causal) <= 7
        causal_valid = 1;
    else
        causal_valid = 0;
    end    
end
fixationcross(0.5)
%% bonus screen

cla 
text(-0.15,1.05,TitleText,'FontSize',17)
text(-0.1,0.95,Bonus_text,'FontSize',14)
text(-0.1,0.88,Caveat_text,'FontSize',13)
text(-0.05,0.8,"Where",'FontSize',16)
text(0.01,0.75,"1: -10%",'FontSize',16)
text(0.01,0.65,"2: -1%",'FontSize',16)
text(0.01,0.55,"3: 0%",'FontSize',16)
text(0.01,0.45,"4: 1%",'FontSize',16)
text(0.01,0.35,"5: 10%",'FontSize',16)

pause
Response_bonus = get(gcf,'CurrentCharacter');

%input validity check
if str2double(Response_bonus) >= 1 && str2double(Response_bonus) <= 5
   response_valid = 1;
else
   response_valid = 0;
end
while response_valid == 0
    cla
    text(-0.1,0.95,"Invalid response, please input a number between 1 and 5",'FontSize',17)
    pause
    Response_bonus = get(gcf,'CurrentCharacter');
    if str2double(Response_bonus) >= 1 && str2double(Response_bonus) <= 5
        response_valid = 1;
    else
        response_valid = 0;
    end    
end


Feedback_end_time = datestr(now);


end
