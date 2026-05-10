# api-lab-embedding-minimal

> 最小化体验：把两句话变成向量，看它们的 **余弦相似度**。

## 这个仓库不是聊天模型

请先在脑子里把这两类东西分开：

| 类型 | 输入 | 输出 | 干嘛用 |
| --- | --- | --- | --- |
| 聊天模型（LLM） | 一段文本 | 一段文本 | 回答、生成、推理 |
| **Embedding 模型** | 一段文本 | 一串浮点数（向量） | 衡量"语义相似"、检索、聚类、做 RAG |

如果你只跑过 `chat/completions`，那这是你第一次摸到 embedding。它**不会回答问题**，
它的产出是 `[0.0123, -0.0456, 0.0789, ...]` 这样长长的数字数组。

## 它在做什么

1. 加载 `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`（约 470MB，多语言，小巧）
2. 把两句话各自编码成向量
3. 计算两个向量的余弦相似度（范围 -1 到 1，越接近 1 越像）

输入两句话语义很接近：

- A: 我想学习 API 调用。
- B: 我想知道怎么连接模型接口。

预期 cosine 应该在 0.7~0.9 区间，**亲眼看到「语义相似」是数字也能量化的**。

## 运行步骤

```bash
cd api-lab-embedding-minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt        # 会装 torch + transformers，比前几个仓库慢一些

# 不一定要 cp .env.example .env，因为默认模型名脚本里就有
# 想改模型再 cp 然后改 EMBEDDING_MODEL

python3 main.py
cat output/result.json
```

第一次运行时会从 HuggingFace 下载几百 MB 模型权重，下载完缓存到 `~/.cache/huggingface/`，
之后再跑就是秒级加载。

## 常见报错

| 终端打印 | 可能原因 | 怎么处理 |
| --- | --- | --- |
| `没装 sentence-transformers` | 没装依赖 | `pip install -r requirements.txt` |
| `加载/下载模型失败` + 网络错误 | 下载 HF 权重失败 | 检查能否访问 huggingface.co；不要循环重试。可以换镜像或暂时挂代理 |
| 进程很慢甚至卡住 | 第一次下载 + CPU 推理 | 等几分钟；模型加载完后 encode 会很快 |
| 内存爆 | 你换了大 embedding 模型 | 用默认 MiniLM 即可，没必要追大模型 |

## 你应该能感受到的事

- **维度**：MiniLM 输出 384 维左右
- **相似度**：两句话语义接近，相似度高
- **可拓展**：把这个产出扔进向量数据库（Qdrant / FAISS / Milvus），就是 RAG 检索

但本仓库**不**做 RAG，本仓库只做"产出向量并对比"。

## .env.example

```
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

## 不会做的事

- 不会下载大模型（默认 MiniLM）
- 不会反复重试网络
- 不会拉一个向量数据库
- 不会做 RAG（那是另一类项目）
