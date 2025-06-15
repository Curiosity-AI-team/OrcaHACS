# OrcaHACS

**Home Assistant to OrcaVA Integration**

OrcaHACS is a custom integration that bridges Home Assistant with the OrcaVA service, allowing you to integrate the OrcaVA system into your Home Assistant environment seamlessly. It enables communication between Home Assistant and OrcaVA using FastAPI, HTTP requests, and other backend services, making it possible to manage OrcaVA's data and control its actions directly from Home Assistant.

---

## Installation

> Home Assistant version requirement:
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

## 1. Install via HACS

1. Install **HACS Add-on Manager** in your Home Assistant install if you haven’t already.
2. In Home Assistant go to **HACS → Integrations → ⋮ (top right) → Custom repositories**.
3. Add the repository URL and select **Integration**:

   * **Repository:** `https://github.com/Curiosity-AI-team/OrcaHACS`
   * **Category:** Integration
4. Click **Add** and then **Reload** or **Restart Home Assistant**.

---

## 2. Add the Integration

1. Go to **Settings → Devices & Services → + Add Integration**.
2. Search for **Orca Bridge** and click **Submit** on the default form (no additional fields required).
3. After a moment, you should see **Orca Bridge** in your integrations list, and the `sensor.orca_dashboard` will appear in **Developer Tools → States**.

---

## 3. Template Sensor for Last Reply

You can create **sensor.orca\_last\_reply** entirely from the Home Assistant UI—no YAML needed. Here’s how:

---

1. In Home Assistant, go to **Settings → Devices & Services**.
2. Click the **Helpers** tab.
3. Click **+ Create Helper**.
4. Select **Template**.
5. Click **Next**.
6. Configure the Template
  * **Name:** `Orca Last Reply`
  * **Icon (optional):** choose something like `mdi:message-reply`
  * **Entity ID:** it will auto-populate as `sensor.orca_last_reply`

7. In the **Template** box, paste:

```jinja
{% set r = state_attr('sensor.orca_dashboard','last_response') %}
{{ r[0] if (r is defined and r) else '' }}
```
8. Click **Create**.
9. Verify the New Sensor
- Go to **Developer Tools → States**.
- In the **Entity** filter type `sensor.orca_last_reply`.
- You should see its **State** change to the most recent bot reply after you click **Send**.

---

## 4 Add a text‐box + button in Lovelace

**Create** a helper text input for your outgoing message:
Go to **Settings → Devices & Services → Helpers → + Add helper → Text**
  * **Name:** Orca message
  * **Entity ID:** `input_text.orca_message_input`

---

## 5. Create a Send-Message Script (No YAML Edit Required)

You can configure a script entirely via the UI to send text from a Lovelace helper to your Rasa webhook:

1. Go to **Settings → Automations & Scenes → Scripts → + Add Script**.
2. Choose **Start with empty script** and name it **Orca Bridge Send Message**.
3. Fill the **Entity ID** with **orca_bridge_send_message**
4. Under **Sequence**, click **Add action → Call service**:

   * **service:** `orca_bridge.send_message`
   * **data:**

     ```yaml
     text: "{{ states('input_text.orca_message_input') }}"
     ```
5. Click **Save**. A new script entity (e.g. `script.orca_bridge_send_message`) will be created.

---

## 6. Configure Lovelace Dashboard

Add the following to your **Lovelace** UI (via **Edit Dashboard → Raw Configuration Editor** or your `ui-lovelace.yaml`):

```yaml
views:
  - title: Home
    cards:
      - type: entities
        title: Orca Bridge Chat
        show_header_toggle: false
        entities:
          # Display the current world name (sensor state)
          - entity: sensor.orca_dashboard
            name: World Name

          # Display the last bot reply (sensor attribute)
          - entity: sensor.orca_last_reply  # if you created the template sensor
            name: Last Bot Reply

          # Free-form text input helper
          - entity: input_text.orca_message_input
            name: Message to Send

          # Script row to send the message
          - entity: script.orca_bridge_send_message
            name: Send to Orca
```

Once saved, you’ll have a chat-like interface where you can type a message, click **Send to Orca**, and see the bot’s reply update in real time.

---

## 7. Advanced Configuration

If you need to change the dashboard endpoint, poll interval, webhook URL, or sender name:

1. Go to **Settings → Devices & Services → Orca Bridge**.
2. Click **Options**.
3. Update the:

   * **Dashboard URL** (default `http://127.0.0.1:4567/get_dashboard`)
   * **Poll Interval** (seconds)
   * **Webhook URL** (default `http://127.0.0.1:5005/webhooks/rest/webhook`)
   * **Sender** (default `homeassistant`)
4. Click **Submit**. The integration will reload with your new settings.

## (ALTERNATIVE). Advanced Configuration

You can manually add Send-Message Script and Templates by adding the following to your **configuration.yaml** and restart HA:

```yaml
template:
  - sensor:
      - name: "Orca Last Reply"
        state: >-
          {% set r = state_attr('sensor.orca_dashboard','last_response') %}
          {{ r[0] if (r is defined and r) else '' }}

script:
  orca_bridge_send_message:
    alias: "Orca Bridge Send Message"
    sequence:
      - service: orca_bridge.send_message
        data_template:
          text: "{{ states('input_text.orca_message_input') }}"
```

This will create `sensor.orca_last_reply` whose state is the first element of the `last_response` list.


---

## Troubleshooting

* **405 Method Not Allowed** when polling `/get_dashboard`: Make sure your external server endpoint supports **GET** (recommended) or update the integration to use `session.post()`.
* **No sensor appearing**: Verify HACS install, manifest `platforms: ["sensor"]`, and that you forwarded the sensor in `async_setup_entry`.
* **Service errors**: Check **Developer Tools → Logs** and enable debug logging for `custom_components.orca_bridge` in `configuration.yaml` under `logger:`.

---


## License

OrcaHACS is licensed under the [MIT License](https://opensource.org/licenses/MIT).
