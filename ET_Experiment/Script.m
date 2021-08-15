%% Initialise Variables
clear
Participantnum = 57; %change for each participant
Num_rounds = 32;
ResponseStruct(Num_rounds) = struct('ParticipantNum',[],'TrialNumber', [],'StartTime',[],...,
    'EndTime',[],'Causal_Response',[],'Bonus_Response',[], 'Agent',[],...,
    'Action',[],'Outcome1',[],'Outcome2',[],'Pivotality',[],'Incentive',[],...,
    'Dummy',[],'ResponseStart',[],'ResponseEnd',[],'Context',[]) ;
PersonalInfo(1) = struct('ParticipantNum',[],'Age',[],'Nationality',[],'Numeracy',[],'Email',[],'Employment',[],'Education',[],'KeepPosted',[],'ConfStart',[],'ConfEnd',[]);
Vignettes = table2struct(readtable('C:\Users\Matt\PycharmProjects\MSCThesis\OT_Proj\Vignettes.csv','PreserveVariableNames',true));
MyParticipant = [Vignettes(:).Subject]==Participantnum; 
Agent = {Vignettes(:).Agent};
Outcome1 = {Vignettes(:).Outcome1};
Outcome2 = {Vignettes(:).Outcome2};
Action = {Vignettes(:).Action};
Incentive = {Vignettes(:).Incentive};
Pivotality = {Vignettes(:).Pivotality};
Context = {Vignettes(:).Context};

OutputfileXLSX = append('Results_',string(Participantnum),'.xlsx');
PersonalInfoXLSX = append('Personal_',string(Participantnum),'.xlsx');

MP = get(0,'MonitorPositions');
%if there is 1 screen, make fullscreen, otherwise set it manually to fullscreen on screen 2
if size(MP,1)==1
    s = get(0, 'ScreenSize');
    figure('Position', [0 0 s(3) s(4)]);
else
    figure('Position', [1921 -7 1300 655.3333]); %hardcoded to my monitor. this obtained using "get(gcf)" 
end

% Hide axes
set(gca,'visible','off');
set(gcf,'Color','w');

%% Instructions + Pause to begin
    cla
    text(-0.1,0.95,"Welcome to this online experiment. Please refer to the instructions provided in the PDF document",'FontSize',16)
    text(-0.1,0.85,"On the following screens, several Xs will appear. Please simply look at each X while it is displayed",'FontSize',16)
    text(-0.1,0.75,"Please wait for the experimenter's instruction to begin",'FontSize',16)
    pause
    
    
%% (Matlab) Configure axis
    [Configuration_starts, Configuration_ends] = Configuration();

    %% Example Trials     
    cla
    text(-0.1,0.85,"Next you will be provided with an example of each context, to familiarize yourself with how to interpret the information",'FontSize',16)
    text(-0.1,0.75,"Press any key to begin.",'FontSize',16)
    pause
    [ExFt_start, ExFt_end] = ExampleFootball();
    [ExBS_start, ExBS_end] = ExampleBusiness();


%% Instructions + Pause to begin (2)
    cla
    text(-0.1,0.95,"Thank you for completing the examples. When you are ready to begin the experiment, please press any key",'FontSize',16)
    pause
%% Trials 
for trial=1:Num_rounds
    %% Fixation Cross
    fixationcross(1.5)
    %% Trial 
    MyRow = [Vignettes(:).RoundNum]==trial; 
    
    ThisAgent = string(Agent(MyRow & MyParticipant));
    ThisOutcome1  = string(Outcome1(MyRow & MyParticipant));
    ThisOutcome2  = string(Outcome2(MyRow & MyParticipant));
    ThisAction  = string(Action(MyRow & MyParticipant));
    ThisIncentive  = string(Incentive(MyRow & MyParticipant));
    ThisContext  = string(Context(MyRow & MyParticipant));
    ThisPivotal  = string(Pivotality(MyRow & MyParticipant));
    ThisDummy = pickone(["A","B"]);
        
    [round_start, round_end] = plotpoints(ThisAgent,ThisAction,ThisIncentive,ThisPivotal,ThisOutcome1,ThisDummy,ThisOutcome2, ThisContext, trial);
    
    %% Response (includes both response pages)
    fixationcross(0.5)
    [Feedback_start_time, Feedback_end_time, Response_causal, Response_bonus] = Response(ThisOutcome2, ThisContext, trial);
    
    
    %% Save results to a struct
    ResponseStruct(trial).ParticipantNum = string(Participantnum);
    ResponseStruct(trial).TrialNumber = trial;
    ResponseStruct(trial).ResponseStart = Feedback_start_time;
    ResponseStruct(trial).ResponseEnd = Feedback_end_time;
    ResponseStruct(trial).StartTime = round_start;
    ResponseStruct(trial).EndTime = round_end;
    ResponseStruct(trial).Causal_Response = Response_causal;
    ResponseStruct(trial).Bonus_Response = Response_bonus;
    ResponseStruct(trial).Agent = ThisAgent;
    ResponseStruct(trial).Action = ThisAction;
    ResponseStruct(trial).Outcome1 = ThisOutcome1;
    ResponseStruct(trial).Outcome2 = ThisOutcome2;
    ResponseStruct(trial).Incentive = ThisIncentive;
    ResponseStruct(trial).Pivotality = ThisPivotal;
    ResponseStruct(trial).Dummy = ThisDummy;
    ResponseStruct(trial).Context = ThisContext;
   

end
%% Inform user that they're nearly done
cla
    text(-0.1,0.95,"Thank you! You have now completed the experiment.",'FontSize',16)
    text(-0.1,0.85,"The experimenter will now give you a numeracy question, please answer this to the best of your ability.",'FontSize',16)
    text(-0.1,0.75,"Following this, you will be asked to capture your personal information.",'FontSize',16)
    text(-0.1,0.65,"The experimenter will now stop the eye-recording, thank you for your participation.",'FontSize',16)
    pause

close all


%% Numeracy Test 
Numeracy_ans = inputdlg("Out of 1000 people in a small town 500 are members of a choir. Out of these 500 members in the choir, 100 are men. Out of the 500 inhabitants that are not in the choir, 300 are men. What is the percentage-probability that a randomly drawn man is a member of the choir?","Numeracy Test");
%% Post-Experiment survey
prompt = {'Age','Nationality','Highest Education','Employment Status','Email'};
dlgtitle = 'Post Experiment Questions';
dims = [1 50];
definput = {'100','','example: Masters','example: Full time Student','xyz@gmail.com'};
answers = inputdlg(prompt,dlgtitle,dims,definput);

Keep_Posted = inputdlg('Would you like to receive a copy of the results when they become available? (Y/N)','Keep posted',dims);
PersonalInfo(1).ParticipantNum = string(Participantnum);
PersonalInfo(1).Age = string(answers(1));
PersonalInfo(1).Nationality = answers(2);
PersonalInfo(1).Education = string(answers(3));
PersonalInfo(1).Employment = string(answers(4));
PersonalInfo(1).Email = string(answers(5));
PersonalInfo(1).KeepPosted = string(Keep_Posted);
PersonalInfo(1).Numeracy = string(Numeracy_ans);
PersonalInfo(1).ConfStart = Configuration_starts;
PersonalInfo(1).ConfEnd = Configuration_ends;

%% Save the results
writetable(struct2table(ResponseStruct), OutputfileXLSX);
writetable(struct2table(PersonalInfo), PersonalInfoXLSX);

