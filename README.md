# Connect Four AI Implementation

## Project Overview
This project implements the classic Connect Four game with an artificial intelligence opponent using the Minimax algorithm enhanced with Alpha-Beta pruning. The implementation includes a graphical user interface built with Pygame, customizable AI difficulty settings, and comprehensive performance testing tools. The project was developed as part of the INFO-H410 Techniques of Artificial Intelligence course at Université Libre de Bruxelles.

## Game Description
Connect Four is a two-player connection game where players take turns dropping colored discs into a seven-column, six-row vertically suspended grid. The objective is to connect four discs of the same color vertically, horizontally, or diagonally before your opponent.

## Features
- Interactive graphical user interface using Pygame
- Multiple game modes:
  - Human vs AI
  - AI vs AI (for demonstrations and algorithm comparison)
- Adjustable AI difficulty levels (search depth from 1-10)
- Custom difficulty settings via text input
- Visual feedback with colored player indicators
- Performance testing tools for algorithm comparison
- Reset and main menu buttons for improved user experience

## Technical Implementation
The game is implemented in Python with the following components:
- **Game Logic**: Core game rules, state management, and win detection
- **AI Player**: Minimax algorithm with Alpha-Beta pruning optimization
- **Human Player**: Interface for human input via mouse clicks
- **GUI**: Interactive game display using Pygame
- **Performance Testing**: Tools to compare standard Minimax vs Alpha-Beta pruning

## AI Algorithm
The AI uses Minimax with Alpha-Beta pruning to make optimal decisions:

### Minimax
A recursive algorithm that simulates all possible game states to a certain depth, assuming both players play optimally. The AI maximizes its advantage while assuming the opponent will minimize it.

### Alpha-Beta Pruning
An optimization technique that dramatically reduces the number of nodes evaluated in the search tree by eliminating branches that cannot possibly influence the final decision. Our testing shows this reduces node evaluations by up to 84.5% and provides a 7.1x speedup at depth 5.

### Evaluation Function
The board positions are evaluated based on:
- Center control (pieces in central columns are weighted higher)
- Connection patterns (potential winning sequences)
- Defensive positioning (blocking opponent's potential wins)

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
   pip install pygame numpy
   ```

3. Run the game
   ```bash
   python src/main.py
   ```

4. Run performance tests (optional)
   ```bash
   python src/main.py --performance-test
   ```

## Project Structure
```
IA_infoh410/
│
├── src/                # Source code
│   ├── main.py         # Entry point
│   ├── performance_test.py         # perfermance script
│   ├── game/           # Game logic
│   │   ├── game.py     # Main game controller
│   │   ├── AiPlayer.py # AI implementation
│   │   └── humanplayer.py # Human player implementation
│   └── ui/             # User interface
│       |── GameGUI.py  # Pygame-based GUI
│       └── Welcomepage.py  # Welcomepage-based GUI

│
├── results/              # Results of performance tests
├── docs/              # screenshots of the ui
└── README.md           # This file
```

## Usage
- Use mouse clicks to select columns and drop discs
- Press 'R' to reset the game
- Press 'ESC' to exit

## Contributors
- Imad Sharof
- Kerim Esiev
- Mohamed Sewif



