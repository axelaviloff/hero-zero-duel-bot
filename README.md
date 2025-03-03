# Hero Zero Duel Bot

An automation bot for duels in **Hero Zero**, using `pyautogui` and `tkinter`. This bot is useful for earning points in the HeroCon duel event. It automates the duel process, uses image recognition to locate buttons on the screen, and has a simple and intuitive GUI. The bot allows configurable delay between actions for better control.


## 📌 Requirements

Make sure you have Python installed. Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

## ⚙️ Game Settings

To ensure the bot works correctly, configure the game as follows:

- The game must be set to Portuguese.

- Go to Settings -> General, and enable "Pegar recompensas diretamente".

- Go to Settings -> Combates, and disable "Mostrar lutas de duelo".

## ▶️ Usage

Run the script using:

```sh
python main.py
```

Then, configure the **initial ranking**, **delay**, and **duel interval** in the GUI before starting.

## 🛠 Troubleshooting

- If the bot does not detect buttons, check if the images and their resolution are correct.
- Adjust the confidence level in `pyautogui.locateCenterOnScreen` if necessary.

## 📜 License

This project is open-source under the MIT License.

---

Feel free to contribute and improve the bot! 🤖🔥

