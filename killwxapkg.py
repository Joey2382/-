import os
import subprocess

# --- 配置区域 ---
# KillWxapkg 工具的绝对路径
EXE_PATH = r"C:\KillWxapkg_2.4.1\KillWxapkg_2.4.1_windows_amd64.exe"
# 微信小程序包根目录
BASE_IN_DIR = r"C:\Users\Only_You\AppData\Roaming\Tencent\xwechat\radium\Applet\packages"
# 解密后存放的根目录
BASE_OUT_DIR = r"C:\wxapkg_output"

def batch_decrypt():
    if not os.path.exists(BASE_OUT_DIR):
        os.makedirs(BASE_OUT_DIR)

    # 1. 遍历 packages 目录下的所有 AppID 文件夹
    for app_id in os.listdir(BASE_IN_DIR):
        app_path = os.path.join(BASE_IN_DIR, app_id)
        
        if os.path.isdir(app_path) and app_id.startswith("wx"):
            # 2. 遍历 AppID 目录下的版本文件夹（如 "60", "61" 等）
            for version in os.listdir(app_path):
                version_path = os.path.join(app_path, version)
                
                if os.path.isdir(version_path):
                    # 3. 寻找该版本目录下的 .wxapkg 文件
                    for file in os.listdir(version_path):
                        if file.endswith(".wxapkg"):
                            pkg_path = os.path.join(version_path, file)
                            output_path = os.path.join(BASE_OUT_DIR, f"{app_id}_{version}")
                            
                            print(f"[*] 正在处理: {app_id} (版本: {version})")
                            
                            # 4. 构造命令并调用
                            cmd = [
                                EXE_PATH,
                                f"-id={app_id}",
                                f"-in={pkg_path}",
                                f"-out={output_path}"
                            ]
                            
                            try:
                                subprocess.run(cmd, check=True)
                                print(f"[+] 成功导出至: {output_path}")
                            except Exception as e:
                                print(f"[!] 处理 {app_id} 失败: {e}")

if __name__ == "__main__":
    batch_decrypt()