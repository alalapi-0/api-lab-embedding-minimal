"""api-lab-embedding-minimal

体验「embedding 模型」最小调用：
- 把两句话各自变成一个向量
- 打印向量维度
- 算两个向量的余弦相似度

embedding 模型不是聊天模型！它的输入是文本，输出是数字数组。
本仓库默认用一个体积较小的 sentence-transformers 多语言模型。
"""

import json
import math
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

SENTENCE_A = "我想学习 API 调用。"
SENTENCE_B = "我想知道怎么连接模型接口。"


def cosine(a, b) -> float:
    """手算 cosine similarity，避免依赖 numpy 之外的额外包。"""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def main() -> int:
    load_dotenv()
    model_name = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ).strip()

    print(f"[信息] 模型名: {model_name}")
    print("[信息] 第一次运行时会从 HuggingFace 下载模型权重（几十~几百 MB）。")
    print("       如果当前网络不通，请稍后再试。本脚本不会反复重试。")

    try:
        # 故意把 import 放进 main，便于错误提示更友好
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("[失败] 没装 sentence-transformers。请先运行: pip install -r requirements.txt")
        return 2

    started = time.time()
    try:
        model = SentenceTransformer(model_name)
    except Exception as exc:  # 包括网络错误、模型文件错误等
        print(f"[失败] 加载/下载模型失败: {exc}")
        print("       常见原因: 当前网络无法访问 HuggingFace、磁盘空间不足、模型名拼错。")
        return 1
    load_elapsed = time.time() - started
    print(f"[信息] 模型加载耗时 {load_elapsed:.2f}s")

    print(f"[信息] 句子 A: {SENTENCE_A}")
    print(f"[信息] 句子 B: {SENTENCE_B}")

    started = time.time()
    embeddings = model.encode([SENTENCE_A, SENTENCE_B])
    encode_elapsed = time.time() - started

    vec_a = list(map(float, embeddings[0]))
    vec_b = list(map(float, embeddings[1]))

    sim = cosine(vec_a, vec_b)

    print()
    print("[成功] 输出结果：")
    print(f"  向量 A 维度: {len(vec_a)}")
    print(f"  向量 B 维度: {len(vec_b)}")
    print(f"  cosine similarity: {sim:.4f}")
    print(f"  encode 耗时: {encode_elapsed:.2f}s")

    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)
    result = {
        "model": model_name,
        "sentence_a": SENTENCE_A,
        "sentence_b": SENTENCE_B,
        "dim_a": len(vec_a),
        "dim_b": len(vec_b),
        "cosine_similarity": round(sim, 6),
        "encode_seconds": round(encode_elapsed, 3),
        "load_seconds": round(load_elapsed, 3),
        # 不写完整向量，太长了；只存前 8 维做样例
        "vec_a_preview": [round(x, 6) for x in vec_a[:8]],
        "vec_b_preview": [round(x, 6) for x in vec_b[:8]],
    }
    out_file = out_dir / "result.json"
    out_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[信息] 已写入 {out_file}（不会被 git 提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
