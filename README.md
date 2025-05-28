# Maze-Escape-Game
## 🧩 Maze Escape Game – Python + Pygame
Welcome to Maze Escape! A fully playable 2D puzzle game built using Python and Pygame. You control a player trapped in a maze full of surprises — collect keys, dodge fake doors, grab time boosts, and escape before time runs out!

⚙️ Each playthrough generates a brand new maze using a recursive backtracking algorithm, making the experience unique every time.

## 🎮 Game Features

🌀 Randomized maze generation using a recursive backtracking algorithm

🧍 Smooth tile-to-tile player movement with directional rotation

🗝️ Multiple keys and doors — unlock them in order

🚪 Fake doors that disappear on collision

⏳ Countdown timer and collectible time boosts

📊 Top bar HUD showing collected keys and remaining time

📍 End-of-game pathfinding visualization using the A* algorithm

🖼️ Custom start, win, lose, and end screens with background visuals


## 🧠 How It Works

- The maze is generated recursively at runtime using a depth-first search (DFS) approach.

- Each playthrough is unique thanks to random path carving.

- All keys must be collected to escape the maze , also the doors open when their respective keys are collected .

- At the end or if the time runs out, the game visualizes the optimal escape path using the A* algorithm, showcasing the correct sequence of moves.

- All images are loaded dynamically.
