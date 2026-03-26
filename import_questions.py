#!/usr/bin/env python3
# import_questions.py
# - Đọc khối câu hỏi bạn dán (user_questions.txt) hoặc RAW_INPUT trong mã
# - Trích các cặp {"q":"...","a":"..."} bằng regex linh hoạt
# - Loại bỏ trùng lặp (dựa trên q+a)
# - Bổ sung câu (từ templates/pool) nếu cần để đạt 400 câu
# - Ghi questions.json với encoding utf-8 và ensure_ascii=False

import re
import json
import random
import os
import sys

# Nếu bạn muốn paste trực tiếp vào script, thay RAW_INPUT = None bằng chuỗi của bạn (kèm newline)
RAW_INPUT = None
INPUT_FILENAME = "user_questions.txt"
OUT_FILENAME = "questions.json"
TARGET_COUNT = 400

# Pool and templates used for filler generation (can be expanded)
POOL = [
    "mèo","chó","cá","chim","gà","vịt","bò","ngựa","trâu","dê","thỏ","rùa","ếch","kiến","ong",
    "cây","hoa","lá","rừng","núi","sông","biển","mặt trời","mặt trăng","mây","mưa","gió",
    "bóng tối","ánh sáng","đất","nước","lửa","nhà","xe máy","ô tô","điện thoại","máy tính",
    "sách","bút","vở","bàn","ghế","giường","tủ","cửa","ví","tiền","phở","cơm","bánh mì","trứng",
    "táo","chuối","cam","xoài","dưa hấu","khoai tây","gạo","bếp","tivi","đàn piano","con tem"
]
TEMPLATES = [
    "Đố mẹo: {hint}. Bạn đoán là gì?",
    "Đố chữ: {hint}. Đáp án là gì?",
    "Câu đố: {hint}. Là gì?",
    "Đố vui: {hint}. Bạn biết không?",
    "Hỏi: {hint}. Là gì?"
]

def read_input():
    if RAW_INPUT:
        return RAW_INPUT
    if os.path.exists(INPUT_FILENAME):
        with open(INPUT_FILENAME, "r", encoding="utf-8") as f:
            return f.read()
    print(f"Không tìm thấy {INPUT_FILENAME} và RAW_INPUT = None. Hãy lưu khối câu hỏi vào {INPUT_FILENAME} hoặc set RAW_INPUT.")
    sys.exit(1)

def extract_pairs(text):
    pairs = []
    # Try to parse valid JSON list first
    try:
        candidate = json.loads(text)
        if isinstance(candidate, list):
            for it in candidate:
                if isinstance(it, dict) and "q" in it and "a" in it:
                    pairs.append((str(it["q"]).strip(), str(it["a"]).strip()))
            if pairs:
                return pairs
    except Exception:
        pass

    # Fallback: regex extraction of patterns like {"q": "....", "a": "...."}
    # This is tolerant: it finds occurrences of "q": "..." and "a": "..." near each other.
    # It may not catch entries with nested quotes; if so, please pre-escape or provide valid JSON.
    pattern = re.compile(
        r'"q"\s*:\s*"([^"]+)"\s*,\s*"a"\s*:\s*"([^"]+)"',
        flags=re.IGNORECASE | re.DOTALL
    )
    for m in pattern.finditer(text):
        q = m.group(1).strip()
        a = m.group(2).strip()
        pairs.append((q, a))

    # Another pattern variant for single-quoted or with spaces
    if not pairs:
        pattern2 = re.compile(r"\{\s*['\"]q['\"]\s*:\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]a['\"]\s*:\s*['\"]([^'\"]+)['\"]\s*\}", flags=re.DOTALL)
        for m in pattern2.finditer(text):
            pairs.append((m.group(1).strip(), m.group(2).strip()))

    return pairs

def normalize_for_dedupe(q, a):
    # simple normalization for deduping
    return (re.sub(r"\s+", " ", q).strip().lower(), re.sub(r"\s+", " ", a).strip().lower())

def generate_filler(existing_set, needed):
    fillers = []
    seen_answers = set(a for (_, a) in existing_set)
    # create synthetic hints combining pool and templates
    idx = 0
    while len(fillers) < needed:
        noun = random.choice(POOL)
        if noun in seen_answers:
            # still allow duplicates of answers? skip to increase uniqueness
            noun = noun + ("" if idx==0 else f"_{idx}")
        hint = f"gợi ý: {noun}"
        q = random.choice(TEMPLATES).format(hint=hint)
        a = noun
        key = (q, a)
        k_norm = normalize_for_dedupe(q, a)
        if k_norm in existing_norms or any(normalize_for_dedupe(x,y)==k_norm for (x,y) in fillers):
            idx += 1
            continue
        fillers.append((q, a))
        idx += 1
    return fillers

if __name__ == "__main__":
    raw = read_input()
    pairs = extract_pairs(raw)
    print(f"Đã trích được {len(pairs)} cặp câu hỏi từ input.")

    # Deduplicate preserving order
    unique = []
    seen = set()
    for q,a in pairs:
        key = normalize_for_dedupe(q,a)
        if key not in seen:
            unique.append((q,a))
            seen.add(key)
    print(f"Sau loại trùng: {len(unique)} cặp.")

    # If less than target, generate fillers
    existing_norms = set(normalize_for_dedupe(q,a) for q,a in unique)
    if len(unique) < TARGET_COUNT:
        need = TARGET_COUNT - len(unique)
        print(f"Cần thêm {need} câu nữa để đạt {TARGET_COUNT}. Đang tạo câu phụ...")
        fillers = []
        # Use deterministic filler generation to be repeatable
        random.seed(42)
        idx = 0
        while len(fillers) < need:
            noun = random.choice(POOL)
            q = random.choice(TEMPLATES).format(hint=f"từ {noun}")
            a = noun
            k_norm = normalize_for_dedupe(q,a)
            if k_norm in existing_norms:
                idx += 1
                continue
            fillers.append((q,a))
            existing_norms.add(k_norm)
        unique.extend(fillers)
        print(f"Đã thêm {len(fillers)} câu phụ.")
    elif len(unique) > TARGET_COUNT:
        # Trim to TARGET_COUNT
        unique = unique[:TARGET_COUNT]
        print(f"Cắt xuống còn {TARGET_COUNT} câu.")

    # Shuffle final list
    random.shuffle(unique)

    # Build dict list
    out_list = [{"q": q, "a": a} for q,a in unique]

    # Write to questions.json with utf-8 and ensure_ascii=False
    with open(OUT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(out_list, f, ensure_ascii=False, indent=2)
    print(f"Viết {len(out_list)} câu vào {OUT_FILENAME} (utf-8, ensure_ascii=False).")