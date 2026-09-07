# Evidence Model

Every claim in a recovery should have a provenance class.

| Level | Meaning | Proof strength |
|---|---|---|
| OBSERVED | directly supported by stable source pixels/modules | primary |
| RECOVERED_BY_RS | solved from QR parity equations | mathematical |
| CONSTRAINED_BY_METADATA | narrowed by trusted external context | search-only |
| INFERRED_UNVERIFIED | heuristic/semantic guess | none |

A confirmed payload must ultimately survive QR-native validation. External context can shrink the candidate set but cannot turn an unobserved byte into a fact by itself.
