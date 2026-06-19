\# TomatoAI - Tomato Disease Detector



A deep learning app that detects diseases in tomato leaves using MobileNetV2 transfer learning.



\## Features

\- Detects 10 tomato leaf diseases

\- Rejects non-leaf images automatically

\- Built with Gradio for easy web UI



\## Setup



1\. Install dependencies:

&#x20;  pip install -r requirements.txt



2\. Train the model:

&#x20;  python train.py



3\. Run the app:

&#x20;  python app.py



\## Files

\- app.py — Gradio web interface

\- train.py — Full training script (2-phase fine-tuning)

\- quick\_train.py — Fast training script

\- leaf\_checker.py — Filters out non-leaf images

\- disease\_info.py — Disease descriptions and treatments

