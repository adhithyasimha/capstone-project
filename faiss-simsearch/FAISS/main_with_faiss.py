import os
import ast
import re
import zss
import numpy as np
from tqdm import tqdm
from tabulate import tabulate

from config import CODE_DIR, FILE_EXTENSIONS, SIMILARITY_THRESHOLD, TOP_K
from embedding import get_embedding
from preprocessing import preprocess
from function_extraction import extract_functions
from faiss_index import build_faiss_index

def get_code_files(directory):
    code_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                code_files.append(os.path.join(root, file))
    return code_files

def read_file(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def ast_similarity_score(ast1_str, ast2_str):
    try:
        tree1 = ast.parse(ast1_str)
        tree2 = ast.parse(ast2_str)

        def get_label(node): return type(node).__name__
        def get_children(node): return list(ast.iter_child_nodes(node))

        distance = zss.simple_distance(
            tree1, tree2,
            get_children=get_children,
            get_label=get_label
        )
        return 1.0 / (1.0 + distance)
    except Exception:
        return 0.0

def behavior_signature(code):
    return {
        "has_loop": "for" in code or "while" in code,
        "has_recursion": any(fn in code and f"return {fn}" in code for fn in re.findall(r'def (\w+)', code)),
        "has_print": "print" in code,
        "has_condition": "if" in code or "elif" in code,
        "num_lines": len(code.splitlines())
    }

def main():
    file_paths = get_code_files(CODE_DIR)
    print(f"[INFO] Found {len(file_paths)} code files.")

    all_file_functions = []
    embedding_list = []
    metadata_list = []

    for path in tqdm(file_paths, desc="Extracting functions"):
        code = read_file(path)
        processed_code = preprocess(code)
        functions = extract_functions(processed_code)
        all_file_functions.append(functions)

        for func in functions:
            if len(func['code'].splitlines()) < 4:
                continue  # skip trivial functions

            embedding = get_embedding(func['code'])
            if not np.all(np.isfinite(embedding)) or np.linalg.norm(embedding) == 0:
                continue

            embedding_list.append(embedding)
            metadata_list.append({
                "file": path,
                "func_name": func["name"],
                "code": func["code"]
            })

    print(f"\n[INFO] Building FAISS index with {len(embedding_list)} function embeddings...")

    pooled_embeddings = [vec for vec in embedding_list if np.all(np.isfinite(vec)) and np.linalg.norm(vec) > 0]
    index, normalized_embeddings = build_faiss_index(pooled_embeddings)

    print(f"[INFO] Querying top-{TOP_K} most similar functions using FAISS...\n")
    D, I = index.search(normalized_embeddings, TOP_K + 1)

    results = []
    seen_pairs = set()

    alpha = 0.55  # cosine weight
    beta = 0.2   # AST weight
    gamma = 0.25  # behavior penalty weight

    for i, (distances, indices) in enumerate(zip(D, I)):
        source = metadata_list[i]
        for j, idx in enumerate(indices):
            if idx == i:
                continue
            target = metadata_list[idx]
            if source["file"] == target["file"]:
                continue

            key = tuple(sorted([
                source["file"] + source["func_name"],
                target["file"] + target["func_name"]
            ]))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)

            cosine_sim = float(distances[j])
            ast_sim = ast_similarity_score(source["code"], target["code"])
            behavior_src = behavior_signature(source["code"])
            behavior_tgt = behavior_signature(target["code"])

            penalty = 0
            if behavior_src["has_print"] != behavior_tgt["has_print"]:
                penalty += 0.05
            if behavior_src["has_loop"] != behavior_tgt["has_loop"]:
                penalty += 0.05
            if behavior_src["has_recursion"] != behavior_tgt["has_recursion"]:
                penalty += 0.1
            if abs(behavior_src["num_lines"] - behavior_tgt["num_lines"]) > 10:
                penalty += 0.05

            final_score = alpha * cosine_sim + beta * ast_sim - gamma * penalty

            results.append({
                "file_a": source["file"],
                "func_a": source["func_name"],
                "file_b": target["file"],
                "func_b": target["func_name"],
                "combined": final_score
            })

    results = sorted(results, key=lambda x: x["combined"], reverse=True)

    print("[INFO] Detailed Function-to-Function Matches (Descending Similarity):\n")
    table_rows = []
    for r in results:
        table_rows.append([
            os.path.basename(r["file_a"]),
            r["func_a"],
            os.path.basename(r["file_b"]),
            r["func_b"],
            f"{r['combined']:.3f}"
        ])
    print(tabulate(table_rows, headers=["File A", "Func A", "File B", "Func B", "Similarity"], tablefmt="github"))

    best_matches = {}
    for r in results:
        file_pair = tuple(sorted((r["file_a"], r["file_b"])))
        if file_pair not in best_matches or r["combined"] > best_matches[file_pair]["combined"]:
            best_matches[file_pair] = r

    top_matches = sorted(best_matches.values(), key=lambda x: x["combined"], reverse=True)
    top_matches = [m for m in top_matches if m["combined"] >= SIMILARITY_THRESHOLD][:TOP_K]

    print(f"\n[INFO] Final Summary of File-Level Best Matches (Top {TOP_K} with Similarity >= {SIMILARITY_THRESHOLD}):\n")
    for match in top_matches:
        file_a = os.path.basename(match['file_a'])
        file_b = os.path.basename(match['file_b'])
        print(f"[{match['combined']:.3f}] {file_a} <--> {file_b}")
        print(f"  - Functions: {match['func_a']} <--> {match['func_b']}\n")

if __name__ == "__main__":
    main()
