from dotenv import load_dotenv
import os

load_dotenv()

keys = {
    "OCEAN_API_KEY": os.getenv("OCEAN_API_KEY"),
    "PROSPEO_API_KEY": os.getenv("PROSPEO_API_KEY"),
    "EAZYREACH_API_KEY": os.getenv("EAZYREACH_API_KEY"),
    "BREVO_API_KEY": os.getenv("BREVO_API_KEY"),
    "SENDER_EMAIL": os.getenv("SENDER_EMAIL"),
    "DRY_RUN": os.getenv("DRY_RUN"),
}

for key, value in keys.items():
    if value:
        print(f"{key}: Loaded ✅")
    else:
        print(f"{key}: Missing ❌")