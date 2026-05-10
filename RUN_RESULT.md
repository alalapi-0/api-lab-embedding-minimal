# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 是否已运行 | 否 |
| 运行时间 | — |
| 是否成功 | — |
| 模型名 | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2（默认，未实跑） |
| 向量维度 | — |
| cosine similarity | — |
| 错误原因 | — |

## 备注

- 仓库已生成，**未实际运行**。
- 不实跑的原因：
  1. `sentence-transformers` + `torch` 安装包较大（约 500MB+），不在「初始化每个仓库就装一遍」的范围。
  2. 第一次运行还会从 HuggingFace 下载几百 MB 模型权重，需要你确认网络可用。
- 跑通后请把表里的 `向量维度` 和 `cosine similarity` 真实值回填进来。

## 运行日志（你跑完后手动追加）

```
（在这里粘贴 main.py 的终端输出片段）
```
