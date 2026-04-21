import os
import time
import shutil
import win32clipboard
import win32con
from pywinauto import Application, Desktop
from pywinauto.keyboard import send_keys

# --- 配置 ---
# 目标小程序白名单
# TARGET_APPIDS = ["wx50a143ee78658d2a", "wx9b8aeb791f332a5f"]

TARGET_APPIDS = ["wx258208c871dcc2d0", "wx4d19e373739530cb", "wx163261a6f8d0d29b", "wxcdf7ba5e0e19ee1d", "wxbc565978b714c7d4", "wxc1527ffeb35b574d", "wx21881ba3138650ed", "wx0785751e7aabd398", "wx596a71d1f62acab0", "wx750e237c22f7ab57", "wx65934ee32a88d726", "wx11c4f9a6778e021f", "wx88297831a71c80e3", "wxd4e2eba3b84d8fa5", "wxc5c9072480f91de0", "wx316eda082f800ccf", "wx49cf1f25d8d60edc", "wxb22d550fec7ecd5a", "wxf5d91e4d30189db2", "wx5600da392376a236", "wx51b00cdbfd1aace3", "wx3cda886e57f3fcf5", "wxf78503a10c58798a", "wx0d424629d87fc5d6", "wxfedbf3472ef4791e", "wx823debdd28f1fc80", "wx5344e5c0e3e416ae"]



# 微信包存放根目录
BASE_PATH = r"C:\Users\Only_You\AppData\Roaming\Tencent\xwechat\radium\Applet\packages"

def set_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()

def clean_extra_directories():
    """清理不在目标列表中的额外生成的目录"""
    if not os.path.exists(BASE_PATH):
        return
    
    current_dirs = os.listdir(BASE_PATH)
    for dirname in current_dirs:
        # 如果目录名不在我们的目标列表中，且不是必须保留的系统目录
        # 注意：这里你可以根据实际观察到的额外目录名增加过滤条件
        if dirname not in TARGET_APPIDS:
            full_path = os.path.join(BASE_PATH, dirname)
            try:
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path) # 强制删除额外目录
                    print(f"[清理] 已移除额外目录: {dirname}")
            except Exception as e:
                # 有时文件被占用无法删除，跳过即可
                pass

def start_automated_task():
    dt = Desktop(backend="uia")
    
    # 任务开始前先清空一次干扰目录
    print("[*] 正在执行预清理...")
    clean_extra_directories()

    for appid in TARGET_APPIDS:
        print(f"\n[>>>] 正在处理目标: {appid}")
        
        try:
            # 1. 锁定“雨天小助手”
            helper_win = None
            for win in dt.windows():
                if "雨天小助手" in win.window_text() and win.is_visible():
                    helper_win = win
                    break
            
            if not helper_win:
                print("[!] 未找到雨天小助手，请确保其已打开。")
                break

            helper_win.set_focus()
            h_rect = helper_win.rectangle()
            w, h = h_rect.width(), h_rect.height()

            # 2. 输入 AppID 并点击跳转
            helper_win.click_input(coords=(int(w * 0.5), int(h * 0.35))) 
            send_keys('^a{BACKSPACE}') 
            set_clipboard(appid)
            send_keys('^v')
            time.sleep(1)
            helper_win.click_input(coords=(int(w * 0.5), int(h * 0.57)))
            time.sleep(2)

            # 3. 处理“允许”确认弹窗 (盲点 + 回车)
            helper_win.click_input(coords=(int(w * 0.65), int(h * 0.55)))
            send_keys('{ENTER}')

            # 4. 监测目标包生成
            print(f"[*] 等待目标包生成...")
            target_dir = os.path.join(BASE_PATH, appid)
            success = False
            for _ in range(15):
                if os.path.exists(target_dir):
                    success = True
                    break
                time.sleep(1)
            
            if success:
                print(f"[√] {appid} 目录已生成。")
            
            # 5. 精准关闭目标小程序窗口
            for win in dt.windows():
                try:
                    title = win.window_text()
                    if win.is_visible() and win.element_info.class_name == "Chrome_WidgetWin_0":
                        if "雨天小助手" not in title and title != "":
                            win.close()
                except: continue

            # 6. 每处理完一个，立即清理产生的额外缓存目录
            time.sleep(2) # 给系统一点释放文件占用的时间
            clean_extra_directories()
            
            print(f"[---] {appid} 环节结束。")

        except Exception as e:
            print(f"[!] 出错: {e}")

if __name__ == "__main__":
    start_automated_task()
    print("\n[*] 所有指定任务完成，干扰目录已清理。")
