# Motivation
In medicine, documentation plays a central role. Recording detailed information, such as diagnoses, treatments, and medication, enables ongoing, quality care for the patient. It also forms the basis for other aspects of healthcare.

Speech recognition systems are already being used as a more efficient method of documentation. However, according to project partners, these are only sporadically used on a regular basis. Therefore, no significant efficiency gains have been achieved so far.

In light of the continuous development in the field of artificial intelligence (AI), there is growing interest in using AI-based technologies to improve the efficiency of medical documentation. The fundamental goal is to transcribe, analyze, and extract the most relevant information from conversations between doctors and patients for documentation purposes.

# Project
This is a student project at the Bern University of Applied Sciences ([BFH](https://www.bfh.ch/en/)). It was developed to support mainly german for the audio and transcript language. The transcription should support most other major languages without any issues. The extraction of clinical data is finetuned to work with german

The software was designed, planned and programmed by:
- Nicolas Gujer ([nicolas.gujer@protonmail.com](mailto:nicolas.gujer@protonmail.com.de))
- Jorma Steiner ([jorma.steiner@students.bfh.ch](jorma.steiner@students.bfh.ch))

# Architecture
We developed a system with a backend and frontend to support the documentation process with ambient speech recognition. It uses the Large Language Models (LLMs) of OpenAI to extract clinical information out of a transcript. A transcript can either be provided or an audio file can be uploaded/recorded.

### Frontend
The [VueJS 3 frontend](https://github.com/AngryBacteria/lc2_ambispeech/tree/main/frontend_vue3) can display the extracted symptoms and anamnesis text. Additionally audio can be recorded and sent to the backend.

### Backend
The [backend](https://github.com/AngryBacteria/lc2_ambispeech/tree/main/backend_fastapi) is developed with the python framework fastapi. It can transcribe audio either with azure speech to text or locally with whisper (gpu support is available). 

# Architecture Diagram (german)
![Architecture diagram](/media/LC2SystemArchitektur.png "Architecture")
