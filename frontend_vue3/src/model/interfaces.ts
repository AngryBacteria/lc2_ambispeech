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
 * Possible transcribtion languages (azure)
 */
export type TranscriptionLanguage = 'de-CH' | 'de-DE' | 'de-AT' | 'en-GB' | 'en-US';

export interface Patient {
  resourceType: string;
  id: string;
  meta: Meta;
  identifier: Identifier[];
  name: Name[];
  telecom: Telecom[];
  gender: string;
  birthDate: string;
  address: Address[];
  maritalStatus: MaritalStatus;
  generalPractitioner: GeneralPractitioner[];
}

export interface Address {
  use: string;
  line: string[];
  city: string;
  postalCode: string;
}

export interface GeneralPractitioner {
  reference: string;
}

export interface Identifier {
  system: string;
  value: string;
}

export interface MaritalStatus {
  coding: Coding[];
}

export interface Coding {
  system: string;
  code: string;
  display: string;
}

export interface Meta {
  source: string;
  profile: string[];
}

export interface Name {
  family: string;
  given: string[];
}

export interface Telecom {
  system: string;
  value: string;
  use?: string;
}

export interface Practitioner {
  resourceType: string;
  id: string;
  meta: Meta;
  identifier: Identifier[];
  name: Name_Doctor[];
  gender: string;
  birthDate: string;
}

export interface Name_Doctor {
  family: string;
  given: string[];
  prefix: string[];
  _prefix: Array<Prefix | null>;
}

export interface Prefix {
  extension: Extension[];
}

export interface Extension {
  url: string;
  valueCode: string;
}

export interface NLPData {
  symptoms: Symptom[];
  medications: Medication[];
  findings: Finding[];
}

//https://build.fhir.org/valueset-observation-status.html
export type NLPStatus = 'amended' | 'preliminary' | 'entered-in-error';

export interface NLPEntry {
  context: string;
  isInTranscript?: boolean;
  status: NLPStatus;
}

export interface Finding extends NLPEntry {
  finding: string;
  value: string;
}

export interface Medication extends NLPEntry {
  name: string;
  dosage: string;
}

export interface Symptom extends NLPEntry {
  symptom: string;
  onset: string;
  location: string;
}
