import os

# 設定路徑 (建議檢查資料夾路徑是否正確)
img_dir = r"\\120.127.241.127\工讀生專用\110\二校\0000"
txt_dir = r"\\120.127.241.127\工讀生專用\110\二校\0000"

img_ext = {'.jpg', '.jpeg', '.png', '.webp'}

def clean(name):
    return name.strip().lower()

# 1. 收集所有文字檔名 (不含副檔名)
txt_dict = {} # 使用字典存 {主檔名: 完整路徑}
for root, dirs, files in os.walk(txt_dir):
    for f in files:
        if f.lower().endswith(".txt"):
            name = clean(os.path.splitext(f)[0])
            txt_dict[name] = os.path.join(root, f)

# 2. 收集所有圖片檔名 (不含副檔名)
img_dict = {}
for root, dirs, files in os.walk(img_dir):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in img_ext:
            name = clean(os.path.splitext(f)[0])
            img_dict[name] = os.path.join(root, f)

# 3. 比對邏輯
missing_txt = [path for name, path in img_dict.items() if name not in txt_dict]
missing_img = [path for name, path in txt_dict.items() if name not in img_dict]

# --- 輸出結果 ---

print(f"--- 檢查報告 ---")
print(f"圖片總數: {len(img_dict)}")
print(f"文字總數: {len(txt_dict)}")
print("-" * 30)

if missing_txt:
    print(f"\n❌ [有圖片、沒文字] 共 {len(missing_txt)} 件:")
    for path in missing_txt:
        print(path)
else:
    print("\n✅ 所有圖片都有對應的文字檔。")

if missing_img:
    print(f"\n⚠️ [有文字、沒圖片] 共 {len(missing_img)} 件 (請確認是否正常):")
    for path in missing_img:
        print(path)

print("\n檢查完成")