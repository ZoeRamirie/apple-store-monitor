#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控 - 大陆门店快捷启动
"""

import json
import sys
import subprocess
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         🍎  Apple Store 库存监控 - 大陆门店  🍎                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    # 检查配置文件
    config_file = 'config.json'
    example_config = 'config.example.json'
    
    if not Path(config_file).exists():
        if Path(example_config).exists():
            print(f"{Fore.YELLOW}⚠️ config.json 不存在，正在使用示例配置...{Style.RESET_ALL}")
            config_file = example_config
        else:
            print(f"{Fore.RED}❌ 找不到配置文件！{Style.RESET_ALL}")
            sys.exit(1)
    
    # 加载配置
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 确保是大陆配置
        config['region'] = 'CN'
        
        # 保存到config.json
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"{Fore.GREEN}✅ 配置已加载（大陆区域）{Style.RESET_ALL}")
        
        # 显示基本信息
        products = len(config.get('target_products', []))
        stores = len(config.get('target_stores', []))
        print(f"\n{Fore.CYAN}📊 监控配置:{Style.RESET_ALL}")
        print(f"   • 产品: {products} 个")
        print(f"   • 门店: {stores} 个")
        print(f"   • 区域: 中国大陆 (CN)")
        
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


