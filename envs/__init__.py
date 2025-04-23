# point.py

# -*- coding: utf-8 -*-
# Author: Dhia Neifar <neifar@umich.edu>


from gymnasium.envs.registration import register

register(
    id="RubikCube-v0",
    entry_point="envs.rubikcubeEnv:rubikcubeEnv",
)
