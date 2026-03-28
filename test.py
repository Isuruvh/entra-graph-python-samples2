from dotenv import load_dotenv
import os

load_dotenv()

print("TENANT_ID:", os.getenv("TENANT_ID"))
print("CLIENT_ID:", os.getenv("CLIENT_ID"))
print("CLIENT_SECRET:", os.getenv("CLIENT_SECRET"))
