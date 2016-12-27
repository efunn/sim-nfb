###########
# analysis of controller parameters
###########
data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_001/timed_trial_sim_ai_001.txt')
data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_002/timed_trial_sim_ai_002.txt')

summary_data = aggregate(time_to_target~controller_type, data=data, FUN=mean)
arrange(summary_data,time_to_target)

summary_data_1 = aggregate(time_to_target~controller_type, data=data_1, FUN=mean)
summary_data_2 = aggregate(time_to_target~controller_type, data=data_2, FUN=mean)
summary_data_5 = aggregate(time_to_target~controller_type, data=data_5, FUN=mean)
summary_data_6 = aggregate(time_to_target~controller_type, data=data_6, FUN=mean)
summary_data_8 = aggregate(time_to_target~controller_type, data=data_8, FUN=mean)
library(plyr)
arrange(summary_data,time_to_target)
arrange(summary_data_1,time_to_target)
arrange(summary_data_2,time_to_target)
arrange(summary_data_5,time_to_target)
arrange(summary_data_6,time_to_target)
arrange(summary_data_8,time_to_target)
arrange(summary_data_9,time_to_target)

summary(subset(data_5,controller_type==497))
summary(subset(data_7,controller_type==16))

data_10 = read.csv('sim_ai_demo_10/timed_trial_sim_ai_demo_10.txt')
summary_data_10 = aggregate(time_to_target~controller_type, data=data_10, FUN=mean)
arrange(summary_data_10,time_to_target)
