#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控系统 - 统一启动入口
支持大陆和香港区域选择
"""

import sys
import json
import os
from pathlib import Path
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

def print_banner():
    """打印欢迎横幅"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         🍎  Apple Store 库存监控系统  🍎                          ║
║                                                                   ║
║                  统一启动入口 - 区域选择                           ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def select_region():
    """选择监控区域"""
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📍 请选择监控区域:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}  1. 🇨🇳 中国大陆{Style.RESET_ALL}")
    print(f"     • API: https://www.apple.com.cn/shop/retail/pickup-message")
    print(f"     • Part Number格式: CH/A")
    print(f"     • 门店数量: 42+家")
    print(f"     • 网络要求: 无需VPN\n")
    
    print(f"{Fore.GREEN}  2. 🇭🇰 中国香港{Style.RESET_ALL}")
    print(f"     • API: https://www.apple.com/hk-zh/shop/fulfillment-messages")
    print(f"     • Part Number格式: ZA/A")
    print(f"     • 门店数量: 6家")
    print(f"     • 网络要求: 可能需要VPN\n")
    
    while True:
        choice = input(f"{Fore.GREEN}请选择 (1-2): {Style.RESET_ALL}").strip()
        if choice in ['1', '2']:
            return 'CN' if choice == '1' else 'HK'
        print(f"{Fore.RED}❌ 无效选择，请输入 1 或 2{Style.RESET_ALL}")

def select_config(region):
    """选择配置方案"""
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📋 请选择配置方案:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
    
    if region == 'HK':
        print(f"{Fore.GREEN}  1. 交互式配置（推荐）⭐{Style.RESET_ALL}")
        print(f"     • 根据需求自定义生成配置")
        print(f"     • 支持多种监控策略")
        print(f"     • 自动计算频率和风险\n")
        
        print(f"{Fore.GREEN}  2. 优先配置（快速）{Style.RESET_ALL}")
        print(f"     • 监控门店: 3个核心门店")
        print(f"     • 监控产品: 3个（256GB系列）")
        print(f"     • 请求频率: 3次/分钟")
        print(f"     • 安全等级: ✅✅✅ 非常安全\n")
        
        print(f"{Fore.GREEN}  3. 平衡配置{Style.RESET_ALL}")
        print(f"     • 监控门店: 6个（全部）")
        print(f"     • 监控产品: 6个（256GB + 512GB）")
        print(f"     • 请求频率: 6次/分钟")
        print(f"     • 安全等级: ✅✅ 安全\n")
        
        print(f"{Fore.YELLOW}  4. 使用现有配置（高级）{Style.RESET_ALL}")
        print(f"     • 使用当前的 config.json")
        print(f"     • ⚠️ 会验证配置是否匹配香港区域\n")
        
        while True:
            choice = input(f"{Fore.GREEN}请选择 (1-4，推荐1): {Style.RESET_ALL}").strip()
            if choice in ['1', '2', '3', '4']:
                if choice == '1':
                    # 启动香港交互式配置生成器
                    print(f"\n{Fore.CYAN}🎯 启动香港交互式配置生成器...{Style.RESET_ALL}")
                    import subprocess
                    result = subprocess.run(['python3', 'interactive_config_hk.py'], check=False)
                    if result.returncode == 0 and os.path.exists('config.json'):
                        return 'config.json'
                    else:
                        print(f"{Fore.RED}❌ 交互式配置失败{Style.RESET_ALL}")
                        return None
                elif choice == '2':
                    return 'config_hongkong_promax_priority.json'
                elif choice == '3':
                    return 'config_hongkong_promax_all.json'
                else:
                    return 'config.json'
            print(f"{Fore.RED}❌ 无效选择，请输入 1、2、3 或 4{Style.RESET_ALL}")
    
    else:  # CN
        print(f"{Fore.GREEN}  1. 交互式配置（推荐）⭐{Style.RESET_ALL}")
        print(f"     • 根据需求自定义生成配置")
        print(f"     • 支持多种监控策略")
        print(f"     • 自动计算频率和风险\n")
        
        print(f"{Fore.GREEN}  2. 使用示例配置{Style.RESET_ALL}")
        print(f"     • 使用 config.example.json 作为模板")
        print(f"     • 包含大陆门店和产品配置\n")
        
        print(f"{Fore.YELLOW}  3. 使用现有配置（高级）{Style.RESET_ALL}")
        print(f"     • 使用当前的 config.json")
        print(f"     • ⚠️ 会验证配置是否匹配大陆区域\n")
        
        while True:
            choice = input(f"{Fore.GREEN}请选择 (1-3，推荐1): {Style.RESET_ALL}").strip()
            if choice in ['1', '2', '3']:
                if choice == '1':
                    return '__interactive__'
                elif choice == '2':
                    return 'config.example.json'
                else:
                    return 'config.json'
            print(f"{Fore.RED}❌ 无效选择，请输入 1、2 或 3{Style.RESET_ALL}")

