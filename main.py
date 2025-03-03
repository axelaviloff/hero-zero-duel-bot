import pyautogui
import tkinter as tk
import time
import logging
from config import IMAGES
import threading

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', 
    level=logging.INFO, 
    datefmt='%Y-%m-%d %H:%M:%S'
)

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2

running = False

def find_image(images):
    for image_path in images:
        position = pyautogui.locateCenterOnScreen(image_path, grayscale=True, confidence=0.8)
        if position:
            return position
    return None

def move_and_click(images, clicks=1, duration=0.5, retries=3):
    for attempt in range(retries):
        try:
            position = find_image(images)
            if position:
                pyautogui.moveTo(position, duration=duration)
                time.sleep(1)
                for _ in range(clicks):
                    pyautogui.click()
                return True
            logging.warning(f"Attempt {attempt+1}/{retries}: Could not find {images}.")
            time.sleep(1) 
        except Exception as e:
            logging.warning(f"Error trying to locate {images}: {e}")
            time.sleep(1)
    return False

def move_to_center():
    pyautogui.moveTo(CENTER_X, CENTER_Y)

def update_waiting_time(label, remaining_time):
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    label.config(text=f"Waiting {minutes:02}:{seconds:02} for the next duel.")
    label.update_idletasks()

def run_script():
    global time_remaining_label, running
    LOOP = 1
    ranking_initial = int(entry_ranking.get())
    delay = int(entry_delay.get())
    waiting_cycle = int(entry_waiting_cycle.get())

    time_remaining_label.config(text="Running...") 
    time_remaining_label.update_idletasks() 

    running = True

    try:
        while running:
            print("\n")
            logging.info(f"Loop {LOOP}")

            if move_and_click(IMAGES["ranking_button"]):
                logging.info("Accessing ranking screen.")
                time.sleep(delay)

            if move_and_click(IMAGES["ranking_no_result_ok_button"], retries=1):
                logging.info("Confirming no ranking results.")
                time.sleep(delay)

            if move_and_click(IMAGES["search_input"]):
                logging.info(f"Entering ranking position: {ranking_initial}")
                pyautogui.write(str(ranking_initial))
                ranking_initial += 1
                move_to_center()
                time.sleep(delay)

            if move_and_click(IMAGES["search_button"]):
                logging.info("Searching for opponent.")
                time.sleep(delay)

            if move_and_click(IMAGES["show_hero_button"]):
                logging.info("Displaying opponent hero details.")
                time.sleep(2)

            if move_and_click(IMAGES["attack_ready_button"]):
                logging.info("Starting duel against opponent.")
                time.sleep(delay)

            if move_and_click(IMAGES["ok_button"], retries=1):
                logging.info("Collecting duel reward.")
                time.sleep(delay)
            
            if move_and_click(IMAGES["pick_reward_button"]):
                logging.info("Collecting mission reward.")
                time.sleep(delay)
            
            if move_and_click(IMAGES["discount_later_button"], retries=1):
                logging.info("Postponing reward discount.")
                time.sleep(delay)

            move_to_center()
            LOOP += 1
            
            # Countdown between duels
            for remaining_time in range(waiting_cycle, 0, -1):
                if not running:
                    logging.info("Execution stopped by user.")
                    return
                update_waiting_time(time_remaining_label, remaining_time)  
                time.sleep(1)
            
            time_remaining_label.config(text="Running...")
            time_remaining_label.update_idletasks()
            
    except KeyboardInterrupt:
        logging.info("Script stopped by user.")
        time_remaining_label.config(text="Stopped")
        

def stop_script():
    global running
    running = False  
    time_remaining_label.config(text="Execution stopped") 
    time_remaining_label.update_idletasks()


def start_script():
    global running
    if running:
        logging.info("The script is already running.")
        return
    script_thread = threading.Thread(target=run_script)
    script_thread.start()

window = tk.Tk()
window.title("Duel Automation")

frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

label_ranking = tk.Label(frame, text="Initial Ranking:")
label_ranking.grid(row=0, column=0, padx=5, pady=5)
entry_ranking = tk.Entry(frame)
entry_ranking.grid(row=0, column=1, padx=5, pady=5)

label_delay = tk.Label(frame, text="Delay between actions (seconds):")
label_delay.grid(row=1, column=0, padx=5, pady=5)
entry_delay = tk.Entry(frame)
entry_delay.grid(row=1, column=1, padx=5, pady=5)
entry_delay.insert(0, "1")

label_waiting_cycle = tk.Label(frame, text="Interval between duels (seconds):") 
label_waiting_cycle.grid(row=2, column=0, padx=5, pady=5)
entry_waiting_cycle = tk.Entry(frame)  
entry_waiting_cycle.grid(row=2, column=1, padx=5, pady=5)

time_remaining_label = tk.Label(frame, text="Waiting for execution.", font=("Arial", 10, "italic"))
time_remaining_label.grid(row=3, column=0, columnspan=2, pady=10)

btn_start = tk.Button(frame, text="Start Script", command=start_script)
btn_start.grid(row=4, column=0, padx=5, pady=5)

btn_stop = tk.Button(frame, text="Stop Execution", command=stop_script)
btn_stop.grid(row=4, column=1, padx=5, pady=5)

window.mainloop()
