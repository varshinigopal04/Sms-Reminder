import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from twilio.rest import Client
from tkcalendar import Calendar
from tkinter import ttk

# Twilio credentials
account_sid = 'AC9200c3e6c03f20b4096087f0e342bc3e'
auth_token = '5c90ff1117c094719b8442ecf5633875'
twilio_phone_number = '+16096421055'
client = Client(account_sid, auth_token)

class MedicineReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medicine Reminder App")

        # Variables to store prescription data
        self.medicine_var = tk.StringVar()
        self.times_var = tk.IntVar()
        self.time_of_day_var = tk.StringVar()  # Variable to store selected time of day options
        self.food_timing_var = tk.StringVar()  # Variable to store selected food timing options
        self.phone_var = tk.StringVar()  # Variable to store patient phone number
        self.country_code_var = tk.StringVar(value='+91')  # Default to India (+91)

        # GUI elements for prescription entry
        tk.Label(self.root, text="Medicine:").grid(row=0, column=0, padx=5, pady=5)
        self.medicine_entry = tk.Entry(self.root, textvariable=self.medicine_var)
        self.medicine_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Times per day:").grid(row=1, column=0, padx=5, pady=5)
        self.times_entry = tk.Entry(self.root, textvariable=self.times_var)
        self.times_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Time of Day:").grid(row=2, column=0, padx=5, pady=5)
        self.time_of_day_listbox = tk.Listbox(self.root, selectmode="multiple", exportselection=False)
        self.time_of_day_listbox.grid(row=2, column=1, padx=5, pady=5)
        time_of_day_options = ["Morning", "Afternoon", "Night"]
        for option in time_of_day_options:
            self.time_of_day_listbox.insert(tk.END, option)

        tk.Label(self.root, text="Food Timing:").grid(row=3, column=0, padx=5, pady=5)
        self.food_timing_listbox = tk.Listbox(self.root, selectmode="multiple", exportselection=False)
        self.food_timing_listbox.grid(row=3, column=1, padx=5, pady=5)
        food_timing_options = ["Before Food", "After Food"]
        for option in food_timing_options:
            self.food_timing_listbox.insert(tk.END, option)

        tk.Label(self.root, text="Patient Phone Number:").grid(row=4, column=0, padx=5, pady=5)
        self.country_code_menu = tk.OptionMenu(self.root, self.country_code_var, '+91', '+1')  # Dropdown menu for country code
        self.country_code_menu.grid(row=4, column=1, padx=5, pady=5)
        self.phone_entry = tk.Entry(self.root, textvariable=self.phone_var)
        self.phone_entry.grid(row=4, column=2, padx=5, pady=5)

        tk.Button(self.root, text="Save Prescription", command=self.save_prescription).grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # GUI elements for appointment registration
        tk.Label(self.root, text="Appointment Date:").grid(row=6, column=0, padx=5, pady=5)
        self.calendar = Calendar(self.root, selectmode="day", date_pattern='yyyy-mm-dd')
        self.calendar.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Appointment Time:").grid(row=7, column=0, padx=5, pady=5)
        self.hour_var = tk.StringVar()
        self.hour_var.set("08")
        self.minute_var = tk.StringVar()
        self.minute_var.set("00")
        self.time_picker = ttk.Frame(self.root)
        self.time_picker.grid(row=7, column=1, padx=5, pady=5)
        ttk.Label(self.time_picker, text="Hour:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(self.time_picker, textvariable=self.hour_var, values=[str(i).zfill(2) for i in range(24)]).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.time_picker, text="Minute:").grid(row=0, column=2, padx=5, pady=5)
        ttk.Combobox(self.time_picker, textvariable=self.minute_var, values=[str(i).zfill(2) for i in range(60)]).grid(row=0, column=3, padx=5, pady=5)

        tk.Button(self.root, text="Register Appointment", command=self.register_appointment).grid(row=8, column=0, columnspan=3, padx=5, pady=5)

        # Button to send medicine reminders
        tk.Button(self.root, text="Send Medicine Reminder", command=self.send_medicine_reminder).grid(row=9, column=0, columnspan=3, padx=5, pady=5)

    def save_prescription(self):
        medicine = self.medicine_var.get()
        times_per_day = self.times_var.get()

        # Save prescription data or perform necessary actions

        messagebox.showinfo("Prescription Saved", "Prescription saved successfully.")

    def send_medicine_reminder(self):
        patient_phone = self.country_code_var.get() + self.phone_var.get()  # Concatenate country code with phone number
        medicine = self.medicine_var.get()
        times_per_day = self.times_var.get()
        time_of_day_options = [self.time_of_day_listbox.get(idx) for idx in self.time_of_day_listbox.curselection()]
        food_timing_options = [self.food_timing_listbox.get(idx) for idx in self.food_timing_listbox.curselection()]

        for time_of_day in time_of_day_options:
            for food_timing in food_timing_options:
                for i in range(times_per_day):
                    reminder_time = self.calculate_reminder_time(time_of_day, i, food_timing)
                    if reminder_time > datetime.now():
                        if food_timing == "Before Food":
                            message = f"Hi! Don't forget to take your {medicine}. Reminder at: {reminder_time}. Take it before food."
                        else:
                            message = f"Hi! Don't forget to take your {medicine}. Reminder at: {reminder_time}. Take it after food."
                        send_sms(patient_phone, message)

    def calculate_reminder_time(self, time_of_day, iteration, food_timing):
    # Map time of day selections to specific times
        time_mappings = {"Morning": "08:00:00", "Afternoon": "02:30:00", "Night": "20:00:00"}

    # Get the selected time for the specific time of day
        specific_time = time_mappings.get(time_of_day)

    # Extract hour, minute, and second from the specific time
        hour, minute, second = map(int, specific_time.split(':'))

    # Adjust the reminder time based on the iteration
        reminder_time = datetime.now().replace(hour=hour, minute=minute, second=second) + timedelta(days=iteration)

    # Adjust the reminder time based on food timing
        if food_timing == "Before Food":
            reminder_time -= timedelta(minutes=30)  # Remind 30 minutes before food

        return reminder_time


    def register_appointment(self):
        selected_date = self.calendar.get_date()
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        appointment_time = datetime.strptime(selected_date, '%Y-%m-%d').replace(hour=hour, minute=minute)

        reminder_time = appointment_time - timedelta(hours=2)
        current_time = datetime.now()

        if current_time > reminder_time:
            messagebox.showwarning("Invalid Appointment Time", "Please choose a future appointment time.")
            return

        patient_phone = self.country_code_var.get() + self.phone_var.get()  # Concatenate country code with phone number
        message = f"Hi, your appointment is scheduled for {appointment_time}."
        send_sms(patient_phone, message)

        messagebox.showinfo("Appointment Registered", "Appointment registered successfully. Reminder will be sent 2 hours before.")

def send_sms(to, body):
    message = client.messages.create(
        to=to,
        from_=twilio_phone_number,
        body=body)

    print(f"Message sent to {to}: {message.sid}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineReminderApp(root)
    root.mainloop()
