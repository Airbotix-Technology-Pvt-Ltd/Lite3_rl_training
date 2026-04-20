# Copyright (c) 2025 Deep Robotics
# SPDX-License-Identifier: BSD 3-Clause

import math
from isaaclab.utils import configclass
from isaaclab.terrains import (
    TerrainGeneratorCfg,
    MeshPyramidStairsTerrainCfg,
    MeshInvertedPyramidStairsTerrainCfg,
    HfPyramidSlopedTerrainCfg,
    HfInvertedPyramidSlopedTerrainCfg,
)

from rl_training.tasks.manager_based.locomotion.velocity.config.quadruped.deeprobotics_lite3.rough_env_cfg import DeeproboticsLite3RoughEnvCfg

# Copied verbatim from omni.isaac.lab_quadruped_tasks.cfg.quadruped_terrains_cfg
STAIRS_TERRAINS_CFG = TerrainGeneratorCfg(
    seed=42,
    size=(8.0, 8.0),
    border_width=20.0,
    num_rows=10,
    num_cols=16,
    horizontal_scale=0.1,
    vertical_scale=0.005,
    slope_threshold=0.75,
    use_cache=True,
    sub_terrains={
        "pyramid_stairs_inv": MeshInvertedPyramidStairsTerrainCfg(
            proportion=0.4,
            step_height_range=(0.05, 0.23),
            step_width=0.3,
            platform_width=3.0,
            border_width=1.0,
            holes=False,
        ),
        "pyramid_stairs": MeshPyramidStairsTerrainCfg(
            proportion=0.4,
            step_height_range=(0.05, 0.23),
            step_width=0.3,
            platform_width=3.0,
            border_width=1.0,
            holes=False,
        ),
        "hf_pyramid_slope_inv": HfInvertedPyramidSlopedTerrainCfg(
            proportion=0.1, slope_range=(0.0, 0.4), platform_width=2.0, border_width=0.25
        ),
        "hf_pyramid_slope": HfPyramidSlopedTerrainCfg(
            proportion=0.1, slope_range=(0.0, 0.4), platform_width=2.0, border_width=0.25
        ),
    },
    curriculum=True,
    difficulty_range=(0.0, 1.0),
)

@configclass
class DeeproboticsLite3StairEnvCfg(DeeproboticsLite3RoughEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # 1. Use the exact STAIRS_TERRAINS_CFG copied from isaac_quadruped_tasks
        self.scene.terrain.terrain_generator = STAIRS_TERRAINS_CFG
        self.scene.env_spacing = 8.0

        # 2. Copied commands configuration: Force the robot to constantly walk forward and not strafe
        self.commands.base_velocity.ranges.lin_vel_x = (0.5, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-math.pi / 6, math.pi / 6)

        # 3. Copied event configuration: Ensure robot always spawns facing the stairs perfectly (yaw=0)
        self.events.randomize_reset_base.params["pose_range"]["yaw"] = (0.0, 0.0)

        # 4. Disable zero-weight rewards to prevent IsaacLab crashing on unconfigured parameters
        self.disable_zero_weight_rewards()
scm-history-item:/home/lite3/work/Lite3Robot/rl_training?%7B%22repositoryId%22%3A%22scm7%22%2C%22historyItemId%22%3A%2289ede87496afda000eadb756cb4d3d43b74c52f8%22%2C%22historyItemParentId%22%3A%221a0e7fec975491ea5c2822775d5ac7b73ddd5ca2%22%2C%22historyItemDisplayId%22%3A%2289ede87%22%7D