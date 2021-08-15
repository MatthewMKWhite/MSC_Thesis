function [Configuration_starts, Configuration_ends] = Configuration()
cla
text(-0.1,0.95,"Eye-tracker to matlab configuration",'FontSize',17)


cla
hold on 
Configuration_starts = datestr(now);
ConfigurationText = "X";

text(0.2,0.9,ConfigurationText,'FontSize',16)
pause(3)
cla 
text(0.8,0.9,ConfigurationText,'FontSize',16)
pause(3)
cla 
text(0.0,0.6,ConfigurationText,'FontSize',16)
pause(3)
cla 
text(0.9,0.6,ConfigurationText,'FontSize',16)
pause(3)
cla 
text(0.2,0.3,ConfigurationText,'FontSize',16)
pause(3)
cla 
text(0.8,0.3,ConfigurationText,'FontSize',16)
pause(3)
cla 
text(0.45,0.1,ConfigurationText,'FontSize',16)
pause(3)

Configuration_ends = datestr(now);