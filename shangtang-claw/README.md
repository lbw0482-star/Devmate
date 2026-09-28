# ShangTangClaw

ShangTangClaw 是基于 DeepAgents 与 LangGraph 的、开源可自部署的 Dev 场景 Agent 工程框架。产品形态是 DevMate：在隔离沙箱里看代码、改 Issue、跑测试，并通过飞书、Web、CLI、Webhook 为团队提供服务。

## 项目简介

核心理念是 Agent Harness（智能体工程骨架）：把不可控的大模型套进可控的工程骨架，覆盖隔离、多租户、限流、评估和可观测。

工程红线是「Claw 调度、沙箱执行、密钥绝不进沙箱」。生产链路按职责拆开：构建、隔离、多渠道接入、异步化、多租户治理、可观测、评估、压测、部署上线。

## 产品亮点

- **Harness，不是模型调用 demo。** 要解决的是如何把大模型放进可控骨架，包括隔离、多租户、限流、评估和可观测。
- **开源、可自部署、多渠道。** DevMate 不绑定 SaaS，可部署到团队自己的服务器或内网。飞书群、CLI、Web、Webhook 的差异收在适配器里，业务核心只认统一请求。
- **按企业级 Agent 系统的能力面搭建。** 沙箱、人在回路（HITL）、任务队列、API 网关、可观测、Eval、压测都有对应包。
- **边界场景放进骨架。** 飞书 3 秒响应约束、慢任务可靠后台、prompt injection 防御、跨租户数据隔离、压测找瓶颈、Eval 防退化。

## 目录

Git 仓库根目录是上一级 `Devmate`，应用在 `shangtang-claw/`。Python 包是 `src/shangtang_claw/`。

```text
shangtang-claw/
├── pyproject.toml          # 依赖与入口 shangtang-claw
├── uv.lock                 # 锁定版本，随 pyproject.toml 一起入库
├── .python-version         # 3.14
├── .env.example            # 配置示例，只有占位符
├── .gitignore
├── README.md
└── src/shangtang_claw/
    ├── agent/              # Claw 调度，Harness 主体
    ├── subagents/          # 子 Agent
    ├── skills/             # 技能说明（SKILL.md）
    ├── tools/              # Agent 可调用工具
    ├── profiles/           # 模型与运行配置档
    ├── middleware/         # HITL、注入防护等横切逻辑
    ├── sandbox/            # 沙箱执行；密钥停在沙箱外
    ├── channels/           # 飞书 / Web / CLI / Webhook 适配
    ├── gateway/            # 渠道接入与统一请求入口
    ├── api/                # HTTP API
    ├── tasks/              # 异步任务队列，慢任务后台化
    ├── concurrency/        # 限流与并发
    ├── resilience/         # 超时、重试、弹性
    ├── infra/              # 配置与 Postgres / Redis 底座
    ├── obs/                # 追踪与可观测
    ├── eval/               # 评估，防止能力退化
    └── loadtest/           # 压测
```

截图中的十个职责模块都在这棵树里：`agent`、`channels`、`tasks`、`sandbox`、`gateway`、`middleware`、`obs`、`infra`、`api`、`profiles`。`subagents`、`skills`、`tools`、`concurrency`、`resilience`、`eval`、`loadtest` 是同一条链路的细分包。

当前已有实现的是 `infra/`：`settings.py` 读取项目根目录 `.env`，`verify_env.py` 检查 Postgres 与 Redis。其余包是职责边界，还没有业务代码。

本地底座与配置：

- Postgres（pgvector）：`localhost:5432`，库 `shanyang`，容器 `syc-postgres`，数据在 `~/docker-data/postgres`
- Redis Stack：`localhost:6379`，管理台 `8001`，容器 `syc-redis`，数据在 `~/docker-data/redis`
- 复制 `.env.example` 为 `.env` 后填写 `SYC_API_KEY` 与 `LANGSMITH_API_KEY`

## 分支

- `main` 只放可运行代码。不在 `main` 上直接做未完成改动。
- 分支从最新 `main` 拉出，用完合并后删除。
- 命名：`<type>/<scope>`。`type` 与提交类型相同，`scope` 用目录名。

```text
feat/infra
fix/settings
docs/readme
chore/deps
```

## 提交信息

使用 [Conventional Commits](https://www.conventionalcommits.org/)。主题一行，说清为什么改。

```text
<type>(<scope>): <主题>

<正文，可选>
```

- **type**: `feat` 功能，`fix` 缺陷，`refactor` 行为不变的结构调整，`docs` 文档，`test` 测试，`chore` 依赖、忽略规则、工程杂项。
- **scope**: 上表中的包名，或 `deps`、`docs`。跨目录且无法归一时省略 scope。
- 主题用简体中文，动词开头，不加句号，不超过 50 字。
- 一次提交只做一件事。格式化、依赖升级不和功能混在同一个提交里。

```text
feat(infra): 增加启动时的环境自检

Postgres 与 Redis 在进程启动前确认可用，避免请求打到未就绪的底座。
```

```text
chore(deps): 锁定 uv 依赖

uv.lock 与 pyproject.toml 一起入库，保证其他人解析到同一套版本。
```

## 入库范围

提交：

- `src/`、`pyproject.toml`、`uv.lock`、`.python-version`
- `.env.example`、`.gitignore`、`README.md`

不提交：

- `.env`：含 `SYC_API_KEY`、`LANGSMITH_API_KEY`
- `.venv/`、`__pycache__/`、`*.pyc`
- `dist/`、`*.egg-info/`、本地缓存和 `.DS_Store`
- Docker 数据目录（本机在 `~/docker-data/`，不要挪进仓库）

密钥只放本地 `.env`。示例值放 `.env.example`，用占位符，不写真实 key。

## 提交前

在 `shangtang-claw/` 下确认这三件事，再回到仓库根目录提交：

```bash
git status
git diff
uv run python src/shangtang_claw/infra/verify_env.py
```

`git status` 里不能出现 `.env` 或 `.venv`。自检要看到 Postgres 与 Redis 连通。只改文档时可以不跑自检。

在仓库根目录：

```bash
git add shangtang-claw
git commit -m "$(cat <<'EOF'
feat(infra): 增加启动时的环境自检

EOF
)"
```

`git add shangtang-claw` 之后再看一次 `git diff --cached`，确认没有把 `.env` 带进去。
