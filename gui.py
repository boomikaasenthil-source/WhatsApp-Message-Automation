import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import pywhatkit
import time
from datetime import datetime

# -----------------------------
# Browse Excel File
# -----------------------------
excel_file = ""

def browse_file():
    global excel_file

    excel_file = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx")]
    )

    if excel_file:
        status.config(text="Excel Selected", fg="green")
    else:
        status.config(text="No File Selected", fg="red")


# -----------------------------
# Send Messages
# -----------------------------
def send_messages():

    global excel_file

    if excel_file == "":
        messagebox.showerror("Error", "Please Select Excel File")
        return

    try:

        data = pd.read_excel(excel_file, dtype={"Phone": str})

        custom_message = message_box.get("1.0", tk.END).strip()

        for index, row in data.iterrows():

            name = str(row["Name"])
            phone = str(row["Phone"]).strip()

            # If message box is empty use Excel message
            if custom_message == "":
                message = str(row["Message"])
            else:
                message = custom_message

            phone = phone.replace(" ", "")

            if phone.endswith(".0"):
                phone = phone[:-2]

            if not phone.startswith("+"):
                if len(phone) == 10:
                    phone = "+91" + phone
                elif phone.startswith("91"):
                    phone = "+" + phone

            status.config(text=f"Sending to {name}...")
            window.update()

            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone,
                message=message,
                wait_time=20,
                tab_close=True,
                close_time=3
            )

            with open("log.txt", "a") as file:
                file.write(
                    f"{datetime.now()} | {name} | {phone} | Success\n"
                )

            time.sleep(5)

        status.config(
            text="All Messages Sent Successfully",
            fg="green"
        )

        messagebox.showinfo(
            "Success",
            "All Messages Sent Successfully"
        )

    except Exception as e:

        with open("log.txt", "a") as file:
            file.write(
                f"{datetime.now()} | Failed | {e}\n"
            )

        messagebox.showerror("Error", str(e))


# -----------------------------
# GUI
# -----------------------------
window = tk.Tk()

window.title("WhatsApp Message Automation")

window.geometry("500x500")

window.resizable(False, False)

title = tk.Label(
    window,
    text="WhatsApp Message Automation",
    font=("Arial",18,"bold")
)

title.pack(pady=20)

browse_button = tk.Button(
    window,
    text="Browse Excel",
    width=25,
    command=browse_file
)

browse_button.pack()

status = tk.Label(
    window,
    text="No File Selected",
    fg="red"
)

status.pack(pady=10)

message_label = tk.Label(
    window,
    text="Message (Optional)"
)

message_label.pack()

message_box = tk.Text(
    window,
    width=45,
    height=6
)

message_box.pack()

send_button = tk.Button(
    window,
    text="Send WhatsApp Messages",
    bg="green",
    fg="white",
    width=25,
    command=send_messages
)

send_button.pack(pady=20)

window.mainloop()