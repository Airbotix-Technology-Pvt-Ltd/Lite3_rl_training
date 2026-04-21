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
        
        # INCREASE KNEE MOBILITY: The default 0.25 scale (14 degrees) is not enough for stairs.
        self.actions.joint_pos.scale = {".*_HipX_joint": 0.125, "^(?!.*_HipX_joint).*": 0.5}

        # 2. Copied commands configuration: Force the robot to constantly walk forward and not strafe
        self.commands.base_velocity.ranges.lin_vel_x = (0.5, 1.0)
        self.commands.base_velocity.ranges.lin_vel_y = (0.0, 0.0)
        self.commands.base_velocity.ranges.ang_vel_z = (-math.pi / 6, math.pi / 6)

        # 3. Copied event configuration: Ensure robot always spawns facing the stairs perfectly (yaw=0)
        self.events.randomize_reset_base.params["pose_range"]["yaw"] = (0.0, 0.0)

        # 4. Fix Knee Stiffness: Remove joint deviation penalties so it can freely bend its knees
        self.rewards.joint_deviation_l1.weight = 0.0
        
        # 5. Fix Knee Stiffness: Reduce energy starvation penalties that cause stiff-legged walking
        self.rewards.action_rate_l2.weight = -0.005 # heavily reduced from -0.02
        self.rewards.joint_power.weight = -2e-6 # heavily reduced from -2e-5
        
        # 6. Encourage Height: Target high steps to force the knee to actuate
        self.rewards.feet_height.weight = 1.0 # Increase weight
        self.rewards.feet_height.params["target_height"] = 0.15 # Force 15cm lift

        # Disable zero-weight rewards to prevent IsaacLab crashing on unconfigured parameters
        self.disable_zero_weight_rewards()