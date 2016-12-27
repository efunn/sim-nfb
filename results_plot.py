import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from math import ceil
from scipy import nanmean
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Helvetica'

################
# Colors/codes #
################

# AI: orange
# human: blue
# target visible: grey out
# no hrf: dashed line

# match y-axis for all time-to-target (based on overall max)
# match y-axis for all strategies (360 degrees ish?)

##################################################
# Effect of hidden target & hemodynamic response #
##################################################

# (1)
# bar graph of human time-to-target
# factors: delay, visibility

# (2)
# bar graph of human vs. AI time-to-target (low noise)
# factors: human/ai (show main effect)

# (3)
# bar graph of human vs. AI time-to-target (low noise)
# factors: distance to target, human/ai

def plot_delay_bars(mode='plot'):
    ai_color = (.9,.5,0)
    human_color = (0,.5,.9)
    human_color_lighter = (0.5,0.7,.9)
    human_color_grey = (.5,.5,.5)
    human_color_grey_lighter = (.75,.75,.75)
    start_pos = 0.
    width = 1
    gap = .25

    human_visible_mean = [11.15,15.97]
    human_visible_sd = [0.24,0.17]
    human_visible_color = human_color_lighter

    ai_invisible_mean = [21.75]
    ai_invisible_sd = [0.33]

    human_invisible_mean = [14.31,35.86]
    human_invisible_sd = [0.35,2.11]
    human_invisible_color = human_color_grey

    human_angle_mean = [40.01,34.6,35.19,31.38]
    human_angle_sd = [4.39,3.54,4.64,2.62]

    ai_angle_mean = [26.63,21,19,19]
    ai_angle_sd = [0.48,0.65,0.26,0.21]

    human_visible_pos = start_pos + np.array([0,2+gap])
    human_invisible_pos = human_visible_pos + 1
    ai_angle_pos = start_pos + 4*gap + np.array([4,6+gap,8+2*gap,10+3*gap])
    human_angle_pos = ai_angle_pos + 1

    fig, ax = plt.subplots()

    rects1 = ax.bar(human_invisible_pos, human_invisible_mean, width, color=[human_color_grey,human_color], linewidth=1)
    errbars1 = ax.errorbar(human_invisible_pos+.5*width, human_invisible_mean, yerr=human_invisible_sd,
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=4,capthick=1)

    rects2 = ax.bar(human_visible_pos, human_visible_mean, width, color=[human_color_grey_lighter, human_visible_color], linewidth=1)
    errbars2 = ax.errorbar(human_visible_pos+.5*width, human_visible_mean, yerr=human_visible_sd,
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=4,capthick=1)

    # rects3 = ax.bar(ai_visible_pos, ai_invisible_mean, width, color=ai_color, linewidth=1)
    # errbars3 = ax.errorbar(ai_visible_pos+.5*width, ai_invisible_mean, yerr=ai_invisible_sd,
    #                        fmt=None, ecolor=(0,0,0), elinewidth=1,
    #                        capsize=4,capthick=1)

    rects3 = ax.bar(ai_angle_pos, ai_angle_mean, width, color=ai_color, linewidth=1)
    errbars3 = ax.errorbar(ai_angle_pos+.5*width, ai_angle_mean, yerr=ai_angle_sd,
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=4,capthick=1)

    rects4 = ax.bar(human_angle_pos, human_angle_mean, width, color=human_color, linewidth=1)
    errbars4 = ax.errorbar(human_angle_pos+.5*width, human_angle_mean, yerr=human_angle_sd,
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=4,capthick=1)

    ax.set_ylabel('Time to target (s)',fontsize=18)
    ax.set_yticks([0,10,20,30,40,50,60])
    ax.set_yticklabels([0,10,20,30,40,50,60],fontsize=18)
    ax.set_xticks([])
    # ax.set_xticks([1.5+start_pos,4.5+gap+start_pos])
    # ax.set_xticklabels(('Noise s.d. = 0.01', 'Noise s.d. = 0.15'),fontsize=18)
    ax.tick_params('y', length=7, width=2)
    ax.tick_params('x', length=0, width=0)
    ax.set_xlim(-.75,14.5)
    ax.set_ylim(0,65)
    legend = ax.legend((rects2[0], rects1[0], rects2[1], rects1[1], rects3[0]), ('Target visible, no delay',
                                                           'Target invisible, no delay',
                                                           'Target visible, delayed',
                                                           'Target invisible, delayed', 'AI'),
                        fontsize=18, loc=2)
    legend.get_frame().set_linewidth(2)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)

    fig.set_size_inches(6,8,forward=True)

    if mode == 'plot':
        plt.show()
    else:
        plt.savefig('test.pdf', dpi=300, transparent=True)

