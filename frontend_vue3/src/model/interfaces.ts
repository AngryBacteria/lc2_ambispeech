export type FileTranscriptionProps = {
  transcriptionError: boolean;
  transcriptionIsLoading: boolean;
  uploadProgress: number;
  errorMessage: string;
};

/**
 * Typical States to help with component state management
 */
export enum StateFlag {
  INITIAL,
  ERROR,
  SUCCESS
}

/**
 * Possible Buffer Sizes for the StereoRecorder (https://recordrtc.org/StereoAudioRecorder.html)
 */
export type BufferSize = 4096 | 256 | 512 | 1024 | 2048 | 8192 | 16384;

/**
 * Possible States for the the StereoRecorder (https://recordrtc.org/StereoAudioRecorder.html)
 */
export type RecorderState = 'inactive' | 'recording' | 'paused' | 'stopped';
