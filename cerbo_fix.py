# This code is for remotely fixing URL & bluetooth issue of Cerbo GX. Internet access is required for Cerbo to apply the change.
# Updated 27 June 2025

import ssl
import json
import paho.mqtt.client as mqtt
import sys

# Read VRM ID from the command line

if len(sys.argv) == 3:
    print("\n----------")
    print("\nVRM PORTAL ID RECEIVED:", sys.argv[1])
    print("\nVRM ACCOUNT:", sys.argv[2])
    print("\n----------")
else:
    sys.exit("\nVRM PORTAL ID WAS NOT PROVIDED. GOOD BYE!")

# === DEVICE INFO ===
VRM_PORTAL_ID = sys.argv[1]
VRM_ACCOUNT = sys.argv[2]
EMAIL = ""
PASSWORD = ""
# ====================

if VRM_ACCOUNT == "vrm1":
    EMAIL = "vrm1@arizon.com.au"
    PASSWORD = "H8&jmuP~c(09"
    print("\nLogged in to:", EMAIL)
    print("\n")
else:
    EMAIL = "vrm2@arizon.com.au"
    PASSWORD = "£#4dJ6+aC:R0"
    print("\nLogged in to:", EMAIL)
    print("\n")



def get_broker(systemid):
    return f"mqtt{sum(ord(c) for c in systemid) % 128}.victronenergy.com"


broker_url = get_broker(VRM_PORTAL_ID)


# Topics and payloads
fixes = {
    f"W/{VRM_PORTAL_ID}/settings/0/Settings/Vrmlogger/Url": {"value": ""},
    f"W/{VRM_PORTAL_ID}/settings/0/Settings/Services/Bluetooth": {"value": 1}
}


def on_connect(client, userdata, flags, rc):
    print(f"[Connected] MQTT code: {rc}")
    for topic, payload in fixes.items():
        print(f"[Sending] Topic: {topic} → {payload}")
        client.publish(topic, json.dumps(payload))
    client.disconnect()


client = mqtt.Client()
client.username_pw_set(EMAIL, PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)
client.on_connect = on_connect


print(f"[Connecting] {broker_url} on port 443...")
client.connect(broker_url, 443)
client.loop_forever()
