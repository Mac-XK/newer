import time
import subprocess
import datetime
import sys
import os

def send_wechat_message(message):
    """
    通过 AppleScript 控制微信发送消息。
    使用剪贴板中转方式，支持中文。
    """
    # AppleScript 脚本内容
    # 1. 将消息存入剪贴板
    # 2. 激活微信
    # 3. 模拟 Cmd+V 粘贴
    # 4. 模拟回车发送
    # AppleScript 脚本内容
    # 1. 将消息存入剪贴板
    # 2. 激活微信
    # 3. 模拟 Cmd+V 粘贴
    # 4. 模拟回车发送
    # 优化延迟：保持每条消息之间的极速发送
    script = f'''
    set the clipboard to "{message}"
    tell application "WeChat"
        activate
    end tell
    delay 0.2
    tell application "System Events"
        tell process "WeChat"
            keystroke "v" using command down
            delay 0.1
            key code 36
        end tell
    end tell
    '''
    
    try:
        # 执行 AppleScript
        subprocess.run(['osascript', '-e', script], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ 发送失败，AppleScript 执行出错。")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False

def get_start_delay(start_time_str):
    """
    计算距离目标开始时间的秒数。
    格式: HH:MM:SS
    """
    now = datetime.datetime.now()
    try:
        # 解析输入的时间
        target_time = datetime.datetime.strptime(start_time_str, "%H:%M:%S").time()
        target_datetime = datetime.datetime.combine(now.date(), target_time)
        
        # 如果目标时间已经过了，假设是明天的这个时间
        if target_datetime <= now:
            target_datetime += datetime.timedelta(days=1)
            
        return (target_datetime - now).total_seconds()
    except ValueError:
        print("❌ 时间格式错误，请使用 HH:MM:SS 格式 (例如 14:30:00)")
        return -1

def main():
    print("=======================================")
    print("   macOS 微信自动发送消息脚本 (Python版)   ")
    print("=======================================")
    print("⚠️  注意: 脚本运行时请保持微信已登录，并打开你要发送消息的聊天窗口。")
    print("⚠️  首次运行可能需要授权终端的[辅助功能]权限。")
    print("=======================================\n")

    # 1. 获取消息内容
    message = input("请输入要发送的消息内容: ").strip()
    if not message:
        print("消息内容不能为空。")
        return

    # 2. 获取开始时间
    print("\n请选择开始模式:")
    print("1. 立即开始")
    print("2. 指定时间开始 (格式 HH:MM:SS)")
    mode = input("请输入模式编号 (1/2): ").strip()
    
    wait_seconds = 0
    if mode == '2':
        while True:
            time_str = input("请输入开始时间 (例如 14:30:00): ").strip()
            seconds = get_start_delay(time_str)
            if seconds > 0:
                wait_seconds = seconds
                print(f"✅ 设定成功！脚本将在 {time_str} 启动 (约 {int(seconds)} 秒后)")
                break
    else:
        print("✅ 将立即开始发送。")

    # 3. 获取循环间隔
    while True:
        try:
            interval = float(input("\n请输入发送间隔 (秒): "))
            if interval < 0.5:
                print("间隔太短可能会被系统拦截或操作失败，建议大于 0.5 秒。")
                continue
            break
        except ValueError:
            print("请输入有效的数字。")

    # 4. 获取发送次数
    count_input = input("\n请输入发送次数 (输入 0 表示无限循环): ").strip()
    try:
        max_count = int(count_input)
    except ValueError:
        max_count = 0
    
    # 确认开始
    print("\n=======================================")
    print(f"消息内容: {message}")
    print(f"开始倒计时: {int(wait_seconds)} 秒")
    print(f"发送间隔: {interval} 秒")
    print(f"发送次数: {'无限' if max_count == 0 else max_count}")
    print("=======================================")
    
    confirm = input("按回车键开始挂机 (Ctrl+C 可随时停止)...")
    
    # 启动等待
    if wait_seconds > 0:
        print(f"正在等待启动... 请勿关闭窗口")
        time.sleep(wait_seconds)
    
    print("\n🚀 开始发送任务...")
    
    sent_count = 0
    try:
        while True:
            # 检查次数限制
            if max_count > 0 and sent_count >= max_count:
                print("\n✅ 已达到设定发送次数，任务完成。")
                break
            
            # 执行发送
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 正在发送第 {sent_count + 1} 条...", end="", flush=True)
            
            success = send_wechat_message(message)
            
            if success:
                print(" 成功")
            else:
                print(" 失败 (请检查权限或微信状态)")
            
            sent_count += 1
            
            # 等待下一次
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n🛑 用户手动停止脚本。")
    
    print("👋 脚本已退出。")

if __name__ == "__main__":
    main()
