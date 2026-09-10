# NEUROMOYO Responsible AI / Inclusion Note

NEUROMOYO is an AI-assisted neurological screening and voice-intelligence system. It is not presented as an autonomous diagnostic system.

## Data

AfriSwitch is used for public code-switching ASR benchmarking. Any clinical-domain evaluation must use appropriately governed data. Future local recordings require informed consent, de-identification, purpose limitation and a suitable data-sharing basis.

## Privacy

Raw health-related audio is not committed to the source repository or public benchmark page. Production recordings are processed through temporary files and deleted by the voice-intelligence service. API credentials remain backend secrets.

## Safety

ASR benchmark performance is not clinical validation. Speech transcription does not diagnose Parkinson's disease. Clinical findings are evidence for qualified clinical interpretation. The neurological model remains a screening signal and is not an autonomous diagnostic authority.

## Inclusion

The benchmark focuses explicitly on African code-switching and reports the actual source-data composition rather than implying that Pidgin represents Africa as a whole.

## Methodological boundary

The AfriSwitch Pidgin split has 1,799 code-switched and only 2 non-code-switched utterances. NEUROMOYO therefore does not report a CS/non-CS penalty from this split. It instead analyses CMI, switch-point and duration variation within the code-switched population.

## Proposed metric

Clinical Information Preservation is a NEUROMOYO-proposed metric, not an official Intron metric.
