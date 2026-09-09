# 📻 Hassan Global Radio (CLI Player)

A lightweight, cross-platform, and fully open-source terminal-based internet radio player. Built for cybersecurity enthusiasts, it features a sleek Kali-inspired interface and accesses over 40,000 live radio stations globally via the Radio Browser API.

## ✨ Features
- **Global Open-Source DB:** Search by name, genre, or country using the Radio Browser API.
- **Cyberpunk UI:** Built with `rich` for a beautiful, hacker-style terminal dashboard.
- **Cross-Platform:** Works seamlessly on Kali Linux, Windows, and macOS.
- **In-Terminal Controls:** Volume adjustment, play, stop, and dynamic search directly from the command line prompt.

## 🛠️ Prerequisites
- **Python 3.x**
- **VLC Media Player:** The python-vlc wrapper relies on the host system's VLC engine.
  - *Kali / Ubuntu / Debian:* `sudo apt install vlc`
  - *Windows / Mac:* Download and install from [VideoLAN](https://www.videolan.org/)

## 🚀 Installation & Setup 

*(Note for Kali Linux users: This setup uses a Virtual Environment to comply with PEP 668 environment restrictions.)*

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/waqarhassanh78/global-radio.git](https://github.com/waqarhassanh78/global-radio.git)
   cd global-radio
Set up the virtual environment:

```Bash
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
```
Install the required Python packages:

```Bash
pip install python-vlc rich requests
```
🕹️ Usage
Whenever you want to run the radio, ensure your virtual environment is active, then execute the script:

```Bash
source venv/bin/activate
python3 radio.py
```
📜 Available Commands:
search <keyword> : Scans the global database (e.g., search lofi, search rock, search pakistan).

play <id> : Plays a station based on the ID from your recent search results.

vol <0-100> : Adjusts the playback volume (e.g., vol 50).

stop : Stops the current audio stream.

exit : Closes the application securely.

Developed by Waqar Hassan | BS Cyber Security | 
