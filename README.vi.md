# CodexKit Engineer Pro Final Plus

[English](README.md) | Tiếng Việt | [简体中文](README.zh-CN.md)

CodexKit Engineer Pro Final Plus là một **hệ điều hành kỹ thuật native cho Codex** dành cho các nhóm muốn AI coding agent hành xử bớt giống kiểu “code theo cảm hứng” và giống kỹ sư senior hơn.

Phiên bản này có chủ đích định hướng mạnh hơn v1:

- **ưu tiên kiến trúc trước, không ưu tiên viết code trước**
- **spec -> architecture -> nfr -> plan -> tasks -> execute**
- **phân loại thay đổi rõ ràng** cho lỗi nhỏ, tính năng giới hạn, thay đổi cắt ngang nhiều phần, và dự án mới
- **maintainability, scalability, performance, reliability và rollback** được xem là artifact hạng nhất
- **skills + subagents + CI prompts native theo repo** thay vì một DSL lệnh tùy biến khổng lồ

## Điểm mới trong bản phát hành cuối

1. Một **bootstrap + architecture gate** bắt buộc cho dự án mới và các tính năng không tầm thường
2. Một lane bootstrap sâu có thể quét repo, tạo project memory và cập nhật hướng dẫn CodexKit theo kiến trúc hiện tại
3. Agent `bootstrap_curator` và các script bootstrap có tính quyết định
4. Tài liệu project-context được sinh ra cùng repo profile dạng máy đọc được, dashboard, continuity memory và constitution rules
5. Các lane greenfield và brownfield sẵn có:
   - `$project-bootstrap`
   - `$brownfield-mapping`
   - `$architecture-discovery`
   - `$architecture-review`
   - `$nfr-capture`
6. Nhiều agent thiên về kiến trúc hơn, gồm `bootstrap_curator`, `constitution_keeper`, `consistency_auditor`, `knowledge_librarian`, `debug_detective` và `ui_ux_auditor`
7. Template phong phú hơn, có trích dẫn project context và ép buộc analysis, test strategy và implementation readiness artifact
8. Xác thực cục bộ mạnh hơn:
   - `scripts/validate-plans.py`
   - `scripts/validate-bootstrap.py`
   - `scripts/audit-placeholders.py`
9. Workflow GitHub **architecture gate** và workflow **artifact consistency** mới
10. Một lớp **constitution + continuity + artifact-consistency + closeout** lấy cảm hứng từ những điểm tốt nhất của workflow spec-driven và agentic
11. Project-context mở rộng: constitution, module index, delivery system, hotspots, design-system map, agent context, continuity và dashboard
12. Kỷ luật triển khai mới: `$artifact-consistency`, `$implementation-readiness`, `$tdd-loop`, `$systematic-debugging`, `$closeout-learning` và `$design-system-forensics`
13. Có thể sinh `AGENTS.md` lồng nhau tùy chọn cho các repo lớn

## Lớp lệnh nhanh

Phiên bản này thêm một bề mặt alias mỏng để bạn gọi bộ kit nhanh hơn mà không cần nhớ toàn bộ tên skill chính tắc.

Các dạng hỗ trợ:

- `/ck:<alias> [payload]` trong chat
- `$ck-<alias> [payload]` ở chế độ giống skill
- các skill chính tắc như `$plan-feature` vẫn dùng bình thường

Ví dụ:

```text
/ck:bootstrap
/ck:feature tenant-rate-limits
/ck:plan-feature add per-tenant rate limits
/ck:ready
/ck:build phase 1
/ck:review
/ck:ship
```

Đọc `docs/command-palette.md` để xem đầy đủ alias và luật định tuyến.

## Nguyên tắc thiết kế

1. **Hiểu hệ thống trước khi thay đổi nó**
2. **Làm kiến trúc sớm, nhưng giữ tỷ lệ hợp lý**
3. **Dùng thiết kế đơn giản nhất vẫn có thể chịu được tăng trưởng**
4. **Ưu tiên các lát cắt có thể rollback và migration nhàm chán nhưng an toàn**
5. **Đo các hot path; đừng đoán**
6. **Biến vận hành, observability và rollback thành thứ tường minh**
7. **Để lại artifact bền vững, không chỉ lịch sử chat**

