#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍎 Apple Store 库存监控 - 交互式配置工具
让每个用户轻松配置自己想要监控的机型
"""

import json
import sys
import os
from colorama import Fore, Style, init

# 初始化colorama
init(autoreset=True)

def print_header():
    """打印欢迎界面"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}╔══════════════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║                                                                  ║")
    print(f"{Fore.GREEN}║     🍎  Apple Store 库存监控 - 配置向导  🍎                    ║")
    print(f"{Fore.GREEN}║                                                                  ║")
    print(f"{Fore.GREEN}║         让我们一起配置您的专属监控方案                          ║")
    print(f"{Fore.GREEN}║                                                                  ║")
    print(f"{Fore.GREEN}╚══════════════════════════════════════════════════════════════════╝")
    print(f"{Fore.CYAN}{'='*70}\n{Style.RESET_ALL}")

def load_models():
    """加载iPhone型号数据"""
    try:
        with open('iphone17_all_models.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 错误：找不到型号数据文件{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 请确保 iphone17_all_models.json 存在{Style.RESET_ALL}")
        sys.exit(1)

def load_stores():
    """加载门店数据"""
    try:
        with open('apple_stores_china.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('stores', [])
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 错误：找不到门店数据文件{Style.RESET_ALL}")
        sys.exit(1)

def display_series_menu():
    """显示系列选择菜单"""
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}📱 第1步：选择iPhone系列{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"{Fore.WHITE}请选择您想要监控的系列：\n")
    print(f"  {Fore.YELLOW}1.{Style.RESET_ALL} iPhone 17 (10个型号)")
    print(f"     {Fore.CYAN}├─{Style.RESET_ALL} 5种颜色：黑色、白色、青雾蓝色、薰衣草紫色、鼠尾草绿色")
    print(f"     {Fore.CYAN}└─{Style.RESET_ALL} 2种容量：256GB、512GB\n")
    
    print(f"  {Fore.YELLOW}2.{Style.RESET_ALL} iPhone 17 Pro (9个型号)")
    print(f"     {Fore.CYAN}├─{Style.RESET_ALL} 3种颜色：银色、星宇橙色、深蓝色")
    print(f"     {Fore.CYAN}└─{Style.RESET_ALL} 3种容量：256GB、512GB、1TB\n")
    
    print(f"  {Fore.YELLOW}3.{Style.RESET_ALL} iPhone 17 Pro Max (12个型号)")
    print(f"     {Fore.CYAN}├─{Style.RESET_ALL} 3种颜色：银色、星宇橙色、深蓝色")
    print(f"     {Fore.CYAN}└─{Style.RESET_ALL} 4种容量：256GB、512GB、1TB、2TB\n")
    
    print(f"  {Fore.YELLOW}4.{Style.RESET_ALL} iPhone 16 系列 (测试用)")
    print(f"     {Fore.CYAN}└─{Style.RESET_ALL} 已知有货的型号，用于测试程序\n")
    
    print(f"  {Fore.YELLOW}5.{Style.RESET_ALL} 混合选择 (从所有型号中自由选择)\n")

def select_models_by_filters(models, series):
    """通过筛选条件选择型号"""
    filtered = [m for m in models if m['series'] == series]
    
    # 提取颜色和容量选项
    colors = []
    storages = []
    
    for m in filtered:
        desc = m['description']
        
        # 提取容量
        for s in ['2TB', '1TB', '512GB', '256GB', '128GB']:
            if s in desc:
                storages.append(s)
                break
        
        # 提取颜色（在容量和编号之间的文字）
        # 格式：苹果iPhone17 Pro Max 2TB 银色 0F4-154
        parts = desc.split()
        color = ''
        for i, part in enumerate(parts):
            # 找到容量后面的词，且不包含数字和特殊字符的就是颜色
            if any(cap in part for cap in ['GB', 'TB']) and i+1 < len(parts):
                next_part = parts[i+1]
                # 如果下一个词不包含数字和'-'，就是颜色
                if not any(char.isdigit() or char == '-' for char in next_part):
                    color = next_part
                    break
        
        if color and color not in colors:
            colors.append(color)
    
    colors = sorted(colors)
    storages = sorted(set(storages), key=lambda x: int(x.replace('GB', '').replace('TB', '000')))
    
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}🎨 第2步：选择配置{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 选择容量
    print(f"{Fore.WHITE}可选容量：")
    for i, storage in enumerate(storages, 1):
        print(f"  {Fore.YELLOW}{i}.{Style.RESET_ALL} {storage}")
    
    print(f"\n{Fore.CYAN}💡 提示：输入数字选择，多个用逗号分隔（如：1,2），输入 0 选择全部{Style.RESET_ALL}")
    storage_input = input(f"{Fore.GREEN}请选择容量：{Style.RESET_ALL}").strip()
    
    selected_storages = []
    if storage_input == '0':
        selected_storages = storages
    else:
        indices = [int(x.strip()) for x in storage_input.split(',') if x.strip().isdigit()]
        selected_storages = [storages[i-1] for i in indices if 0 < i <= len(storages)]
    
    # 选择颜色
    print(f"\n{Fore.WHITE}可选颜色：")
    for i, color in enumerate(colors, 1):
        print(f"  {Fore.YELLOW}{i}.{Style.RESET_ALL} {color}")
    
    print(f"\n{Fore.CYAN}💡 提示：输入数字选择，多个用逗号分隔，输入 0 选择全部{Style.RESET_ALL}")
    color_input = input(f"{Fore.GREEN}请选择颜色：{Style.RESET_ALL}").strip()
    
    selected_colors = []
    if color_input == '0':
        selected_colors = colors
    else:
        indices = [int(x.strip()) for x in color_input.split(',') if x.strip().isdigit()]
        selected_colors = [colors[i-1] for i in indices if 0 < i <= len(colors)]
    
    # 筛选出符合条件的型号
    result = []
    for model in filtered:
        desc = model['description']
        # 检查容量
        has_storage = any(s in desc for s in selected_storages)
        # 检查颜色
        has_color = any(c in desc for c in selected_colors)
        
        if has_storage and has_color:
            result.append(model)
    
    return result

def select_stores():
    """选择监控门店"""
    stores = load_stores()
    
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}🏪 第3步：选择监控门店{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    print(f"{Fore.WHITE}选择方式：\n")
    print(f"  {Fore.YELLOW}1.{Style.RESET_ALL} 推荐门店 (北京、上海、深圳等5个主要门店)")
    print(f"  {Fore.YELLOW}2.{Style.RESET_ALL} 按城市选择")
    print(f"  {Fore.YELLOW}3.{Style.RESET_ALL} 全部门店 (42个，查询较慢)")
    print(f"  {Fore.YELLOW}4.{Style.RESET_ALL} 自定义输入门店编号\n")
    
    choice = input(f"{Fore.GREEN}请选择 (1-4)：{Style.RESET_ALL}").strip()
    
    if choice == '1':
        # 推荐门店
        return ['R485', 'R448', 'R409', 'R388', 'R505'], False
    
    elif choice == '2':
        # 按城市选择
        cities = {}
        for store in stores:
            city = store['city']
            if city not in cities:
                cities[city] = []
            cities[city].append(store)
        
        print(f"\n{Fore.WHITE}可选城市：\n")
        city_list = sorted(cities.keys())
        for i, city in enumerate(city_list, 1):
            count = len(cities[city])
            print(f"  {Fore.YELLOW}{i:2d}.{Style.RESET_ALL} {city} ({count}家门店)")
            if i % 3 == 0:
                print()
        
        print(f"\n{Fore.CYAN}💡 提示：输入数字选择城市，多个用逗号分隔{Style.RESET_ALL}")
        city_input = input(f"{Fore.GREEN}请选择城市：{Style.RESET_ALL}").strip()
        
        indices = [int(x.strip()) for x in city_input.split(',') if x.strip().isdigit()]
        selected_stores = []
        for i in indices:
            if 0 < i <= len(city_list):
                city = city_list[i-1]
                selected_stores.extend([s['storeNumber'] for s in cities[city]])
        
        return selected_stores, False
    
    elif choice == '3':
        # 全部门店
        print(f"\n{Fore.RED}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.RED}⚠️  重要警告：监控全部42个门店{Style.RESET_ALL}")
        print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}风险：{Style.RESET_ALL}")
        print(f"  • 查询时间长：每个产品约90秒")
        print(f"  • 触发限制：查询35个门店后可能被限制")
        print(f"  • 成功率低：第2/3个产品可能全部失败")
        print(f"  • IP风险：可能需要等待30-60分钟才能恢复\n")
        print(f"{Fore.GREEN}建议方案：{Style.RESET_ALL}")
        print(f"  ✅ 按城市选择（选项2）- 选择10-15个门店")
        print(f"  ✅ 推荐门店（选项1）- 5个核心门店，成功率>95%")
        print(f"  ✅ 分批监控 - 早上监控北京，下午监控上海\n")
        confirm = input(f"{Fore.RED}仍然确认选择全部42个门店？(y/n)：{Style.RESET_ALL}").strip().lower()
        if confirm == 'y':
            print(f"\n{Fore.YELLOW}💡 提示：建议将检查间隔设置为180秒或更长{Style.RESET_ALL}")
            return [], True
        else:
            return select_stores()  # 重新选择
    
    elif choice == '4':
        # 自定义输入
        print(f"\n{Fore.WHITE}请输入门店编号，多个用逗号分隔 (如：R485,R448,R409)")
        print(f"{Fore.CYAN}💡 查看门店编号：cat apple_stores_china.json{Style.RESET_ALL}\n")
        store_input = input(f"{Fore.GREEN}门店编号：{Style.RESET_ALL}").strip()
        selected_stores = [s.strip() for s in store_input.split(',')]
        return selected_stores, False
    
    else:
        print(f"{Fore.RED}无效选择，请重新输入{Style.RESET_ALL}")
        return select_stores()

