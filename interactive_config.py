#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交互式配置生成器
根据用户需求动态生成监控配置
所有数据从真实数据文件动态加载，避免硬编码错误
"""

import json
import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

def clean_input():
    """清理输入缓冲区"""
    try:
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except:
        pass  # Windows系统不支持termios


class InteractiveConfigGenerator:
    """交互式配置生成器"""
    
    def __init__(self):
        self.config = {
            "region": "CN",
            "target_products": [],
            "target_stores": [],
            "check_interval": 60,
            "notification_enabled": True,
            "sound_enabled": True,
            "save_history": True
        }
        
        # 从真实数据文件加载产品和门店信息
        self.products_data = self._load_products_data()
        self.stores_data = self._load_stores_data()
    
    def _load_products_data(self):
        """从 iphone17_all_models.json 加载产品数据"""
        try:
            with open('iphone17_all_models.json', 'r', encoding='utf-8') as f:
                products = json.load(f)
            
            # 按系列分类
            categorized = {
                "16_standard": [],
                "16_plus": [],
                "17_standard": [],
                "17_pro": [],
                "17_promax": []
            }
            
            for product in products:
                series = product.get('series', '')
                if series == 'iPhone 16':
                    categorized['16_standard'].append({
                        'name': product['name'],
                        'part_number': product['part_number'],
                        'color': product['color'],
                        'storage': product['storage']
                    })
                elif series == 'iPhone 16 Plus':
                    categorized['16_plus'].append({
                        'name': product['name'],
                        'part_number': product['part_number'],
                        'color': product['color'],
                        'storage': product['storage']
                    })
                elif series == 'iPhone 17':
                    categorized['17_standard'].append({
                        'name': product['name'],
                        'part_number': product['part_number'],
                        'color': product['color'],
                        'storage': product['storage']
                    })
                elif series == 'iPhone 17 Pro':
                    categorized['17_pro'].append({
                        'name': product['name'],
                        'part_number': product['part_number'],
                        'color': product['color'],
                        'storage': product['storage']
                    })
                elif series == 'iPhone 17 Pro Max':
                    categorized['17_promax'].append({
                        'name': product['name'],
                        'part_number': product['part_number'],
                        'color': product['color'],
                        'storage': product['storage']
                    })
            
            print(f"{Fore.GREEN}✅ 已加载产品数据: {len(products)}个型号{Style.RESET_ALL}")
            return categorized
            
        except Exception as e:
            print(f"{Fore.RED}❌ 加载产品数据失败: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}请确保 iphone17_all_models.json 文件存在{Style.RESET_ALL}")
            return {"16_standard": [], "16_plus": [], "17_standard": [], "17_pro": [], "17_promax": []}
    
    def _load_stores_data(self):
        """从 apple_stores_china.json 加载门店数据"""
        try:
            with open('apple_stores_china.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stores = data.get('stores', [])
            
            # 按城市分类，并标记热门门店
            categorized = {}
            
            # 定义热门门店（基于真实数据的门店编号）
            hot_stores = {
                'R320', 'R359', 'R401', 'R448', 'R479',  # 北京、上海旗舰
                'R484', 'R577', 'R580', 'R678', 'R761'   # 深圳、广州、成都、上海
            }
            
            for store in stores:
                if not store.get('valid', False):
                    continue
                
                city_key = store['city'].lower()
                if city_key not in categorized:
                    categorized[city_key] = []
                
                # 判断是否为热门门店
                popularity = "高" if store['storeNumber'] in hot_stores else "中"
                
                categorized[city_key].append({
                    'id': store['storeNumber'],
                    'name': store['storeName'],
                    'city': store['city'],
                    'district': store.get('state', ''),
                    'popularity': popularity,
                    'address': store.get('address', '')
                })
            
            print(f"{Fore.GREEN}✅ 已加载门店数据: {len(stores)}家门店，{len(categorized)}个城市{Style.RESET_ALL}")
            return categorized
            
        except Exception as e:
            print(f"{Fore.RED}❌ 加载门店数据失败: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}请确保 apple_stores_china.json 文件存在{Style.RESET_ALL}")
            return {}
    
    # 移除硬编码的产品和门店数据
    # 现在所有数据都从文件动态加载
    
    @property
    def IPHONE_17_PRODUCTS(self):
        """返回产品数据（动态加载）"""
        return self.products_data
    
    @property
    def MAINLAND_STORES(self):
        """返回门店数据（动态加载）"""
        return self.stores_data
    
    def print_header(self, title):
        """打印标题"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def select_strategy(self):
        """选择监控策略"""
        self.print_header("📊 步骤1: 选择监控策略")
        
        print(f"{Fore.GREEN}  1. 保守策略（推荐新手）{Style.RESET_ALL}")
        print(f"     • 1-2店 + 1-2品")
        print(f"     • 随机间隔: 3-6秒")
        print(f"     • 请求频率: 约10次/分钟")
        print(f"     • 风险等级: {Fore.GREEN}✅ 极低{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}  2. 平衡策略（推荐）{Style.RESET_ALL}")
        print(f"     • 2-3店 + 2-3品")
        print(f"     • 随机间隔: 3-6秒")
        print(f"     • 请求频率: 约10次/分钟")
        print(f"     • 风险等级: {Fore.GREEN}✅ 低{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}  3. 积极策略{Style.RESET_ALL}")
        print(f"     • 3-4店 + 3-4品")
        print(f"     • 随机间隔: 3-6秒")
        print(f"     • 请求频率: 约15次/分钟")
        print(f"     • 风险等级: {Fore.YELLOW}⚠️ 中{Style.RESET_ALL}\n")
        
        print(f"{Fore.RED}  4. 激进策略（高风险）{Style.RESET_ALL}")
        print(f"     • 5店 + 5品")
        print(f"     • 随机间隔: 2-4秒")
        print(f"     • 请求频率: 约25次/分钟")
        print(f"     • 风险等级: {Fore.RED}❌ 高（可能被限制）{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}  5. 自定义配置{Style.RESET_ALL}")
        print(f"     • 完全自主配置\n")
        
        print(f"{Fore.MAGENTA}  0. 退出程序{Style.RESET_ALL}\n")
        
        while True:
            clean_input()  # 清理输入缓冲
            choice = input(f"{Fore.GREEN}请选择策略 (1-5, 0=退出): {Style.RESET_ALL}").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            elif choice == '0':
                print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
                return None
            print(f"{Fore.RED}❌ 无效选择{Style.RESET_ALL}")
    
    def select_products(self, max_count=None):
        """选择监控产品（支持跨系列多选）"""
        self.print_header("📱 步骤2: 选择监控产品")
        
        # 统计各系列数量
        i16_std_count = len(self.IPHONE_17_PRODUCTS.get('16_standard', []))
        i16_plus_count = len(self.IPHONE_17_PRODUCTS.get('16_plus', []))
        i17_std_count = len(self.IPHONE_17_PRODUCTS.get('17_standard', []))
        i17_pro_count = len(self.IPHONE_17_PRODUCTS.get('17_pro', []))
        i17_promax_count = len(self.IPHONE_17_PRODUCTS.get('17_promax', []))
        
        print(f"{Fore.YELLOW}产品系列:{Style.RESET_ALL}\n")
        
        # 显示iPhone 16系列（如果有）
        option_num = 1
        series_map = {}
        
        if i16_std_count > 0:
            print(f"  {option_num}. {Fore.CYAN}iPhone 16 标准版（{i16_std_count}个型号）- 测试用{Style.RESET_ALL}")
            series_map[str(option_num)] = '16_standard'
            option_num += 1
        
        if i16_plus_count > 0:
            print(f"  {option_num}. {Fore.CYAN}iPhone 16 Plus（{i16_plus_count}个型号）- 测试用{Style.RESET_ALL}")
            series_map[str(option_num)] = '16_plus'
            option_num += 1
        
        # 显示iPhone 17系列
        if i17_std_count > 0:
            print(f"  {option_num}. iPhone 17 标准版（{i17_std_count}个型号）")
            series_map[str(option_num)] = '17_standard'
            option_num += 1
        
        if i17_pro_count > 0:
            print(f"  {option_num}. iPhone 17 Pro（{i17_pro_count}个型号）")
            series_map[str(option_num)] = '17_pro'
            option_num += 1
        
        if i17_promax_count > 0:
            print(f"  {option_num}. iPhone 17 Pro Max（{i17_promax_count}个型号）")
            series_map[str(option_num)] = '17_promax'
            option_num += 1
        
        print(f"\n{Fore.YELLOW}💡 提示：可以选择多个系列，用逗号分隔（如: 1,3,5）{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回上一步{Style.RESET_ALL}")
        clean_input()  # 清理输入缓冲
        series_input = input(f"\n{Fore.GREEN}请选择系列 (1-{option_num-1}，多选用逗号分隔): {Style.RESET_ALL}").strip()
        
        # 处理特殊输入
        if series_input == '0':
            print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
            return 'EXIT'
        elif series_input.lower() == 'b':
            print(f"{Fore.CYAN}↩️ 返回上一步{Style.RESET_ALL}")
            return 'BACK'
        
        # 解析用户选择的系列
        selected_series = []
        for choice in series_input.split(','):
            choice = choice.strip()
            if choice in series_map:
                selected_series.append(series_map[choice])
        
        if not selected_series:
            print(f"{Fore.RED}❌ 无效选择，使用默认（第一个系列）{Style.RESET_ALL}")
            selected_series = [list(series_map.values())[0]] if series_map else []
        
        # 收集所有选中系列的产品
        all_products = []
        for series_key in selected_series:
            products_in_series = self.IPHONE_17_PRODUCTS.get(series_key, [])
            all_products.extend(products_in_series)
        
        products = all_products
        
        print(f"\n{Fore.YELLOW}可选型号:{Style.RESET_ALL}\n")
        for i, p in enumerate(products, 1):
            print(f"  {i}. {p['name']} ({p['part_number']})")
        print(f"  {len(products)+1}. 全选")
        
        if max_count:
            print(f"\n{Fore.YELLOW}💡 建议最多选择 {max_count} 个产品{Style.RESET_ALL}")
        
        print(f"{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回上一步{Style.RESET_ALL}")
        clean_input()  # 清理输入缓冲
        choices = input(f"\n{Fore.GREEN}请选择型号（多选用逗号分隔，如: 1,2,3）: {Style.RESET_ALL}").strip()
        
        # 处理特殊输入
        if choices == '0':
            print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
            return 'EXIT'
        elif choices.lower() == 'b':
            print(f"{Fore.CYAN}↩️ 返回上一步{Style.RESET_ALL}")
            return 'BACK'
        
        selected = []
        if choices == str(len(products)+1):
            selected = products
        else:
            for choice in choices.split(','):
                try:
                    idx = int(choice.strip()) - 1
                    if 0 <= idx < len(products):
                        selected.append(products[idx])
                except:
                    pass
        
        if not selected:
            print(f"{Fore.YELLOW}⚠️ 未选择产品，默认选择第一个{Style.RESET_ALL}")
            selected = [products[0]]
        
        if max_count and len(selected) > max_count:
            print(f"{Fore.YELLOW}⚠️ 选择过多，仅保留前{max_count}个{Style.RESET_ALL}")
            selected = selected[:max_count]
        
        return selected
    
    def select_stores(self, max_count=None):
        """选择监控门店"""
        self.print_header("🏪 步骤3: 选择监控门店")
        
        if not self.MAINLAND_STORES:
            print(f"{Fore.RED}❌ 门店数据加载失败{Style.RESET_ALL}")
            return []
        
        print(f"{Fore.YELLOW}可选城市:{Style.RESET_ALL}\n")
        cities = sorted(self.MAINLAND_STORES.keys())  # 排序便于查找
        
        # 显示所有城市及门店数量
        for i, city in enumerate(cities, 1):
            store_count = len(self.MAINLAND_STORES[city])
            print(f"  {i:2d}. {city} ({store_count}家门店)")
        
        print(f"  {len(cities)+1:2d}. 所有热门门店")
        
        print(f"\n{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回上一步{Style.RESET_ALL}")
        clean_input()  # 清理输入缓冲
        city_choice = input(f"\n{Fore.GREEN}请选择城市（多选用逗号分隔，如: 1,2,3）: {Style.RESET_ALL}").strip()
        
        # 处理特殊输入
        if city_choice == '0':
            print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
            return 'EXIT'
        elif city_choice.lower() == 'b':
            print(f"{Fore.CYAN}↩️ 返回上一步{Style.RESET_ALL}")
            return 'BACK'
        
        available_stores = []
        if city_choice == str(len(cities)+1):
            # 选择所有
            for stores in self.MAINLAND_STORES.values():
                available_stores.extend(stores)
        else:
            for choice in city_choice.split(','):
                try:
                    idx = int(choice.strip()) - 1
                    if 0 <= idx < len(cities):
                        available_stores.extend(self.MAINLAND_STORES[cities[idx]])
                except:
                    pass
        
        if not available_stores:
            print(f"{Fore.YELLOW}⚠️ 未选择城市，默认选择北京{Style.RESET_ALL}")
            available_stores = self.MAINLAND_STORES['beijing']
        
        print(f"\n{Fore.YELLOW}可选门店:{Style.RESET_ALL}\n")
        for i, s in enumerate(available_stores, 1):
            popularity = s['popularity']
            pop_icon = "🔥" if popularity == "高" else "⭐"
            print(f"  {i}. {s['name']} ({s['city']}-{s['district']}) {pop_icon}")
        print(f"  {len(available_stores)+1}. 全选")
        
        if max_count:
            print(f"\n{Fore.YELLOW}💡 建议最多选择 {max_count} 个门店{Style.RESET_ALL}")
        
        print(f"{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回上一步（重新选择城市）{Style.RESET_ALL}")
        clean_input()  # 清理输入缓冲
        choices = input(f"\n{Fore.GREEN}请选择门店（多选用逗号分隔）: {Style.RESET_ALL}").strip()
        
        # 处理特殊输入
        if choices == '0':
            print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
            return 'EXIT'
        elif choices.lower() == 'b':
            print(f"{Fore.CYAN}↩️ 返回上一步（重新选择城市）{Style.RESET_ALL}")
            return 'BACK_TO_CITY'
        
        selected = []
        if choices == str(len(available_stores)+1):
            selected = available_stores
        else:
            for choice in choices.split(','):
                try:
                    idx = int(choice.strip()) - 1
                    if 0 <= idx < len(available_stores):
                        selected.append(available_stores[idx])
                except:
                    pass
        
        if not selected:
            print(f"{Fore.YELLOW}⚠️ 未选择门店，默认选择第一个{Style.RESET_ALL}")
            selected = [available_stores[0]]
        
        if max_count and len(selected) > max_count:
            print(f"{Fore.YELLOW}⚠️ 选择过多，仅保留前{max_count}个{Style.RESET_ALL}")
            selected = selected[:max_count]
        
        return selected
    
    def set_interval(self, recommended=60):
        """设置检查间隔"""
        self.print_header("⏰ 步骤4: 设置检查间隔")
        
        print(f"{Fore.YELLOW}推荐间隔: {recommended}秒{Style.RESET_ALL}\n")
        print(f"  • 60秒: {Fore.GREEN}✅ 安全，推荐{Style.RESET_ALL}")
        print(f"  • 30秒: {Fore.YELLOW}⚠️ 注意，可能触发限制{Style.RESET_ALL}")
        print(f"  • 15秒: {Fore.RED}❌ 危险，不推荐{Style.RESET_ALL}")
        
        interval = input(f"\n{Fore.GREEN}请输入检查间隔（秒，直接回车使用推荐值）: {Style.RESET_ALL}").strip()
        
        if not interval:
            return recommended
        
        try:
            interval = int(interval)
            if interval < 15:
                print(f"{Fore.RED}⚠️ 间隔过短（<15秒），强制设为15秒{Style.RESET_ALL}")
                return 15
            return interval
        except:
            print(f"{Fore.YELLOW}⚠️ 无效输入，使用推荐值{Style.RESET_ALL}")
            return recommended
    
    def calculate_frequency(self, products_count, stores_count, interval):
        """计算请求频率"""
        requests_per_check = products_count * stores_count
        frequency = requests_per_check * (60 / interval)
        
        if frequency <= 10:
            level = f"{Fore.GREEN}✅ 安全{Style.RESET_ALL}"
            risk = "低"
        elif frequency <= 30:
            level = f"{Fore.YELLOW}⚠️ 注意{Style.RESET_ALL}"
            risk = "中"
        else:
            level = f"{Fore.RED}❌ 危险{Style.RESET_ALL}"
            risk = "高"
        
        return {
            'frequency': frequency,
            'level': level,
            'risk': risk,
            'requests_per_check': requests_per_check
        }
    
    def show_summary(self, products, stores, interval):
        """显示配置摘要"""
        self.print_header("📊 配置摘要")
        
        freq_info = self.calculate_frequency(len(products), len(stores), interval)
        
        print(f"{Fore.CYAN}监控产品 ({len(products)}个):{Style.RESET_ALL}")
        for p in products:
            print(f"  • {p['name']}")
        
        print(f"\n{Fore.CYAN}监控门店 ({len(stores)}个):{Style.RESET_ALL}")
        for s in stores:
            print(f"  • {s['name']} ({s['city']})")
        
        print(f"\n{Fore.CYAN}监控参数:{Style.RESET_ALL}")
        print(f"  • 检查间隔: {interval}秒")
        print(f"  • 每轮请求: {freq_info['requests_per_check']}次")
        print(f"  • 请求频率: {freq_info['frequency']:.1f}次/分钟 {freq_info['level']}")
        
        if freq_info['risk'] == '高':
            print(f"\n{Fore.RED}{'='*70}{Style.RESET_ALL}")
            print(f"{Fore.RED}⚠️ 警告: 当前配置存在高风险！{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}可能后果:{Style.RESET_ALL}")
            print(f"  • 触发API限制（HTTP 541）")
            print(f"  • IP被临时封禁")
            print(f"  • 监控失败")
            print(f"\n{Fore.YELLOW}建议:{Style.RESET_ALL}")
            print(f"  • 减少产品或门店数量")
            print(f"  • 增加检查间隔（≥60秒）")
            print(f"  • 选择保守或平衡策略")
            print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")
        elif freq_info['risk'] == '中':
            print(f"\n{Fore.YELLOW}💡 提示: 当前配置需要注意，建议监控时关注API响应{Style.RESET_ALL}\n")
    
    def generate(self):
        """生成配置（支持返回上一步）"""
        print(f"\n{Fore.CYAN}╔{'='*68}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' '*68}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' '*20}🎯 交互式配置生成器{' '*25}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' '*68}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'='*68}╝{Style.RESET_ALL}")
        
        # 步骤1: 选择策略
        while True:
            strategy = self.select_strategy()
            
            if strategy is None:  # 用户选择退出
                return None
            
            # 步骤2: 选择产品
            while True:
                if strategy == '1':  # 保守
                    products = self.select_products(max_count=2)
                    max_stores = 2
                    interval = 30
                elif strategy == '2':  # 平衡
                    products = self.select_products(max_count=3)
                    max_stores = 3
                    interval = 60
                elif strategy == '3':  # 积极
                    products = self.select_products(max_count=4)
                    max_stores = 4
                    interval = 90
                elif strategy == '4':  # 激进
                    products = self.select_products(max_count=5)
                    max_stores = 5
                    interval = 90
                else:  # 自定义
                    products = self.select_products()
                    max_stores = None
                    interval = None
                
                if products == 'EXIT':
                    return None
                elif products == 'BACK':
                    break  # 返回步骤1
                
                # 步骤3: 选择门店
                while True:
                    if max_stores:
                        stores = self.select_stores(max_count=max_stores)
                    else:
                        stores = self.select_stores()
                    
                    if stores == 'EXIT':
                        return None
                    elif stores == 'BACK':
                        break  # 返回步骤2
                    elif stores == 'BACK_TO_CITY':
                        continue  # 重新选择门店
                    
                    # 自定义策略需要设置间隔
                    if strategy == '5' and interval is None:
                        interval = self.set_interval()
                    
                    # 显示摘要并确认
                    self.show_summary(products, stores, interval)
        
                    # 确认
                    print(f"\n{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回重新选择{Style.RESET_ALL}")
                    clean_input()  # 清理输入缓冲
                    confirm = input(f"{Fore.GREEN}确认使用此配置？(y/n/b/0): {Style.RESET_ALL}").strip().lower()
                    
                    if confirm == '0':
                        return None
                    elif confirm == 'b':
                        break  # 返回步骤3
                    elif confirm == 'y':
                        # 生成配置并返回
                        return self._save_config(products, stores, interval)
                    else:
                        print(f"{Fore.YELLOW}已取消{Style.RESET_ALL}")
                        return None
    
    def _save_config(self, products, stores, interval):
        """保存配置到文件"""
        # 生成配置
        self.config['target_products'] = [
            {
                'name': p['name'],
                'part_number': p['part_number'],
                'color': p['color'],
                'storage': p['storage'],
                'priority': 'high'
            }
            for p in products
        ]
        
        self.config['target_stores'] = [s['id'] for s in stores]
        self.config['check_interval'] = interval
        
        return self.config


if __name__ == "__main__":
    generator = InteractiveConfigGenerator()
    config = generator.generate()
    
    if config:
        # 保存配置
        with open('config_custom.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Fore.GREEN}✅ 配置已保存到: config_custom.json{Style.RESET_ALL}")