## Workflow cốt lõi

### Dự án mới hoặc major subsystem

```bash
scripts/new-project.sh billing-platform
```

Sau đó dùng:

```text
$bootstrap
$continuity-memory
$constitution-governance
$project-bootstrap
$architecture-review
$plan-feature
$artifact-consistency
$implementation-readiness
$task-breakdown
```

### Tính năng mới trong codebase hiện có

```bash
scripts/new-feature.sh tenant-rate-limits
```

Sau đó dùng:

```text
$bootstrap
$continuity-memory
$constitution-governance
$brownfield-mapping
$architecture-discovery
$nfr-capture
$plan-feature
$artifact-consistency
$implementation-readiness
$task-breakdown
$tdd-loop
$execute-plan
```

### Sửa lỗi nhỏ

```text
$fix-issue
```

Chỉ dùng lane kiến trúc nếu lỗi đó lộ ra một vấn đề thiết kế sâu hơn.

## Artifact bắt buộc theo quy mô thay đổi

| Change class | Phạm vi điển hình | Artifact tối thiểu |
|---|---|---|
| `L0` | lỗi nhỏ, docs, thay đổi an toàn một file | ghi chú validation, có thể kèm repro |
| `L1` | tính năng giới hạn trong một subsystem | `spec.md`, `analysis.md`, `architecture.md`, `nfr.md`, `plan.md`, `tasks.md`, `test-strategy.md`, `consistency-report.md` |
| `L2` | thay đổi cắt ngang, migration, nhiều module | toàn bộ `L1` cộng `decision-matrix.md`, `rollout.md`, `observability.md`, `risk-register.md`, `perf-budget.md`, `threat-model.md` |
| `L3` | dự án mới, platform capability, subsystem lớn | toàn bộ `L2` cộng `context-map.md`, `interfaces.md`, `data-model.md`, `runbook.md`, và `adr.md` |

## Bố cục repository

```text
.
├── AGENTS.md
├── .codex/
│   ├── config.toml
│   ├── config.mcp.example.toml
│   └── agents/
├── .agents/
│   └── skills/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── codex/prompts/
│   └── workflows/
├── docs/
│   └── project-context/
├── plans/
│   ├── active/
│   ├── archive/
│   └── templates/
├── runbooks/
└── scripts/
```

## Thứ tự áp dụng gợi ý

1. Chép bộ kit vào thư mục gốc của repository.
2. Chạy `python3 scripts/bootstrap-codexkit.py --apply`.
3. Xem lại `docs/project-context/` và khối bootstrap được quản lý trong `AGENTS.md`.
4. Xem lại `.codex/config.toml`.
5. Giữ `plans/templates/` trong repo để mọi agent dùng chung cùng một delivery grammar.
6. Chạy `scripts/check-kit.sh`.
7. Bật GitHub workflows sau khi test và secrets của bạn đã ổn định.
8. Chạy `scripts/audit-placeholders.py` sau khi tinh chỉnh bộ kit cho repo của bạn.

## Các file nên đọc đầu tiên

- `docs/bootstrap-playbook.md`
- `docs/project-memory-system.md`
- `docs/architecture-first-development.md`
- `docs/new-project-playbook.md`
- `docs/new-feature-playbook.md`
- `docs/brownfield-playbook.md`
- `docs/quality-gates.md`
- `docs/agent-roster.md`
- `docs/command-palette.md`
- `docs/skill-catalog.md`
- `docs/v3-improvements.md`
- `docs/final-improvements.md`
- `docs/external-benchmark-analysis.md`
- `docs/source-patterns.md`
- `docs/constitution-playbook.md`
- `docs/continuity-memory.md`
- `docs/implementation-readiness.md`
- `docs/systematic-debugging.md`
- `docs/design-system-forensics.md`
- `docs/initiative-lifecycle.md`
