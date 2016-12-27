#############
# data preprocessing
#############


data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20151213-pilot-001/timed_trial_20151213-pilot-001.txt')
data = read.csv('/home/efun/Dropbox/sim-nfb/datasets/20160115-pilot-001/timed_trial_20160115-pilot-001.txt')

data1 = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20160115-pilot-001/timed_trial_20160115-pilot-001.txt')
data2 = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20160121-pilot-001/timed_trial_20160121-pilot-001.txt')
data3 = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20160121-pilot-002/timed_trial_20160121-pilot-002.txt')
data4 = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20160121-pilot-003/timed_trial_20160121-pilot-003.txt')
data = rbind(data1,data2,data3,data4)

data$snr_factor = as.factor(data$snr)
data$dist_to_target = abs(abs(data$target_pos)-90)/90
data$dist_to_target_2 = data$dist_to_target*data$dist_to_target
data$dist_to_target_3 = data$dist_to_target_2*data$dist_to_target
data$tr_base = data$tr-1
data$tr_factor = as.factor(data$tr)
data = within(data, hrf <- relevel(hrf, ref = 'impulse'))
data = within(data, visible <- relevel(visible, ref = 'True'))
delay_vis_data = subset(data,snr==.025&tr==1)
snr_tr_data = subset(data,visible=='False'&hrf=='hrf')
delay_data = subset(data,snr==.025&tr==1&visible=='False')
reduced_target_data = subset(snr_tr_data,dist_to_target==.25|dist_to_target==.5|dist_to_target==.75)

###########
# statistical model analysis
###########

vis_hrf_model = lm(time_to_target~(hrf+visible+dist_to_target)+hrf:visible,data=delay_vis_data)
summary(vis_hrf_model)
vis_hrf_model_2 = lm(time_to_target~(hrf+visible+dist_to_target+dist_to_target:hrf),data=delay_vis_data)
summary(vis_hrf_model_2)

snr_tr_model = lm(time_to_target~snr_factor,data=snr_tr_data)
snr_tr_model = lm(time_to_target~(tr_base+snr_factor+dist_to_target+dist_to_target_2)+tr_base:snr_factor,data=snr_tr_data)
summary(snr_tr_model)

snr_tr_model_reg = lm(time_to_target~(dist_to_target+dist_to_target_2),data=snr_tr_data)
snr_tr_data_reg = snr_tr_data
snr_tr_data_reg$time_to_target = snr_tr_data$time_to_target-predict(snr_tr_model_reg)
new_test_model = lm(time_to_target~(tr_base+snr_factor)+tr_base:snr_factor,data=snr_tr_data_reg)

#####################

data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20151220-pilot-002/timed_frame_20151220-pilot-002.txt')
data_human = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20151220-pilot-002/timed_trial_20151220-pilot-002.txt')
data_ai = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/ai_demo_2/timed_trial_ai_demo_2.txt')
data = rbind(data_human,data_ai)
data$snr_factor = as.factor(data$snr)
data$dist_to_target = abs(abs(data$target_pos)-90)/90
data$dist_to_target_deg = data$dist_to_target*90
data = subset(data,dist_to_target!=0)
data$dist_to_target_2 = data$dist_to_target*data$dist_to_target
data$dist_to_target_3 = data$dist_to_target_2*data$dist_to_target
data$tr_base = data$tr-1
data$tr_factor = as.factor(data$tr)
data = within(data, hrf <- relevel(hrf, ref = 'impulse'))
data = within(data, visible <- relevel(visible, ref = 'True'))
delay_vis_data = subset(data,snr==.01&tr==1)
delay_invis_data = subset(delay_vis_data,visible=='False')
snr_tr_data = subset(data,visible=='False'&hrf=='hrf')
delay_data = subset(data,snr==.01&tr==1&visible=='False')

vis_hrf_model = lm(time_to_target~(hrf+visible+dist_to_target)+hrf:visible,data=delay_vis_data)
summary(vis_hrf_model)
vis_hrf_model_2 = lm(time_to_target~(hrf+visible+dist_to_target+dist_to_target:hrf),data=delay_vis_data)
summary(vis_hrf_model_2)

snr_tr_model = lm(time_to_target~snr_factor,data=snr_tr_data)
snr_tr_model = lm(time_to_target~(tr_base+snr_factor+dist_to_target+dist_to_target_2)+tr_base:snr_factor+snr_factor:dist_to_target,data=snr_tr_data)
summary(snr_tr_model)

######################
######################
######################
######################

data_ai = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_002/timed_trial_sim_ai_002.txt')
data_human = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/20160115-pilot-001/timed_trial_20160115-pilot-001.txt')
data_ai_delay_vis = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_001/timed_trial_sim_ai_001.txt')

se = function(x) sqrt(var(x)/length(x))
# plot 1 means:
# no delay, visible
data_human = data
data_human_delay_vis = subset(data_human,tr==1&snr==.01)
data_human_snr_tr = subset(data_human,hrf=='hrf'&visible=='False')

data = subset(data_human_delay_vis,hrf=='impulse'&visible=='True')
mean(data$time_to_target)
se(data$time_to_target)
11.15
0.24
# no delay, invisible 
data = subset(data_human_delay_vis,hrf=='impulse'&visible=='False')
mean(data$time_to_target)
se(data$time_to_target)
14.31
0.35
# delay, visible
data = subset(data_human_delay_vis,hrf=='hrf'&visible=='True')
mean(data$time_to_target)
se(data$time_to_target)
15.97
0.17
# delay, invisible
data = subset(data_human_delay_vis,hrf=='hrf'&visible=='False')
mean(data$time_to_target)
se(data$time_to_target)
35.86
2.11
# ai, snr==.01
mean(data_ai_delay_vis$time_to_target)
se(data_ai_delay_vis$time_to_target)
21.75
0.33

# nodelayvis,nodelayinvis,delayvis,delayinvis,ai
10.72,14.65,15.58,28.72,21.75
0.95,4.72,0.79,12.41,4.74


# delay, invisible
# data = data_ai_delay_vis
data = subset(data_human_delay_vis,hrf=='hrf'&visible=='False')
data$dist_to_target = abs(abs(data$target_pos)-90)/90
data = subset(data,dist_to_target==1)
mean(data$time_to_target)
se(data$time_to_target)

# 22.5, 45, 67.5, 90
# human
40.01, 34.6, 35.19, 31.38
4.39, 3.54, 4.64, 2.62

# 23.51,25.63,31.63,39.51
# 3.16,1.98,6.05,6.49
# AI
26.63,21,19,19
0.48,0.65,0.26,0


# SNR/TR
# data = read.csv('/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_001/timed_trial_sim_ai_001.txt')
data = subset(data_human_snr_tr,tr==1&snr==.15)
mean(data$time_to_target)
se(data$time_to_target)


# noise = 0.01
# ai, human1, human6
21.75,35.86,46.61
0.33,2.11,2.55
# 21.75,28.72,49.08
# 0.33,2.34,5.45

# noise = 0.15
# ai, human1, human6
25.90,33.83,44.04
0.84,1.83,2.46

ai_snr_mean = [21.75,25.9]
ai_snr_sd = [4.74,12.29]
human_snr_1_mean = [28.72,36.29]
human_snr_1_sd = [12.41,20.28]
human_snr_6_mean = [49.08,47.58]
human_snr_6_sd = [28.85,29.84]

