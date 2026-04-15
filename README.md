# Lite3 RL Training Hub (Airbotix Fork)

This repository is optimized for **High-Fidelity Simulation-to-Reality RL Development** for the Lite3 quadruped platform using **Isaac Lab** and **Isaac Sim**.

---

> [!IMPORTANT]
> **Airbotix is exclusively focused on the Lite3 platform.** 
> While foundational code for other platforms (M20) is preserved as legacy reference, our research is dedicated to achieving state-of-the-art results on the Jueying Lite3.

---

> [!CAUTION]
> ### 🚧 Branch `new_try_isaac_lab` — PARKED (April 2026)
>
> This branch attempted to replace Isaac Lab's procedural geometric terrain with a **mesh-based terrain imported directly from Isaac Sim** (stairs + slopes as USD mesh geometry). The approach was abandoned due to the following blocking issues:
>
> **1. GPU Memory / Environment Count Limit**
> Mesh-based terrain has a far higher physics memory footprint than procedural terrain. Training is capped at **~512 parallel environments** (vs. 4096 previously). This alone reduces sample throughput by ~8×, killing convergence speed.
>
> **2. Robot Spawn Instability**
> Because the terrain is mesh geometry (not analytic shapes), robots are sometimes spawned **intersecting the terrain or in nonsensical poses**. This causes invalid physics states and the robots cannot move, producing a flood of garbage experience in the replay buffer.
>
> **3. Training Does Not Converge**
> The combination of fewer environments and corrupted rollouts keeps the mean reward **permanently negative**. No meaningful policy improvement was observed regardless of reward tuning.
>
> **Next step:** Switch to a new branch using IsaacLab-Quadruped-Tasks with procedural stair terrain (generator-based) for the Lite3 — see `../isaaclab-quadruped-tasks/`.

---

**Official Airbotix Source**: [Airbotix-Technology-Pvt-Ltd/Lite3_rl_training](https://github.com/Airbotix-Technology-Pvt-Ltd/Lite3_rl_training)

---

### 🌐 Project Central Hubs
- [**Master Hub (Root)**](https://github.com/Airbotix-Technology-Pvt-Ltd/Lite3Robot): Mission, specialized workspaces, and organizational identity.
- [**Master Integration Guide**](../documentation/README.md): **Single Source of Truth** for technical milestones, roadmaps, and reproduction steps.
- [**Contributors Hub**](../Contributors.md): Full technical attribution for the Airbotix development team.

---

# RL Training Environment Setup Guide

A complete, reproducible guide for setting up reinforcement learning training environments for the Lite3 using Isaac Lab.

[**GitHub Source (Legacy Reference)**](https://github.com/DeepRoboticsLab/rl_training/tree/main) | [**Video Playlist**](https://youtube.com/playlist?list=PLy9YHJvMnjO0X4tx_NTWugTUMJXUrOgFH&si=gq3xuWtlPac0y1_o)

---

## 📋 Prerequisites
- **OS**: Ubuntu 22.04 (tested)
- **GPU**: RTX 3090+ recommended
- **RAM**: 16GB+ (32GB recommended)
- **Disk**: 50GB available

---

## 📌 Version Pinning (CRITICAL)
To ensure reproducibility and avoid physics/observation errors, you **MUST** use the exact commits specified. **Version mismatches in Isaac Lab are the primary source of training failures.**

| Component   | Version/Commit | Status |
|-------------|----------------|--------|
| IsaacLab    | [`0f00ca2b4b2d54d5f90006a92abb1b00a72b2f20`](https://github.com/isaac-sim/IsaacLab/commit/0f00ca2b4b2d54d5f90006a92abb1b00a72b2f20) | **REQUIRED** |
| rl_training | [`Airbotix Fork (This Repo)`](https://github.com/Airbotix-Technology-Pvt-Ltd/Lite3_rl_training) | **REQUIRED** |
| Isaac Sim   | 5.1.0 (pip)    | Verified |

---

## ⚡ Setup & Installation

### 1. Isaac Sim & Core Dependencies
```bash
conda create -n env_isaaclab python=3.11 -y && conda activate env_isaaclab
pip install --upgrade pip
pip install "isaacsim[all,extscache]==5.1.0" --extra-index-url https://pypi.nvidia.com
pip install -U torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
```

### 2. Isaac Lab & `rl_training`
```bash
git clone https://github.com/isaac-sim/IsaacLab.git && cd IsaacLab
git checkout 0f00ca2b4b2d54d5f90006a92abb1b00a72b2f20
./isaaclab.sh --install

cd ~ && git clone --recurse-submodules https://github.com/Airbotix-Technology-Pvt-Ltd/Lite3_rl_training.git
cd Lite3_rl_training && python -m pip install -e source/rl_training
```

---

## 🚀 Training & Verification

### Check Envs
```bash
python scripts/tools/list_envs.py  # Task: Rough-Deeprobotics-Lite3-v0
```

### Play & Train
```bash
# Sanity Test (Inference)
python scripts/reinforcement_learning/rsl_rl/play.py --task=Rough-Deeprobotics-Lite3-v0 --num_envs=2

# Start Training (Headless)
python scripts/reinforcement_learning/rsl_rl/train.py --task=Rough-Deeprobotics-Lite3-v0 --num_envs=4096 --headless
```

---

## ❤️ Credits & Tribute
We express our gratitude to **DeepRobotics** for providing the foundational `rl_training` stack and robust robot models. For original technical references and hardware manuals, please refer to the centralized [**Technical Library**](../documentation/README.md).

---
*Airbotix Technology Pvt Ltd - Lite3 P2P Autonomous Navigation Project*
*See our [**Contributors Hub**](../Contributors.md) for full project attribution.*
