# Stickman Fighting Game
## Project Introduction
This project aims to design and implement an action-based competitive game, Stickman Fighting Game, based on the Q-Learning algorithm in reinforcement learning. In this game, the player controls a character to fight against an enemy controlled by artificial intelligence.

## Game Rules
The game is a one-on-one side-scrolling fighting game, where the player competes against an AI-controlled opponent. Each side controls a character, and the objective is to defeat the opponent by reducing their health points (HP) to zero through attacks or skills.
The main rules of the game are as follows:
• Each character starts with 100 HP (Health Points) and 100 MP (Mana Points)
• The player can control the character using the keyboard to move, attack, use skills,and crouch
• Normal attacks deal damage at close range
• Skill attacks are ranged attacks that consume MP
• Crouching allows the character to dodge incoming skill attacks
• The game ends when either character’s HP reaches zero
<img width="1782" height="958" alt="image" src="https://github.com/user-attachments/assets/d366449c-6687-45ca-a7e1-0daca3fe3479" />
<img width="1798" height="948" alt="image" src="https://github.com/user-attachments/assets/79a2bc3c-f327-4983-b361-b394b84261b5" />

## Q-Learning Algorithm Implementation
Q-Learning is a model-free reinforcement learning algorithm that aims to learn the optimal action-selection policy by estimating the Q-value function. The Q-value represents the expected cumulative reward of taking a specific action in a given state.
The reward function is the most crucial component in a reinforcement learning system, directly determining the learning direction of the AI. Firstly, in the attack aspect, positive rewards are given when the AI successfully attacks the player, while negative rewards are given when it is attacked itself. This design makes the AI tend to actively attack and avoid being hit.
Furthermore, to prevent the AI from exhibiting negative behaviors, the system introduces a continuous penalty term, that is, a slight negative reward is given at each step, thereby encouraging the AI to remain active. This reward function not only focuses on attack behaviors but also covers position control and behavioral rhythm, shaping the AI's decision-making ability from multiple dimensions.
