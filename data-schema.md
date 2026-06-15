# 数据格式规范

所有 skill 共享 `~/.ielts/` 目录。每个文件使用 Markdown 格式，顶部有 YAML frontmatter。

---

## 目录结构

```
~/.ielts/
├── profile.md
├── plan.md
├── events.jsonl
├── writing/
│   ├── {YYYY-MM-DD}-{task}-{seq}.md
│   └── summary.md
├── reading/
│   ├── {YYYY-MM-DD}-{test}-{passage}.md
│   └── summary.md
├── listening/
│   ├── {YYYY-MM-DD}-{test}-{section}.md
│   └── summary.md
├── speaking/
│   ├── stories.md
│   ├── topics-covered.md
│   └── summary.md
├── vocab/
│   ├── wordbank.md
│   ├── review-log.md
│   └── synonyms.md
└── dashboard/
    └── index.html
```

---

## 机器可读事件主记录

Dashboard 和长期趋势优先读取 `events.jsonl`。每行一个 JSON 对象：

```json
{"date":"2026-06-12","module":"writing","kind":"correction","source":"Task 2 education","metrics":{"overall":6.5,"tr":6.5,"cc":6.0,"lr":7.0,"gra":6.5},"notes":"CC 是主要短板"}
```

详细 Markdown 报告用于复盘，`events.jsonl` 用于聚合。

## 文件格式

### profile.md

```markdown
---
type: profile
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# 用户档案

## 基本信息
- 目标分数：7.5
- 考试日期：YYYY-MM-DD
- 考试类型：Academic / General Training

## 当前水平
- 总分：6.5
- 听力：7.0
- 阅读：6.5
- 写作：6.0
- 口语：6.0
- 测评日期：YYYY-MM-DD
- 测评来源：模考 / 真考

## 薄弱科目
1. 写作（6.0 → 目标 6.5）
2. 口语（6.0 → 目标 6.5）

## 策略
- 默认优先听力阅读；如有单项小分要求，先补最低单项
```

### plan.md

```markdown
---
type: plan
created: YYYY-MM-DD
exam_date: YYYY-MM-DD
weeks: 8
---

# 8 周备考计划

## 第 1 周：诊断 + 基础
| 日 | 科目 | 任务 | 时长 |
|----|------|------|------|
| 一 | 词汇 | 背 15 新词 + 复习旧词 | 45min |
| 二 | 阅读 | 做一套 + 精读四步法 | 1h45min |
| ... | ... | ... | ... |
```

### writing/{date}-{task}-{seq}.md

```markdown
---
type: writing
date: YYYY-MM-DD
task: 1/2
topic: "Some people think..."
word_count: 280
scores:
  tr: 6.5
  cc: 6.0
  lr: 6.5
  gra: 6.0
  total: 6.5
---

# 写作批改记录

## 原文
{用户原文}

## 四维评分
{评分详情}

## 逐段分析
{句子级标注}

## 改写对比
{目标分数版本}

## 提分优先级
{具体建议}
```

### reading/{date}-{test}-{passage}.md

```markdown
---
type: reading
date: YYYY-MM-DD
test: "Cambridge 18 Test 1 Passage 2"
correct: 12
total: 13
accuracy: 92%
---

# 阅读分析记录

## 错题分析
{逐题拆解}

## 同义替换词表
{提取的同义替换}

## 生词
{不认识的词 → 自动入库 vocab/wordbank.md}

## 长难句
{拆解的长难句 + 同结构练习}
```

### listening/{date}-{test}-{section}.md

```markdown
---
type: listening
date: YYYY-MM-DD
test: "Cambridge 18 Test 1 Section 3"
correct: 8
total: 10
accuracy: 80%
---

# 听力分析记录

## 错题分析
{逐题分析}

## 听不懂的词/表达
{列表}

## 精听建议
{针对错题的精听任务}
```

### vocab/wordbank.md

```markdown
---
type: wordbank
updated: YYYY-MM-DD
total_words: 156
---

# 生词库

## 场景：自然地理
| 词 | 词性 | 中文 | 语境例句 | 来源 | 掌握 |
|----|------|------|---------|------|------|
| erosion | n. | 侵蚀 | The erosion of the coastline... | C18T1P2 | ❌ |

## 场景：经济学
| ... |
```

### vocab/synonyms.md

```markdown
---
type: synonyms
updated: YYYY-MM-DD
total_pairs: 89
---

# 同义替换库

| 题目用词 | 原文用词 | 出处 | 掌握 |
|---------|---------|------|------|
| significant | substantial | C18T1P2-Q3 | ❌ |
| decline | deteriorate | C18T1P2-Q5 | ✅ |
```

### vocab/review-log.md

```markdown
---
type: review-log
updated: YYYY-MM-DD
total_reviews: 12
---

# 词汇复习记录

## YYYY-MM-DD
- 测试词数：30
- 正确：24（80%）
- 错误：6
- 间隔：第 2 天复习
- 错误词汇：erosion, deteriorate, substantial, accumulate, furthermore, nonetheless

## YYYY-MM-DD
- 测试词数：15
- 正确：15（100%）
- 错误：0
- 间隔：第 4 天复习
- 错误词汇：无
```

### speaking/summary.md

```markdown
---
type: speaking-summary
updated: YYYY-MM-DD
stories_count: 5
topics_covered: 38
topics_total: 50
coverage: 76%
---

# 口语进度汇总

## 万能故事
| # | 故事标题 | 覆盖话题数 | 状态 |
|---|---------|-----------|------|
| 1 | 香港旅行 | 12 | ✅ 已练熟 |
| 2 | 大学老师 | 10 | ✅ 已练熟 |
| 3 | 学吉他 | 8 | 🔄 练习中 |
| 4 | 创业失败 | 6 | 🔄 练习中 |
| 5 | 三体 | 2 | ❌ 未开始 |

## 练习记录
| 日期 | 内容 | 时长 |
|------|------|------|
| YYYY-MM-DD | Part 2 练习 2 个话题 | 30min |
```

---

## 规则

1. **文件名用日期前缀**：方便按时间排序
2. **frontmatter 必填**：type + date + 关键指标
3. **生词入库自动化**：阅读/听力分析后自动追加到 wordbank.md
4. **同义替换去重**：按题目用词 + 原文用词去重
5. **summary 文件可选**：优先从 `events.jsonl` 生成趋势；summary 是人类阅读层
6. **数据只增不删**：历史记录永远保留，用 `状态` 字段标记状态
