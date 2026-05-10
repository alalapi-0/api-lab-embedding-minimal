# LEARNING — api-lab-embedding-minimal

> 这份文件回答：「我跑完这个仓库，应该真的学到什么？」

## 你跑完应该能回答的问题

1. embedding 模型和 LLM **不是同一类东西**——它们各自的输入输出是什么？
2. 「向量」「维度」「余弦相似度」分别在描述什么？
3. 为什么大家叫 embedding 是"语义指纹"？它能干什么，不能干什么？
4. 如果有一天你要做 RAG（检索增强生成），embedding 在这个流程里扮演什么角色？

## 实操验证清单（务必动手）

### 阶段 A — 环境就绪
- [ ] `python3 -m venv .venv && source .venv/bin/activate`
- [ ] `pip install -r requirements.txt`（会装 torch + sentence-transformers，几分钟）
- [ ] 默认 `EMBEDDING_MODEL` 已在脚本里，**不需要 .env**

### 阶段 B — 跑通最小调用
- [ ] `python3 main.py`
  - 第一次会下载 ~470MB 模型权重到 `~/.cache/huggingface/`
  - 之后再跑就只是秒级加载
- [ ] 看终端打印的：
  - 向量维度（应该是 384）
  - cosine similarity（应该在 0.7~0.9 之间）

### 阶段 C — 改输入做对照实验（关键）
**embedding 真正的乐趣在于"改输入看相似度变化"。**

- [ ] 把 `SENTENCE_B` 改成**完全无关**的句子，比如「今天天气真好」
  - 重跑 → cosine 应该明显变低（0.2~0.4 区间）
- [ ] 把 `SENTENCE_B` 改成 `SENTENCE_A` 的英文翻译："I want to learn how to call APIs."
  - 重跑 → 因为模型是多语言的，相似度仍然会比较高
- [ ] 把 `SENTENCE_B` 改成 `SENTENCE_A` 完全相同的内容
  - 重跑 → cosine 应该 ≈ 1.0
- [ ] 把 `SENTENCE_B` 改成"我不想学习 API 调用。"（取反）
  - 重跑 → 注意：cosine **不会**因为"语义相反"而变成 -1，多半还是挺高（embedding 看的是"主题相似"，不是"立场对立"）
  - **这是教科书级别的常见陷阱**

### 阶段 D — 维度 vs 模型对比（可选）
- [ ] 把 `EMBEDDING_MODEL` 改成 `sentence-transformers/all-MiniLM-L6-v2`（更小，只支持英文）
- [ ] 重跑 → 维度可能变成 384，但中文相似度可能突然变差（这是只学过英文的代价）
- [ ] 改回多语言模型

### 阶段 E — 思考连接 RAG
- [ ] 假设你有 1000 篇笔记，想做"问问题，找最相关的笔记"：
  1. 先用 embedding 把 1000 篇都变成向量，存进向量数据库（Qdrant/FAISS/...）
  2. 用户问题来了 → 也变成向量
  3. 在向量数据库里找 cosine 最高的几篇 → 给 LLM 当上下文
- [ ] 上面这个流程就是 RAG，**embedding 是它的第一阶段**
- [ ] 本仓库**故意**没做完整 RAG，让你先把 embedding 这一阶单独搞清楚

## 自检题

1. 一个 384 维的向量是啥意思？模型是从这 384 个数字里读出"语义"的吗？
2. 我自己手算 cosine：把模型输出的两个向量复制出来，能不能用纸笔验证 main.py 算出的那个数？
3. 如果我把 `SENTENCE_A` 多打几个空格，相似度会变吗？为什么？
4. 在做"语义搜索"的时候，cosine 0.85 算高还是低？取决于什么？

## 与其它仓库的连接

| 关系 | 仓库 | 为什么去看 |
| --- | --- | --- |
| **小模型对照** | `api-lab-whisper-asr-minimal` | embedding（文→向量）和 ASR（声→文）是另外两种"非聊天"的小模型；放一起看你会有"AI 不只是 chat"的直觉 |
| **下一步进阶** | `api-lab-tool-calling-minimal` | RAG 经常和 tool-calling 联用：先 embedding 检索，再让 LLM 调工具或回答 |
| **本地 vs 云端** | `api-lab-ollama-local-minimal` | 本地小 LLM + 本地 embedding，是搭建私有 RAG 的常见组合 |

## 你应该感受到的"啊哈"瞬间

- 当你看见 `[0.0123, -0.0456, ...]` 一长串数字，模型却用它"知道"两句话是同一个意思——**这是你第一次摸到"分布式表示"**。
- 当你输入"我喜欢猫"和"我讨厌猫"，cosine 居然挺高——**你瞬间理解了"语义相似 ≠ 立场相同"**，以后再也不会把 embedding 当成万能搜索引擎了。
- 当你想到"这玩意儿能塞进数据库"——你已经为下一阶 RAG 做好了脑回路。