def check_network_for_hk():
    """检查是否能访问香港网站"""
    print(f"\n{Fore.YELLOW}🔍 检查网络连接...{Style.RESET_ALL}")
    
    try:
        import requests
        response = requests.get('https://www.apple.com/hk', timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ 网络正常，可以访问香港Apple网站{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️ 无法访问香港网站（HTTP {response.status_code}）{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ 无法访问香港网站{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 提示: 监控香港门店可能需要开启VPN{Style.RESET_ALL}")
        return False

def validate_config_for_region(config, region):
    """验证配置是否与区域匹配"""
    issues = []
    
    # 检查Part Number格式
    products = config.get('target_products', [])
    for product in products:
        part_number = product.get('part_number', '')
        if region == 'HK' and not part_number.endswith('ZA/A'):
            issues.append(f"产品 {part_number} 不是香港格式（应为 ZA/A）")
        elif region == 'CN' and not part_number.endswith('CH/A'):
            issues.append(f"产品 {part_number} 不是大陆格式（应为 CH/A）")
    
    # 检查门店编号
    stores = config.get('target_stores', [])
    hk_stores = ['R409', 'R428', 'R485', 'R499', 'R610', 'R673']
    
    for store in stores:
        if region == 'HK' and store not in hk_stores:
            issues.append(f"门店 {store} 不是香港门店")
        elif region == 'CN' and store in hk_stores:
            issues.append(f"门店 {store} 是香港门店，不是大陆门店")
    
    return issues

def load_and_update_config(config_file, region):
    """加载并更新配置"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证配置是否与区域匹配
        issues = validate_config_for_region(config, region)
        
        if issues:
            print(f"\n{Fore.RED}⚠️ 配置与所选区域不匹配！{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}发现以下问题:{Style.RESET_ALL}")
            for i, issue in enumerate(issues[:5], 1):  # 最多显示5个
                print(f"  {i}. {issue}")
            if len(issues) > 5:
                print(f"  ... 还有 {len(issues) - 5} 个问题")
            
            print(f"\n{Fore.YELLOW}建议:{Style.RESET_ALL}")
            if region == 'HK':
                print(f"  • 香港监控请选择香港预设配置（选项1或2）")
            else:
                print(f"  • 大陆监控请选择示例配置或重新配置")
            
            choice = input(f"\n{Fore.GREEN}是否继续使用此配置？(y/n): {Style.RESET_ALL}").strip().lower()
            if choice != 'y':
                return None
        
        # 确保region字段正确
        config['region'] = region
        
        # 保存到config.json
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return config
    except Exception as e:
        print(f"{Fore.RED}❌ 加载配置失败: {e}{Style.RESET_ALL}")
        return None

def show_summary(config, region):
    """显示配置摘要"""
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 配置摘要:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
    
    region_name = "中国大陆" if region == "CN" else "中国香港"
    print(f"{Fore.CYAN}  区域:{Style.RESET_ALL} {region_name} ({region})")
    
    products = config.get('target_products', [])
    stores = config.get('target_stores', [])
    interval = config.get('check_interval', 15)
    
    print(f"{Fore.CYAN}  监控产品:{Style.RESET_ALL} {len(products)} 个")
    print(f"{Fore.CYAN}  监控门店:{Style.RESET_ALL} {len(stores)} 个")
    print(f"{Fore.CYAN}  检查间隔:{Style.RESET_ALL} {interval} 秒")
    
    # 计算频率（考虑随机延迟）
    requests_per_check = len(products) * len(stores)
    # 考虑随机延迟（平均2.0秒）
    avg_request_time = requests_per_check * 2.0
    total_cycle_time = avg_request_time + interval
    frequency = (requests_per_check / total_cycle_time) * 60
    
    safety = "✅ 安全" if frequency <= 10 else ("⚠️ 注意" if frequency <= 30 else "❌ 危险")
    print(f"{Fore.CYAN}  请求频率:{Style.RESET_ALL} {frequency:.1f} 次/分钟 {safety}")
    
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")

def main():
    """主函数"""
    print_banner()
    
    while True:  # 添加循环，允许重试
        # 步骤1: 选择区域
        region = select_region()
        
        # 步骤2: 香港区域检查网络
        if region == 'HK':
            network_ok = check_network_for_hk()
            if not network_ok:
                print(f"\n{Fore.YELLOW}⚠️ 网络检查失败，是否继续？{Style.RESET_ALL}")
                continue_choice = input(f"{Fore.GREEN}继续 (y/n): {Style.RESET_ALL}").strip().lower()
                if continue_choice != 'y':
                    print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}")
                    sys.exit(0)
        
        # 步骤3: 选择配置
        config_file = select_config(region)
        
        # 步骤4: 加载配置
        if config_file == '__interactive__':
            # 使用交互式配置生成器
            print(f"\n{Fore.CYAN}🎯 启动交互式配置生成器...{Style.RESET_ALL}")
            try:
                from interactive_config import InteractiveConfigGenerator
                generator = InteractiveConfigGenerator()
                config = generator.generate()
                
                if not config:
                    print(f"\n{Fore.YELLOW}⚠️ 配置生成取消{Style.RESET_ALL}")
                    retry = input(f"{Fore.GREEN}是否重新选择？(y/n): {Style.RESET_ALL}").strip().lower()
                    if retry == 'y':
                        continue
                    else:
                        print(f"\n{Fore.YELLOW}程序退出{Style.RESET_ALL}")
                        sys.exit(0)
                
                # 保存生成的配置
                with open('config.json', 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
            except Exception as e:
                print(f"\n{Fore.RED}❌ 交互式配置生成失败: {e}{Style.RESET_ALL}")
                retry = input(f"{Fore.GREEN}是否重新选择？(y/n): {Style.RESET_ALL}").strip().lower()
                if retry == 'y':
                    continue
                else:
                    sys.exit(0)
        else:
            print(f"\n{Fore.YELLOW}📁 正在加载配置: {config_file}{Style.RESET_ALL}")
            config = load_and_update_config(config_file, region)
        
        if not config:
            print(f"\n{Fore.YELLOW}⚠️ 配置加载失败{Style.RESET_ALL}")
            retry = input(f"{Fore.GREEN}是否重新选择？(y/n): {Style.RESET_ALL}").strip().lower()
            if retry == 'y':
                continue  # 重新开始
            else:
                print(f"\n{Fore.YELLOW}程序退出{Style.RESET_ALL}")
                sys.exit(0)
        
        # 配置加载成功，跳出循环
        break
    
    print(f"{Fore.GREEN}✅ 配置加载成功{Style.RESET_ALL}")
    
    # 步骤5: 显示摘要
    show_summary(config, region)
    
    # 步骤6: 确认启动
    print(f"\n{Fore.GREEN}准备启动监控程序...{Style.RESET_ALL}")
    confirm = input(f"{Fore.GREEN}确认启动？(y/n): {Style.RESET_ALL}").strip().lower()
    
    if confirm != 'y':
        print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}")
        sys.exit(0)
    
    # 步骤7: 启动监控
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}🚀 正在启动监控程序...{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    # 调用main.py
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'main.py'], cwd=os.getcwd())
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}用户中断{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ 启动失败: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}用户取消操作{Style.RESET_ALL}")
        sys.exit(0)

