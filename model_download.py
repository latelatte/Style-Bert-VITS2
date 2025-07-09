import os
import subprocess

def download_model():
    if not os.path.exists("model_assets/himari-v3/model.pth"):
        print("モデルをダウンロード中…")
        subprocess.run([
            "gdown", "--folder", "https://drive.google.com/drive/folders/1pePr_0dj_f77NXngyFBAscbruWpKgwG3?usp=sharing"
        ], check=True)

        # gdown --folder が himari-v3/himari-v3/... を作ってしまった場合に備えて
        if os.path.exists("himari-v3/himari-v3"):
            subprocess.run(["mv", "himari-v3/himari-v3", "model_assets/"], check=True)
        elif os.path.exists("himari-v3"):
            subprocess.run(["mv", "himari-v3", "model_assets/"], check=True)

        print("モデルダウンロード完了")