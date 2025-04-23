# 🎮 3D Rubik's Cube Game Manager

![Rubik's Cube GIF](./assets/rubikcube.gif)

## 🧩 Introduction

This project is a **game manager** built using **Pygame** that simulates 3D projections on a 2D screen. It currently features:
- A basic 3D cube
- A fully functional 3D Rubik's Cube
- A 3D Referential (coordinate axes)

At the core of this project is a base `Game` class that handles rotation, projection, and drawing logic for 3D objects. New objects or games can inherit from this class for transformation and rendering utilities.

## 🚀 Getting Started

### ✅ Requirements

- Python **3.8 – 3.10**

### 🔧 Setup

#### Option 1: Using `venv` (recommended for most users)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using Conda

```bash
conda create -n cube python=3.10
conda activate cube
pip install -r requirements.txt
```

## 🧠 How It Works

### 3D Simulation

The Rubik's Cube is made of **27 smaller cubes** (each of diameter = 1). These are transformed through a pipeline of:
1. **Global rotation**
2. **Padding and translation in z-axis**
3. **Perspective projection**
4. **Scaling to the 2D screen**

All transformations are handled using NumPy matrix operations.

### Class: `Game`

The `Game` class provides core transformation logic such as:
- Rotation (`GlobalRotation`)
- Projection (`Project`)
- Translation (`Translate`)
- Scaling to fit Pygame window

Every new 3D object/game should inherit from `Game`.

### Rubik's Cube Setup

The Rubik's Cube is implemented as:
- A 3D array of shape `(6, 3, 3)`, one for each face
- Stickers are color-coded from 0–5 (Yellow, Red, White, Orange, Green, Blue)
- Face rotations are handled as discrete actions

## 🕹️ Reinforcement Learning Integration

The cube is wrapped in a **Gym-compatible environment** (`RubikCube-v0`) for training AI agents using **Proximal Policy Optimization (PPO)**.

### Observation Space

- A 1D array of length **54** representing all stickers (excluding centers in reward computation).

### Action Space

- 12 discrete actions: quarter-turn rotations in both directions for each face (e.g., F, F’, R, R’, etc.).

### Reward

- Reward = fraction of **non-center** stickers that match the solved configuration (out of 48 total).

## 🧪 Training the Agent

> PPO is imported from the [CleanRL repository](https://github.com/vwxyzjn/cleanrl) and slightly adapted.

### Train PPO Agent

```bash
python3 ppo.py --seed 1 --env-id RubikCube-v0 --total-timesteps 5000
```

### Evaluate PPO Agent

```bash
python3 eval.py
```

### Monitor Progress

```bash
tensorboard --logdir runs
```

> 🔧 To change how many moves are used to scramble the cube before training, modify the values in `rubikcubeEnv.py`.

## ▶️ Run the Simulation

To see the 3D Rubik's Cube float and rotate:

```bash
python3 main.py
```
## ⌨️ Keyboard Controls

You can interact with the 3D Rubik's Cube using your keyboard:

- **Arrow Keys**
  - `↑` / `↓`: Rotate the entire cube along the **X-axis**
  - `→` / `←`: Rotate the entire cube along the **Y-axis**

- **Face Rotations (Clockwise / Counter-clockwise)**
  - `f` / `g`: Front face
  - `r` / `e`: Right face
  - `b` / `v`: Back face
  - `l` / `k`: Left face
  - `u` / `y`: Upper face
  - `d` / `s`: Down face

- **Scrambling**
  - `p`: Scramble the cube with 50 random face rotations

Each face key pair corresponds to clockwise and counter-clockwise rotations, respectively. These inputs trigger smooth animated turns for a more realistic simulation.

## 📁 File Structure

```plaintext
├── main.py                  # Entry point for rendering the cube
├── config/                  # Contains all transformation logic
├── rubikcubeEnv.py          # Gym-compatible Rubik’s Cube environment
    .
    .
    .
├── ppo.py                   # PPO agent from CleanRL
├── eval.py                  # Evaluation script
├── requirements.txt         # Dependencies
├── assets/rubiks_demo.gif   # Animation used in README
```

## 📜 License

MIT License

---

Happy coding! 🧠🧊
