# EMS V1 – Energy Management System

A smart Home Assistant custom integration for optimizing energy usage, solar production, and battery behavior.

## ⚡ Features

- SolarEdge PV integration
- P1 smart meter load tracking
- Dynamic energy pricing support
- 24h forecasting (PV, load, price)
- Battery simulation (5–20 kWh scenarios)
- ROI optimization
- Self-learning correction (PV + load bias)
- Decision engine (CHARGE / DISCHARGE / IDLE)

## 🧠 EMS V2 Architecture

- Pipeline-based processing
- Forecast → Simulation → Decision
- Learning feedback loop
- Coordinator-driven (HA-native)

## 📊 Sensors

- EMS ROI
- EMS Action
- EMS Learning (bias tracking)
- EMS PV Forecast
- EMS Load Forecast

## 🔧 Installation (HACS)

1. Add this repository as a custom repository in HACS
2. Install "EMS V1"
3. Restart Home Assistant
4. Add integration via Settings → Devices & Services

## ⚙️ Configuration

Requires:

- PV data (SolarEdge or other)
- Load data (P1 meter)
- Energy price source (EnergyZero, ANWB, etc.)

## 🚀 Roadmap

- Horizon optimization (24h planning)
- Battery control integration
- Advanced learning models
- Multi-day optimization

## 📍 Status

Production-ready (v2 pipeline active)
