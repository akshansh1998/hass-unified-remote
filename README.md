# Unified Remote Integration for HASS

> **🚧 REVIVAL PROJECT 🚧**
> This repository is actively being revived and modernized to support the latest Home Assistant standards (including UI setup, async operations, and more). If you are interested in contributing, testing, or suggesting features, **collaboration is completely open and welcome!** Please feel free to open issues or pull requests.

> This is a Home Assistant integration that allows you to control your computer by using [Unified Remote](https://www.unifiedremote.com/)

[![license](https://img.shields.io/github/license/DaviPtrs/hass-unified-remote)](License)

<p align="center">
  <img width="1073" height="908" alt="image" src="https://github.com/user-attachments/assets/95b63be1-bb9e-4824-9378-7cb3fcf8818c" />
</p>


## Documentation guide

- [Unified Remote Integration for HASS](#unified-remote-integration-for-hass)
  - [Documentation guide](#documentation-guide)
  - [Installation](#installation)
    - [Unified Remote](#unified-remote)
    - [Home Assistant](#home-assistant)
  - [Getting Started](#getting-started)
  - [How to use](#how-to-use)
  - [Contribute](#contribute)
  - [Submit Feedback](#submit-feedback)

## Installation

### Unified Remote

Just download [Unified Remote server](https://www.unifiedremote.com/download) for your computer and follow the installation steps provided on the Unified Remote web page.

**If you use Windows, make sure to allow the "Windows service (Experimental)" option on installation.**

#### Setting up

We need to set some options to make this integration work properly.
1. Go to the web management panel (usually `http://localhost:9510/web/`).
2. In the left corner, click on **Settings**, then click on **Network**. 
3. Make sure that **"Enable web-based client (http://localhost:9510/client)"** is allowed.
4. **Important**: You must allow **"Allow management from a different LAN computer"**. To avoid unauthorized access, set up a firewall rule on your host machine that only allows access from your Home Assistant's private IP address.
5. In the **Security** section, change Authentication to **"Do not require apps to enter a password before connecting."** (The integration currently does not support password auth).
6. If you're using Windows, click on the **Advanced** tab, and ensure **Enable driver on Windows** is enabled.

### Home Assistant

*(Note: We are currently working on HACS support and UI setup. For now, manual installation is supported.)*

1. Clone this repository or download the ZIP.
2. Copy the **`custom_components/unified_remote`** folder to your **`<home-assistant-config-path>/custom_components`** directory.
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration** and search for **Unified Remote**.
*(Alternatively, you can still use `configuration.yaml` as per older versions, but UI setup is recommended).*

## Getting Started & How to Use
*(Documentation for remotes.yml and service calls remains the same as previous versions...)*

## Contribute
Contributions are always welcome! Since this is a revived project, we are actively looking for testers and developers. Be free to open an issue telling your experience, suggesting new features, or asking questions.
