# NEUROMOYO — Sahara CodeSwitch Africa Benchmark Report

## Benchmark question

Can African code-switched speech be converted reliably into information useful for downstream neurological care workflows?

## Dataset

- Dataset: `intronhealth/AfriSwitch`
- Configuration: `pidgin`
- Split: `test`
- Full split: 1,801 utterances
- Code-switched: 1,799
- Non-code-switched: 2
- Evaluation subset: 100 utterances
- Random seed: `20260909`

The clean benchmark run uses a reproducible metadata-aware sample. The observed evaluation subset was entirely code-switched because the source Pidgin split is overwhelmingly code-switched.

## Models

- Intron Sahara
- Whisper Tiny
- Whisper Base
- Meta MMS 1B

Every model received the same paired evaluation utterances.

## Overall results

| model | n | mean WER | median WER | mean CER | median CER | mean latency (s) | mean RTF |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sahara | 100 | 0.526 | 0.500 | 0.338 | 0.281 | 2.488 | 0.350 |
| MMS-1B | 100 | 0.656 | 0.618 | 0.365 | 0.308 | 0.408 | 0.047 |
| Whisper Tiny | 100 | 2.436 | 0.870 | 2.083 | 0.577 | 1.261 | 0.161 |
| Whisper Base | 100 | 2.841 | 0.809 | 1.926 | 0.462 | 1.736 | 0.184 |

Sahara had the lowest mean WER and CER in this evaluation. MMS-1B had the lowest RTF, so speed and transcription accuracy should be treated as separate engineering dimensions.

## Code-switch robustness

A conventional CS penalty is **not reported**. The full Pidgin split contains only two non-code-switched utterances, which is not a meaningful control group. NEUROMOYO does not manufacture additional labels or rebalance the source data synthetically.

Instead, robustness is examined descriptively across CMI, switch-point count and duration slices. These analyses are within the code-switched population and should not be interpreted as causal estimates of the effect of code-switching.

## Paired Sahara comparisons

- Sahara − Whisper Tiny mean WER difference: `-1.910`, bootstrap 95% CI `[-2.843, -1.115]`
- Sahara − Whisper Base: `-2.315`, CI `[-3.284, -1.490]`
- Sahara − MMS-1B: `-0.129`, CI `[-0.170, -0.091]`

## Clinical Information Preservation

NEUROMOYO proposes an additional downstream measure evaluating whether clinically meaningful facts survive transcription. This requires appropriately annotated clinical-domain data and is not an official Intron metric. It is not claimed as completed by this benchmark run.

## Limitations

The benchmark is Pidgin-focused and does not represent all African languages, accents, countries or clinical populations. MMS is an independent multilingual baseline; no dedicated Cameroon-Pidgin adapter is claimed. ASR benchmark performance is not clinical validation and must not be presented as diagnostic accuracy.
