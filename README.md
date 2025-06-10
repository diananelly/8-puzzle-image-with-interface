8-Puzzle Solver — Final Project Report 

Project Description 
This project is a graphical web-based implementation of the 8-puzzle game 
using Streamlit. Users can upload any square image, which is then sliced into 
8 tiles and one blank tile, forming a playable 3x3 puzzle. 

The app allows the user to: 
1. Shuffle the puzzle 
2. Solve it using A* (default), Breadth-First Search (BFS), or Depth-First 
Search (DFS)
3. Watch a step-by-step animation of the selected solution 
4. Interact manually with the steps using highlighted arrows and tile 

User Interface Features 
 1. Image Upload & Slice : Users upload an image which is converted into 
3x3 tiles. 
2. Puzzle Shuffle: Random shuffling ensures solvable starting states. 
3. Animated Solution: A real-time animation visualizes the algorithm's 
optimal steps. 
4. Interactive Step Navigation: Buttons with directional arrows allow 
users to navigate steps manually and understand tile transitions. 
5. Replay Button: Allows users to rerun the animation any time after 
solving. 

How to Run
1- Install dependencies: pip install streamlit  
2- Run the app: streamlit run app-1.py
