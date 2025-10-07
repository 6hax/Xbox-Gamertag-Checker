## Xbox Gamertag Checker

Python utility that generates and checks random Xbox gamertags against `xboxgamertag.com`. When an available gamertag is found, it is printed to the console, appended to `Gamertags_Available.txt`, and optionally sent to a Discord webhook.

### Features
- **Random gamertag generation** with the first character always a letter.
- **Online availability check** against `xboxgamertag.com`.
- **File logging**: saves available gamertags to `Gamertags_Available.txt` (with an ASCII header).
- **Discord webhook (optional)**: sends an embed for each available gamertag.
- **CLI UI** with colors and an animated banner.

### Requirements
- Python 3.9+ (recommended)
- Windows (optimized; sets console title and size). Works on other OSes, but without console adjustments.

### Installation
1) Clone or download this repository.
2) Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration (optional Discord webhook)
Edit `config.json` and set `webhookUrl` to your Discord webhook URL. Leave it empty to disable sending.

```json
{
    "webhookUrl": "https://discord.com/api/webhooks/YOUR_WEBHOOK"
}
```

Notes:
- The embed uses a fixed username and avatar in the payload. Customize inside `checker.py` in the `send_to_webhook` function if desired.
- Requests to the webhook use a 5s timeout; failures are ignored silently.

### Usage
Run the main script:

```bash
python checker.py
```

Then enter the desired gamertag length (integer) when prompted. The program will:
- Generate random gamertags of that length.
- Perform a GET request to `https://xboxgamertag.com/search/<gamertag>`.
- Consider it available when the response contains the text "Gamertag doesn't exist".
- Print to the console, append to the file, and send to Discord if configured.

The program runs continuously until interrupted (Ctrl+C). Every 40 checks, it pauses for 60 seconds to reduce load.

### Main files
- `checker.py`: main script with generation, checking, banner, and webhook integration.
- `config.json`: webhook configuration (`webhookUrl`).
- `requirements.txt`: dependencies (`requests`, `colorama`).
- `Gamertags_Available.txt`: created automatically on first run to record available gamertags.

### How it works (technical overview)
- `generate_username(length)`: creates a string with the first character as a letter and the rest chosen from letters and digits.
- `check_gamertags()`: infinite loop that generates, queries, and classifies as `[AVAILABLE]` or `[TAKEN]`, with counters and periodic pauses.
- `send_to_webhook(username, length)`: if `webhookUrl` is set, sends an embed to Discord.
- `print_banner()` and `animate_banner()`: show an animated ASCII banner at startup.
- On Windows, `set_console_title` and `set_console_size` adjust the console title and dimensions.

### Limitations and disclaimers
- This project depends on the public `xboxgamertag.com` page. Site changes can break detection (the code looks for the string "Gamertag doesn't exist").
- Be mindful of rate limits: there is an automatic 60s pause every 40 checks. Adjust responsibly.
- Use at your own risk. Review the target site's and platform's terms of service.
- Webhook: do not expose your URL publicly.

### Troubleshooting
- "Module not found": run `pip install -r requirements.txt` using the same Python that will run the script.
- Terminal colors: `colorama` is initialized with `autoreset=True`. On non-Windows environments, console sizing is skipped.
- Network issues: the script uses timeouts (GET: 10s, webhook: 5s) and waits 2s after exceptions during checks.
- Missing output file: it is created automatically (`create_file_with_ascii`). Ensure write permissions to the directory.

### Development
- Main code is in `checker.py`. Contributions are welcome via PR.
- Style: keep descriptive names and avoid catching broad exceptions where better handling is possible.

### Authors
- dan — https://github.com/Dansvn
- hax — https://github.com/6hax

