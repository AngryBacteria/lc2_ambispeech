# How to install and run
## Whisper
Whisper needs some special dependencies to run on a GPU with CUDA support. These
instructions will help you install it on a Windows machine. 

1) First install Nvidia CUDA Toolkit Version 1.11.8. You can use [this link](https://developer.nvidia.com/cuda-11-8-0-download-archive).
This will install the Toolkit and set all the important Path configurations. 
The files should be in a folder similar to this (you will need this later):
```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8```
2) Now you have to download the NVIDIA cuDNN for CUDA 11.x. You have to create an NVIDIA account
for this. You can use [this link](https://developer.nvidia.com/rdp/cudnn-download).
Extract the downloaded zip. There should be 3 folders (bin, include, lib).
Copy all 3 folders to the location from before.

If these instructions did not work, maybe these guides are better:
- https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-841/install-guide/index.html
- https://medium.com/analytics-vidhya/installing-cuda-and-cudnn-on-windows-d44b8e9876b5
- https://medium.com/geekculture/install-cuda-and-cudnn-on-windows-linux-52d1501a8805

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