

### Step-by-Step Guide to Install Home Assistant on WSL2 (Ubuntu 22.04)

Here’s a complete guide for installing Home Assistant Core on WSL2 using only the Ubuntu 22.04 terminal.

---

### Step 1: Update and Upgrade the System
```bash
sudo apt update && sudo apt upgrade -y
```

---

### Step 2: Install Required Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv libffi-dev libssl-dev zlib1g-dev autoconf build-essential
```

---

### Step 3: Create a Python Virtual Environment
1. Navigate to a directory where you want to install Home Assistant:
   ```bash
   mkdir ~/homeassistant && cd ~/homeassistant
   ```
2. Create the virtual environment:
   ```bash
   python3 -m venv .
   ```
3. Activate the virtual environment:
   ```bash
   source bin/activate
   ```

---

### Step 4: Install Home Assistant Core
```bash
pip install wheel
pip install homeassistant
```

---

### Step 5: Start Home Assistant
```bash
hass
```

After a few moments, Home Assistant will be running. You can access it by opening your browser and navigating to:
```
http://localhost:8123
```

---

### Step 6: Configure Auto-Start (Optional)
To ensure Home Assistant starts automatically when you open your WSL terminal, you can add a simple script to your `.bashrc` or `.zshrc` file.

1. Open the `.bashrc` file for editing:
   ```bash
   nano ~/.bashrc
   ```
2. Add the following line at the end:
   ```bash
   (cd ~/homeassistant && source bin/activate && hass &) >/dev/null 2>&1
   ```
3. Save and close the file (`CTRL+O`, `CTRL+X`).
4. Reload `.bashrc`:
   ```bash
   source ~/.bashrc
   ```

---

### Step 7: Managing Home Assistant
- **Stop Home Assistant**: Press `CTRL+C` in the terminal running Home Assistant.
- **Restart Home Assistant**:
  ```bash
  source ~/homeassistant/bin/activate
  hass
  ```

---

### Notes:
- This setup runs **Home Assistant Core**, which does not include the add-on store or supervisor.
- To get the full experience (including add-ons and supervisor), you'd need to run Home Assistant OS in a virtual machine or on a dedicated device like a Raspberry Pi.

---

### Step-by-Step Guide to Install HACS on Home Assistant Core (WSL2 Ubuntu 22.04 Terminal Only)

HACS (Home Assistant Community Store) allows you to easily manage custom integrations and plugins in Home Assistant. Below is a step-by-step guide to install HACS on your Home Assistant Core setup in WSL2.

---

### **Step 1: Activate the Home Assistant Virtual Environment**

Since you're using Home Assistant Core in a virtual environment, you first need to activate it:

```bash
cd ~/homeassistant
source bin/activate
```

---

### **Step 2: Install Git**

HACS requires Git to download custom components.

```bash
sudo apt install git -y
```

---

### **Step 3: Navigate to Home Assistant Configuration Directory**

Assuming that Home Assistant is running in your home directory and the configuration directory is `~/.homeassistant`:

```bash
cd ~/.homeassistant
```

---

### **Step 4: Download and Install HACS**

Use Git to clone the HACS repository:

```bash
git clone https://github.com/hacs/integration.git custom_components/hacs
```

This command will create a `custom_components/hacs` folder in your Home Assistant configuration directory.

---

### **Step 5: Restart Home Assistant**

Now, restart Home Assistant to recognize HACS:

```bash
hass
```

Wait for Home Assistant to start up.

---

### **Step 6: Add HACS to `configuration.yaml`**

1. Open the `configuration.yaml` file:
   ```bash
   nano ~/.homeassistant/configuration.yaml
   ```
2. Add the following under your existing configuration:
   ```yaml
   hacs:
     token: YOUR_GITHUB_PERSONAL_ACCESS_TOKEN
     sidepanel_title: HACS
     sidepanel_icon: "mdi:tools"
   ```

   - **`token`**: You need a GitHub Personal Access Token (PAT) for HACS to work. Follow these steps to generate one:
     1. Go to [GitHub Personal Access Token generation page](https://github.com/settings/tokens).
     2. Click "Generate new token."
     3. Give it a name (e.g., `HACS Token`) and select `repo` scope.
     4. Generate the token and copy it.
     5. Paste the token in the `configuration.yaml` file as shown above.

3. Save the file (`CTRL+O`, `Enter`, `CTRL+X`).

---

### **Step 7: Restart Home Assistant Again**

After adding HACS to the `configuration.yaml` file, restart Home Assistant:

```bash
hass
```

---

### **Step 8: Access HACS in the Home Assistant UI**

1. Open your web browser and go to:
   ```
   http://localhost:8123
   ```
2. Go to the **"Configuration"** section and then to **"Integrations."**
3. Click the “+” button to add a new integration and search for “HACS.”
4. Follow the on-screen instructions to complete the setup.

---

### **Step 9: Start Using HACS**

Once HACS is installed, you can use it to manage and install custom integrations and plugins directly from the Home Assistant web UI.

---

### **Troubleshooting**

- If HACS does not appear in the UI, check the logs for errors:
  ```bash
  cat ~/.homeassistant/home-assistant.log
  ```

Would you like assistance with creating the GitHub token or further customization of your Home Assistant setup?