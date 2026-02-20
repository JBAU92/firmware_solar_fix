
Meshtastic nRF52 Solar Recovery Fix ☀️🔋
This repository contains modified versions of the Meshtastic firmware specifically optimized for solar repeater nodes based on the nRF52840 architecture.

🚀 The Problem: The Solar "Deep Coma"
Many users of RAK4631 or XIAO nRF52 nodes suffer from the same issue: after several cloudy days, the node depletes its battery and enters a sleep state from which it never wakes up, even when the sun comes out again and the battery recharges. This forces physical trips to manually reset the device.

🛠️ Implemented Solution
I have audited and modified the power management flow to fix this behavior:

Smart FSM Management: The "Critical Battery" threshold has been redefined to 3.4V.

The node now enters deep sleep in a controlled manner before the voltage drops to levels that cause regulator instability.

Hardware Resurrection (LPCOMP): The low-power comparator of the nRF52 chip has been enabled and configured.

The hardware monitors the voltage and triggers an automatic reset (Wake-up) when it detects that the solar charge has raised the battery to safe levels (~3.7V).

📂 Downloads and Hardware
You can find the .uf2 binaries ready to flash in the Releases section:

RAK4631: Optimized for WisBlock.

XIAO nRF52840: Standard version and I2C version.

Pro Micro DIY: For custom implementations.

☕ Support
This fix is the result of several hours analyzing schematics and the Meshtastic source code to improve the resilience of our networks.
If this work has saved you a trip to the roof to reset a node:

👉 [Buy me a coffee  https://buy.stripe.com/4gM00l2Qp7V26Ye0UgbMQ00 ]

For technical consulting on professional Mesh network deployments or low-power audits, you can contact me privately.





<div align="center" markdown="1">

<img src=".github/meshtastic_logo.png" alt="Meshtastic Logo" width="80"/>
<h1>Meshtastic Firmware</h1>

![GitHub release downloads](https://img.shields.io/github/downloads/meshtastic/firmware/total)
[![CI](https://img.shields.io/github/actions/workflow/status/meshtastic/firmware/main_matrix.yml?branch=master&label=actions&logo=github&color=yellow)](https://github.com/meshtastic/firmware/actions/workflows/ci.yml)
[![CLA assistant](https://cla-assistant.io/readme/badge/meshtastic/firmware)](https://cla-assistant.io/meshtastic/firmware)
[![Fiscal Contributors](https://opencollective.com/meshtastic/tiers/badge.svg?label=Fiscal%20Contributors&color=deeppink)](https://opencollective.com/meshtastic/)
[![Vercel](https://img.shields.io/static/v1?label=Powered%20by&message=Vercel&style=flat&logo=vercel&color=000000)](https://vercel.com?utm_source=meshtastic&utm_campaign=oss)

<a href="https://trendshift.io/repositories/5524" target="_blank"><img src="https://trendshift.io/api/badge/repositories/5524" alt="meshtastic%2Ffirmware | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

</div>

</div>

<div align="center">
	<a href="https://meshtastic.org">Website</a>
	-
	<a href="https://meshtastic.org/docs/">Documentation</a>
</div>

## Overview

This repository contains the official device firmware for Meshtastic, an open-source LoRa mesh networking project designed for long-range, low-power communication without relying on internet or cellular infrastructure. The firmware supports various hardware platforms, including ESP32, nRF52, RP2040/RP2350, and Linux-based devices.

Meshtastic enables text messaging, location sharing, and telemetry over a decentralized mesh network, making it ideal for outdoor adventures, emergency preparedness, and remote operations.

### Get Started

- 🔧 **[Building Instructions](https://meshtastic.org/docs/development/firmware/build)** – Learn how to compile the firmware from source.
- ⚡ **[Flashing Instructions](https://meshtastic.org/docs/getting-started/flashing-firmware/)** – Install or update the firmware on your device.

Join our community and help improve Meshtastic! 🚀

## Stats

![Alt](https://repobeats.axiom.co/api/embed/8025e56c482ec63541593cc5bd322c19d5c0bdcf.svg "Repobeats analytics image")
