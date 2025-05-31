# LeagueBot 🧠🎮

## 🛡️ Overview

**LeagueBot** is a fully automated bot designed for **League of Legends**. It leverages real-time **object detection**, screen analysis, and **in-game decision making** to control a champion on the mid lane. The bot is capable of detecting minions, turrets, inhibitors, and even enemy champions, and makes strategic decisions based on battlefield conditions.

This project integrates **TensorFlow Hub**, **PyAutoGUI**, **PIL**, and **custom heuristics** to build an agent capable of surviving and progressing through the midlane.

---

## ⚙️ Features

- 🎯 **Object Detection** with a custom-trained TensorFlow model
- 🎮 Full control of in-game movement and attacks via `pyautogui` & `pydirectinput`
- 🧠 Smart decisions: turret diving logic, minion tanking detection, retreat logic
- 🗺️ Resolution-aware coordinates & dynamic minimap control
- 🛡️ Turret range prediction using screen resolution scaling
- 🧪 Real-time inference loop with game-over detection

---

## 🧠 How It Works

- Takes full-screen screenshots every 0.5s
- Runs detection using a **custom-trained TensorFlow model** loaded from TF Hub
- Classifies detected objects into minions, turrets, champions, etc.
- Calculates distances from player (center of screen) to each object
- Decides whether to attack, move, or retreat based on conditions:
  - Minions tanking turret? Push.
  - Alone in turret range? Retreat.
  - More allies than enemies? Engage.
  - Enemy champion nearby with low risk? Attack with ability.
- Uses hardcoded screen-scaling logic to make decisions portable across resolutions

---
## 🎯 Object Classes

Class ID	Label

1	    Ally Caster
  
2  	  Ally Melee

3  	  Ally Cannon

4  	  Enemy Caster

5  	  Enemy Melee

6  	  Enemy Cannon

7	    Ally Turret

8	    Enemy Turret

9	    Enemy Inhibitor

10	  Ally Super



## 🚀 Getting Started

### 1. Install Requirements
Ensure you have Python 3.9+ and install the dependencies:
```bash
pip install -r requirements.txt
You must also install Tesseract OCR and have League of Legends installed.

Download or train your TensorFlow object detection model and place it under:

venv/object_detection_model/my_model/saved_model/

Make sure League of Legends is running, then:
Run the bot: python main.py
By default, the bot waits for the game to start and controls a midlane champion only

## Example Decisions
Minion waves closer to turret → bot holds position

2+ allies under turret → bot attacks turret

Enemy champion near, but alone → bot engages with Q

No minions or support nearby → retreat to safer position
