from win10toast import ToastNotifier
import threading
import Tkinter as tk

def send_notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=5)

def show_task_window():
    root = tk.Tk()
    root.title("Task Window")

    # Replace the following label text with your desired task details
    task_label = tk.Label(root, text="Your task goes here.")
    task_label.pack(padx=20, pady=20)

    root.mainloop()

def timer_callback():
    # Replace the following values with your desired timer duration and notification details
    timer_duration = 1  # 60 seconds (1 minute)
    notification_title = "Timer Complete!"
    notification_message = "Your timer has finished!"

    # Wait for the specified duration
    timer = threading.Timer(timer_duration, send_notification, args=(notification_title, notification_message))
    timer.start()

    # Show the task window after the timer is done
    show_task_window()

if __name__ == "__main__":
    # Start the timer in the background
    timer_callback()
    # You can add more code here to continue running your application in the background
    # For example, you might have a loop that performs other tasks while the timer runs.
    # For this example, the script will exit after displaying the notification and task window.
