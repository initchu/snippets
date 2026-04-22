# DevPulse Actions

**业界最佳实践**：基于 GitHub Actions 的自动提交方案，零基础设施，提交 100% 计入贡献图。

## 为什么选择 Actions 方案？

| 特性 | GitHub Actions | Docker 方案 |
|------|----------------|-------------|
| 基础设施 | ✅ 零成本，GitHub 原生 | ❌ 需要服务器 |
| 贡献图计入 | ✅ 100% 计入（用 PAT） | ⚠️ 需正确配置邮箱 |
| 维护成本 | ✅ 无需维护 | ❌ 需管理容器 |
| 灵活性 | ✅ cron + 手动触发 | ⚠️ 固定间隔 |
| 提交质量 | ✅ Conventional Commits | ✅ 同样支持 |

## 快速开始

### 1. Fork 本仓库

点击右上角 **Fork** 按钮，将仓库 fork 到你的账号下。

### 2. 配置 Secrets 和 Variables

进入 **Settings → Secrets and variables → Actions**：

#### Secrets（敏感信息）

- `PAT_TOKEN`：GitHub Personal Access Token
  - 创建地址：https://github.com/settings/tokens/new
  - 权限：勾选 `repo`（完整仓库访问权限）
  - 过期时间：建议选择 **No expiration**

#### Variables（公开配置）

- `GIT_AUTHOR_NAME`：你的 GitHub 用户名（如 `octocat`）
- `GIT_AUTHOR_EMAIL`：你的 GitHub 邮箱（**必须与账号关联**）

### 3. 启用 Actions

进入 **Actions** 标签页，点击 **I understand my workflows, go ahead and enable them**。

### 4. 手动触发测试

进入 **Actions → Auto Commit → Run workflow**，选择提交数量（1-5），点击 **Run workflow**。

几秒后刷新页面，查看 workflow 运行状态。成功后，你的贡献图会立即更新！

## 工作原理

### 调度策略

- **工作日（周一到周五）**：每天 6 次提交（北京时间 09:00 / 11:30 / 14:00 / 17:00 / 20:00 / 23:00）
- **周末（周六周日）**：每天 1 次提交（北京时间 12:00）

模拟真实开发者的活动节奏，避免机械化痕迹。

### 提交内容

- **文件类型**：`.py` / `.md` / `.txt` / `.yaml` / `.json`，内容与扩展名匹配
- **提交消息**：遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
  - `feat:` 新功能（权重最高）
  - `fix:` 修复 bug（权重次高）
  - `refactor:` / `docs:` / `chore:` / `test:` / `perf:`

### 为什么用 PAT 而非 GITHUB_TOKEN？

GitHub Actions 默认的 `GITHUB_TOKEN` 提交**不计入个人贡献图**，只有用 Personal Access Token (PAT) 的提交才会显示在你的 profile 上。

## 自定义配置

### 修改调度频率

编辑 `.github/workflows/auto-commit.yml` 中的 `cron` 表达式：

```yaml
schedule:
  - cron: '0 1 * * 1-5'   # 每天 UTC 01:00（北京时间 09:00）
```

[Cron 表达式生成器](https://crontab.guru/)

### 修改提交内容

编辑 `scripts/generate.py`：

- `COMMIT_TEMPLATES`：提交消息模板
- `CONTENT_GENERATORS`：文件内容生成器
- `CATEGORY_WEIGHTS`：提交类型权重

## 注意事项

1. **邮箱必须关联**：`GIT_AUTHOR_EMAIL` 必须在 [GitHub 邮箱设置](https://github.com/settings/emails) 中添加并验证
2. **仓库必须非 Fork**：Fork 仓库的提交不计入贡献图（本仓库 fork 后会自动计入）
3. **PAT 安全**：不要泄露 PAT，定期轮换（建议每 90 天）
4. **Actions 配额**：GitHub 免费账号每月 2000 分钟，本方案每月约消耗 50 分钟

## 常见问题

### Q: 提交了但贡献图没更新？

A: 检查：
1. `GIT_AUTHOR_EMAIL` 是否与 GitHub 账号关联
2. 是否使用了 `PAT_TOKEN` 而非 `GITHUB_TOKEN`
3. 仓库是否为 Fork（Fork 仓库不计入）
4. 等待 24 小时，GitHub 贡献图有延迟

### Q: 如何停止自动提交？

A: **Settings → Actions → General → Actions permissions** 选择 **Disable actions**。

### Q: 可以用在私有仓库吗？

A: 可以，但需要在 **Settings → Profile settings** 中勾选 **Include private contributions on my profile**。

## License

MIT
