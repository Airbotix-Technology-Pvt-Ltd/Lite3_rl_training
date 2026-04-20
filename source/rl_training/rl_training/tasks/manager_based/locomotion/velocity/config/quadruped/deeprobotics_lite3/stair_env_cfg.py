# Copyright (c) 2025 Deep Robotics
# SPDX-License-Identifier: BSD 3-Clause

from isaaclab.utils import configclass

from rl_training.tasks.manager_based.locomotion.velocity.config.quadruped.deeprobotics_lite3.rough_env_cfg import DeeproboticsLite3RoughEnvCfg

@configclass
class DeeproboticsLite3StairEnvCfg(DeeproboticsLite3RoughEnvCfg):
    def __post_init__(self):
        # post init of parent RoughEnvCfg
        super().__post_init__()

        # ==========================================
        # STAIRS TERRAIN CONFIGURATION
        # ==========================================
        # Purposely restrict the terrain generator to only stair-like structures.
        # This prevents the agent from finding loopholes by avoiding stairs and
        # maximizing reward on easier terrains, which happens when mixed heavily.
        
        # Zero out the ones we don't want
        self.scene.terrain.terrain_generator.sub_terrains["random_rough"].proportion = 0.0
        self.scene.terrain.terrain_generator.sub_terrains["boxes"].proportion = 0.0
        
        # Use strictly stairs and intense slopes
        self.scene.terrain.terrain_generator.sub_terrains["hf_pyramid_slope"].proportion = 0.1
        self.scene.terrain.terrain_generator.sub_terrains["hf_pyramid_slope_inv"].proportion = 0.1
        self.scene.terrain.terrain_generator.sub_terrains["pyramid_stairs"].proportion = 0.4
        self.scene.terrain.terrain_generator.sub_terrains["pyramid_stairs_inv"].proportion = 0.4

        # Real stairs configuration
        self.scene.terrain.terrain_generator.sub_terrains["pyramid_stairs"].step_height_range = (0.05, 0.18)
        self.scene.terrain.terrain_generator.sub_terrains["pyramid_stairs"].step_width = 0.3
        self.scene.terrain.terrain_generator.sub_terrains["pyramid_stairs_inv"].step_height_range = (0.05, 0.18)
        self.scene.terrain.terrain_generator.sub_terrains["pyramid_stairs_inv"].step_width = 0.3

        # Disable caching to ensure we genuinely generate stairs instead of pulling an old random rough map
        self.scene.terrain.terrain_generator.use_cache = False

        # ==========================================
        # STAIR-SPECIFIC REWARD LOOPHOLE PREVENTION
        # ==========================================
        # Loophole 1: "Dragging" legs up the stairs. 
        # Fix: Heavily penalize shin/thigh contact so the robot is forced to cleanly step over edges.
        self.rewards.undesired_contacts.weight = -2.0 # Increased from -0.5

        # Loophole 2: Stubbing toes.
        # Fix: Increase target foot height significantly so the robot learns to clear 18cm steps.
        self.rewards.feet_height.params["target_height"] = 0.20 # Increased from 0.08

        # Loophole 3: Standing still or moving extremely slowly to abuse survival time.
        # Fix: Reduce standard feet slide penalties slightly if needed, but maintain tracking penalty.
        self.rewards.track_lin_vel_xy_exp.weight = 4.0 # Increased to push forward tracking

        # Loophole 4: Extreme torso pitching to "crawl" up.
        # Fix: Keep flat_orientation heavily penalized to force an upright trot on stairs.
        self.rewards.flat_orientation_l2.weight = -5.0 

        # We can also increase the feet air time reward a bit to encourage a pronounced stepping gait
        self.rewards.feet_air_time.weight = 10.0 # Increased from 8.0
