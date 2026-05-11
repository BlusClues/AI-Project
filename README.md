# 📦 Autonomous Tank Battle on a Dynamically Changing World Map

Generate a dynamic game map on any uploaded image of your choice!
Have two AI tanks duke it out in the arena!

## 🌟 Highlights

- Uses Otsu's Method to get an average of the colour intensity of the image
- A* Grid 2D runs the tanks pathfinding algorithm
- Finite State Machine for the decision making of the tanks

## ℹ️ Overview

This project addresses procedural generation of a 2D game from unstructured real-world images. The generative method of the project uses a customized image processing pipeline, using Otsu’s method for dynamic thresholding with a flood fill algorithm for the topological cleanup. It converts the image using the gameplay rules so that the final output is recognizable and playable. This pipeline translates high-quality photographs into a retro, top-down, grid-based art style suitable for a 32x32 tile tank combat simulation.  By placing the AI in this chaotic, generated environment, the tanks are forced to rely on dynamic A* pathfinding and real-time ray casting. This proves the robustness of their FSMs as arenas cannot be pre-calculated or memorized.
This project was made as my final project for my COMP 3710 Applied Artificial Intelligence. The project was made with one requirement, make a computational artist.

## 🚀 Usage/Requirements

This project has a few required packages to run:
-Python 3.x
-Pygame (For seeing and showcasing the game)
-Pillow (For image processing and GIF generation)

Once those are installed, Go into Settings.py
Change BACKGROUND_IMAGE to your image path. 

Then when you press play you will see the game play on screen and a new gif will be created as test.gif
Make sure if you want to save the GIF that you move it out of the project folder or rename it as the program will overwrite the pervious GIF
