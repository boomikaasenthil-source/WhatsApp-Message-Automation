import pandas as pd
import pywhatkit
import time
from datetime import datetime

# Read Excel File
data = pd.read_excel("Contacts.xlsx", dtype={"Phone": str})

print("Contacts Loaded Successfully\n")

# Loop through each 
# contact
for index, row in data.iterrows():

    name = str(row["Name"])
    phone = str(row["Phone"]).strip()
    message = str(row["Message"])

    # Remove spaces
    phone = phone.replace(" ", "")

    # Remove .0 if Excel added it
    if phone.endswith(".0"):
        phone = phone[:-2]

    # Add +91 if not present
    if not phone.startswith("+"):
        if len(phone) == 10:
            phone = "+91" + phone
        elif phone.startswith("91") and len(phone) == 12:
            phone = "+" + phone

    print(f"Sending message to {name}")
    print(f"Phone : {phone}")
    print(f"Message : {message}")

    try:

        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=20,
            tab_close=True,
            close_time=3
        )

        print("Message Sent Successfully\n")

        with open("log.txt", "a") as file:
            file.write(
                f"{datetime.now()} | {name} | {phone} | Success\n"
            )

        time.sleep(5)

    except Exception as e:

        print("Error:", e)

        with open("log.txt", "a") as file:
            file.write(
                f"{datetime.now()} | {name} | {phone} | Failed | {e}\n"
            )

print("All Messages Processed Successfully")