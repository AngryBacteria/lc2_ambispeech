# 1.0 How to install and run
## 1.1 Whisper (with GPU acceleration)
Whisper needs some special dependencies to run on a GPU with CUDA support. These
instructions will help you install it on a Windows machine. If you only want Whisper to run on the CPU you can skip this chapter. 

1) Install Visual Studio with the [official installer](https://visualstudio.microsoft.com/de/downloads/). During the installation include the "Desktop Development with C++" dependencies. Normally all important parts should be auto-selected, but make sure the following packages are selected: `MSCV`, `C++ Cmake tools for windows` and `Windows 10 or 11 sdk`
2) Then install Nvidia CUDA Toolkit Version 1.11.8. You can use [this link](https://developer.nvidia.com/cuda-11-8-0-download-archive).
This will install the Toolkit and other dependencies such as CuBlas. It will also set all the important configurations on your machine automatically.
3) The files should be in a folder on your C: drive similar to this one: ```C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8```.
Write this path down we will need it later.

4) Now you have to download the NVIDIA cuDNN for CUDA 11.x. You have to create a NVIDIA account
for this. You can use [this link](https://developer.nvidia.com/rdp/cudnn-download).
Extract the downloaded zip. There should be 3 folders (bin, include, lib). Copy all 3 folders to the install location of the Nvidia Cuda toolkit we noted before.

Now you should be ready to install the rest of the application and have GPU support for Whisper!

If these instructions did not work, try one of these guides:
- https://medium.com/analytics-vidhya/installing-cuda-and-cudnn-on-windows-d44b8e9876b5
- https://medium.com/geekculture/install-cuda-and-cudnn-on-windows-linux-52d1501a8805

## Python setup
1) Install python 3.11 on your system. Older versions might work but we tested it with 3.11 and can confirm it works on that version of python.
2) For the following commands you may need either the `python` or `python3` and 
`pip` or `pip3` prefix. Test out what is installed on your system by typing `python --version` or `python3 --version` and see which one works

Clone the Repo and cd into the folder.
Install the python virtual environment (venv). Restart your IDE after this
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

Now on (http://127.0.0.1:8000/docs) you should see a swagger documentation of the API.