# Synthetic fixture harness preparation evidence
TD-01 is a preloaded isolated fixture alias, not production data. Verify role, selected S-A/Y-2/C-A and saved values in the fixture harness before each run.
Target: S-A/Y-2/C-A T1 saved=17. Non-target sentinels: S-B/Y-2/C-A N-school=31; S-A/Y-1/C-A N-year=43; S-A/Y-2/C-B N-course=59.
Inputs are replaceable positive scores 79,80,81 or percentage values 79.9,80.1; role aliases admin/teacher. Disabled state is configurable.
Restore all saved values and flags from this snapshot between cases. This preparation evidence supports normal/role/off tests only.
No verified preparation currently creates a missing-source-score state: C8 readiness remains blocked pending that fixture seam.