# (4)
# plot human strategies vs. time
# factors: delay, visibility
# average over 1s intervals
def preproc_delay_lines(filename='filename.csv',hrf='hrf',visible=False):
    data = pd.read_csv(filename)
    subset_data = data[(data.snr==.01)&(data.tr==1)]
    subset_data = subset_data[(data.hrf==hrf)&(data.visible==visible)]
    subset_data.cursor_pos = subset_data.cursor_pos-subset_data.target_pos
    out_dataset = []
    target_pos_list = subset_data.target_pos.unique()
    for trial_number in sorted(subset_data.trial_number.unique()):
        trial_data = subset_data[subset_data.trial_number==trial_number]
        target_pos = np.mean(trial_data.target_pos)
        if any(np.in1d(target_pos_list,target_pos)):
            trial_pos_data = np.array(trial_data.cursor_pos)
            FRAME_RATE = 60
            pad_size = ceil(float(trial_pos_data.size)/FRAME_RATE)*FRAME_RATE - trial_pos_data.size
            trial_pos_data = np.append(trial_pos_data, np.zeros(pad_size)*np.NaN)
            trial_pos_data_subsample = nanmean(trial_pos_data.reshape(-1,FRAME_RATE), axis=1)
            if trial_pos_data_subsample[-1] > 90:
                trial_pos_data_subsample -= 180
            elif trial_pos_data_subsample[-1] < -90:
                trial_pos_data_subsample += 180
            out_dataset.append(trial_pos_data_subsample)
            target_pos_list=np.delete(target_pos_list,np.where(target_pos_list==target_pos)) 
        else:
            pass
    return out_dataset

def plot_delay_lines(mode='plot'):
    ai_color = (.9,.5,0)
    human_color = (0,.5,.9)
    human_color_lighter = (0.5,0.7,.9)
    human_color_grey = (.5,.5,.5)
    human_color_grey_lighter = (.75,.75,.75)
    human_filename = '/Users/efun/Dropbox/sim-nfb/datasets/20160115-pilot-001/timed_frame_20160115-pilot-001.txt'

    # ai_filename_high_snr = '/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_005/timed_frame_sim_ai_005.txt'
    # ai_filename_low_snr = '/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_006/timed_frame_sim_ai_006.txt'
    out_data_1 = preproc_delay_lines(filename=human_filename,hrf='impulse',visible=True)
    out_data_2 = preproc_delay_lines(filename=human_filename,hrf='impulse',visible=False)
    out_data_3 = preproc_delay_lines(filename=human_filename,hrf='hrf',visible=True)
    out_data_4 = preproc_delay_lines(filename=human_filename,hrf='hrf',visible=False)
    plot_single_lines(out_data_1, color=human_color_grey_lighter, outname='human_vis_nodelay.pdf', mode='save')
    plot_single_lines(out_data_2, color=human_color_grey, outname='human_novis_nodelay.pdf', mode='save')
    plot_single_lines(out_data_3, color=human_color_lighter, outname='human_vis_delay.pdf', mode='save')
    plot_single_lines(out_data_4, color=human_color, outname='human_novis_delay.pdf', mode='save')

# Layout:
# (1) (2) (3)
# (    4    )


########################
# Effect of TR and SNR #
########################

# low noise: saturated
# noise high: unsaturated
# 1s TR: thin line
# 6s TR: thick line

# (1)
# bar graph of time-to-target
# factors: human/ai, TR, SNR

