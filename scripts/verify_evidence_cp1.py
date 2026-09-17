"""
Script xác minh bằng chứng (Evidence Verification) cho CP1 - Track A1: VLearn Tutor
Chạy lệnh: python scripts/verify_evidence_cp1.py
"""
import csv
import os
import sys

# Đảm bảo in UTF-8 trên Windows terminal
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'vlearn-pack', 'chatlog', 'tutor_turns.csv')

def verify():
    if not os.path.exists(DATA_PATH):
        print(f"Không tìm thấy file: {DATA_PATH}")
        return

    total = 0
    k4_total = 0
    no_cite_total = 0
    no_cite_k4 = 0
    preset_total = 0
    probing_total = 0
    highlight_no_cite = 0
    
    samples = []
    
    with open(DATA_PATH, mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            is_k4 = (row.get('cohort_hint') == 'K4')
            if is_k4:
                k4_total += 1
                
            has_cite = row.get('has_citation', '').strip().lower() in ['true', '1', 't']
            if not has_cite:
                no_cite_total += 1
                if is_k4:
                    no_cite_k4 += 1
            
            q = row.get('student_question', '')
            if 'đoạn được chọn:' in q and not has_cite:
                highlight_no_cite += 1
                
            if row.get('is_preset', '').strip().lower() in ['true', '1', 't']:
                preset_total += 1
                
            if row.get('move_used') == 'ask_probing_question':
                probing_total += 1
                
            tid = row.get('turn_id')
            if tid in ['T00009', 'T00213', 'T10288', 'T10289', 'T10301']:
                samples.append(row)

    print("=" * 65)
    print(" BÁO CÁO XÁC MINH BẰNG CHỨNG (DATA MINING EVIDENCE) - TRACK A1")
    print("=" * 65)
    print(f"• Tổng số lượt hỏi-đáp trong dataset:         {total:,} lượt")
    print(f"• Số lượt tutor KHÔNG có trích dẫn nguồn:    {no_cite_total:,} ({no_cite_total/total*100:.2f}%)")
    print(f"• Số lượt riêng khóa K4:                     {k4_total:,} lượt")
    print(f"• Số lượt K4 KHÔNG có trích dẫn nguồn:       {no_cite_k4:,} ({no_cite_k4/k4_total*100:.2f}%)")
    print(f"• Số lượt có bôi đen nhưng vẫn KHÔNG có cite: {highlight_no_cite:,} lượt")
    print(f"• Tỷ lệ câu hỏi mẫu bấm sẵn (is_preset):     {preset_total:,} ({preset_total/total*100:.2f}%)")
    print(f"• Tỷ lệ tutor hỏi ngược (probing question):   {probing_total:,} ({probing_total/total*100:.2f}%)")
    print("=" * 65)
    print(" CÁC VÍ DỤ NGUYÊN VĂN MINH CHỨNG TỪ CHATLOG:")
    print("=" * 65)
    for s in samples:
        print(f"\n[Mã Turn: {s.get('turn_id')}] (Cohort: {s.get('cohort_hint')}, has_citation={s.get('has_citation')})")
        print(f"  Câu hỏi: {s.get('student_question')[:130]}...")
        print(f"  Trả lời: {s.get('tutor_reply')[:160]}...")
    print("\n" + "=" * 65)

if __name__ == '__main__':
    verify()
