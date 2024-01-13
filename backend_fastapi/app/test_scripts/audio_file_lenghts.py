import os
import wave


def get_wav_duration(file_path):
    """Get the duration of a WAV file in seconds."""
    with wave.open(file_path, "r") as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration


def sort_wav_files(folder_path):
    """Sort WAV files in a folder by their duration in descending order."""
    wav_files = [f for f in os.listdir(folder_path) if f.endswith(".wav")]
    durations = [
        (file, get_wav_duration(os.path.join(folder_path, file))) for file in wav_files
    ]
    durations.sort(key=lambda x: x[1], reverse=True)
    return durations


path = (
    "F:\\OneDrive - Berner Fachhochschule\\Dokumente\\UNI\\Semester "
    "5\\LC2\\speech_to_text\\testfiles\\with_ambient_noise"
)
sorted_files = sort_wav_files(path)

seconds = 0
for file, file_duration in sorted_files:
    seconds = seconds + file_duration
    print(f"{file}: {file_duration:.2f} seconds [{file_duration / 60:.2f} minutes]")

print(f"\nTotal duration: {seconds:.2f} seconds over {len(sorted_files)} files")
average_duration_seconds = seconds / len(sorted_files)
average_duration_minutes = average_duration_seconds / 60
print(f"Average duration: {average_duration_seconds:.2f} seconds per file")
print(f"Average duration: {average_duration_minutes:.2f} minutes per file")