def plot_snr_bars(mode='plot'):
    ai_color_1 = (.9,.5,0)
    ai_color_2 = (.9,.5,0)
    human_color_1 = (0,.5,.9)
    human_color_2 = (0.5,0.7,.9)
    human_color_3 = (0,.5,.9)
    human_color_4 = (0.5,0.7,.9)
    start_pos = 0.
    width = 1
    gap = .25
    ai_mean = [21.75,25.9]
    ai_sd = [0.33,0.84]
    human_1_mean = [35.86,46.61]
    human_1_sd = [2.11,2.55]
    human_2_mean = [33.83,44.04]
    human_2_sd = [1.83,2.46]

    fig, ax = plt.subplots()
    rects1 = ax.bar(start_pos, ai_mean[0], width, color=ai_color_1, linewidth=1)
    errbars1 = ax.errorbar(start_pos+.5*width, ai_mean[0], yerr=ai_sd[0],
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=7,capthick=1)

    rects2 = ax.bar(1+start_pos, human_1_mean[0], width, color=human_color_1, linewidth=1)
    errbars2 = ax.errorbar(start_pos+1.5*width, human_1_mean[0], yerr=human_1_sd[0],
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=7,capthick=1)

    rects3 = ax.bar(2+start_pos, human_1_mean[1], width, color=human_color_2, linewidth=1)
    errbars3 = ax.errorbar(start_pos+2.5*width, human_1_mean[1], yerr=human_1_sd[1],
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=7,capthick=1)

    rects4 = ax.bar(3+gap+start_pos, ai_mean[1], width, color=ai_color_2, linewidth=1)
    errbars4 = ax.errorbarects4 = ax.bar(3+gap+start_pos, ai_mean[1], width, color=ai_color_2, linewidth=1)
    errbars4 = ax.errorbar(gap+start_pos+3.5*width, ai_mean[1], yerr=ai_sd[1],
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=7,capthick=1)

    rects5 = ax.bar(4+gap+start_pos, human_2_mean[0], width, color=human_color_3, linewidth=1)
    errbars5 = ax.errorbar(gap+start_pos+4.5*width, human_2_mean[0], yerr=human_2_sd[0],
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=7,capthick=1)

    rects6 = ax.bar(5+gap+start_pos, human_2_mean[1], width, color=human_color_4, linewidth=1)
    errbars6 = ax.errorbar(gap+start_pos+5.5*width, human_2_mean[1], yerr=human_2_sd[1],
                           fmt=None, ecolor=(0,0,0), elinewidth=1,
                           capsize=7,capthick=1)


    ax.set_ylabel('Time to target (s)',fontsize=18)
    ax.set_yticks([0,20,40,60,80])
    ax.set_yticklabels([0,20,40,60,80],fontsize=18)
    ax.set_xticks([1.5+start_pos,4.5+gap+start_pos])
    # ax.set_xticklabels(('Noise s.d. = 0.01', 'Noise s.d. = 0.15'),fontsize=18)
    ax.tick_params('y', length=7, width=2)
    ax.tick_params('x', length=0, width=0)
    ax.set_xlim(-.5,6.75)
    ax.set_ylim(0,70)
    legend = ax.legend((rects1[0], rects2[0], rects3[0]), ('AI', 'Human, TR=1', 'Human, TR=6'),
                        fontsize=18, loc=2)
    legend.get_frame().set_linewidth(2)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)

    fig.set_size_inches(4,8,forward=True)

    if mode == 'plot':
        plt.show()
    else:
        plt.savefig('test.pdf', dpi=300, transparent=True)

# (2/3)
# plot of human and ai strategies vs. time

