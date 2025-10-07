#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存实时监控系统 - 智能交互式版本 v3.0
特性：
- 人性化交互界面
- 智能防爬虫保护
- 实时安全评估
- 多种监控模式
"""

import json
import time
import signal
import sys
import threading
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Style
from tabulate import tabulate

from apple_store_monitor import AppleStoreMonitor
from notifier import Notifier
from logger_config import setup_logger

# 初始化
init(autoreset=True)
logger = setup_logger()
stop_event = threading.Event()
print_lock = threading.Lock()


def signal_handler(signum, frame):
    """处理中断信号"""
    print(f"\n\n{'='*60}")
    print("收到中断信号，正在安全退出...")
    print(f"{'='*60}\n")
    stop_event.set()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def calculate_request_frequency(num_products, num_stores, check_interval):
    """
    计算请求频率和安全评估
    
    Args:
        num_products: 产品数量
        num_stores: 门店数量
        check_interval: 检查间隔(秒)
    
    Returns:
        dict: 包含频率、安全等级等信息
    """
    store_delay = 0.5  # 每个门店间延迟0.5秒
    requests_per_round = num_products * num_stores
    total_round_time = (num_stores * store_delay) + check_interval
    requests_per_minute = (requests_per_round / total_round_time) * 60
    
    # 安全评级（基于实测数据：10次/分钟绝对安全）
    if requests_per_minute <= 10:
        safety_level = "非常安全"
        safety_score = 100
        color = Fore.GREEN
        recommendation = "可以长期运行数小时甚至一整天"
        icon = "✅"
    elif requests_per_minute <= 12:
        safety_level = "安全"
        safety_score = 90
        color = Fore.GREEN
        recommendation = "可以持续运行2-4小时"
        icon = "✅"
    elif requests_per_minute <= 15:
        safety_level = "较安全"
        safety_score = 70
        color = Fore.YELLOW
        recommendation = "建议运行1-2小时，注意观察"
        icon = "⚠️ "
    elif requests_per_minute <= 20:
        safety_level = "有风险"
        safety_score = 40
        color = Fore.YELLOW
        recommendation = "可能在30-60分钟内触发限制"
        icon = "⚠️ "
    else:
        safety_level = "高风险"
        safety_score = 20
        color = Fore.RED
        recommendation = "很可能在10-20分钟内触发限制"
        icon = "🔴"
    
    return {
        'requests_per_round': requests_per_round,
        'total_round_time': total_round_time,
        'requests_per_minute': requests_per_minute,
        'safety_level': safety_level,
        'safety_score': safety_score,
        'safety_color': color,
        'recommendation': recommendation,
        'icon': icon
    }


def suggest_safe_interval(num_products, num_stores):
    """建议安全的检查间隔"""
    requests_per_round = num_products * num_stores
    store_delay = num_stores * 0.5
    
    # 目标：10次/分钟（最安全）
    target_frequency = 10
    required_total_time = (requests_per_round / target_frequency) * 60
    safe_interval = max(15, int(required_total_time - store_delay))
    
    return safe_interval


def print_banner():
    """打印欢迎横幅"""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{' '*78}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{' '*20}🍎 Apple Store 智能库存监控系统 v3.0 🍎{' '*19}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{' '*78}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{' '*15}实时监控 • 智能防护 • 安全高效 • 人性化操作{' '*18}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║{' '*78}║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}💡 智能防爬虫保护:{Style.RESET_ALL}")
    print(f"   • 基于301次实测数据的安全阈值")
    print(f"   • 10次/分钟 = 100%安全（实测验证）")
    print(f"   • 智能间隔建议，防止触发限制")
    print(f"   • 实时安全评估，让您安心使用\n")


def select_monitoring_mode():
    """选择监控模式"""
    print(f"\n{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📋 请选择监控模式:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    modes = [
        {
            'id': 1,
            'name': '快速开始模式',
            'desc': '使用当前配置文件直接运行',
            'safety': '根据配置而定',
            'suitable': '已配置好的用户、快速启动',
            'icon': '⚡'
        },
        {
            'id': 2,
            'name': '标准监控模式（推荐）',
            'desc': '3-5个门店 + 1个产品 + 30秒间隔',
            'safety': '非常安全 (8-10次/分钟)',
            'suitable': '日常监控、长期运行、后台挂机',
            'icon': '⭐'
        },
        {
            'id': 3,
            'name': '积极监控模式',
            'desc': '2-3个门店 + 1个产品 + 20秒间隔',
            'safety': '安全 (9-12次/分钟)',
            'suitable': '确定近期有货、短期冲刺',
            'icon': '🚀'
        },
        {
            'id': 4,
            'name': '极限监控模式',
            'desc': '1个门店 + 1个产品 + 10秒间隔',
            'safety': '中等风险 (6次/分钟)',
            'suitable': '紧急抢购、首发瞬间(发现有货立即停止)',
            'icon': '🔥'
        },
        {
            'id': 5,
            'name': '自定义模式',
            'desc': '完全自定义所有参数',
            'safety': '智能评估',
            'suitable': '高级用户、特殊需求、精确控制',
            'icon': '🎨'
        }
    ]
    
    for mode in modes:
        print(f"{Fore.CYAN}{mode['icon']} {mode['id']}. {mode['name']}{Style.RESET_ALL}")
        print(f"   {Fore.WHITE}描述:{Style.RESET_ALL} {mode['desc']}")
        print(f"   {Fore.WHITE}安全性:{Style.RESET_ALL} {mode['safety']}")
        print(f"   {Fore.WHITE}适合:{Style.RESET_ALL} {mode['suitable']}")
        print()
    
    while True:
        try:
            choice = input(f"{Fore.GREEN}➤ 请选择模式 (1-5): {Style.RESET_ALL}").strip()
            mode = int(choice)
            if 1 <= mode <= 5:
                return mode
            else:
                print(f"{Fore.RED}✖ 请输入1-5之间的数字{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}✖ 请输入有效的数字{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}")
            sys.exit(0)


def load_stores_data():
    """加载门店数据"""
    try:
        with open('apple_stores_china.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {s['storeNumber']: s for s in data['stores']}
    except Exception as e:
        logger.error(f"加载门店数据失败: {e}")
        return {}


def select_stores(all_stores, max_stores=None):
    """
    选择监控门店
    
    Args:
        all_stores: 所有门店字典
        max_stores: 最大门店数限制
    """
    print(f"\n{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🏪 选择监控门店:{Style.RESET_ALL}")
    if max_stores:
        print(f"{Fore.YELLOW}   (建议选择{max_stores}个门店以保证安全){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    # 按城市分组
    cities = {}
    for store in all_stores.values():
        city = store['city']
        if city not in cities:
            cities[city] = []
        cities[city].append(store)
    
    # 显示热门城市
    hot_cities = ['北京', '上海', '深圳', '广州', '成都', '杭州']
    
    print(f"{Fore.CYAN}热门城市：{Style.RESET_ALL}")
    for i, city in enumerate(hot_cities, 1):
        if city in cities:
            print(f"  {i}. {city} ({len(cities[city])}家)")
    print(f"  7. 查看所有城市")
    print(f"  8. 手动输入门店编号")
    print()
    
    while True:
        try:
            choice = input(f"{Fore.GREEN}➤ 请选择 (1-8): {Style.RESET_ALL}").strip()
            
            if choice == '7':
                # 显示所有城市
                print(f"\n{Fore.CYAN}所有城市 (共{len(cities)}个):{Style.RESET_ALL}")
                sorted_cities = sorted(cities.items(), key=lambda x: -len(x[1]))
                city_list = []
                for i, (city, stores) in enumerate(sorted_cities, 1):
                    print(f"  {i:2d}. {city:8s} ({len(stores)}家)")
                    city_list.append(city)
                print()
                
                # 让用户从所有城市中选择
                while True:
                    try:
                        city_choice = input(f"{Fore.GREEN}➤ 请选择城市 (1-{len(city_list)}) 或输入0返回: {Style.RESET_ALL}").strip()
                        if city_choice == '0':
                            break
                        
                        city_idx = int(city_choice)
                        if 1 <= city_idx <= len(city_list):
                            selected_city = city_list[city_idx - 1]
                            city_stores = cities[selected_city]
                            
                            print(f"\n{Fore.CYAN}{selected_city}的门店 (共{len(city_stores)}家):{Style.RESET_ALL}")
                            for i, store in enumerate(city_stores, 1):
                                print(f"  {i}. {store['storeNumber']} - {store['storeName']}")
                            
                            if max_stores and len(city_stores) > max_stores:
                                print(f"\n  0. 选择前{max_stores}家（推荐）")
                                print(f"  00. 全选所有{len(city_stores)}家（不推荐）")
                            else:
                                print(f"\n  0. 全选所有{len(city_stores)}家")
                            print()
                            
                            selection = input(f"{Fore.GREEN}➤ 请选择门店 (可多选，用逗号分隔，如 1,2,3): {Style.RESET_ALL}").strip()
                            
                            if selection == '0':
                                if max_stores and len(city_stores) > max_stores:
                                    selected = [s['storeNumber'] for s in city_stores[:max_stores]]
                                    print(f"{Fore.GREEN}✓ 已自动选择前{max_stores}家{Style.RESET_ALL}")
                                else:
                                    selected = [s['storeNumber'] for s in city_stores]
                            elif selection == '00':
                                selected = [s['storeNumber'] for s in city_stores]
                                print(f"{Fore.YELLOW}⚠️  已选择全部{len(selected)}家，请注意安全{Style.RESET_ALL}")
                            else:
                                indices = [int(x.strip()) for x in selection.split(',')]
                                selected = [city_stores[i-1]['storeNumber'] for i in indices if 1 <= i <= len(city_stores)]
                            
                            if selected:
                                print(f"\n{Fore.GREEN}✅ 已选择 {len(selected)} 个门店{Style.RESET_ALL}")
                                return selected
                        else:
                            print(f"{Fore.RED}✖ 请输入1-{len(city_list)}之间的数字{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}✖ 请输入有效的数字{Style.RESET_ALL}")
                
                continue
            
            elif choice == '8':
                # 手动输入
                print(f"\n{Fore.CYAN}请输入门店编号:{Style.RESET_ALL}")
                print(f"  格式: 用逗号分隔，如 R320,R448,R388")
                print(f"  可用编号范围: R320-R793")
                store_input = input(f"{Fore.GREEN}➤ {Style.RESET_ALL}").strip()
                store_numbers = [s.strip().upper() for s in store_input.split(',')]
                
                # 验证门店编号
                valid_stores = []
                invalid_stores = []
                for sn in store_numbers:
                    if sn in all_stores:
                        valid_stores.append(sn)
                    else:
                        invalid_stores.append(sn)
                
                if invalid_stores:
                    print(f"\n{Fore.RED}❌ 无效的门店编号: {', '.join(invalid_stores)}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}   提示: 使用 scan_valid_stores.py 可查看所有有效门店{Style.RESET_ALL}")
                
                if valid_stores:
                    if max_stores and len(valid_stores) > max_stores:
                        print(f"\n{Fore.YELLOW}⚠️  您选择了{len(valid_stores)}个门店，建议不超过{max_stores}个{Style.RESET_ALL}")
                        print(f"   过多门店可能导致请求频率过高")
                        
                        confirm = input(f"{Fore.YELLOW}是否继续? (y/n): {Style.RESET_ALL}").strip().lower()
                        if confirm != 'y':
                            continue
                    
                    print(f"\n{Fore.GREEN}✅ 已选择 {len(valid_stores)} 个门店:{Style.RESET_ALL}")
                    for sn in valid_stores:
                        store = all_stores[sn]
                        print(f"   • {sn} - {store['storeName']} ({store['city']})")
                    
                    confirm = input(f"\n{Fore.GREEN}➤ 确认选择? (y/n): {Style.RESET_ALL}").strip().lower()
                    if confirm == 'y':
                        return valid_stores
                else:
                    print(f"{Fore.RED}没有选择有效的门店{Style.RESET_ALL}")
                
                continue
            
            else:
                idx = int(choice)
                if 1 <= idx <= 6 and hot_cities[idx-1] in cities:
                    city = hot_cities[idx-1]
                    city_stores = cities[city]
                    
                    print(f"\n{Fore.CYAN}{city}的门店 (共{len(city_stores)}家):{Style.RESET_ALL}")
                    for i, store in enumerate(city_stores, 1):
                        print(f"  {i}. {store['storeNumber']} - {store['storeName']}")
                    
                    if max_stores and len(city_stores) > max_stores:
                        print(f"\n  0. 选择前{max_stores}家（推荐）")
                        print(f"  00. 全选所有{len(city_stores)}家（不推荐）")
                    else:
                        print(f"\n  0. 全选所有{len(city_stores)}家")
                    print()
                    
                    selection = input(f"{Fore.GREEN}➤ 请选择门店 (可多选，用逗号分隔，如 1,2,3): {Style.RESET_ALL}").strip()
                    
                    if selection == '0':
                        if max_stores and len(city_stores) > max_stores:
                            selected = [s['storeNumber'] for s in city_stores[:max_stores]]
                            print(f"{Fore.GREEN}✓ 已自动选择前{max_stores}家{Style.RESET_ALL}")
                        else:
                            selected = [s['storeNumber'] for s in city_stores]
                    elif selection == '00':
                        selected = [s['storeNumber'] for s in city_stores]
                        print(f"{Fore.YELLOW}⚠️  已选择全部{len(selected)}家，请注意安全{Style.RESET_ALL}")
                    else:
                        indices = [int(x.strip()) for x in selection.split(',')]
                        selected = [city_stores[i-1]['storeNumber'] for i in indices if 1 <= i <= len(city_stores)]
                    
                    if selected:
                        print(f"\n{Fore.GREEN}✅ 已选择 {len(selected)} 个门店{Style.RESET_ALL}")
                        return selected
                else:
                    print(f"{Fore.RED}✖ 无效选择{Style.RESET_ALL}")
        
        except (ValueError, IndexError):
            print(f"{Fore.RED}✖ 输入错误，请重新选择{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}")
            sys.exit(0)


def select_products():
    """选择监控产品"""
    print(f"\n{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}📱 选择监控产品:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    print("1. 使用配置文件中的产品")
    print("2. 手动输入产品信息 (Part Number)")
    print("3. 从iPhone 17型号库选择")
    print()
    
    choice = input(f"{Fore.GREEN}➤ 请选择 (1-3): {Style.RESET_ALL}").strip()
    
    if choice == '1':
        # 从配置文件读取
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                products = config.get('target_products', [])
                if products:
                    print(f"\n{Fore.GREEN}✅ 使用配置文件中的产品:{Style.RESET_ALL}")
                    for p in products:
                        print(f"   • {p['name']} ({p['part_number']})")
                    return products
                else:
                    print(f"{Fore.RED}✖ 配置文件中没有产品{Style.RESET_ALL}")
                    return select_products()
        except:
            print(f"{Fore.RED}✖ 读取配置文件失败{Style.RESET_ALL}")
            return select_products()
    
    elif choice == '2':
        # 手动输入
        print(f"\n{Fore.CYAN}请输入产品信息:{Style.RESET_ALL}")
        name = input("  产品名称 (如: iPhone 17 Pro Max 星宇橙色 2TB): ").strip()
        part_number = input("  Part Number (如: MG0G4CH/A): ").strip().upper()
        color = input("  颜色 (如: 星宇橙色): ").strip()
        storage = input("  容量 (如: 2TB): ").strip()
        series = input("  系列 (如: iPhone 17 Pro Max): ").strip()
        
        product = {
            'name': name,
            'part_number': part_number,
            'color': color,
            'storage': storage,
            'series': series
        }
        
        print(f"\n{Fore.GREEN}✅ 已创建产品配置{Style.RESET_ALL}")
        return [product]
    
    elif choice == '3':
        # 从型号库选择
        try:
            with open('iphone17_all_models.json', 'r', encoding='utf-8') as f:
                models = json.load(f)
                
                print(f"\n{Fore.CYAN}iPhone 17系列型号库:{Style.RESET_ALL}\n")
                
                # 按系列分组
                series_groups = {}
                for model in models:
                    series = model.get('series', 'Unknown')
                    if series not in series_groups:
                        series_groups[series] = []
                    series_groups[series].append(model)
                
                # 显示系列
                series_list = list(series_groups.keys())
                for i, series in enumerate(series_list, 1):
                    print(f"  {i}. {series} ({len(series_groups[series])}款)")
                
                series_choice = int(input(f"\n{Fore.GREEN}➤ 请选择系列 (1-{len(series_list)}): {Style.RESET_ALL}").strip())
                selected_series = series_list[series_choice - 1]
                models_in_series = series_groups[selected_series]
                
                # 显示该系列的型号
                print(f"\n{Fore.CYAN}{selected_series} 型号列表:{Style.RESET_ALL}\n")
                for i, model in enumerate(models_in_series, 1):
                    print(f"  {i}. {model['color']} {model['storage']} ({model['part_number']})")
                
                model_choice = int(input(f"\n{Fore.GREEN}➤ 请选择型号 (1-{len(models_in_series)}): {Style.RESET_ALL}").strip())
                selected_model = models_in_series[model_choice - 1]
                
                print(f"\n{Fore.GREEN}✅ 已选择: {selected_model['name']}{Style.RESET_ALL}")
                return [selected_model]
        
        except Exception as e:
            print(f"{Fore.RED}✖ 加载型号库失败: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   提示: 确保 iphone17_all_models.json 文件存在{Style.RESET_ALL}")
            return select_products()
    
    else:
        print(f"{Fore.RED}✖ 无效选择{Style.RESET_ALL}")
        return select_products()


def select_check_interval(num_products, num_stores):
    """选择检查间隔"""
    print(f"\n{Fore.YELLOW}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⏱️  设置检查间隔:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*80}{Style.RESET_ALL}\n")
    
    # 计算推荐间隔
    safe_interval = suggest_safe_interval(num_products, num_stores)
    
    intervals = [
        {'value': 10, 'name': '10秒 - 极限模式', 'desc': '紧急抢购，发现有货立即停止'},
        {'value': 15, 'name': '15秒 - 积极模式', 'desc': '短期监控1-2小时'},
        {'value': 20, 'name': '20秒 - 平衡模式', 'desc': '速度与安全平衡'},
        {'value': 30, 'name': '30秒 - 标准模式', 'desc': '推荐，可长期运行'},
        {'value': 60, 'name': '60秒 - 保守模式', 'desc': '最安全，适合后台挂机'},
        {'value': 0, 'name': '自定义间隔', 'desc': '手动输入间隔时间'}
    ]
    
    for i, interval in enumerate(intervals, 1):
        if interval['value'] > 0:
            stats = calculate_request_frequency(num_products, num_stores, interval['value'])
            safety_indicator = f"{stats['safety_color']}{stats['icon']} {stats['safety_level']}{Style.RESET_ALL}"
            
            print(f"{i}. {interval['name']}")
            print(f"   {interval['desc']}")
            print(f"   请求频率: {stats['requests_per_minute']:.1f}次/分钟 - {safety_indicator}")
            print()
        else:
            print(f"{i}. {interval['name']}")
            print(f"   {interval['desc']}")
            print()
    
    print(f"{Fore.CYAN}💡 智能推荐间隔: {safe_interval}秒 (确保≤10次/分钟){Style.RESET_ALL}\n")
    
    while True:
        try:
            choice = input(f"{Fore.GREEN}➤ 请选择 (1-{len(intervals)}): {Style.RESET_ALL}").strip()
            idx = int(choice)
            
            if 1 <= idx <= len(intervals):
                if intervals[idx-1]['value'] == 0:
                    # 自定义
                    custom = int(input(f"{Fore.GREEN}➤ 请输入间隔秒数 (5-300): {Style.RESET_ALL}").strip())
                    if 5 <= custom <= 300:
                        # 显示评估
                        stats = calculate_request_frequency(num_products, num_stores, custom)
                        print(f"\n{Fore.CYAN}安全评估:{Style.RESET_ALL}")
                        print(f"  每轮请求: {stats['requests_per_round']}次")
                        print(f"  请求频率: {stats['requests_per_minute']:.1f}次/分钟")
                        print(f"  安全等级: {stats['safety_color']}{stats['icon']} {stats['safety_level']} ({stats['safety_score']}分){Style.RESET_ALL}")
                        print(f"  建议: {stats['recommendation']}")
                        print()
                        
                        if stats['safety_score'] < 70:
                            print(f"{Fore.YELLOW}⚠️  此配置有一定风险{Style.RESET_ALL}")
                            confirm = input(f"{Fore.YELLOW}➤ 确认使用此配置? (y/n): {Style.RESET_ALL}").strip().lower()
                            if confirm != 'y':
                                continue
                        
                        return custom
                    else:
                        print(f"{Fore.RED}✖ 间隔必须在5-300秒之间{Style.RESET_ALL}")
                else:
                    return intervals[idx-1]['value']
            else:
                print(f"{Fore.RED}✖ 请输入1-{len(intervals)}之间的数字{Style.RESET_ALL}")
        
        except ValueError:
            print(f"{Fore.RED}✖ 请输入有效的数字{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}")
            sys.exit(0)


def display_final_config(products, stores, check_interval, all_stores):
    """显示最终配置和安全评估"""
    stats = calculate_request_frequency(len(products), len(stores), check_interval)
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  📋 最终监控配置{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}📱 监控产品 ({len(products)}个):{Style.RESET_ALL}")
    for i, p in enumerate(products, 1):
        print(f"   {i}. {p['name']}")
        print(f"      Part Number: {p['part_number']}")
    print()
    
    print(f"{Fore.YELLOW}🏪 监控门店 ({len(stores)}个):{Style.RESET_ALL}")
    for i, store_num in enumerate(stores, 1):
        store = all_stores.get(store_num, {})
        print(f"   {i}. {store_num} - {store.get('storeName', 'Unknown')} ({store.get('city', '')})")
    print()
    
    print(f"{Fore.YELLOW}⚙️  监控参数:{Style.RESET_ALL}")
    print(f"   • 检查间隔: {check_interval}秒")
    print(f"   • 每轮请求: {stats['requests_per_round']}次")
    print(f"   • 每轮耗时: 约{stats['total_round_time']:.0f}秒")
    print(f"   • 请求频率: {stats['requests_per_minute']:.1f}次/分钟")
    print()
    
    print(f"{Fore.YELLOW}🛡️  安全评估:{Style.RESET_ALL}")
    print(f"   • 安全等级: {stats['safety_color']}{stats['icon']} {stats['safety_level']} ({stats['safety_score']}分){Style.RESET_ALL}")
    print(f"   • 评估结论: {stats['recommendation']}")
    print()
    
    # 额外提示
    if stats['safety_score'] >= 90:
        print(f"{Fore.GREEN}✨ 配置优秀！可以放心长期运行{Style.RESET_ALL}\n")
    elif stats['safety_score'] >= 70:
        print(f"{Fore.GREEN}👍 配置合理，注意观察运行情况{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}⚠️  建议: 如触发限制，请增加检查间隔或减少门店数量{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")


def save_to_config(products, stores, check_interval):
    """保存到配置文件"""
    try:
        # 读取现有配置
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            config = {}
        
        # 更新配置
        config['target_products'] = products
        config['target_stores'] = stores
        config['check_interval'] = check_interval
        config['all_stores'] = False
        
        # 保存其他默认配置
        if 'enable_notification' not in config:
            config['enable_notification'] = True
        if 'enable_sound' not in config:
            config['enable_sound'] = True
        if 'notification_types' not in config:
            config['notification_types'] = ['desktop', 'sound', 'log']
        if 'max_retries' not in config:
            config['max_retries'] = 3
        if 'timeout' not in config:
            config['timeout'] = 10
        if 'save_history' not in config:
            config['save_history'] = True
        if 'log_level' not in config:
            config['log_level'] = 'INFO'
        if 'user_agent' not in config:
            config['user_agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        
        # 保存
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"{Fore.GREEN}✅ 配置已保存到 config.json{Style.RESET_ALL}\n")
        return True
    except Exception as e:
        logger.error(f"保存配置失败: {e}")
        print(f"{Fore.RED}❌ 保存配置失败: {e}{Style.RESET_ALL}\n")
        return False


def run_with_interactive_config():
    """使用交互式配置运行"""
    print_banner()
    
    # 1. 选择模式
    mode = select_monitoring_mode()
    
    if mode == 1:
        # 快速开始 - 使用现有配置
        print(f"\n{Fore.GREEN}⚡ 快速开始模式{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ 使用现有配置文件 config.json{Style.RESET_ALL}\n")
        return None  # 返回None表示使用现有配置
    
    # 2. 加载门店数据
    all_stores = load_stores_data()
    if not all_stores:
        print(f"{Fore.RED}❌ 无法加载门店数据{Style.RESET_ALL}")
        sys.exit(1)
    
    # 3. 根据模式配置
    if mode == 2:
        # 标准监控模式
        print(f"\n{Fore.GREEN}⭐ 标准监控模式（推荐）{Style.RESET_ALL}")
        print(f"   正在为您配置安全参数...")
        print()
        
        products = select_products()
        stores = select_stores(all_stores, max_stores=5)
        check_interval = 15
    
    elif mode == 3:
        # 积极监控模式
        print(f"\n{Fore.GREEN}🚀 积极监控模式{Style.RESET_ALL}")
        print(f"   正在为您配置参数...")
        print()
        
        products = select_products()
        stores = select_stores(all_stores, max_stores=3)
        check_interval = 15
    
    elif mode == 4:
        # 极限监控模式
        print(f"\n{Fore.RED}🔥 极限监控模式{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   ⚠️  注意: 此模式适合紧急抢购，发现有货立即停止监控{Style.RESET_ALL}")
        print()
        
        products = select_products()
        stores = select_stores(all_stores, max_stores=1)
        
        if len(stores) > 1:
            print(f"\n{Fore.YELLOW}⚠️  极限模式只能选择1个门店，已自动选择第一个{Style.RESET_ALL}")
            stores = stores[:1]
        
        check_interval = 15
    
    else:  # mode == 5
        # 自定义模式
        print(f"\n{Fore.CYAN}🎨 自定义模式{Style.RESET_ALL}")
        print(f"   完全由您控制所有参数")
        print()
        
        products = select_products()
        stores = select_stores(all_stores)
        check_interval = select_check_interval(len(products), len(stores))
    
    # 4. 显示最终配置
    display_final_config(products, stores, check_interval, all_stores)
    
    # 5. 确认
    confirm = input(f"{Fore.GREEN}➤ 确认并开始监控? (y/n): {Style.RESET_ALL}").strip().lower()
    if confirm != 'y':
        print(f"\n{Fore.YELLOW}✖ 已取消{Style.RESET_ALL}")
        sys.exit(0)
    
    # 6. 保存配置
    save_to_config(products, stores, check_interval)
    
    # 返回配置
    return {
        'target_products': products,
        'target_stores': stores,
        'check_interval': check_interval,
        'all_stores': False,
        'enable_notification': True,
        'enable_sound': True,
        'notification_types': ['desktop', 'sound', 'log'],
        'max_retries': 3,
        'timeout': 10,
        'save_history': True,
        'log_level': 'INFO',
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }


# =============================================================================
# 以下是原main.py的监控逻辑
# =============================================================================

def display_stock_status(results: dict, monitor: AppleStoreMonitor):
    """显示库存状态"""
    with print_lock:
        print(f"\n{Fore.CYAN}{'='*100}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 库存查询结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")
        
        for part_number, data in results.items():
            product = data.get('product', {})
            product_name = f"{product.get('name', 'Unknown')} {product.get('color', '')} {product.get('storage', '')}"
            
            print(f"{Fore.YELLOW}📱 {product_name}{Style.RESET_ALL}")
            print(f"   型号: {part_number}\n")
            
            result = data.get('result', {})
            if not result.get('success', False):
                print(f"   {Fore.RED}❌ 查询失败: {result.get('error', 'Unknown')}{Style.RESET_ALL}\n")
                continue
            
            available_stores = result.get('available_stores', [])
            requested_stores_count = result.get('requested_stores_count', 0)
            responded_stores_count = result.get('responded_stores_count', 0)
            requested_stores_list = result.get('requested_stores', [])
            all_stores_data = result.get('stores', {})
            
            # 构建有响应和无响应的门店列表
            responded_stores = []
            no_response_stores = []
            
            for store_num in requested_stores_list:
                store_info = monitor.stores.get(store_num, {})
                store_name = store_info.get('storeName', store_num)
                city = store_info.get('city', '')
                
                if store_num in all_stores_data:
                    responded_stores.append(f"{store_name} ({city})")
                else:
                    no_response_stores.append(f"{store_name} ({city})")
            
            if available_stores:
                print(f"   {Fore.GREEN}✅ 有货! 共 {len(available_stores)} 个门店有货 (已查询 {requested_stores_count} 个门店){Style.RESET_ALL}\n")
                
                # 创建表格
                table_data = []
                for store in available_stores:
                    table_data.append([
                        store.get('store_name', 'Unknown'),
                        store.get('city', ''),
                        store.get('state', store.get('province', '')),
                        f"{Fore.GREEN}✓ 可取货{Style.RESET_ALL}",
                        store.get('pickup_quote', '')
                    ])
                
                headers = ['门店名称', '城市', '省份', '状态', '备注']
                print(tabulate(table_data, headers=headers, tablefmt='simple'))
                print()
            else:
                if requested_stores_count > responded_stores_count:
                    print(f"   {Fore.RED}❌ 暂无库存 (已查询 {requested_stores_count} 个门店，收到 {responded_stores_count} 个门店响应){Style.RESET_ALL}\n")
                else:
                    print(f"   {Fore.RED}❌ 暂无库存 (已查询 {requested_stores_count} 个门店){Style.RESET_ALL}\n")
            
            if responded_stores:
                print(f"   {Fore.CYAN}📡 有响应的门店 ({len(responded_stores)}个):{Style.RESET_ALL}")
                for store in responded_stores:
                    print(f"      {Fore.GREEN}✓{Style.RESET_ALL} {store}")
                print()
            
            if no_response_stores:
                print(f"   {Fore.YELLOW}⚠️  未响应的门店 ({len(no_response_stores)}个):{Style.RESET_ALL}")
                for store in no_response_stores:
                    print(f"      {Fore.YELLOW}○{Style.RESET_ALL} {store}")
                print()
        
        print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")


def monitor_loop(monitor: AppleStoreMonitor, notifier: Notifier, config: dict):
    """主监控循环"""
    products = config['target_products']
    target_stores = config.get('target_stores', []) if not config.get('all_stores', False) else None
    check_interval = config.get('check_interval', 15)
    
    iteration = 0
    
    while not stop_event.is_set():
        try:
            iteration += 1
            logger.info(f"开始第 {iteration} 轮库存检查...")
            
            # 检查所有商品
            results = monitor.check_multiple_products(products, target_stores)
            
            # 显示结果
            display_stock_status(results, monitor)
            
            # 检查库存并发送通知（持续提醒模式）
            for part_number, data in results.items():
                product = data.get('product', {})
                result = data.get('result', {})
                
                if not result.get('success'):
                    continue
                
                available_stores = result.get('available_stores', [])
                
                if available_stores:
                    # 持续提醒模式：只要有货就通知
                    if len(available_stores) == 1:
                        notifier.notify_stock_available(product, available_stores[0])
                    else:
                        notifier.notify_multiple_stores_available(product, available_stores)
                    
                    logger.info(f"🎉 {product.get('name')} 在 {len(available_stores)} 个门店有货！")
            
            # 等待下次检查
            logger.info(f"本轮检查完成，{check_interval}秒后进行下一轮...")
            stop_event.wait(check_interval)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"监控循环出错: {e}")
            notifier.notify_error(str(e))
            stop_event.wait(5)
    
    logger.info("监控循环已退出")


def main():
    """主函数"""
    # 交互式配置
    config = run_with_interactive_config()
    
    # 如果返回None，使用现有配置
    if config is None:
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            print(f"{Fore.RED}❌ 加载配置文件失败: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   请先运行 setup_monitor.py 创建配置{Style.RESET_ALL}")
            sys.exit(1)
    
    # 初始化监控器
    logger.info("正在初始化监控器...")
    monitor = AppleStoreMonitor(config, stop_event)
    
    # 初始化通知器
    notifier = Notifier(config)
    
    # 计算监控范围
    product_count = len(config['target_products'])
    store_count = len(config.get('target_stores', []))
    
    # 最终确认
    print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✨ 监控系统已就绪！{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}\n")
    print(f"  将监控 {Fore.CYAN}{product_count}{Style.RESET_ALL} 个产品在 {Fore.CYAN}{store_count}{Style.RESET_ALL} 个门店的库存情况")
    print(f"  按 {Fore.YELLOW}Ctrl+C{Style.RESET_ALL} 可随时安全停止")
    print()
    
    # 发送启动通知
    notifier.notify_monitoring_started(product_count, store_count)
    
    # 开始监控
    try:
        monitor_loop(monitor, notifier, config)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"程序异常: {e}")
        notifier.notify_error(str(e))
    
    # 导出历史记录
    if config.get('save_history', True):
        logger.info("正在导出历史记录...")
        monitor.export_history()
    
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  程序已退出。感谢使用 Apple Store 智能库存监控系统 v3.0！{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    logger.info("程序正常退出")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"程序发生错误: {e}")
        print(f"\n{Fore.RED}❌ 程序发生错误: {e}{Style.RESET_ALL}")
        sys.exit(1)