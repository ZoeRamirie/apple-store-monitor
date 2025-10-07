#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控 - 香港门店快捷启动
"""

import json
import sys
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def check_network():
    """检查网络连接"""
    try:
        import requests
        response = requests.get('https://www.apple.com/hk', timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         🍎  Apple Store 库存监控 - 香港门店  🍎                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    # 检查网络
    print(f"{Fore.YELLOW}🔍 检查网络连接...{Style.RESET_ALL}")
    if check_network():
        print(f"{Fore.GREEN}✅ 网络正常{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ 无法访问香港Apple网站{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 提示: 可能需要开启VPN{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}是否继续？(y/n): {Style.RESET_ALL}").strip().lower()
        if choice != 'y':
            sys.exit(0)
    
    # 选择配置
    print(f"\n{Fore.CYAN}📋 请选择配置:{Style.RESET_ALL}")
    print(f"  1. 优先配置 (3门店 × 3产品)")
    print(f"  2. 平衡配置 (6门店 × 6产品)")
    print(f"  3. 使用现有 config.json")
    
    while True:
        choice = input(f"\n{Fore.GREEN}请选择 (1-3): {Style.RESET_ALL}").strip()
        if choice in ['1', '2', '3']:
            break
        print(f"{Fore.RED}❌ 无效选择{Style.RESET_ALL}")
    
    # 确定配置文件
    if choice == '1':
        config_file = 'config_hongkong_promax_priority.json'
    elif choice == '2':
        config_file = 'config_hongkong_promax_all.json'
    else:
        config_file = 'config.json'
    
    # 检查配置文件
    if not Path(config_file).exists():
        print(f"{Fore.RED}❌ 配置文件不存在: {config_file}{Style.RESET_ALL}")
        sys.exit(1)
    
    # 加载配置
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 确保是香港配置
        config['region'] = 'HK'
        
        # 保存到config.json
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Fore.GREEN}✅ 配置已加载（香港区域）{Style.RESET_ALL}")
        
        # 显示基本信息
        products = len(config.get('target_products', []))
        stores = len(config.get('target_stores', []))
        check_interval = config.get('check_interval', 60)
        
        # 计算频率（考虑随机延迟）
        requests_per_check = products * stores
        avg_request_time = requests_per_check * 4.5
        total_cycle_time = avg_request_time + check_interval
        frequency = (requests_per_check / total_cycle_time) * 60
        
        print(f"\n{Fore.CYAN}📊 监控配置:{Style.RESET_ALL}")
        print(f"   • 产品: {products} 个")
        print(f"   • 门店: {stores} 个")
        print(f"   • 区域: 中国香港 (HK)")
        print(f"   • 频率: {frequency:.1f} 次/分钟")
        
        print(f"\n{Fore.GREEN}🚀 正在启动监控...{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
        
        # 启动main.py
        result = subprocess.run([sys.executable, 'main.py'])
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"{Fore.RED}❌ 启动失败: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}用户中断{Style.RESET_ALL}")
        sys.exit(0)