def preproc_snr_lines(filename='filename.csv',snr=.01,tr=1,controller='human'):
    data = pd.read_csv(filename)
    if controller == 'human':
        subset_data = data[(data.visible==False)&(data.hrf=='hrf')]
    else:
        subset_data = data
    subset_data = subset_data[(data.snr==snr)&(data.tr==tr)]
    subset_data.cursor_pos = subset_data.cursor_pos-subset_data.target_pos
    out_dataset = []
    target_pos_list = subset_data.target_pos.unique()
    for trial_number in sorted(subset_data.trial_number.unique()):
        trial_data = subset_data[subset_data.trial_number==trial_number]
        target_pos = np.mean(trial_data.target_pos)
        if any(np.in1d(target_pos_list,target_pos)):
            trial_pos_data = np.array(trial_data.cursor_pos)
            FRAME_RATE = 60
            pad_size = ceil(float(trial_pos_data.size)/FRAME_RATE)*FRAME_RATE - trial_pos_data.size
            trial_pos_data = np.append(trial_pos_data, np.zeros(pad_size)*np.NaN)
            trial_pos_data_subsample = nanmean(trial_pos_data.reshape(-1,FRAME_RATE), axis=1)
            if trial_pos_data_subsample[-1] > 90:
                trial_pos_data_subsample -= 180
            elif trial_pos_data_subsample[-1] < -90:
                trial_pos_data_subsample += 180
            out_dataset.append(trial_pos_data_subsample)
            target_pos_list=np.delete(target_pos_list,np.where(target_pos_list==target_pos)) 
        else:
            pass
    return out_dataset


def plot_single_lines(data, color, outname='test.pdf', mode='plot'):
    fig, ax = plt.subplots()
    for i in range(len(data)):
        plt.plot(data[i],color=color,linewidth=1,zorder=1)
    for i in range(len(data)):
        plt.scatter(len(data[i])-1,data[i][-1],s=40,c=color,zorder=2)

    ax.set_xlabel('Time to target (s)',fontsize=18)
    ax.set_xticks([0,20,40,60,80,100])
    ax.set_xticklabels([0,20,40,60,80,100],fontsize=18)
    ax.set_yticks([90,0,-90])
    ax.set_yticklabels(('+90','Target','-90'),fontsize=18)
    ax.tick_params('x', length=7, width=2)
    ax.tick_params('y', length=7, width=2)
    ax.set_xlim(-10,165)
    ax.set_ylim(-200,200)
    # legend = ax.legend((rects1[0], rects2[0], rects3[0]), ('AI', 'Human, TR=1', 'Human, TR=6'),
    #                     fontsize=18, loc=2)
    # legend.get_frame().set_linewidth(2)

    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(2)

    fig.set_size_inches(11,2,forward=True)
    if mode == 'plot':
        plt.show()
    else:
        plt.savefig(outname, dpi=300, transparent=True)

def plot_snr_lines(mode='plot'):
    ai_color = (.9,.5,0)
    human_color = (0,.5,.9)
    human_color_lighter = (0.5,0.7,.9)
    human_color_grey = (.5,.5,.5)
    human_color_grey_lighter = (.75,.75,.75)
    human_filename = '/Users/efun/Dropbox/sim-nfb/datasets/20160115-pilot-001/timed_frame_20160115-pilot-001.txt'

    ai_filename_high_snr = '/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_005/timed_frame_sim_ai_005.txt'
    ai_filename_low_snr = '/Users/efun/Dropbox/sim-nfb/datasets/sim_ai_006/timed_frame_sim_ai_006.txt'
    out_data_1 = preproc_snr_lines(filename=human_filename,snr=.01,tr=1)
    out_data_2 = preproc_snr_lines(filename=human_filename,snr=.01,tr=6)
    out_data_3 = preproc_snr_lines(filename=human_filename,snr=.15,tr=1)
    out_data_4 = preproc_snr_lines(filename=human_filename,snr=.15,tr=6)
    out_data_5 = preproc_snr_lines(filename=ai_filename_high_snr,snr=.01,tr=1, controller='ai')
    out_data_6 = preproc_snr_lines(filename=ai_filename_low_snr,snr=.15,tr=1, controller='ai')
    plot_single_lines(out_data_1, color=human_color, outname='human_high_snr_tr_1.pdf', mode='save')
    plot_single_lines(out_data_2, color=human_color_lighter, outname='human_high_snr_tr_6.pdf', mode='save')
    plot_single_lines(out_data_3, color=human_color, outname='human_low_snr_tr_1.pdf', mode='save')
    plot_single_lines(out_data_4, color=human_color_lighter, outname='human_low_snr_tr_6.pdf', mode='save')
    plot_single_lines(out_data_5, color=ai_color, outname='ai_high_snr.pdf', mode='save')
    plot_single_lines(out_data_6, color=ai_color, outname='ai_low_snr.pdf', mode='save')

