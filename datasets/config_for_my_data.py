import datetime

exp = { '1': False,
        '2': False,
        '3_1': False,
        '3_2': False,
        # want an adaptive model saved based on arch size for model_loc
        'data': 'avenue', #st, avenue,hr-st
        'data_consecutive': True,
        'model_name': 'bitrap_640_360', #lstm_network, bitrap
        }


hyparams = {
    'epochs':350,
    'batch_size': 32,
    'buffer_size': 10000,
    
    'frames': 20,
    'input_seq': 13,
    'pred_seq': 13,

    'to_xywh':True, # This is assuming file is in tlbr format
    # 'max':913.0, # wonder better way to pick
    # 'min':-138.5, # wonder better way to pick

    'networks': {
        'lstm':{
            'loss':'mse',
            'lr': 8.726e-06,
            'early_stopping': True,
            'mointor':'loss',
            'min_delta': 0.00005,
            'patience': 15,
            'val_ratio': 0.3,
        },



    }

}

# name_exp = None
if exp['1']:
    name_exp = '1'
elif exp['2']:
    name_exp = '2'
elif exp['3_1']:
    name_exp ='3_1'
elif exp['3_2']:
    name_exp = '3_2'
else:
    name_exp = 'traj_model'

now = datetime.datetime.now()
date = now.strftime("%m_%d_%Y")
time = now.strftime("%H:%M:%S")

if exp['data_consecutive']:
    model_path_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'saved_model_consecutive']
    metrics_path_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'metrics_plot_consecutive']
    visual_trajectory_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'visual_trajectory_consecutive', '{}_{}_{}_{}'.format(date, exp['data'], time, hyparams['frames'])]
    
    if exp['model_name'] == 'bitrap' or exp['model_name'] == 'bitrap_640_360' or exp['model_name'] == 'bitrap_1080_1020':
         model_path_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'saved_model_consecutive']
         metrics_path_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'metrics_plot_consecutive_bitrap']
         visual_trajectory_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'visual_trajectory_consecutive_bitrap', '{}_{}_{}_{}'.format(date, exp['data'], time, hyparams['frames'])]

else:
    model_path_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'saved_model']
    metrics_path_list ['results_all_datasets', 'experiment_{}'.format(name_exp), 'metrics_plot']
    visual_trajectory_list = ['results_all_datasets', 'experiment_{}'.format(name_exp), 'visual_trajectory', '{}_{}_{}_{}'.format(date, exp['data'], time, hyparams['frames'])]


loc =  {
    # if I'm running a test where don't want to save anything
    # how do I do that. Maybe move them to tmp
    
    'model_path_list': model_path_list,
    'metrics_path_list': metrics_path_list, 
    'visual_trajectory_list': visual_trajectory_list,
    
    'nc':{
        'model_name': exp['model_name'],
        'model_name_binary_classifer': 'binary_network',
        'data_coordinate_out': 'xywh',
        'dataset_name': exp['data'], # avenue, st             
        'date': date,
        },    # is nc the best way to propate and save things as same name
    # Might want to automatically  create a new folder with model arch saved
    # as a text file as well as in folder name

    'data_load':{
            'avenue':{
                # These are good because these locations are perm unless I manually move them
                'train_file': "/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/avenue/train_txt/",
                'test_file': "/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/avenue/test_txt/",
                'train_vid': '/mnt/roahm/users/akanu/dataset/Anomaly/Avenue_Dataset/training_videos',
                'test_vid': '/mnt/roahm/users/akanu/dataset/Anomaly/Avenue_Dataset/testing_videos',
                'train_poses': '/mnt/roahm/users/akanu/projects/AlphaPose/avenue_alphapose_out/train/{}/alphapose-results.json',
                'test_poses': '/mnt/roahm/users/akanu/projects/anomalous_pred/output_pose_json_appended/{:02d}_append.json',
                },

            #Need to rerun ped1
            # 'ped1':{
            #     'train_file':"/mnt/roahm/users/akanu/dataset/Anomaly/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Txt_Data/Train_Box_ped1/",
            #     "test_file": "/mnt/roahm/users/akanu/dataset/Anomaly/UCSD_Anomaly_Dataset.v1p2/UCSDped1/Txt_Data/Test_Box_ped1/",
            #     },
            'st':{
                'train_file':"/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/st/train_txt/",
                "test_file": "/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/st/test_txt/",
                'train_vid': '/mnt/workspace/datasets/shanghaitech/training/videos',
                'test_vid':  '/mnt/roahm/users/akanu/projects/Deep-SORT-YOLOv4/tensorflow2.0/deep-sort-yolov4/input_video/st_test',
                'train_poses': '/mnt/roahm/users/akanu/projects/AlphaPose/st_alphapose_out/train/{:02d}_{:03d}.avi/alphapose-results.json',
                'test_poses': '/mnt/roahm/users/akanu/projects/anomalous_pred/output_pose_json_appended_st/{:02d}_{:04d}_append.json',
                },
            'hr-st':{
                'train_file':"/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/HR-ShanghaiTech/train_txt/",
                "test_file": "/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/HR-ShanghaiTech/test_txt/",
                'train_vid': '/mnt/workspace/datasets/shanghaitech/training/videos',
                'test_vid':  '/mnt/roahm/users/akanu/projects/Deep-SORT-YOLOv4/tensorflow2.0/deep-sort-yolov4/input_video/st_test',
                },
            'corridor':{
                'train_file': '/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/corridor/train_txt/',
                'test_file': '/mnt/roahm/users/akanu/projects/anomalous_pred/output_deepsort/corridor/test_txt/',
                # 'train_vid':
                # 'test_vid':
            },
            }
            


}
