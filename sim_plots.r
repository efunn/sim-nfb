

#########################################
#########################################
#########################################
#########################################

# PLOTS TO DO:

# scatter plot of time_to_target ~ dist_to_target | hrf
# bar graph of time to target ~ tr | snr

library(ggplot2)
source('/Users/efun/Dropbox/stats/sim-nfb/summaryse.r')
data_se_vis_dof = summarySE(data, measurevar='time_sec', groupvars=c('dof','visible'))
data_se_vis_hrf = summarySE(data, measurevar='time_sec', groupvars=c('hrf','visible'))
data_se_dof_hrf = summarySE(data_invis, measurevar='time_sec', groupvars=c('dof','hrf'))

library(car)
scatterplot(time_to_target~dist_to_target | hrf, data=delay_invis_data,
    xlab='distance to target', ylab='time to target')

scatterplot(time_to_target~ dist_to_target | visible, data=delay_vis_data,
    xlab='distance to target', ylab='time to target')

scatterplot(time_to_target~ tr | snr, data=snr_tr_data,
    xlab='tr', ylab='time to target')

scatterplot(time_to_target~ dist_to_target | snr, data=snr_tr_data,
    xlab='distance to target', ylab='time to target')

scatterplot(time_to_target~ dist_to_target | tr, data=snr_tr_data,
    xlab='distance to target', ylab='time to target')

scatterplot(time_to_target~ dist_to_target | tr, data=snr_data,
    xlab='distance to target', ylab='time to target')


library(car)

compare_data = subset(data,snr==.01&tr==1&hrf=='hrf'&visible=='False')

scatterplot(time_to_target~ dist_to_target | type, data=compare_data,
    xlab='distance to target', ylab='time to target')

scatterplot(time_to_target~ dist_to_target | tr, data=snr_tr_data,
    xlab='distance to target', ylab='time to target')

library(ggplot2)
source('/Users/efun/Dropbox/stats/sim-nfb/summaryse.r')
data_se_compare = summarySE(compare_data, measurevar='time_to_target', groupvars=c('type','dist_to_target_deg'))
ggplot(data_se_compare, aes(x=dist_to_target_deg, y=time_to_target, fill=type)) + 
    geom_bar(position=position_dodge(), stat='identity') +
    geom_errorbar(aes(ymin=time_to_target-se, ymax=time_to_target+se),
                  width=10,                    # Width of the error bars
                  position=position_dodge(20))

########

library('plotrix')
data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20151213-pilot-001/timed_frame_20151213-pilot-001.txt')
data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/ai_demo_2/timed_frame_ai_demo_2.txt')
data$cursor_pos_radians = (data$cursor_pos-data$target_pos)*pi/90
rad_data = subset(data,visible=='False'&hrf=='hrf'&tr==1&snr==.025)
# rad_data = subset(data,visible=='False')
trial_1 = subset(rad_data,trial_number==0)
trial_2 = subset(rad_data,trial_number==1)
trial_3 = subset(rad_data,trial_number==2)
trial_4 = subset(rad_data,trial_number==3)
trial_5 = subset(rad_data,trial_number==4)
trial_6 = subset(rad_data,trial_number==5)
trial_7 = subset(rad_data,trial_number==6)
trial_8 = subset(rad_data,trial_number==7)
trial_9 = subset(rad_data,trial_number==8)
radial.plot(data$trial_time,data$cursor_pos_radians,rp.type='l')

# auto plot colors and average over TRs
radial.plot(trial_2$trial_time,trial_2$cursor_pos_radians,rp.type='l',line.col='blue',lwd=2)
radial.plot(trial_1$trial_time,trial_1$cursor_pos_radians,rp.type='l',line.col='red',lwd=2,add=TRUE)
radial.plot(trial_3$trial_time,trial_3$cursor_pos_radians,rp.type='l',line.col='green',lwd=2,add=TRUE)
radial.plot(trial_4$trial_time,trial_4$cursor_pos_radians,rp.type='l',line.col='yellow',lwd=2,add=TRUE)
radial.plot(trial_5$trial_time,trial_5$cursor_pos_radians,rp.type='l',line.col='purple',lwd=2,add=TRUE)
radial.plot(trial_6$trial_time,trial_6$cursor_pos_radians,rp.type='l',line.col='pink',lwd=2,add=TRUE)
radial.plot(trial_7$trial_time,trial_7$cursor_pos_radians,rp.type='l',line.col='orange',lwd=2,add=TRUE)
radial.plot(trial_8$trial_time,trial_8$cursor_pos_radians,rp.type='l',line.col='black',lwd=2,add=TRUE)
radial.plot(trial_9$trial_time,trial_9$cursor_pos_radians,rp.type='l',line.col='brown',lwd=2,add=TRUE)

#################
#################
#################



