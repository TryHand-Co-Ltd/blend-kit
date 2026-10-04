# SYN-001 — Synthetic eligibility specification
Status: Confirmed for S1/S2/S4; S3 awaiting business decision. Fixture only; no real customer data.
S1. Teacher-owned preview returns eligible only when enabled=yes AND score is strictly below 60% of maximum, truncating the threshold to an integer. Enabled=no returns not eligible; equality returns not eligible. Preview must not alter stored scores.
S2. Visitor without owner permission must be denied, and target/settings and non-target records must remain unchanged.
S3. Custom overflow calculation is desired, but rounding/clamping is awaiting decision Q1. Do not infer from current code.
S4. Import updates selected school/year only and preserves every non-target school/year. Known requirement; no verified import preparation seam in supplied fixture.
