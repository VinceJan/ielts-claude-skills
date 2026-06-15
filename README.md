# IELTS Claude Skills · v2.0

> 一套跑在 Claude Code 上的雅思备考 AI 教练 skill。
> **8 个训练 Skill + 1 个共享 core + 数据持久化 + 进度可视化。** 装上就能用。

---

## 这是什么

8 个训练 Skill，加 1 个共享 `ielts-core`，构成一个完整的雅思备考教练系统：

| Skill | 干啥 | 触发词 |
|-------|------|--------|
| `/ielts` | 路由入口 + 首次建档 + 进度摘要 | 「我要备考雅思」「IELTS」 |
| `/ielts-diagnose` | 水平诊断 + 8 周个人计划生成 | 「诊断」「规划」「制定计划」 |
| `/ielts-writing` | 写作四维批改 + 改写对比 + 输入期训练 | 「批改作文」「帮我看看这篇」 |
| `/ielts-reading` | 四步法精读 + 同义替换 + 长难句分析 | 「分析阅读」「这道为什么错」 |
| `/ielts-listening` | 听力错题分析 + 倍速精听任务 | 「听力」「精听」「听不懂」 |
| `/ielts-speaking` | 个人故事生成 + 话题分组 + Part 3 预测 | 「口语素材」「话题分组」 |
| `/ielts-vocab` | 语境背词 + 间隔重复 + 同义替换专项 | 「背单词」「词汇」「生词」 |
| `/ielts-dashboard` | 可视化学习报告 + 趋势图 + 错题分布 | 「看进度」「数据」「趋势」 |
| `ielts-core` | 共享事实、数据 schema、归档脚本 | 被其他 skill 调用 |

**核心升级（vs v1.0）：**
- 数据持久化：所有学习记录写入 `~/.ielts/`，跨会话记忆；`events.jsonl` 作为机器可读主记录
- 新增 4 个 skill：诊断、听力、词汇、Dashboard
- 四步法精读：计时做题 → 标生词 → 标长难句 → 对答案
- 个人故事生成：基于用户真实经历生成口语素材
- 间隔重复词汇训练：扩展间隔作为默认方案，按正确率动态调整
- 进度可视化：分数趋势、错题分布、词汇进度

---

## 适合谁

- 备考雅思、想用 AI 当陪练的考生
- 已经在用 Claude Code 的开发者
- 想看看雅思 skill 怎么写的人（拿去改成自己的版本）

---

## 安装

### 前提

