export type FileTranscriptionProps = {
  transcriptionIsLoading: boolean;
  uploadProgress: number;
};

/**
 * Possible Buffer Sizes for the StereoRecorder (https://recordrtc.org/StereoAudioRecorder.html)
 */
export type BufferSize = 4096 | 256 | 512 | 1024 | 2048 | 8192 | 16384;

/**
 * Possible States for the the StereoRecorder (https://recordrtc.org/StereoAudioRecorder.html)
 */
export type RecorderState = 'inactive' | 'recording' | 'paused' | 'stopped';

/**
 * Endpoint response for azure speech to text
 */
export interface S2TEndpointResponse {
  text: string;
  reason: 'RecognizedSpeech' | 'RecognizingSpeech' | 'NoMatch';
  speaker?: string;
}

/**
 * Possible transcribtion languages (azure)
 */
export type TranscriptionLanguage = 'de-CH' | 'de-DE' | 'de-AT' | 'en-GB' | 'en-US';
