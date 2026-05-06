import os

img_dir = r"\\120.127.241.127\cfrt\111-115語料資料夾\中介語\大考中心資料108-109\109 (原稿)"
txt_dir = r"\\120.127.241.127\cfrt\111-115語料資料夾\中介語\大考中心資料108-109\109 (二校)"

img_ext = {'.jpg', '.jpeg', '.png', '.webp'}

# ① 收集二校 txt
txt_set = set()
for root, dirs, files in os.walk(txt_dir):
    for f in files:
        if f.lower().endswith(".txt"):
            txt_set.add(os.path.splitext(f)[0])

# ② 收集原稿圖片
img_set = set()
img_map = {}

for root, dirs, files in os.walk(img_dir):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in img_ext:
            name = os.path.splitext(f)[0]
            img_set.add(name)
            img_map[name] = os.path.join(root, f)

# ③ 原稿有圖，但二校沒有 txt
missing_txt = [img_map[i] for i in img_set if i not in txt_set]

# ④ 二校有 txt，但原稿沒有圖
missing_img = [i for i in txt_set if i not in img_set]

print("=== 原稿有圖，但二校沒有文字 ===")
for i in missing_txt:
    print(i)

print("\n=== 二校有文字，但原稿沒有圖 ===")
for i in missing_img:
    print(i)

print("\n完成")