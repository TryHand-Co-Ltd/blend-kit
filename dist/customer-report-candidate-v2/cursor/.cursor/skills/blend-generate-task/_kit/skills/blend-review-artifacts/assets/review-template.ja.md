<!-- blend-template: review@1.0.0 -->
# {{レビュー対象}} — Artifacts review

<!-- TEMPLATE INSTRUCTIONS: Required schema: source,revision,scope,inventory,verdicts,finding_id,severity,evidence,scenario,impact,proposal,verification,limits. Required H2s and field labels/order stay. Same template for Task-only/standalone Test Spec/combined and chat/file. Replace placeholders and remove instructions. Inventory every assigned file/language/workbook, including skipped/unread. Finding blocks may be absent only when no supported findings remain; state this explicitly. Prior-finding ledger is required only on re-review. Optional advice appears separately only when present. Do not fill unknown facts to conform. -->

## 結論・範囲

- 参照元: {{Spec/current context/latest confirmationの位置・承認状態。Researchは検証対象の証拠}}
- Revision: {{Artifact/source snapshotとcode SHA + relevant working-content identity。private pathsは記載しない}}
- 対象範囲: {{TaskArtifacts / TestSpecArtifacts / combined。指定files/languages/exclusions}}
- 結論: {{各評価軸の結果と決定的な義務/gaps。static reviewをruntime PASSにしない}}

| 評価軸 | 結果 | 根拠・限界 |
| --- | --- | --- |
| Template | {{Conform / mismatch / needs evidence}} | {{Version、required/conditional fields}} |
| 内容 | {{Supported / mismatch / needs evidence}} | {{Source semanticsとbilingual fidelity}} |
| Coverage | {{Complete design / gaps / mismatch / 理由付き対象外}} | {{Clause/branch → case/variant/gap またはtask/AC}} |
| Readiness | {{Ready / Draft / Blocked / 理由付き対象外}} | {{Oracle、preparation、seams}} |
| Execution proof | {{NOT RUN / supplied evidence assessed / needs evidence / 理由付き対象外}} | {{実際のproof type。sourceから格上げしない}} |

### Inventory

| Artifact | Path / revision | 言語 | Template / version | Inspected / skipped | 証拠・理由 |
| --- | --- | --- | --- | --- | --- |
| {{Type}} | {{Repository-relative actual path + identity}} | {{ja/vi/workbook}} | {{Family@versionまたはlegacy limitation}} | {{Inspected / skipped / unread}} | {{Line/sheet scopeまたはmissing access}} |

## Findings・更新提案

### {{Stable finding ID}} — {{Severity}} — {{具体的な問題}}

- 分類: {{Scope、origin、completion effect。実際にある場合のみbehavioral disposition/backend}}
- 証拠: {{Violated source/rule anchor + artifact file:line@revision またはSheet!Cell + Case ID/Variant。確認した反証}}
- 状況: {{不足/誤りを起こすactor/state/input/action。test gapでは違反implementationがPASSできる条件}}
- 影響: {{影響するoutcome/user/data/coverageと重要性}}
- 更新提案: {{変更対象file/AC/TC/variant/fixture/coverage/workbook、根拠付きcorrected expected/branch、維持すべき挙動。unknown oracleは別の判断が必要}}
- 修正後の確認: {{有限のsource/diff/parity/observation check。提案は自動executeの許可ではない}}
- 限界: {{未証明事項・最小確認、または確認済み範囲に未証明事項なし}}

<!-- OPTIONAL only on re-review: preserve prior IDs, even moved/disproved/deferred; no new ID for the same root cause. -->

### 既存Findingの追跡

| ID | 状態 | Change / closure evidence | 限界・次の確認 |
| --- | --- | --- | --- |
| {{Existing ID}} | {{OPEN / FIXED_VERIFIED / DISPROVED / DEFERRED / NEEDS_EVIDENCE}} | {{New revision/location + relevant proof or counter-evidence}} | {{Remaining proof/decision}} |

<!-- OPTIONAL only if non-binding advice exists: use H3 “任意の提案”; state rationale and applicability, separate from required findings. With no findings, replace finding blocks by an explicit no-supported-findings statement; do not invent an empty finding. -->

## Coverage・限界

- Coverage: {{確認したmaterial clauses/branches → assignment/AC/case/variant/gap。妥当な同等coverageと未完了範囲}}
- 実施したChecks: {{実際のread/source/template/parity/formula checks。使用時はrole backend/independence}}
- 未実施Checks: {{未実施または未許可のapplication tests/SQL/browser/runtime/render/recalculation}}
- 限界: {{未読source/artifact、未決事項、不足fixture/proofと最小の次の確認}}
- 保全: {{確認できた場合のみreview入力bytes不変を記載。未確認の保全を主張しない}}
