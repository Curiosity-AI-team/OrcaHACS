

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

Would you like further instructions for setting up a virtual machine for Home Assistant OS, or do you need help with specific configurations?