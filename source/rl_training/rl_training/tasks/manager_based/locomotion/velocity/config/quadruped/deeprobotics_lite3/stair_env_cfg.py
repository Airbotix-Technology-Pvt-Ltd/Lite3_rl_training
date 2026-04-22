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

import isaaclab.sensors as sensor_utils
from isaaclab.sensors import RayCasterCfg, patterns
from rl_training.tasks.manager_based.locomotion.velocity.config.quadruped.deeprobotics_lite3.rough_env_cfg import DeeproboticsLite3RoughEnvCfg
from rl_training.tasks.manager_based.locomotion.velocity.velocity_env_cfg import MySceneCfg

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
class StairSceneCfg(MySceneCfg):
    # Foot scanners: one per leg since regex is not supported in prim_path
    feet_scanner_fl = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/FL_FOOT", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    feet_scanner_fr = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/FR_FOOT", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    feet_scanner_hl = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/HL_FOOT", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    feet_scanner_hr = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/HR_FOOT", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    # Knee/Thigh scanners
    knee_scanner_fl = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/FL_THIGH", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    knee_scanner_fr = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/FR_THIGH", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    knee_scanner_hl = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/HL_THIGH", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )
    knee_scanner_hr = RayCasterCfg(
        prim_path="{ENV_REGEX_NS}/Robot/HR_THIGH", 
        offset=RayCasterCfg.OffsetCfg(pos=(0.0, 0.0, 2.0)),
        ray_alignment="world",
        max_distance=2.5,
        pattern_cfg=patterns.GridPatternCfg(resolution=0.1, size=(0.0, 0.0)),
        mesh_prim_paths=["/World/ground"],
        debug_vis=False,
    )

@configclass
class DeeproboticsLite3StairEnvCfg(DeeproboticsLite3RoughEnvCfg):
    scene: StairSceneCfg = StairSceneCfg()

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

        # 4. Fix Knee Stiffness: Restore a light penalty to prevent "ugly" joint configurations
        self.rewards.joint_deviation_l1.weight = -0.1
        
        # 5. Fix Knee Stiffness: Reduce energy starvation penalties that cause stiff-legged walking
        self.rewards.action_rate_l2.weight = -0.01 
        self.rewards.joint_power.weight = -5e-6 
        
        # 6. Encourage Height (The "Sticks"): Use the NEW Terrain-Aware reward
        self.rewards.feet_height.weight = 0.0 # Disable absolute height
        self.rewards.feet_height_terrain.weight = -5.0 
        self.rewards.feet_height_terrain.params["target_height"] = 0.12 
        self.rewards.feet_height_terrain.params["asset_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_height_terrain.params["sensor_cfg"] = ["feet_scanner_fl", "feet_scanner_fr", "feet_scanner_hl", "feet_scanner_hr"]
        self.rewards.feet_height_body.weight = -0.1 # Relax horizontal movement constraint
        
        # 7. Force Body Lift: Heavily penalize low torso height
        self.rewards.base_height_l2.weight = -50.0
        self.rewards.base_height_l2.params["target_height"] = 0.3
        self.rewards.base_height_l2.params["asset_cfg"].body_names = ["TORSO"]
        self.rewards.base_height_under.weight = -50.0
        self.rewards.base_height_under.params["target_height"] = 0.25
        self.rewards.base_height_under.params["asset_cfg"].body_names = ["TORSO"]
        
        # 8. Stay Level: Prevent the robot from leaning/crawling
        self.rewards.flat_orientation_l2.weight = -15.0
        
        # 9. Strictly Prohibit Kneeling: Maximize penalty for knee/shank contacts
        self.rewards.undesired_contacts.weight = -10.0
        
        # 10. Steady Knee Height: Proactively reward keeping knees at a safe height
        self.rewards.knee_height_terrain.weight = -5.0
        self.rewards.knee_height_terrain.params["target_height"] = 0.25 # 25cm above floor
        self.rewards.knee_height_terrain.params["asset_cfg"].body_names = [".*_THIGH"]
        self.rewards.knee_height_terrain.params["sensor_cfg"] = ["knee_scanner_fl", "knee_scanner_fr", "knee_scanner_hl", "knee_scanner_hr"]

        # Disable zero-weight rewards to prevent IsaacLab crashing on unconfigured parameters
        self.disable_zero_weight_rewards()