import pdb
import os
import sys
#sys.path.remove('/home/brianyao/Documents/intention2021icra')
# work dda
sys.path.append(os.path.realpath('.'))
import torch
from torch import nn, optim
from torch.nn import functional as F

import pickle as pkl
from datasets import make_dataloader, make_dataloader_custom_data
from bitrap.modeling import make_model
from bitrap.engine import build_engine


from bitrap.utils.logger import Logger
import logging
import time

import argparse
from configs import cfg
from termcolor import colored 

import pdb

def main(cfg):
    # build model, optimizer and scheduler
    model = make_model(cfg)
    model = model.to(cfg.DEVICE)
    if os.path.isfile(cfg.CKPT_DIR):
        model.load_state_dict(torch.load(cfg.CKPT_DIR))
        print(colored('Loaded checkpoint:{}'.format(cfg.CKPT_DIR), 'blue', 'on_green'))
    else:
        print(colored('The cfg.CKPT_DIR id not a file: {}'.format(cfg.CKPT_DIR), 'green', 'on_red'))
    
    if cfg.USE_WANDB:
        logger = Logger("MPED_RNN",
                        cfg,
                        project = cfg.PROJECT,
                        viz_backend="wandb"
                        )
    else:
        logger = logging.Logger("MPED_RNN")
    
    # get dataloaders
    # test_dataloader = make_dataloader(cfg, 'test')
    # test_dataloader_av = make_dataloader_custom_data(cfg, 'test')

    # test_dataloader = make_dataloader_custom_data(cfg =cfg, split ='test', dataset =cfg.DATASET.NAME_SECOND)
    test_dataloader = make_dataloader_custom_data(cfg =cfg, load_poses = True, split='test', dataset =cfg.DATASET.NAME_SECOND)

    # # print(test_dataloader.xx[:5])
    # i = 0
    # for data, data_av in zip(test_dataloader, test_dataloader_av):
    #     print(data)
    #     i +=1
    #     if i == 1:
    #         break
    # quit()
    
    if hasattr(logger, 'run_id'):
        run_id = logger.run_id
    else:
        run_id = 'no_wandb'
    _, _, inference = build_engine(cfg)
    
    # inference(cfg, 0, model, test_dataloader, cfg.DEVICE, logger=logger, eval_kde_nll=True, test_mode=True)

    inference(cfg, 0, model, test_dataloader, cfg.DEVICE, logger=logger, eval_kde_nll=True, test_mode=True, custom='pose')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="PyTorch Object Detection Training")
    parser.add_argument('--gpu', default='0', type=str)
    parser.add_argument(
        "--config_file",
        default="",
        metavar="FILE",
        help="path to config file",
        type=str,
    )
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()
    
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    ss_start = time.time()
    main(cfg)
    ss_end = time.time()
    print(ss_end-ss_start) 

    # NOTE: define all the ckpt we want to check
    # all_ckpts = ['data/ETH_UCY_trajectron/checkpoints/goal_cvae_checkpoints/yh58kusd/Epoch_{}.pth'.format(str(i).zfill(3)) for i in range(1, 16)]
    # for ckpt in all_ckpts:
    #     cfg.CKPT_DIR = ckpt
    #     for min_hist_len in [1, 8]:
    #         cfg.MODEL.MIN_HIST_LEN = min_hist_len
    #         main(cfg)