你要先装好 [Claude Code](https://docs.claude.com/en/docs/claude-code)。

### 方法一：直接复制

```bash
# Mac / Linux
cp -r ielts-core ielts ielts-diagnose ielts-writing ielts-reading ielts-listening ielts-speaking ielts-vocab ielts-dashboard ~/.claude/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse ielts-core, ielts, ielts-diagnose, ielts-writing, ielts-reading, ielts-listening, ielts-speaking, ielts-vocab, ielts-dashboard $env:USERPROFILE\.claude\skills\
```

### 方法二：克隆

```bash
git clone https://github.com/VinceJan/ielts-claude-skills.git
cd ielts-claude-skills
cp -r ielts-core ielts ielts-diagnose ielts-writing ielts-reading ielts-listening ielts-speaking ielts-vocab ielts-dashboard ~/.claude/skills/
```

装完之后重启 Claude Code，输入 `/ielts` 就能用。

---

## 怎么用

### 场景 1：首次使用，想被引导

```
你：/ielts
AI：（检测到无 profile，引导建档）
   → 问目标分、考试日期、当前水平
   → 创建 ~/.ielts/profile.md
   → 路由到 /ielts-diagnose 生成计划
```

### 场景 2：直接批改作文

```
你：/ielts-writing
   [粘贴题目 + 你的作文]
AI：
- 四维评分（TR / CC / LR / GRA）
- 句子级标注每个问题
- 改写成目标分数版本
- 自动归档到 ~/.ielts/writing/
```

### 场景 3：四步法精读

```
你：/ielts-reading
   [粘贴文章 + 题目]
AI：
- 第一步：计时做题
- 第二步：标生词（自动入库 ~/.ielts/vocab/）
- 第三步：标长难句（拆解 + 同结构练习句）
- 第四步：对答案 + 错题分析 + 同义替换提取
```

### 场景 4：听力错题分析

```
你：/ielts-listening
   [粘贴 Audio Script + 题目 + 答案]
AI：
- 逐题拆解：连读/弱读/同义替换/干扰信息
- 生成精听任务：1.25x → 1.5x 递进
- 生词自动入库
```

### 场景 5：口语个人故事

```
你：/ielts-speaking
   "帮我准备 Part 2 描述一次旅行"
   "我去年去了香港，住在尖沙咀，逛了维多利亚港..."
AI：
- 基于你的真实经历生成 200-250 词的 Part 2 回答
- 标注关键表达和可替换说法
- 列出这个故事能覆盖的其他话题
- 生成 Part 3 追问预测
```

### 场景 6：每日背词

```
你：/ielts-vocab
   "今天背什么词"
AI：
- 推送 15 个新词（按场景分类）
- 每个词配雅思风格语境例句
- 5 个含今日词汇的长难句
- 第二天自动测试今天的词
```

### 场景 7：看进度

```
你：/ielts-dashboard
AI：
- 四科分数趋势
- 错题类型分布
- 词汇掌握进度
- 数据驱动的下一步建议
```

---

## 文件结构

```
ielts-claude-skills/
├── ielts-core/                 # 共享事实、数据 schema、归档脚本
├── ielts/SKILL.md              # 路由教练
├── ielts-diagnose/SKILL.md     # 诊断 + 规划
├── ielts-writing/SKILL.md      # 写作批改
├── ielts-reading/SKILL.md      # 阅读精读
├── ielts-listening/SKILL.md    # 听力训练
├── ielts-speaking/SKILL.md     # 口语素材
├── ielts-vocab/SKILL.md        # 词汇训练
├── ielts-dashboard/SKILL.md    # 进度可视化
├── data-schema.md              # 数据格式规范
├── scoring-rubrics.md          # 评分标准详表
├── study-plan-template.md      # 8 周备考计划模板
├── README.md                   # 你正在看
└── LICENSE                     # MIT
```

### 数据目录（使用后自动创建）

```
~/.ielts/
├── profile.md                  # 用户档案
├── plan.md                     # 个人备考计划
├── events.jsonl                # 机器可读训练事件
├── writing/                    # 写作批改记录
├── reading/                    # 阅读分析记录
├── listening/                  # 听力分析记录
├── speaking/                   # 口语素材
├── vocab/                      # 生词库 + 同义替换库
└── dashboard/                  # Dashboard 数据
```

---

## 核心方法论

### 阅读四步法

1. **计时做题** — 按考试规则，知道真实水平
2. **标生词** — 不对答案，先把生词全部标出并入库
3. **标长难句** — 拆解结构 + 生成同结构练习句
4. **对答案** — 完成前三步才对答案，然后错题分析

**为什么有效：** 精读 > 刷量。一套题做透比十套题刷过有用。

### 写作两阶段

**第一个月（输入期）：** 背范文 → 拆结构 → 提取关键表达 → 举一反三
**第二个月（输出期）：** 限时写 → 批改 → 背改写版 → 再写

**为什么有效：** 输入够了才能输出好。脑子里没东西写不出来。

### 口语个人故事

1. 用中文想自己的真实经历
2. AI 生成英文万能故事
3. 一个故事覆盖 10-20 个话题
4. 少量故事覆盖高频 Part 2，但要练改编，避免背诵痕迹

**为什么有效：** 记自己的故事比记别人的容易得多。

### 词汇语境背词

- 不背孤立单词，在语境中背
- 结合阅读背词效率最高
- 间隔重复：当天 → 第 2 天 → 第 4 天 → 第 7 天 → 第 14 天（默认方案，可按正确率调整）
- 间隔复习有稳定证据；扩展间隔是实用默认值，但不写成绝对规律

### 听力倍速精听

- 不需要听很多，把一篇听到滚瓜烂熟
- 1.25x → 1.5x 递进
- 目标：正常速度稳定听懂并做对；1.25x/1.5x 作为后期压力训练，不作为提分保证

---

## 参考文档

| 文档 | 内容 |
|------|------|
| `data-schema.md` | 所有数据文件的格式规范 |
| `scoring-rubrics.md` | 雅思四科评分标准详表（Band 5-9） |
| `study-plan-template.md` | 8 周备考计划模板 |
| `ielts-core/references/` | 安装后仍可被 skill 读取的共享事实与数据规范 |

---

## 怎么改

想改成自己的版本：

1. Fork 一份
2. 改对应的 `SKILL.md`——人格、评分标准、模板都在里面
3. 重新复制到 `~/.claude/skills/`
4. 重启 Claude Code

**常见改法：**
- 改 SOUL 段落 → 换教练人格
- 改评分标准表 → 适配托福/GRE
- 改模式表 → 加新的工作流
- 改边界段 → 调整 skill 之间的分工

---

## License

[MIT](./LICENSE)

随便用、随便改、随便商用。注明出处不强制但欢迎。

---

## 反馈

发 [issue](https://github.com/VinceJan/ielts-claude-skills/issues) 或者 PR。
