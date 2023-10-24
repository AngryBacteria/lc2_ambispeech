export type FileTranscriptionProps = {
  transcriptionError: boolean;
  transcriptionIsLoading: boolean;
  uploadProgress: number;
  errorMessage: string;
};

export enum StateFlag {
  INITIAL,
  ERROR,
  SUCCESS
}
