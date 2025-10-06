#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控系统 - 统一入口
支持香港和大陆双区域监控
"""

import json
import os
import sys
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


class UnifiedMonitor:
    """统一监控入口"""
    
    REGIONS = {
        'CN': {
            'name': '中国大陆',
            'name_en': 'China Mainland',
            'part_number_suffix': 'CH/A',
            'stores_file': 'apple_stores_china.json',
            'api_base': 'https://www.apple.com.cn/shop/retail/pickup-message',
            'currency': 'CNY',
            'language': 'zh-CN'
        },
        'HK': {
            'name': '中国香港',
            'name_en': 'Hong Kong',
            'part_number_suffix': 'ZA/A',
            'stores_file': 'apple_stores_hongkong.json',
            'api_base': 'https://www.apple.com/hk-zh/shop/fulfillment-messages',
            'currency': 'HKD',
            'language': 'zh-HK'
        }
    }
    
    PRESETS = {
        'HK': {
            'iphone17_promax_priority': {
                'name': 'iPhone 17 Pro Max 优先配置（香港）',
                'description': '3门店 × 3产品(256GB) = 3次/分钟',
                'config_file': 'config_hongkong_promax_priority.json'
            },
            'iphone17_promax_balanced': {
                'name': 'iPhone 17 Pro Max 平衡配置（香港）',
                'description': '6门店 × 6产品(256GB+512GB) = 6次/分钟',
                'config_file': 'config_hongkong_promax_all.json'
            },
            'custom': {
                'name': '自定义配置',
                'description': '使用 config.json',
                'config_file': 'config.json'
            }
        },
        'CN': {
            'default': {
                'name': '默认配置（大陆）',
                'description': '使用 config.json',
                'config_file': 'config.json'
            },
            'custom': {
                'name': '自定义配置',
                'description': '使用 config.json',
                'config_file': 'config.json'
            }
        }
    }
    
    def __init__(self):
        """初始化"""
        self.region = None
        self.config = None
        self.stores = None
    
    def print_banner(self):
        """打印欢迎横幅"""
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
        print(f"║                                                                   ║")
        print(f"║         🍎 Apple Store 库存监控系统 - 统一入口                   ║")
        print(f"║                                                                   ║")
        print(f"╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def select_region(self):
        """选择监控区域"""
        print(f"{Fore.YELLOW}请选择监控区域：{Style.RESET_ALL}\n")
        
        regions = list(self.REGIONS.keys())
        for i, region_code in enumerate(regions, 1):
            region_info = self.REGIONS[region_code]
            print(f"  {i}. {Fore.GREEN}{region_info['name']}{Style.RESET_ALL} ({region_info['name_en']})")
            print(f"     Part Number格式: {Fore.CYAN}{region_info['part_number_suffix']}{Style.RESET_ALL}")
            print(f"     API: {region_info['api_base']}")
            print()
        
        while True:
            try:
                choice = input(f"{Fore.YELLOW}请选择 (1-{len(regions)}): {Style.RESET_ALL}").strip()
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(regions):
                    self.region = regions[choice_idx]
                    region_info = self.REGIONS[self.region]
                    print(f"\n{Fore.GREEN}✅ 已选择: {region_info['name']} ({self.region}){Style.RESET_ALL}\n")
                    return True
                else:
                    print(f"{Fore.RED}无效选择，请重新输入{Style.RESET_ALL}")
            except (ValueError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
                return False
    
    def load_stores(self):
        """加载门店信息"""
        region_info = self.REGIONS[self.region]
        stores_file = region_info['stores_file']
        
        if not os.path.exists(stores_file):
            print(f"{Fore.RED}❌ 门店文件不存在: {stores_file}{Style.RESET_ALL}\n")
            return False
        
        try:
            with open(stores_file, 'r', encoding='utf-8') as f:
                self.stores = json.load(f)
            
            store_count = len(self.stores.get('stores', []))
            print(f"{Fore.GREEN}✅ 已加载 {store_count} 个门店信息{Style.RESET_ALL}\n")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ 加载门店信息失败: {e}{Style.RESET_ALL}\n")
            return False
    
    def select_preset(self):
        """选择预设配置"""
        presets = self.PRESETS.get(self.region, {})
        
        if not presets:
            print(f"{Fore.YELLOW}该区域暂无预设配置，将使用 config.json{Style.RESET_ALL}\n")
            return 'config.json'
        
        print(f"{Fore.YELLOW}请选择配置方案：{Style.RESET_ALL}\n")
        
        preset_keys = list(presets.keys())
        for i, preset_key in enumerate(preset_keys, 1):
            preset = presets[preset_key]
            print(f"  {i}. {Fore.GREEN}{preset['name']}{Style.RESET_ALL}")
            print(f"     {preset['description']}")
            print()
        
        while True:
            try:
                choice = input(f"{Fore.YELLOW}请选择 (1-{len(preset_keys)}): {Style.RESET_ALL}").strip()
                choice_idx = int(choice) - 1
                
                if 0 <= choice_idx < len(preset_keys):
                    selected_key = preset_keys[choice_idx]
                    config_file = presets[selected_key]['config_file']
                    print(f"\n{Fore.GREEN}✅ 已选择: {presets[selected_key]['name']}{Style.RESET_ALL}\n")
                    return config_file
                else:
                    print(f"{Fore.RED}无效选择，请重新输入{Style.RESET_ALL}")
            except (ValueError, KeyboardInterrupt):
                print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
                return None
    
    def load_config(self, config_file):
        """加载配置文件"""
        if not os.path.exists(config_file):
            print(f"{Fore.RED}❌ 配置文件不存在: {config_file}{Style.RESET_ALL}\n")
            return False
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            # 验证配置
            if 'region' in self.config:
                config_region = self.config['region']
                if config_region != self.region:
                    print(f"{Fore.YELLOW}⚠️  配置文件区域 ({config_region}) 与选择不匹配 ({self.region}){Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}   将使用选择的区域: {self.region}{Style.RESET_ALL}\n")
                    self.config['region'] = self.region
            else:
                self.config['region'] = self.region
            
            # 显示配置信息
            stores_count = len(self.config.get('target_stores', []))
            products_count = len(self.config.get('target_products', []))
            interval = self.config.get('check_interval', 60)
            
            print(f"{Fore.GREEN}✅ 配置加载成功{Style.RESET_ALL}\n")
            print(f"  监控门店: {Fore.CYAN}{stores_count}{Style.RESET_ALL} 个")
            print(f"  监控产品: {Fore.CYAN}{products_count}{Style.RESET_ALL} 个")
            print(f"  检查间隔: {Fore.CYAN}{interval}{Style.RESET_ALL} 秒")
            
            # 计算频率
            frequency = (stores_count * products_count) / (interval / 60)
            print(f"  请求频率: {Fore.CYAN}{frequency:.2f}{Style.RESET_ALL} 次/分钟", end='')
            
            if frequency < 5:
                print(f" {Fore.GREEN}✅ 非常安全{Style.RESET_ALL}")
            elif frequency < 10:
                print(f" {Fore.GREEN}✅ 安全{Style.RESET_ALL}")
            elif frequency < 15:
                print(f" {Fore.YELLOW}⚠️  接近上限{Style.RESET_ALL}")
            else:
                print(f" {Fore.RED}❌ 可能触发限制{Style.RESET_ALL}")
            
            print()
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ 加载配置失败: {e}{Style.RESET_ALL}\n")
            return False
    
    def show_summary(self):
        """显示监控摘要"""
        region_info = self.REGIONS[self.region]
        
        print(f"{Fore.CYAN}{'='*70}")
        print(f"监控配置摘要")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        print(f"  区域: {Fore.GREEN}{region_info['name']} ({self.region}){Style.RESET_ALL}")
        print(f"  Part Number格式: {Fore.GREEN}{region_info['part_number_suffix']}{Style.RESET_ALL}")
        print(f"  货币: {Fore.GREEN}{region_info['currency']}{Style.RESET_ALL}")
        print(f"  语言: {Fore.GREEN}{region_info['language']}{Style.RESET_ALL}")
        print()
        
        # 显示门店列表
        target_stores = self.config.get('target_stores', [])
        print(f"  监控门店 ({len(target_stores)} 个):")
        
        stores_dict = {s['storeNumber']: s for s in self.stores.get('stores', [])}
        for store_num in target_stores[:5]:  # 只显示前5个
            store = stores_dict.get(store_num, {})
            store_name = store.get('storeName', 'Unknown')
            print(f"    • {store_num} - {store_name}")
        
        if len(target_stores) > 5:
            print(f"    ... 及其他 {len(target_stores) - 5} 个门店")
        
        print()
        
        # 显示产品列表
        target_products = self.config.get('target_products', [])
        print(f"  监控产品 ({len(target_products)} 个):")
        
        for product in target_products[:5]:  # 只显示前5个
            part_num = product.get('part_number', 'Unknown')
            name = product.get('name', 'Unknown')
            print(f"    • {part_num} - {name}")
        
        if len(target_products) > 5:
            print(f"    ... 及其他 {len(target_products) - 5} 个产品")
        
        print()
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    def start_monitoring(self):
        """启动监控"""
        print(f"{Fore.GREEN}准备启动监控...{Style.RESET_ALL}\n")
        
        # 确认
        confirm = input(f"{Fore.YELLOW}确认启动？(y/n): {Style.RESET_ALL}").strip().lower()
        
        if confirm != 'y':
            print(f"\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
            return False
        
        print(f"\n{Fore.GREEN}{'='*70}")
        print(f"正在启动监控系统...")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        # TODO: 这里调用实际的监控模块
        # 需要根据区域选择不同的监控实现
        
        print(f"{Fore.CYAN}提示: 实际监控功能需要集成到 main.py 或创建区域特定的监控器{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}当前为演示模式{Style.RESET_ALL}\n")
        
        return True
    
    def run(self):
        """运行主流程"""
        self.print_banner()
        
        # 1. 选择区域
        if not self.select_region():
            return
        
        # 2. 加载门店信息
        if not self.load_stores():
            return
        
        # 3. 选择配置
        config_file = self.select_preset()
        if not config_file:
            return
        
        # 4. 加载配置
        if not self.load_config(config_file):
            return
        
        # 5. 显示摘要
        self.show_summary()
        
        # 6. 启动监控
        self.start_monitoring()


def main():
    """主函数"""
    try:
        monitor = UnifiedMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}错误: {e}{Style.RESET_ALL}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


