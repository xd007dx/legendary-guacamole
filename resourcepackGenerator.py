from tkinter import filedialog, Tk
from PIL import Image
import os
import random
import json
import zipfile

def procedure():
    # GUI 初期化
    root = Tk()
    root.withdraw()

    # 対象の鉱石ブロック（バニラに存在する鉱石関連）
    TARGET_BLOCKS = {
        "coal_ore": "blocks/coal_ore.png",
        "deepslate_coal_ore": "blocks/deepslate_coal_ore.png",
        "iron_ore": "blocks/iron_ore.png",
        "deepslate_iron_ore": "blocks/deepslate_iron_ore.png",
        "gold_ore": "blocks/gold_ore.png",
        "deepslate_gold_ore": "blocks/deepslate_gold_ore.png",
        "redstone_ore": "blocks/redstone_ore.png",
        "deepslate_redstone_ore": "blocks/deepslate_redstone_ore.png",
        "lapis_ore": "blocks/lapis_ore.png",
        "deepslate_lapis_ore": "blocks/deepslate_lapis_ore.png",
        "diamond_ore": "blocks/diamond_ore.png",
        "deepslate_diamond_ore": "blocks/deepslate_diamond_ore.png",
        "emerald_ore": "blocks/emerald_ore.png",
        "deepslate_emerald_ore": "blocks/deepslate_emerald_ore.png",
        "copper_ore": "blocks/copper_ore.png",
        "deepslate_copper_ore": "blocks/deepslate_copper_ore.png",
        "nether_gold_ore": "blocks/nether_gold_ore.png",
        "nether_quartz_ore": "blocks/nether_quartz_ore.png",
        "raw_iron_block": "blocks/raw_iron_block.png",
        "raw_gold_block": "blocks/raw_gold_block.png",
        "raw_copper_block": "blocks/raw_copper_block.png",
        "coal_block": "blocks/coal_block.png",
        "iron_block": "blocks/iron_block.png",
        "gold_block": "blocks/gold_block.png",
        "copper_block": "blocks/copper_block.png",
        "lapis_block": "blocks/lapis_block.png",
        "diamond_block": "blocks/diamond_block.png",
        "emerald_block": "blocks/emerald_block.png",
        "redstone_block": "blocks/redstone_block.png",
        "netherite_block": "blocks/netherite_block.png"
    }

    RESOURCE_PACK_NAME = "RandomizedOrePack"
    TARGET_SIZE = (512, 512)
    NUM_VARIANTS = 3

    # フォルダ選択（画像ソース）
    image_folder = filedialog.askdirectory(title="画像フォルダを選択してください")
    if not image_folder:
        raise Exception("画像フォルダが選択されませんでした。")

    # 保存先選択（Zipで保存）
    save_path = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("ZIPファイル", "*.zip")],
        title="保存先を選択してください",
        initialfile=RESOURCE_PACK_NAME + ".zip"
    )
    if not save_path:
        raise Exception("保存先が選択されませんでした。")

    # 利用可能な画像を取得
    all_images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(".png")]
    needed = NUM_VARIANTS * len(TARGET_BLOCKS)
    if len(all_images) < needed:
        raise Exception(f"画像が不足しています。最低でも {needed} 枚必要です。")

    random.shuffle(all_images)

    # 一時作業フォルダ
    temp_base = os.path.join(os.getcwd(), RESOURCE_PACK_NAME)
    os.makedirs(temp_base, exist_ok=True)

    for i in range(NUM_VARIANTS):
        variant_name = f"variant_{i+1}"
        variant_dir = os.path.join(temp_base, variant_name, "assets", "minecraft", "textures", "block")
        os.makedirs(variant_dir, exist_ok=True)

        used = all_images[i * len(TARGET_BLOCKS):(i + 1) * len(TARGET_BLOCKS)]
        block_images = {}

        for (block_name, rel_path), image_path in zip(TARGET_BLOCKS.items(), used):
            dest_path = os.path.join(variant_dir, os.path.basename(rel_path))
            img = Image.open(image_path).convert("RGBA").resize(TARGET_SIZE)
            img.save(dest_path)
            block_images[block_name] = image_path

        # pack.mcmeta を作成
        pack_meta = {
            "pack": {
                "pack_format": 15,  # Minecraft 1.20.x 用
                "description": f"Randomized Ore Pack Variant {i+1}"
            }
        }
        with open(os.path.join(temp_base, variant_name, "pack.mcmeta"), "w", encoding="utf-8") as f:
            json.dump(pack_meta, f, ensure_ascii=False, indent=2)

        # coal_block の画像を pack.png としてコピー
        coal_img_path = block_images.get("coal_block")
        if coal_img_path:
            img = Image.open(coal_img_path).convert("RGBA").resize((128, 128))
            img.save(os.path.join(temp_base, variant_name, "pack.png"))

    # 最後に全バリアントを ZIP にまとめる
    with zipfile.ZipFile(save_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root_dir, _, files in os.walk(temp_base):
            for file in files:
                full_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(full_path, temp_base)
                zipf.write(full_path, arcname)

    print("✅ 完了しました！作成されたZIPファイル:", save_path)

def main():
    procedure()
