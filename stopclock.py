import tkinter as tk
from datetime import datetime
from pynput import mouse
import threading
import random
import winsound
import win32gui

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd)

class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto-Reset Stopwatch")

        
        self.clock_label = tk.Label(root, text="", font=("Arial", 18))
        self.clock_label.pack(pady=10)

         
        self.elapsed_label = tk.Label(root, text="", font=("Arial", 18))
        self.elapsed_label.pack(pady=10)

        
        self.title_label = tk.Label(root, text="Time since last click", font=("Arial", 18))
        self.title_label.pack(pady=10)

       
        self.stopwatch_label = tk.Label(root, text="0:00", font=("Arial", 40), fg="red")
        self.stopwatch_label.pack(pady=10)

        
        self.consulate_label = tk.Label(root, text="SELECT CONSULATE NOW", font=("Arial", 20), fg="blue")
        
        self.consulate_label.place_forget()

        self.seconds = 0
        self.elapsed_seconds = 0
        self.running = True
        self.showing_consulate = False

        self.consulate_trigger_second = random.randint(121, 299)


        self.update_stopwatch()
        self.update_clock()
        self.update_elapsed()
        self.start_mouse_listener()

    def update_stopwatch(self):
        if self.running:
            self.seconds += 1

            
            mins = self.seconds // 60
            secs = self.seconds % 60
            self.stopwatch_label.config(text=f"{mins}:{secs:02}")

            
            if self.seconds < 120 or self.seconds > 300:
                self.stopwatch_label.config(fg="red")
            else:
                self.stopwatch_label.config(fg="green")
                self.maybe_show_consulate_prompt()

        self.root.after(1000, self.update_stopwatch)

    def update_elapsed(self):
        if self.running:
            self.elapsed_seconds += 1

            
            hours = self.elapsed_seconds // 3600
            mins = (self.elapsed_seconds % 3600) // 60
            secs = self.elapsed_seconds % 60
            self.elapsed_label.config(text=f"Time elapsed: {hours:02}:{mins:02}:{secs:02}")

            
        self.root.after(1000, self.update_elapsed)

    def maybe_show_consulate_prompt(self):
    
        if (
            not self.showing_consulate
            and self.consulate_trigger_second is not None
            and self.seconds in (self.consulate_trigger_second, self.consulate_trigger_second + 1)
        ):
            self.showing_consulate = True
            self.consulate_label.place(relx=0.5, rely=0.85, anchor="center")
            threading.Thread(target=self.play_alert_sound, daemon=True).start()
            self.root.after(15000, self.hide_consulate_prompt)

    
    def play_alert_sound(self):
        end_time = datetime.now().timestamp() + 15
        while datetime.now().timestamp() < end_time:
            winsound.Beep(1000, 500)

    def hide_consulate_prompt(self):
        self.consulate_label.place_forget()
        self.showing_consulate = False

    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_clock)

    def reset_stopwatch(self):
        self.seconds = 0
        self.stopwatch_label.config(fg="red")
        self.consulate_label.place_forget()
        self.showing_consulate = False

        
        self.consulate_trigger_second = random.randint(121, 299)


    def on_click(self, x, y, button, pressed):
        if pressed:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)

            if "Chrome" in window_title and "Chrome_WidgetWin_1" in class_name:
                
                rect = win32gui.GetWindowRect(hwnd)
                left, top, right, bottom = rect

               
                if left <= x <= right and top <= y <= bottom:
                    self.reset_stopwatch()



    def start_mouse_listener(self):
        listener = mouse.Listener(on_click=self.on_click)
        listener.daemon = True
        listener.start()


root = tk.Tk()
root.geometry("400x400")
app = StopwatchApp(root)
root.mainloop()
