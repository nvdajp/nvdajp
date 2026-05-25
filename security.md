# セキュリティ問題の報告

セキュリティ脆弱性の報告は GitHub の公開 issues, discussions や NVDA 日本語チームのメーリングリストで行わないでください。
NVDA日本語版については、メールの題名を「脆弱性の報告」として https://www.nvda.jp/contact に報告してください。
NVDA本家版については info@nvaccess.org に英語で報告してください。

脆弱性の報告については3営業日以内に返信します。
返信が届かない場合は再度ご連絡ください。

問題の性質と範囲をよりよく理解するために、なるべく以下の情報を含めてください。
ご報告をより迅速に検討するのに役立ちます。

* 問題の種類(サービス拒否、特権エスカレーションなど)
* 影響を受けるソースコードの場所(タグ/ブランチ/コミットまたはURL)
* 問題を再現するために必要な特別な設定
* 問題を再現するための具体的な操作の手順
* 概念実証または(可能な場合)脆弱性実証コード
* 問題の影響（攻撃者が問題を悪用して達成できることを含む）
* 問題を軽減するための潜在的な回避策
* 問題によって引き起こされる妥協の指標

NVDA で扱われるセキュリティ問題の例は [NVDA日本語版](https://github.com/nvdajp/nvdajp/security/advisories) および [NVDA本家版](https://github.com/nvaccess/nvda/security/advisories) GitHub セキュリティ勧告のページにあります。

## Security Advisory Group

NV Access is committed to maintaining the highest standards of security in NVDA. In line with this commitment, we have established a Security Advisory Group. This group plays a pivotal role in enhancing the security of NVDA.

Objectives and Functioning:

* The group is composed of dedicated users and security enthusiasts who volunteer their expertise.
* It focuses on identifying, analysing and resolving security issues in a collaborative manner.
* The group's contributions are instrumental in maintaining and elevating our security standards.
* Their insights and recommendations are directly incorporated into our development process, leading to more secure and reliable software.

We welcome participation from our user community. If you have a keen interest in security and wish to contribute, please [contact us](mailto:info@nvaccess.org).

## Severity Levels

* P1 (Exploitable high): Vulnerabilities of critical or high severity (CVSS v3/v4 score 7+) that demonstrate practical exploitability (e.g. active exploitation, public PoC or trivial execution) and pose an imminent threat to NVDA users.
* P2 (Theoretical high): Vulnerabilities with significant potential impact (high CVSS) where the risk is deemed theoretical due to high attack complexity, specific non-default configurations or lack of a viable exploit path.
* P3 (Standard): All other issues, including minor security weaknesses, best-practice hardening or library vulnerabilities confirmed to be unreachable or unused in NVDA.

## Response Timelines (SLAs)

* Acknowledgement and Triage: Within 3 business days of receipt.
* P1 - Immediate action:
  * Planning and mitigation: Detailed assessment of the issue and possible technical solutions, within 1 week of triage.
  * Release: Target patch release within 2 weeks of completing assessment.
  If only a workaround is achievable in this timeframe, a thorough and complete resolution may need to be scheduled into the next minor release.
* P2 - Scheduled remediation:
  * Planning and mitigation: Assessment within 2 weeks of triage.
  * Release: Target patch release or the next scheduled minor release (if within 60 days).
* P3 - Backlog:
  * To be addressed on a best-effort basis.
* Security Advisory: A security advisory will be published concurrently with the release of the patch.
The advisory will provide details of the vulnerability and rectification steps.
As details of the vulnerability will be available in the code repository, immediate disclosure aligns with responsible disclosure principles.

## Resource Allocation

* P1 (Critical): Immediate attention from core developers and/or the Security Advisory Group. Other development tasks may be temporarily deprioritised.
* P2 (High): Dedicated resources will be allocated, with prioritisation based on severity and available development bandwidth.
* P3 (Moderate / low): Resources will be allocated on a best-effort basis.
