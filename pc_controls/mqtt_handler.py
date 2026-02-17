import paho.mqtt.client as mqtt


class MQTTHandler:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.client = mqtt.Client()
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect("localhost", 1883)
        self.client.subscribe("door/event")
        self.client.subscribe("door/emergency")
        self.client.loop_start()

    def publish_status(self):
        state = self.state_machine.get_state()
        self.client.publish("room/status", state)

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()

        # Normal door interrupt
        if msg.topic == "door/event":
            if message == "DOOR_INTERACTION":
                if self.state_machine.door_interrupt():
                    print("Door interrupt detected.")

        # Emergency button
        if msg.topic == "door/emergency":
            if message == "REQUEST":
                if self.state_machine.emergency_request():
                    print("Emergency request received.")
