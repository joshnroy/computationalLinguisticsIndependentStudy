import pynder

# Variables
FBTOKEN="CAAGm0PX4ZCpsBALZBaLLTXAFZAOEWRKqNIWezORuzKTtrvitC3RXxnYKpvlPJUa4DZBTisLgL36XgbEBJ3zfprP0a8bGhAI1OP3tnlODxO9gV0UMZCG3jBYFkHuGDPCYbTOCfWKyu1cJYh0f9bmi7SiVtKdlZBxOI069htLvZAcBvSTbun3yzikcK18X1YLS5sjbU3o1BfcW4E48idnOdpf"
FBID="100009426311666"
LAT = "42.312449"
LON = "-71.035905"

# Start the session
session = pynder.Session(FBID,FBTOKEN)
print session.profile
print session.matches()
print session.update_location(LAT, LON)
print session.nearby_users()
