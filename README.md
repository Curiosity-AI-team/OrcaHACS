# OrcaHACS

**Home Assistant to OrcaVA Integration**

OrcaHACS is a custom integration that bridges Home Assistant with the OrcaVA service, allowing you to integrate the OrcaVA system into your Home Assistant environment seamlessly. It enables communication between Home Assistant and OrcaVA using FastAPI, HTTP requests, and other backend services, making it possible to manage OrcaVA's data and control its actions directly from Home Assistant.

## Features

- Easy integration with Home Assistant.
- Provides REST API endpoints using FastAPI.
- Fetches and updates data asynchronously using `httpx`.
- Works seamlessly within Home Assistant's UI.

---

## Installation

### Prerequisites

- Home Assistant 2023.1 or later (works in virtual environments).
- **HACS** (Home Assistant Community Store) installed and set up.

### Installing OrcaHACS via HACS

To install the OrcaHACS integration in Home Assistant via HACS:

1. **Add the OrcaHACS repository to HACS**:

   - Open Home Assistant and go to **HACS** in the left sidebar.
   - Click the **+** button in the bottom-right corner to add a new repository.
   - Paste the following URL into the repository field:
   
     ```
     https://github.com/Curiosity-AI-team/OrcaHACS
     ```
   - Select **Integration** as the type of repository.

2. **Install the integration**:

   - After the repository is added, locate **OrcaVA Integration** in the HACS list.
   - Click **Install** to begin the installation.
   - Wait for HACS to finish the installation process.

3. **Restart Home Assistant**:

   - Once the installation is complete, restart Home Assistant to load the new integration.
   
     ```
     hass --restart
     ```

---

### Manual Installation (Without HACS)

If you prefer to install the integration manually:

1. Navigate to your Home Assistant configuration directory:
   ```bash
   cd ~/.homeassistant/custom_components
   ```

2. Clone the repository or download the files for the **orca_bridge** integration:
   ```bash
   git clone https://github.com/Curiosity-AI-team/OrcaHACS.git orca_bridge
   ```

3. Restart Home Assistant to load the integration:
   ```bash
   hass --restart
   ```

---

## Configuration

Once the integration is installed, follow these steps to configure OrcaHACS:

1. Open your **configuration.yaml** file and add the following:

   ```yaml
   orca_bridge:
   ```

2. Save the file and restart Home Assistant to activate the integration.

---

## Using OrcaHACS

Once installed and configured, you can use the **OrcaVA Integration** in Home Assistant:

- **FastAPI API**: OrcaHACS exposes an API that can be accessed at `http://<home_assistant_ip>:8000/api/status`.
- The integration will automatically set up entities that can be used within Home Assistant's Lovelace UI.

### Example Sensor in Lovelace UI

1. Go to the Home Assistant **Overview** page.
2. Add an **Entities card** to your Lovelace dashboard.
3. Select the `sensor.orca_status` or any other entities you want to display.
4. Save the card to show real-time data from OrcaVA.

---

## Requirements

- **Python Packages**: The integration requires the following Python packages:
  - `uvicorn`
  - `requests`
  - `fastapi`
  - `httpx`

These will be automatically installed via the integration's `manifest.json` file, but you can also manually install them using:

```bash
pip install uvicorn requests fastapi httpx
```

---

## Troubleshooting

### Common Issues

1. **API not accessible**: If you can’t access the API at `http://<home_assistant_ip>:8000/api/status`, ensure that Home Assistant and OrcaHACS are running correctly. Check the logs for any errors related to the integration.

2. **Integration not appearing in Home Assistant**: If you don’t see the integration after installation, try restarting Home Assistant and ensuring the `orca_bridge` entry exists in your **configuration.yaml** file.

---


## License

OrcaHACS is licensed under the [MIT License](https://opensource.org/licenses/MIT).
