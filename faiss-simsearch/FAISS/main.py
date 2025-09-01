import os
from tqdm import tqdm
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate

from config import CODE_DIR, FILE_EXTENSIONS, SIMILARITY_THRESHOLD, TOP_K
from embedding import get_embedding
from preprocessing import preprocess
from function_extraction import extract_functions

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

def compute_combined_similarity(funcs_a, funcs_b):
    detailed_results = []

    for fa in funcs_a:
        emb_code_a = get_embedding(fa['code'])

        for fb in funcs_b:
            emb_code_b = get_embedding(fb['code'])
            sim_code = cosine_similarity([emb_code_a], [emb_code_b])[0][0]

            detailed_results.append({
                "func_a": fa["name"],
                "func_b": fb["name"],
                "combined": sim_code
            })

    return detailed_results

def main():
    file_paths = get_code_files(CODE_DIR)
    print(f"[INFO] Found {len(file_paths)} code files.")

    all_file_functions = []
    for path in tqdm(file_paths, desc="Extracting functions"):
        code = read_file(path)
        processed_code = preprocess(code)
        functions = extract_functions(processed_code)
        all_file_functions.append(functions)

    print("\n[INFO] Computing function-to-function similarities...\n")
    file_count = len(all_file_functions)

    all_comparisons = []
    best_matches = []

    for i in range(file_count):
        for j in range(i + 1, file_count):
            funcs_a = all_file_functions[i]
            funcs_b = all_file_functions[j]

            if not funcs_a or not funcs_b:
                continue

            results = compute_combined_similarity(funcs_a, funcs_b)

            for r in results:
                all_comparisons.append({
                    "file_a": file_paths[i],
                    "func_a": r["func_a"],
                    "file_b": file_paths[j],
                    "func_b": r["func_b"],
                    "combined": r["combined"]
                })

            best_match = max(results, key=lambda x: x["combined"])
            best_matches.append({
                "file_a": file_paths[i],
                "file_b": file_paths[j],
                "similarity": best_match["combined"],
                "func_a": best_match["func_a"],
                "func_b": best_match["func_b"]
            })

    # --- Print DETAILED RESULTS (function-level) in descending order ---
    print("[INFO] Detailed Function-to-Function Matches (Descending Similarity):\n")
    all_comparisons_sorted = sorted(all_comparisons, key=lambda x: x["combined"], reverse=True)

    table_rows = []
    for comp in all_comparisons_sorted:
        table_rows.append([
            os.path.basename(comp["file_a"]),
            comp["func_a"],
            os.path.basename(comp["file_b"]),
            comp["func_b"],
            f"{comp['combined']:.3f}"
        ])

    print(tabulate(
        table_rows,
        headers=["File A", "Func A", "File B", "Func B", "Similarity"],
        tablefmt="github"
    ))

    # --- Print SUMMARY (file-level best matches) using threshold and top-k ---
    best_matches_sorted = sorted(best_matches, key=lambda x: x["similarity"], reverse=True)
    best_matches_sorted = [m for m in best_matches_sorted if m["similarity"] >= SIMILARITY_THRESHOLD][:TOP_K]

    print(f"\n[INFO] Final Summary of File-Level Best Matches (Top {TOP_K} with Similarity >= {SIMILARITY_THRESHOLD}):\n")
    for match in best_matches_sorted:
        file_a = os.path.basename(match['file_a'])
        file_b = os.path.basename(match['file_b'])
        print(f"[{match['similarity']:.3f}] {file_a} <--> {file_b}")
        print(f"  - Functions: {match['func_a']} <--> {match['func_b']}\n")

if __name__ == "__main__":
    main()