def configure_parameters(model_count, store_count):
    """配置监控参数"""
    print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"{Fore.GREEN}⚙️  第4步：配置监控参数{Style.RESET_ALL}")
    print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 计算预估查询次数
    queries_per_round = model_count * store_count
    
    # 根据查询量推荐间隔
    if queries_per_round <= 10:
        recommended_interval = 15
        risk = "🟢 低"
    elif queries_per_round <= 20:
        recommended_interval = 15
        risk = "🟢 低"
    elif queries_per_round <= 40:
        recommended_interval = 15
        risk = "🟡 中"
    elif queries_per_round <= 80:
        recommended_interval = 15
        risk = "🟠 中高"
    else:
        recommended_interval = 15
        risk = "🔴 高"
    
    print(f"{Fore.WHITE}根据您的配置：")
    print(f"  • 监控型号：{Fore.YELLOW}{model_count}{Style.RESET_ALL} 个")
    print(f"  • 监控门店：{Fore.YELLOW}{store_count}{Style.RESET_ALL} 个")
    print(f"  • 每轮查询：{Fore.YELLOW}{queries_per_round}{Style.RESET_ALL} 次")
    print(f"  • 风险等级：{risk}\n")
    
    print(f"{Fore.CYAN}💡 推荐检查间隔：{Fore.YELLOW}{recommended_interval}秒{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   (平衡了响应速度和API限制风险)\n")
    
    # 对大量查询给出特别警告
    if queries_per_round > 80:
        print(f"{Fore.RED}⚠️  警告：您的配置查询量很大（{queries_per_round}次/轮）{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   • Apple会在查询约35个门店后触发限制{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   • 建议减少型号数量或门店数量{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   • 或者分时段监控不同城市\n{Style.RESET_ALL}")
    
    print(f"{Fore.WHITE}常用间隔选项：")
    print(f"  {Fore.YELLOW}1.{Style.RESET_ALL} 30秒  - 快速响应（适合1-2个型号）")
    print(f"  {Fore.YELLOW}2.{Style.RESET_ALL} 60秒  - 平衡模式（推荐）")
    print(f"  {Fore.YELLOW}3.{Style.RESET_ALL} 90秒  - 保守模式（多型号/多门店）")
    print(f"  {Fore.YELLOW}4.{Style.RESET_ALL} 120秒 - 安全模式")
    print(f"  {Fore.YELLOW}5.{Style.RESET_ALL} 180秒 - 超安全模式（大量门店）")
    print(f"  {Fore.YELLOW}6.{Style.RESET_ALL} 自定义\n")
    
    choice = input(f"{Fore.GREEN}请选择 (直接回车使用推荐值 {recommended_interval}秒)：{Style.RESET_ALL}").strip()
    
    interval_map = {'1': 15, '2': 15, '3': 15, '4': 15, '5': 15}
    
    if not choice:
        check_interval = recommended_interval
    elif choice in interval_map:
        check_interval = interval_map[choice]
    elif choice == '6':
        custom = input(f"{Fore.GREEN}请输入间隔秒数 (建议>=30)：{Style.RESET_ALL}").strip()
        check_interval = int(custom) if custom.isdigit() else recommended_interval
    else:
        check_interval = recommended_interval
    
    print(f"\n{Fore.GREEN}✅ 检查间隔设置为：{check_interval}秒{Style.RESET_ALL}")
    
    return {
        'check_interval': check_interval,
        'enable_notification': True,
        'enable_sound': True,
        'notification_types': ['desktop', 'sound', 'log'],
        'max_retries': 3,
        'timeout': 10,
        'save_history': True,
        'log_level': 'INFO',
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

def format_model_for_config(model):
    """格式化型号为配置格式"""
    desc = model['description']
    
    # 提取容量
    storage = ''
    for s in ['2TB', '1TB', '512GB', '256GB', '128GB']:
        if s in desc:
            storage = s
            break
    
    # 提取颜色（在容量和编号之间，不包含数字和'-'的词）
    parts = desc.split()
    color = ''
    for i, part in enumerate(parts):
        # 找到容量
        if any(cap in part for cap in ['GB', 'TB']) and i+1 < len(parts):
            # 容量后面的词，如果不包含数字和'-'，就是颜色
            next_part = parts[i+1]
            if not any(char.isdigit() or char == '-' for char in next_part):
                color = next_part
                break
    
    return {
        'name': f"{model['series']} {color} {storage}",
        'part_number': model['part_number'],
        'color': color,
        'storage': storage,
        'series': model['series']
    }

def save_config(products, target_stores, all_stores, params):
    """保存配置到文件"""
    config = {
        'target_products': products,
        'all_stores': all_stores,
        'target_stores': target_stores if not all_stores else [],
        **params
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n{Fore.GREEN}✅ 配置已保存到 config.json{Style.RESET_ALL}")

def show_summary(products, target_stores, all_stores, params):
    """显示配置摘要"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.GREEN}📋 配置摘要{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}\n")
    
    print(f"{Fore.WHITE}监控型号 ({len(products)}个)：")
    for i, p in enumerate(products, 1):
        print(f"  {Fore.YELLOW}{i}.{Style.RESET_ALL} {p['name']} ({p['part_number']})")
    
    print(f"\n{Fore.WHITE}监控门店：")
    if all_stores:
        print(f"  {Fore.YELLOW}全部 42 个门店{Style.RESET_ALL}")
    else:
        print(f"  {Fore.YELLOW}{len(target_stores)} 个门店{Style.RESET_ALL}")
        if len(target_stores) <= 10:
            for store in target_stores:
                print(f"  • {store}")
    
    print(f"\n{Fore.WHITE}监控参数：")
    print(f"  • 检查间隔：{Fore.YELLOW}{params['check_interval']}秒{Style.RESET_ALL}")
    print(f"  • 桌面通知：{Fore.GREEN}开启{Style.RESET_ALL}")
    print(f"  • 声音提醒：{Fore.GREEN}开启{Style.RESET_ALL}")
    print(f"  • 保存历史：{Fore.GREEN}开启{Style.RESET_ALL}")
    
    # 计算预估
    store_count = 42 if all_stores else len(target_stores)
    queries_per_round = len(products) * store_count
    time_per_round = queries_per_round * 1.2 + (queries_per_round // 5) * 2
    total_cycle = time_per_round + params['check_interval']
    
    print(f"\n{Fore.WHITE}预估运行情况：")
    print(f"  • 每轮查询次数：{Fore.YELLOW}{queries_per_round}{Style.RESET_ALL} 次")
    print(f"  • 每轮查询耗时：约 {Fore.YELLOW}{int(time_per_round)}{Style.RESET_ALL} 秒")
    print(f"  • 总周期时间：约 {Fore.YELLOW}{int(total_cycle)}{Style.RESET_ALL} 秒")
    print(f"  • 每小时查询：约 {Fore.YELLOW}{int(3600/total_cycle)}{Style.RESET_ALL} 轮\n")
    
    print(f"{Fore.CYAN}{'='*70}\n{Style.RESET_ALL}")

def main():
    """主函数"""
    try:
        print_header()
        
        # 加载数据
        all_models = load_models()
        
        # 第1步：选择系列
        display_series_menu()
        series_choice = input(f"{Fore.GREEN}请选择 (1-5)：{Style.RESET_ALL}").strip()
        
        selected_models = []
        
        if series_choice == '1':
            selected_models = select_models_by_filters(all_models, 'iPhone 17')
        elif series_choice == '2':
            selected_models = select_models_by_filters(all_models, 'iPhone 17 Pro')
        elif series_choice == '3':
            selected_models = select_models_by_filters(all_models, 'iPhone 17 Pro Max')
        elif series_choice == '4':
            # iPhone 16 测试型号
            selected_models = [{
                'series': 'iPhone 16 Plus',
                'part_number': 'MXUA3CH/A',
                'description': 'iPhone 16 Plus 白色 128GB'
            }]
        elif series_choice == '5':
            # 混合选择 - 待实现
            print(f"\n{Fore.YELLOW}功能开发中...{Style.RESET_ALL}")
            return
        else:
            print(f"{Fore.RED}无效选择{Style.RESET_ALL}")
            return
        
        if not selected_models:
            print(f"\n{Fore.RED}❌ 未选择任何型号{Style.RESET_ALL}")
            return
        
        # 格式化型号
        products = [format_model_for_config(m) for m in selected_models]
        
        print(f"\n{Fore.GREEN}✅ 已选择 {len(products)} 个型号{Style.RESET_ALL}")
        
        # 第3步：选择门店
        target_stores, all_stores = select_stores()
        
        # 第4步：配置参数
        store_count = 42 if all_stores else len(target_stores)
        params = configure_parameters(len(products), store_count)
        
        # 显示摘要
        show_summary(products, target_stores, all_stores, params)
        
        # 确认并保存
        confirm = input(f"{Fore.GREEN}确认保存配置并开始监控？(y/n)：{Style.RESET_ALL}").strip().lower()
        
        if confirm == 'y':
            save_config(products, target_stores, all_stores, params)
            
            print(f"\n{Fore.CYAN}{'='*70}")
            print(f"{Fore.GREEN}🎉 配置完成！{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*70}\n")
            
            print(f"{Fore.WHITE}下一步操作：\n")
            print(f"  {Fore.YELLOW}启动监控：{Style.RESET_ALL}")
            print(f"    python3 main.py\n")
            print(f"  {Fore.YELLOW}后台运行：{Style.RESET_ALL}")
            print(f"    nohup python3 main.py > monitor.log 2>&1 &\n")
            print(f"  {Fore.YELLOW}查看日志：{Style.RESET_ALL}")
            print(f"    tail -f monitor.log\n")
            
            # 询问是否立即启动
            start_now = input(f"{Fore.GREEN}是否立即启动监控？(y/n)：{Style.RESET_ALL}").strip().lower()
            if start_now == 'y':
                os.system('python3 main.py')
        else:
            print(f"\n{Fore.YELLOW}配置已取消{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}👋 配置已取消{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ 错误：{e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main()
