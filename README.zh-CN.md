# CodexKit Engineer Pro Final Plus

[English](README.md) | [Tiếng Việt](README.vi.md) | 简体中文

CodexKit Engineer Pro Final Plus 是一套**原生面向 Codex 的工程操作系统**，适合希望 AI 编码代理少一些“凭感觉写代码”，多一些资深工程师风格的团队。

这个版本比 v1 更有明确的方法论：

- **先做架构，而不是先写代码**
- **spec -> architecture -> nfr -> plan -> tasks -> execute**
- **明确的变更分级**，覆盖小修复、范围受控的功能、跨模块改动和新项目
- **可维护性、可扩展性、性能、可靠性和回滚**都被视为一等工件
- **仓库原生的 skills + subagents + CI prompts**，而不是一套庞大的自定义命令 DSL

## 最终版本的新内容

1. 针对新项目和非简单功能，增加了强制性的 **bootstrap + architecture gate**
2. 深度 bootstrap 流程可以扫描仓库、生成项目记忆，并按当前架构更新 CodexKit 指南
3. 新增 `bootstrap_curator` agent 和确定性的 bootstrap 脚本
4. 生成 project-context 文档，以及机器可读的 repo profile、dashboard、continuity memory 和 constitution rules
5. 保留了现有的 greenfield 与 brownfield 路径：
   - `$project-bootstrap`
   - `$brownfield-mapping`
   - `$architecture-discovery`
   - `$architecture-review`
   - `$nfr-capture`
6. 增加了更多偏架构的 agents，包括 `bootstrap_curator`、`constitution_keeper`、`consistency_auditor`、`knowledge_librarian`、`debug_detective` 和 `ui_ux_auditor`
7. 更丰富的模板会引用 project context，并强制要求 analysis、test strategy 与 implementation readiness 工件
8. 更强的本地校验：
   - `scripts/validate-plans.py`
   - `scripts/validate-bootstrap.py`
   - `scripts/audit-placeholders.py`
9. 提供 GitHub **architecture gate** workflow 和新的 **artifact consistency** workflow
10. 增加 **constitution + continuity + artifact-consistency + closeout** 层，吸收了 spec-driven 和 agentic workflow 体系中的优秀做法
11. 扩展 project-context 输出：constitution、module index、delivery system、hotspots、design-system map、agent context、continuity 和 dashboard
12. 新的实施纪律：`$artifact-consistency`、`$implementation-readiness`、`$tdd-loop`、`$systematic-debugging`、`$closeout-learning` 和 `$design-system-forensics`
13. 为大型仓库提供可选的嵌套 `AGENTS.md` 生成功能

## 快速命令层

这个版本增加了一层很薄的 alias 表面，让你无需记住所有规范 skill 名称，也能快速调用整个工具包。

支持的形式：

- 在聊天中使用 `/ck:<alias> [payload]`
- 在 skill 风格模式中使用 `$ck-<alias> [payload]`
- 也可以继续直接使用规范 skill，例如 `$plan-feature`

示例：

```text
/ck:bootstrap
/ck:feature tenant-rate-limits
/ck:plan-feature add per-tenant rate limits
/ck:ready
/ck:build phase 1
/ck:review
/ck:ship
```

完整别名目录和路由规则请见 `docs/command-palette.md`。

## 设计原则

1. **修改系统之前先理解系统**
2. **尽早做架构，但保持与问题规模相称**
3. **选择能够支撑增长的最简单设计**
4. **优先选择可回滚的切片和朴素但安全的迁移**
5. **测量热点路径，不要猜**
6. **把运维、可观测性和回滚变成显式要求**
7. **留下可长期复用的工件，而不只是聊天记录**

## 核心工作流

### 新项目或大型子系统

```bash
scripts/new-project.sh billing-platform
```

然后使用：

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

### 现有代码库中的新功能

```bash
scripts/new-feature.sh tenant-rate-limits
```

然后使用：

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

### 小型缺陷修复

```text
$fix-issue
```

只有当这个缺陷暴露出更深层的设计问题时，才进入架构路径。

## 按变更规模要求的工件

| Change class | 典型范围 | 最低工件要求 |
|---|---|---|
| `L0` | 小修复、文档、单文件安全改动 | validation 说明，可选 repro |
| `L1` | 单一子系统中的受控功能 | `spec.md`、`analysis.md`、`architecture.md`、`nfr.md`、`plan.md`、`tasks.md`、`test-strategy.md`、`consistency-report.md` |
| `L2` | 跨模块改动、迁移、多模块修改 | `L1` 全套，再加 `decision-matrix.md`、`rollout.md`、`observability.md`、`risk-register.md`、`perf-budget.md`、`threat-model.md` |
| `L3` | 新项目、平台能力、大型子系统 | `L2` 全套，再加 `context-map.md`、`interfaces.md`、`data-model.md`、`runbook.md` 和 `adr.md` |

## 仓库结构

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

## 建议的采用顺序

1. 把这套工具复制到你的仓库根目录。
2. 运行 `python3 scripts/bootstrap-codexkit.py --apply`。
3. 查看 `docs/project-context/` 和 `AGENTS.md` 中受管理的 bootstrap 区块。
4. 查看 `.codex/config.toml`。
5. 保持 `plans/templates/` 已提交到仓库，这样所有 agent 都会共享同一种交付语法。
6. 运行 `scripts/check-kit.sh`。
7. 当测试和 secrets 稳定后，再启用 GitHub workflows。
8. 在你把这套 kit 定制到自己的仓库后，运行 `scripts/audit-placeholders.py`。

## 值得优先阅读的文件

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
