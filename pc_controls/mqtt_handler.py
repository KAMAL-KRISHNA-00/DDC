import paho.mqtt.client as mqtt
import time


class MQTTHandler:
    def __init__(self, state_machine, broker_host="127.0.0.1", broker_port=1883):
        self.state_machine = state_machine
        self.broker_host = broker_host
        self.broker_port = broker_port

        self.client = mqtt.Client(client_id="DeepWorkController", clean_session=True)

        # ---- Last Will ----
        self.client.will_set("room/status", "DISCONNECTED", retain=True)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        self.connected = False

    # ---------- CONNECTION ----------

    def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port)
            self.client.loop_start()
        except Exception as e:
            print(f"[MQTT] Initial connection failed: {e}")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] Connected to broker")
            self.connected = True
            self._subscribe_topics()
            self.publish_status()  # Publish immediately on connect
        else:
            print(f"[MQTT] Connection error code: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        print("[MQTT] Disconnected. Reconnecting...")
        self.connected = False

        # Auto-reconnect loop
        while not self.connected:
            try:
                time.sleep(3)
                self.client.reconnect()
            except:
                continue

    def _subscribe_topics(self):
        self.client.subscribe("door/event")
        self.client.subscribe("door/emergency")
        print("[MQTT] Subscribed to door topics")

    # ---------- PUBLISH ----------

    def publish_status(self):
        if not self.connected:
            return

        state = self.state_machine.get_state()
        self.client.publish("room/status", state, retain=True)

    # ---------- MESSAGE HANDLING ----------

    def _on_message(self, client, userdata, msg):
        message = msg.payload.decode()

        if msg.topic == "door/event":
            if message == "DOOR_INTERACTION":
                if self.state_machine.door_interrupt():
                    print("[MQTT] Door interrupt processed")

        elif msg.topic == "door/emergency":
            if message == "REQUEST":
                if self.state_machine.emergency_request():
                    print("[MQTT] Emergency request processed")