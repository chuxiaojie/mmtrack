# model settings
_base_ = ['./qdtrack_faster-rcnn_r101_fpn_24e_lvis.py']

model = dict(freeze_detector=True)

data_root = 'data/tao/'
train_dataloader = dict(
    batch_size=2,
    num_workers=2,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=False),
    batch_sampler=dict(type='mmdet.AspectRatioBatchSampler'),
    dataset=dict(
        data_root=data_root,
        load_as_video=True,
        metainfo=dict(CLASSES=(data_root + 'annotations/tao_classes.txt')),
        ann_file='annotations/train_482_classes.json',
        ref_img_sampler=dict(
            num_ref_imgs=1, frame_range=[-1, 1], method='uniform')))

# learning policy
param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=1.0 / 1000,
        by_epoch=False,
        begin=0,
        end=1000),
    dict(
        type='mmdet.MultiStepLR',
        begin=0,
        end=12,
        by_epoch=True,
        milestones=[8, 11])
]
# runtime settings
train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=12, val_interval=1)

# optimizer
optim_wrapper = dict(
    type='OptimWrapper',
    optimizer=dict(type='SGD', lr=0.002, momentum=0.9, weight_decay=0.0001),
    clip_grad=dict(max_norm=35, norm_type=2))

val_evaluator = dict(type='TAOMetric', metric=['tao_track_ap'])
test_evaluator = val_evaluator
load_from = None