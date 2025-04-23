# point.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


from __future__ import annotations

import gymnasium as gym
from gymnasium import spaces
import numpy as np

# ── your rotation primitives ──────────────────────────────────────────────────
from actions.front  import RotateFront
from actions.right  import RotateRight
from actions.back   import RotateBack
from actions.left   import RotateLeft
from actions.up     import RotateUp
from actions.down   import RotateDown
# ──────────────────────────────────────────────────────────────────────────────


class rubikcubeEnv(gym.Env):
    """
    3×3×3 Rubik’s Cube environment.

    * observation  : 1‑D array of 54 uint8 sticker colours (0‑5)
    * action space : 12 quarter‑turns (F F' R R' … D')
    * reward       : fraction ∈ [0, 1] of **non‑center** stickers that match
                     the solved cube (48 movable stickers in total).
                     Full +1 is granted only when the cube is fully solved.
    """

    metadata = {"render_modes": ["human"]}

    # ────────────────────────────────────────────────────────────────────────
    # Environment initialisation
    # ────────────────────────────────────────────────────────────────────────
    def __init__(self, episode_length: int = 4, scramble_moves: int = 4) -> None:
        super().__init__()

        # gyms use 1‑D spaces for vector env compatibility
        self.observation_space = spaces.Box(low=0, high=5, shape=(54,), dtype=np.uint8)
        self.action_space      = spaces.Discrete(12)

        self.episode_length = episode_length
        self.scramble_moves = scramble_moves
        self.episode        = 0

        # cache the solved cube once
        self.solved = self._initial_state()

        # build a boolean mask that is *False* at the six face centres
        self._mask = np.ones((6, 3, 3), dtype=bool)
        self._mask[:, 1, 1] = False                # (row=1, col=1) on every face
        self._masked_total = int(self._mask.sum()) # 48 movable stickers

        # current cube state
        self.state  = self.solved.copy()
        self._state_flat = self.state.flatten()

        # map each action id to its corresponding rotation object
        self._rotation_table = [
            RotateFront(clockwise=True),  RotateFront(clockwise=False),
            RotateRight(clockwise=True),  RotateRight(clockwise=False),
            RotateBack(clockwise=True),   RotateBack(clockwise=False),
            RotateLeft(clockwise=True),   RotateLeft(clockwise=False),
            RotateUp(clockwise=True),     RotateUp(clockwise=False),
            RotateDown(clockwise=True),   RotateDown(clockwise=False),
        ]

    # ────────────────────────────────────────────────────────────────────────
    # Helper utilities
    # ────────────────────────────────────────────────────────────────────────
    @staticmethod
    def _initial_state() -> np.ndarray:
        """Return a (6, 3, 3) array representing the solved cube."""
        arr = np.zeros((6, 3, 3), dtype=np.uint8)
        for face in range(6):
            arr[face] = face
        return arr

    def _compute_reward(self) -> float:
        """Fraction of *non‑center* stickers in correct position."""
        correct = np.sum((self.state == self.solved) & self._mask)
        return correct / self._masked_total        # ∈ [0, 1]

    # ────────────────────────────────────────────────────────────────────────
    # Core Gym API
    # ────────────────────────────────────────────────────────────────────────
    def step(self, action: int):
        assert self.action_space.contains(action), "Invalid action id"

        # apply rotation
        self._rotation_table[action].ApplyRotation(self)

        # bookkeeping
        self.episode += 1
        self._state_flat = self.state.flatten()

        # reward and termination logic
        reward      = self._compute_reward()
        solved_now  = np.array_equal(self.state, self.solved)
        timeout     = self.episode == self.episode_length
        truncated   = timeout and not solved_now
        terminated  = solved_now

        if solved_now:                # full credit if truly solved
            reward = 1.0

        info = {"solved": solved_now}

        return self._state_flat, reward, terminated, truncated, info

    def reset(self, *, seed: int | None = None,
              options: dict | None = None):

        super().reset(seed=seed)        # seeds self.np_random

        # restore solved state then scramble
        self.state   = self.solved.copy()
        self.episode = 0
        for _ in range(self.scramble_moves):
            rnd_action = self.np_random.integers(0, self.action_space.n)
            self._rotation_table[rnd_action].ApplyRotation(self)

        self._state_flat = self.state.flatten()
        info = {}

        return self._state_flat, info

    # ────────────────────────────────────────────────────────────────────────
    # Rendering stubs (optional—nothing yet)
    # ────────────────────────────────────────────────────────────────────────
    def render(self, mode="human"):
        # Simple textual rendering; extend with OpenGL/matplotlib as desired.
        # print(self.state)
        pass

    def close(self):
        pass
