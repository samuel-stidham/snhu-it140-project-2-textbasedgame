# SNHU IT-140 – Project Two  

## Aurelia: Deep-Sea Text Adventure

### Overview

This repository contains my submission for **IT-140 (Introduction to Scripting)** at Southern New Hampshire University.

The project is a text-based adventure game developed in Python. The game demonstrates dictionary-driven room navigation, item collection with input validation, branching movement logic, and clearly defined win/lose conditions.

---

## Story

You are a salvage diver exploring the *Aurelia*, a research station at the bottom of the Mariana Trench that has gone completely silent.  

To escape, you must collect six essential components needed to repair your damaged escape pod. However, a massive bioluminescent Leviathan now stalks the corridors.

Enter the Reactor Core unprepared… and the consequences are immediate.

---

## Game Map

<p align="center">
  <img src="aurelia-map.png" width="600"><br>
  <em>Station layout and room connectivity for the Aurelia.</em>
</p>


---

## Objective

Collect all **6 components** before entering the **Reactor Core**.

- Enter the Reactor Core without all components → Game Over  
- Enter with all components → You win  

---

## Features

- Dictionary-based room connections
- Separate dictionary for room items
- Branching directional logic (Airlock East → Medical or Engineering)
- Input validation for:
  - Invalid directions
  - Invalid item retrieval
  - Ambiguous branching movement
- Explicit player command structure:
  - `go North | South | East | West`
  - `get <item name>`
  - `look`
  - `exit`
- Clear win and loss conditions
- Inline documentation and type hints (`typing` module)

---

## Project Structure

- `TextBasedGame.py`
- `README.md`

---

## How to Run

Ensure Python 3.9+ is installed.

Run:

```bash
python TextBasedGame.py
```

No external dependencies are required.

---

## Design Notes

- All gameplay logic is handled within a main loop.
- Room navigation is validated against a dictionary structure.
- Items are collected manually using the `get` command (not auto-collected).
- The branching logic in the Airlock maintains rubric requirements while supporting expanded map design.

---

## Academic Context

Course: IT-140  
Program: B.S. Computer Science (Software Engineering concentration)  
Institution: Southern New Hampshire University  

---

## Author

Samuel Stidham  
02-2026  
