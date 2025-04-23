# point.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


"""
Evaluate a trained PPO agent on the RubiksCube environment.

• A success is counted only when info["solved"] == True (all 54 stickers match).
• Works with the revised step() signature that returns (obs, reward,
  terminated, truncated, info).
"""

from __future__ import annotations
import argparse
from pathlib import Path

import gymnasium as gym
import numpy as np
import torch
from torch.distributions.categorical import Categorical

# ── project imports ───────────────────────────────────────────────────────────
from envs.rubikcubeEnv import rubikcubeEnv          # environment class
from ppo       import Agent                         # network architecture
# ──────────────────────────────────────────────────────────────────────────────


def resolve_checkpoint(path_like: str | None) -> Path:
    """
    Helper: choose latest checkpoint if none supplied
    """
    if path_like:
        p = Path(path_like)
        if not p.exists():
            raise FileNotFoundError(p)
        print(f"✅ Loading specified checkpoint: {p}")
        return p

    ckpts = sorted(Path("models").glob("*.pth"), key=lambda p: p.stat().st_mtime)
    if not ckpts:
        raise FileNotFoundError("No .pth files found in ./models")
    print(f"✅ Auto-loaded latest checkpoint: {ckpts[-1]}")
    return ckpts[-1]


@torch.no_grad()
def evaluate(
    ckpt_path: Path,
    num_episodes: int = 10,
    scramble_moves: int = 2,
    max_steps: int = 100,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Build env and network skeleton
    env = rubikcubeEnv(scramble_moves=scramble_moves)
    dummy_vec = gym.vector.SyncVectorEnv([lambda: env])
    agent     = Agent(dummy_vec).to(device)

    # Load weights
    checkpoint = torch.load(ckpt_path, map_location=device)
    agent.load_state_dict(checkpoint["policy"])
    agent.eval()

    solved_total, returns = 0, []

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        terminated = truncated = False
        steps = 0
        ep_return = 0.0

        while not (terminated or truncated) and steps < max_steps:
            obs_t = torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
            action = Categorical(logits=agent.actor(obs_t)).sample().item()

            obs, reward, terminated, truncated, info = env.step(action)
            ep_return += reward
            steps += 1

        solved = bool(info.get("solved", False))
        solved_total += solved
        flag = "✅" if solved else "❌"
        returns.append(ep_return)

        print(f"Episode {ep:02d}: return={ep_return:.3f}, steps={steps}, solved={flag}")

    print("\n==== Evaluation summary ====")
    print(f"Checkpoint : {ckpt_path.name}")
    print(f"Episodes   : {num_episodes}")
    print(f"Scramble   : {scramble_moves} move(s)")
    print(f"Mean return: {np.mean(returns):.3f}")
    print(f"Solved     : {solved_total}/{num_episodes}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",     "-m", type=str,
                        help="Path to checkpoint (.pth). Defaults to newest in ./models")
    parser.add_argument("--episodes",  "-n", type=int, default=10000,
                        help="Number of evaluation episodes")
    parser.add_argument("--scramble",  "-s", type=int, default=3,
                        help="Number of random moves used to scramble at reset()")
    args = parser.parse_args()

    ckpt = resolve_checkpoint(args.model)
    evaluate(ckpt,
             num_episodes=args.episodes,
             scramble_moves=args.scramble)
