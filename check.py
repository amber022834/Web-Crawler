import os

img_dir = r"\\120.127.241.127\工讀生專用\108\一校"
txt_dir = r"\\120.127.241.127\工讀生專用\110\二校"

img_ext = {'.jpg', '.jpeg', '.png', '.webp'}

# 正規化函式（關鍵）
def clean(name):
    return name.strip().lower()

# 收集 txt
txt_set = set()

for root, dirs, files in os.walk(txt_dir):
    for f in files:
        if f.lower().endswith(".txt"):
            name = os.path.splitext(f)[0]
            txt_set.add(clean(name))

missing_txt = []

# 掃圖片
for root, dirs, files in os.walk(img_dir):
    for f in files:
        ext = os.path.splitext(f)[1].lower()

        if ext in img_ext:
            name = clean(os.path.splitext(f)[0])

            if name not in txt_set:
                missing_txt.append(os.path.join(root, f))

print("=== 一校有圖，但二校沒有對應文字檔 ===")
for i in missing_txt:
    print(i)

print("\n完成")