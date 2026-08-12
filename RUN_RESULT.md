# RUN_RESULT

| 字段 | 值 |
| --- | --- |
| 是否已加载真实模型 | 否 |
| 离线合同验证时间 | 2026-08-12 |
| 离线合同验证是否成功 | 是 |
| 模型名 | 未使用真实模型；成功路径使用内存 stub `test-embedding-model` |
| 向量维度 | stub 验证为 3；不代表默认真实模型 |
| cosine similarity | stub 验证为 0.5 |
| 未实跑原因 | 宿主缺少 `sentence-transformers`，且真实运行需安装大型依赖并下载模型权重 |

## 备注

- 本轮未安装 `sentence-transformers` / Torch，未联系 Hugging Face，未下载权重。直接运行能力记为 `BLOCKED_ENV`。
- 在仓库外 disposable archive 中使用内存 stub 验证：cosine 同向/正交/零向量边界；缺少重依赖时 exit 2；确定性两向量成功编码与 JSON 写入；模型加载异常时失败。
- 真实模型的维度、相似度与耗时仍待另行授权实跑；stub 数值不是产品证据。

## 运行日志（你跑完后手动追加）

```text
offline-contract-tests: PASS (cosine, missing dependency, success, load failure)
syntax: PASS
```
