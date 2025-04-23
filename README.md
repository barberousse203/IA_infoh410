# IA_infoh410: Connect 4 Game with AI

## Project Overview
This project implements the classic Connect 4 game with an artificial intelligence opponent using the Minimax algorithm and Alpha-Beta pruning. The project was developed as part of the INFO-H410 Techniques of Artificial Intelligence course at Université Libre de Bruxelles.

## Game Description
Connect 4 is a two-player connection game where players take turns dropping colored discs into a seven-column, six-row vertically suspended grid. The objective is to connect four discs of the same color vertically, horizontally, or diagonally before your opponent.

## Features
- Interactive graphical user interface using Pygame
- Human vs Human mode
- Human vs AI mode
- AI vs AI mode (for demonstration)
- Adjustable AI parameteres

## Technical Implementation
The game is implemented in Python with the following components:
- Game logic and state management
- Interactive GUI using Pygame
- AI player using Minimax algorithm with Alpha-Beta pruning

## Installation and Setup

### Prerequisites
- Python 3.7+
- Pygame

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/IA_infoh410.git
   cd IA_infoh410
   ```

2. Install the required packages
   ```bash
   pip install pygame
   ```

3. Run the game
   ```bash
   python src/main.py
   ```

## AI Algorithm Implementation
The AI uses the Minimax algorithm with Alpha-Beta pruning to determine the best move:

### Minimax Algorithm
Minimax is a decision-making algorithm that minimizes the possible loss for a worst-case scenario. In the context of Connect 4:
- The AI evaluates the game board by looking ahead several moves
- It alternates between maximizing its score and minimizing the opponent's score
- The algorithm recursively evaluates all possible moves up to a certain depth

### Alpha-Beta Pruning
Alpha-Beta pruning enhances the Minimax algorithm by eliminating branches that don't need to be explored:
- Alpha represents the minimum score that the maximizing player is assured of
- Beta represents the maximum score that the minimizing player is assured of
- When a node's value exceeds beta (for a maximizing player) or falls below alpha (for a minimizing player), we can "prune" that branch

### Evaluation Function
The AI evaluates board positions based on:
- Connection patterns (potential winning sequences)
- Control of the center columns
- Defensive positioning to block opponent wins

## Project Structure
```
IA_infoh410/
│
├── src/                # Source code
│   ├── main.py         # Entry point
│   ├── game/           # Game logic
│   │   ├── game.py     # Main game controller
│   │   ├── AiPlayer.py # AI implementation
│   │   └── humanplayer.py # Human player implementation
│   └── ui/             # User interface
│       └── GameGUI.py  # Pygame-based GUI
│
├── tests/              # Unit tests
└── README.md           # This file
```

## Usage
- Use mouse clicks to select columns and drop discs
- Press 'R' to reset the game
- Press 'ESC' to exit

## Contributors
- Imad Sharov
- Kerim Esiev
- Mohamed Sewif



