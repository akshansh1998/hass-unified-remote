# Unified Remote Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![license](https://img.shields.io/github/license/akshansh1998/hass-unified-remote)](LICENSE)

A modernized Home Assistant integration that allows you to control your computer using [Unified Remote](https://www.unifiedremote.com/). In Simple Words, you will be able to control your Microsoft Windows Computer using Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=akshansh1998&repository=hass-unified-remote&category=integration)

<p align="center">
  <img src="https://github.com/user-attachments/assets/95b63be1-bb9e-4824-9378-7cb3fcf8818c" alt="Unified Remote HA Demo" />
</p>

## ✨ Features
* **UI Configuration:** Easy setup directly through the Home Assistant integrations page (no YAML required).
* **Dedicated Power Buttons:** Instantly puts Shutdown, Restart, Sleep, Hibernate, Lock, and Logoff buttons right on your dashboard.
* **Media Player Entity:** Standard media controls (Play, Pause, Next, Previous, Volume Up/Down/Mute).
* **Monitor Switch:** A simple toggle switch to turn your computer monitor on and off.
* **Connection Tracking:** A binary sensor that monitors the real-time connection status to your computer.

---

## ⚙️ Prerequisites (Setting up Unified Remote)

Before installing in Home Assistant, you need the [Unified Remote server](https://www.unifiedremote.com/download) running on your target computer. 

*(If you use Windows, make sure to enable the "Windows service (Experimental)" option during installation).*

**Configure the Server:**
1. Open the web management panel (usually `http://localhost:9510/web/` on your PC).
2. Go to **Settings > Network**. Ensure **"Enable web-based client"** is checked.
3. **Important:** Check **"Allow management from a different LAN computer"**. *(To avoid unauthorized access, it is highly recommended to set up a firewall rule on your PC that only allows access from your Home Assistant's IP address).*
4. Go to **Settings > Security**. Set Authentication to **"Do not require apps to enter a password before connecting."** *(Password auth is not currently supported).*
5. Go to **Settings > Advanced**. Ensure **"Enable driver on Windows"** is checked (Windows only).

---

## 📥 Installation

### Method 1: HACS (Recommended)
This integration is fully compatible with the Home Assistant Community Store (HACS).

1. Open HACS in your Home Assistant.
2. Click on **Integrations**.
3. Click the three dots (top right) and select **Custom repositories**.
4. Paste this repository URL: `https://github.com/akshansh1998/hass-unified-remote`
5. Select **Integration** as the category and click **Add**.
6. Search for "Unified Remote" in HACS, click **Download**, and then restart Home Assistant.

### Method 2: Manual
1. Download this repository as a ZIP file.
2. Extract the `custom_components/unified_remote` folder.
3. Copy the folder into your Home Assistant's `<config>/custom_components/` directory.
4. Restart Home Assistant.

---

## 🚀 Configuration

Configuration is now entirely UI-based!

1. In Home Assistant, go to **Settings > Devices & Services**.
2. Click **+ Add Integration** in the bottom right.
3. Search for **"Unified Remote"**.
4. Enter the **Host / IP Address** of your computer and an optional Friendly Name. Leave the port as `9510` unless you changed it in the server settings.
<img width="479" height="519" alt="Demo of Configuration menu" src="https://github.com/user-attachments/assets/f5e345e2-8e10-4e92-b8ea-3e095d86edab" />

6. Click **Submit**. 

Your device will instantly populate with your Power Buttons, Media Player, and Monitor Switch!

---

## 🛠️ Advanced Usage / Service Calls

If you want to map custom remotes (like opening specific apps or triggering custom keyboard shortcuts), you can edit the `remotes.yml` file and trigger them using Home Assistant service calls:

```yaml
action: unified_remote.call
data:
  target: "My PC"
  remote: "prime_video"
  action: "launch"
```

## 🤝 Contribute
Contributions, bug reports, and feature requests are always welcome! Feel free to open an issue or submit a pull request.
