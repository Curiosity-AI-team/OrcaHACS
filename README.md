# OrcaHACS

**Home Assistant to OrcaVA Integration**

OrcaHACS is a custom integration that bridges Home Assistant with the OrcaVA service, allowing you to integrate the OrcaVA system into your Home Assistant environment seamlessly. It enables communication between Home Assistant and OrcaVA using FastAPI, HTTP requests, and other backend services, making it possible to manage OrcaVA's data and control its actions directly from Home Assistant.

---

## Installation

> Home Assistant version requirement:
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

### Method 1: Git clone from GitHub

```bash
cd config
git clone https://github.com/Curiosity-AI-team/OrcaHACS.git
cd OrcaHACS
./install.sh /config
```

We recommend this installation method, for it is convenient to switch to a tag when updating `orca_bridge` to a certain version.

For example, update to version v1.0.0

```bash
cd config/orca_bridge
git fetch
git checkout v1.0.0
./install.sh /config
```

### Method 2: [HACS](https://hacs.xyz/)

HACS > Overflow Menu > Custom repositories > Repository: https://github.com/Curiosity-AI-team/OrcaHACS.git & Category or Type: Integration > ADD > OrcaVA Integration in New or Available for download section of HACS > DOWNLOAD

> OrcaVA Integration has not been added to the HACS store as a default yet. It's coming soon.

### Method 3: Manually installation via [Samba](https://github.com/home-assistant/addons/tree/master/samba) / [FTPS](https://github.com/hassio-addons/addon-ftp)

Download and copy `custom_components/orca_bridge` folder to `config/custom_components` folder in your Home Assistant.

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
