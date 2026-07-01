# TI mmWave Studio Python Orchestrator

## Overview
This project establishes a proof-of-concept for remotely controlling a Texas Instruments mmWave radar from a separate machine without manually interacting with the mmWave Studio GUI. mmWave Studio is the standard TI software for configuring and capturing data from radars like the IWR6843ISK-ODS + DCA1000 EVM. By default, it requires manual GUI interaction. For automated or multi-radar deployments, this doesn't scale. TI ships a scripting framework called RSTD (Remote Studio Test Driver) that enables programmatic control of Studio via Lua scripts and a TCP-based remote interface.

## Goal
Build a working RSTD setup where:

* A radar laptop runs mmWave Studio with RSTD enabled and a connected IWR6843ISK-ODS + DCA1000 EVM
* A master machine connects over the network and executes a complete radar capture cycle programmatically: configuring the radar, starting a capture, and collecting the resulting UDP data packets (all without touching the GUI)

Captured data is forwarded via UDP packets through a packet sniffer and stored in MinIO for downstream processing.

## Installation

## Usage
Run ```python radar_control.py```

## Resources
