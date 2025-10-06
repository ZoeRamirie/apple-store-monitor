#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
请求频率计算工具
帮助用户计算配置是否安全，避免触发Apple API限制
"""

import json
from colorama import Fore, Style, init

init(autoreset=True)


def calculate_request_rate(product_count, store_count, store_delay=1, check_interval=30):
    """
    计算实际请求频率
    
    Args:
        product_count: 产品数量
        store_count: 门店数量
        store_delay: 门店间延迟（秒）
        check_interval: 检查间隔（秒）
    
    Returns:
        详细计算结果
    """
    one_round_time = store_count * store_delay
    total_cycle = one_round_time + check_interval
    rate_per_minute = (product_count * store_count) / total_cycle * 60
    
    # 风险评估
    if rate_per_minute <= 10:
        risk_level = '✅ 安全'
        risk_color = Fore.GREEN
        risk_score = 0
    elif rate_per_minute <= 15:
        risk_level = '⚠️ 中等风险'
        risk_color = Fore.YELLOW
        risk_score = 1
    elif rate_per_minute <= 20:
        risk_level = '🔴 高风险'
        risk_color = Fore.RED
        risk_score = 2
    else:
        risk_level = '💀 危险'
        risk_color = Fore.RED + Style.BRIGHT
        risk_score = 3
    
    return {
        'product_count': product_count,
        'store_count': store_count,
        'store_delay': store_delay,
        'check_interval': check_interval,
        'one_round_time': one_round_time,
        'total_cycle': total_cycle,
        'rate_per_minute': rate_per_minute,
        'safe': rate_per_minute <= 10,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'risk_score': risk_score
    }


def calculate_safe_interval(product_count, store_count, store_delay=1, target_rate=10):
    """
    计算达到目标频率所需的check_interval
    
    Args:
        product_count: 产品数量
        store_count: 门店数量
        store_delay: 门店间延迟（秒）
        target_rate: 目标频率（次/分钟），默认10
    
    Returns:
        安全的check_interval（秒）
    """
    one_round_time = store_count * store_delay
    total_cycle = (product_count * store_count * 60) / target_rate
    check_interval = total_cycle - one_round_time
    
    return max(10, check_interval)


def print_calculation_result(result):
    """打印计算结果"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"📊 请求频率计算结果")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}配置参数：{Style.RESET_ALL}")
    print(f"  • 监控产品数：{result['product_count']} 个")
    print(f"  • 监控门店数：{result['store_count']} 个")
    print(f"  • 门店间延迟：{result['store_delay']} 秒")
    print(f"  • 检查间隔：{result['check_interval']} 秒")
    
    print(f"\n{Fore.YELLOW}计算过程：{Style.RESET_ALL}")
    print(f"  • 一轮耗时：{result['store_count']} × {result['store_delay']} = {result['one_round_time']} 秒")
    print(f"  • 总周期：{result['one_round_time']} + {result['check_interval']} = {result['total_cycle']} 秒")
    print(f"  • 请求频率：({result['product_count']} × {result['store_count']}) / {result['total_cycle']} × 60 = {result['rate_per_minute']:.2f} 次/分钟")
    
    print(f"\n{Fore.YELLOW}风险评估：{Style.RESET_ALL}")
    print(f"  • 实际频率：{result['risk_color']}{result['rate_per_minute']:.2f} 次/分钟{Style.RESET_ALL}")
    print(f"  • 风险级别：{result['risk_color']}{result['risk_level']}{Style.RESET_ALL}")
    print(f"  • 安全标准：≤ 10次/分钟")
    
    if not result['safe']:
        safe_interval = calculate_safe_interval(
            result['product_count'],
            result['store_count'],
            result['store_delay']
        )
        
        print(f"\n{Fore.RED}⚠️  当前配置不安全！{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}建议修改：{Style.RESET_ALL}")
        print(f"  方案1：增加check_interval到 {safe_interval:.0f} 秒")
        print(f"  方案2：减少门店数到 {int(result['store_count'] * 10 / result['rate_per_minute'])} 个")
        print(f"  方案3：减少产品数")
    else:
        print(f"\n{Fore.GREEN}✅ 配置安全，可以使用！{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def analyze_config_file(config_path='config.json'):
    """分析配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        product_count = len(config.get('target_products', []))
        
        if config.get('all_stores', False):
            # 需要读取门店列表
            try:
                with open('apple_stores_china.json', 'r', encoding='utf-8') as f:
                    stores_data = json.load(f)
                store_count = len(stores_data.get('stores', []))
            except:
                store_count = 48  # 默认门店数
        else:
            store_count = len(config.get('target_stores', []))
        
        check_interval = config.get('check_interval', 30)
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"📋 分析配置文件：{config_path}")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        result = calculate_request_rate(product_count, store_count, 1, check_interval)
        print_calculation_result(result)
        
        return result
        
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 配置文件未找到：{config_path}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ 读取配置文件失败：{e}{Style.RESET_ALL}")
        return None


def interactive_mode():
    """交互式模式"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"🧮 Apple API 请求频率计算器（交互式）")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("请输入以下参数：\n")
    
    try:
        product_count = int(input("监控产品数量 (1-5): ").strip() or "1")
        store_count = int(input("监控门店数量 (1-48): ").strip() or "5")
        check_interval = int(input("检查间隔（秒） (10-300): ").strip() or "30")
        
        result = calculate_request_rate(product_count, store_count, 1, check_interval)
        print_calculation_result(result)
        
        return result
        
    except ValueError:
        print(f"\n{Fore.RED}❌ 输入格式错误，请输入数字{Style.RESET_ALL}")
        return None
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已取消{Style.RESET_ALL}")
        return None


def show_safe_configs():
    """显示推荐的安全配置"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"📋 推荐的安全配置")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    configs = [
        {
            'name': '单产品单门店（最安全）',
            'product': 1,
            'store': 1,
            'interval': 6
        },
        {
            'name': '单产品3门店（保守）',
            'product': 1,
            'store': 3,
            'interval': 18
        },
        {
            'name': '单产品5门店（标准）⭐推荐',
            'product': 1,
            'store': 5,
            'interval': 30
        },
        {
            'name': '单产品8门店（需长间隔）',
            'product': 1,
            'store': 8,
            'interval': 48
        },
        {
            'name': '单产品10门店（最大）',
            'product': 1,
            'store': 10,
            'interval': 60
        },
        {
            'name': '2产品5门店',
            'product': 2,
            'store': 5,
            'interval': 60
        },
    ]
    
    for i, cfg in enumerate(configs, 1):
        result = calculate_request_rate(cfg['product'], cfg['store'], 1, cfg['interval'])
        
        print(f"{Fore.YELLOW}{i}. {cfg['name']}{Style.RESET_ALL}")
        print(f"   产品: {cfg['product']}个, 门店: {cfg['store']}个, 间隔: {cfg['interval']}秒")
        print(f"   频率: {result['risk_color']}{result['rate_per_minute']:.2f}次/分钟{Style.RESET_ALL} - {result['risk_level']}\n")


def main():
    """主函数"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"🛠️  Apple Store API 请求频率计算工具")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("选择模式：")
    print("  1. 分析当前配置文件 (config.json)")
    print("  2. 交互式计算")
    print("  3. 查看推荐的安全配置")
    print("  4. 分析指定配置文件")
    
    try:
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == '1':
            analyze_config_file('config.json')
        elif choice == '2':
            interactive_mode()
        elif choice == '3':
            show_safe_configs()
        elif choice == '4':
            config_path = input("配置文件路径: ").strip()
            analyze_config_file(config_path)
        else:
            print(f"{Fore.YELLOW}无效选择，分析默认配置{Style.RESET_ALL}")
            analyze_config_file('config.json')
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已退出{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ 错误：{e}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()


