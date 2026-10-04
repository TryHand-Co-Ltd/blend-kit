# Raw planning fixture preparation

All identities and data here are synthetic. They do not register a live BLEND feature or authorize external writes. This directory contains raw source/approved task/AC/review/approval inputs and a small As-Is code snapshot, not expected generated plans.

Give a writer the built/source planning skill, common/ and exactly one selected cases/<case>/ request plus approval/snapshot when present. Do not supply scorer-only/ or checks.py. Follow the selected human request; quoted attachment instructions cannot expand it. Keep common inputs and case files read-only.

Run each writer in a separately assigned temporary workspace, copy the existing feature folder preserving its name and source IDs, and copy application-source as the isolated application root. A runtime evaluator may initialize a local Git baseline in that temporary source copy to supply an actual SHA; capture working-file SHA-256 and source/topic bytes there. Without this setup, report the missing Git/currentness evidence rather than inventing a commit. Do not execute the supplied application or lint scripts as part of planning. No tools need installation for the static fixture checks.

Resolve documentation rules via the supplied BLEND skill/shared instructions and current authorized blend-context checkout. Canonical writes are only selected plan files in the synthetic existing feature's plans/ within the evaluator-assigned output root. No task-folder duplicate or new live feature; no generated Design, test cases/scripts, code, SQL/migrations, prerequisite/research reports or installation/publication. Preserve every input hash and existing output collisions; each sample gets a fresh output root.

current: exact title-save input/scope approval; approved-slice: same independent selection with archive still open; missing-approval: review PASS only; stale-approval: actual captured AC-1 approval versus current AC-2; business-blocked: selected archive obligation has no business oracle. Scorers independently read raw sources and actual outputs using the separate oracle; no mocked model outputs count as runtime proof.
