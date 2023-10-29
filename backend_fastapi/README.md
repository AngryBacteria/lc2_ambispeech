# How to install and run

## Whisper Setup
For Whisper support, your system needs to have FFmpeg installed and the PATH configured.
If you have a functioning Install, try to type `ffmpeg` into a console prompt and see
if there is output. If yes ffmpeg is installed!

Else you have to install it. 
Here are a couple of ways to install [FFmpeg](https://ffmpeg.org/) for different operating systems:
```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

## Python setup
For the following commands you may need either the `python` or `python3` and 
`pip` or `pip3` prefix. Test out what is installed on your system. 
We tested the system on Python Version 3.11, but older versions should also work.

Clone the Repo and cd into the folder.
Install the python virtual environment (venc). Restart your IDE after this
```bash
python -m venv env
```

Install the requirements
```bash
pip install -r requirements.txt
```

Start the app with uvicorn
```bash
uvicorn app.main:app --reload
```