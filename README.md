# Transport Game Experiment (oTree)

This repository contains an experimental adaptation of the Transport Game described by Cantiani et al. (2024), implemented in oTree (v5.6.0) as part of an ongoing research project. The associated manuscript is currently under preparation.

## The Experiment

This study investigates how **reputation**, operationalized via **Social Value Orientation (SVO)**, influences (a) **trust** in potential coalition partners and (b) **coalition negotiation behavior** in a transport setting.

Participants take part in one of two experimental conditions:

- **SVO visible**: SVO scores are visualized during the game to provide reputation information.
- **SVO not visible**: No SVO information is shown.

To study how reputation affects trust dynamics during negotiations, we use a **two-dimensional trust measure** and assess trust **three times**:
1. Before SVO information is (not) presented  
2. After SVO information is (not) presented  
3. After the negotiation

This setup allows analysis of how SVO-based reputation cues shape **trust (both dimensions)** and how trust relates to **coalition formation outcomes**.

## The Transport Game

The Transport Game is a **three-party coalition formation game** designed to simulate horizontal collaboration within the transport industry. It enables researchers interested in multi-party processes to conduct real-time, online **simple majority coalition** experiments.

This implementation runs as an oTree application and builds on earlier open-source coalition game work (see *Provenance* below). The game is available in **Dutch and English**.

## SVO Preload and Visualization

This implementation **requires** participants' Social Value Orientation (SVO) scores to be preloaded from a CSV file and integrates these scores into the experimental flow.

SVO scores are visualized as gauge-style plots and are displayed **only in the experimental (SVO visible) condition** during the negotiation phase.

To use this feature, place a CSV file in the `data/` folder of the relevant app (e.g., `Logistics_task_nl/data/`). The file should contain an identifier column (e.g., participant code) and an SVO score (e.g., svo_score) column.

No SVO data are included in this repository.

---

## Provenance and Credits

This repository is a **modified/extended version** of Anabela Cantiani's open-source Transport Game implementation.

- **Upstream base implementation**: Cantiani, A. (2023) — Transport Game codebase (GPL-3.0).  
  (See https://github.com/anabelac3/The-Transport-Game for original documentation and history.)

- **Academic reference (Transport Game implementation)**:  
  Cantiani, A., Van Beest, I., Cruijssen, F., Kant, G., & Erle, T. M. (2024). *Perspective-taking predicts success in coalition formation.* European Journal of Social Psychology, *54*(6), 1364–1377. https://doi.org/10.1002/ejsp.3091

- **Earlier foundation referenced by upstream**:  
  Cantiani's repository references the Online Coalition Game by Wissink et al. (2022).  
  For earlier provenance and details, please consult the upstream repository documentation and history.

## Summary of modifications in this repository

Compared to the upstream Transport Game codebase, this version includes (among others):

- Added **experimental manipulation**: SVO **visible vs. not visible**
- Added **CSV-based integration** for participant-level SVO scores
- Implemented **SVO visualizations (gauge-style plots)** and display logic so that SVO information is shown **only in the experimental condition**
- Implemented a **two-dimensional trust measure** and integrated **three trust measurement points** during the study (baseline, post-information, post-negotiation)
- Added/modified **HTML templates** and visual elements to improve readability and participant experience
- Reduced/adapted instruction texts and flow for an experimental context
- Adjusted app structure/configuration to support the experimental workflow (e.g., condition assignment, measurement pages)

---

## Installation

### Option A — Anaconda Navigator (GUI)

- Download all the necessary files to your PC.
- Install Anaconda from https://www.anaconda.com/download
- Open Anaconda Navigator. In the Environments tab, import the environment.yaml file and name the environment otree-env.
- Click on the green play button next to the otree-env environment and select Terminal.
- Specify the path where you placed the game files by typing:
  ``` bash
  cd path/to/your/repository
  ```
- Start the oTree server by typing: 
  ``` bash
  otree devserver
  ```
- Copy the URL shown in the terminal into your browser.

### Option B — Command Line (alternative)

- Download all the necessary files to your PC.
- Install Anaconda from https://www.anaconda.com/download
- Create the environment using the provided YAML file: 
  ``` bash
  conda env create -f environment.yaml
  ```
- Activate the environment: 
  ``` bash
  conda activate otree-env
  ```
- Start the oTree server: 
  ``` bash
  otree devserver
  ```
- Copy the URL shown in the terminal into your browser.

- **Note: This experiment requires participants' Social Value Orientation (SVO) scores to be preloaded from a CSV file.**
Before running the game, place a CSV file in the data folder of the relevant app (for example: Logistics_task_nl/data/).
**No SVO data are included in this repository, and the experiment will not run correctly without this file.**
- **Note:** For clean runs and for review purposes, it is recommended to reset the database before starting the server. 
- **Note:** If you wish to inspect or modify the code, you can use Visual Studio Code, PyCharm, or any IDE of your choice.

## Requirements / Versions

- Python: 3.9.x (e.g., runtime.txt specifies python-3.9.7)
- oTree: 5.6.0 (otree==5.6.0)

**Dependencies are listed in**:
- requirements_base.txt
- requirements.txt
- environment.yaml

## Session Configurations (example)

This project includes Dutch and English session configs (3-player sessions):

- Logistics_game_dutch
- Logistics_game_english

See settings.py for adjustable parameters such as language, timers, and incentives, etc.

---

## Additional Material

- oTree documentation: https://otree.readthedocs.io/en/latest/tutorial/intro.html
- Online Coalition Game article by Wissink et al. (2022) (as referenced upstream): https://link.springer.com/article/10.3758/s13428-021-01591-9

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
See the LICENSE file for details.

**Note**: This repository is a derivative work of a GPL-licensed upstream codebase; therefore, this repository remains GPL-licensed.

