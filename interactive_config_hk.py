#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
香港区域交互式配置生成器
根据用户需求动态生成香港监控配置
所有数据从真实数据文件动态加载
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


class InteractiveConfigGeneratorHK:
    """香港区域交互式配置生成器"""
    
    def __init__(self):
        self.config = {
            "region": "HK",
            "target_products": [],
            "target_stores": [],
            "check_interval": 60,
            "notification_enabled": True,
            "sound_enabled": True,
            "save_history": True
        }
        
        # 从真实数据文件加载香港产品和门店信息
        self.products_data = self._load_hk_products()
        self.stores_data = self._load_hk_stores()
    
    def _load_hk_products(self):
        """加载香港产品数据（包括iPhone 16和iPhone 17）"""
        try:
            products = {
                "16_standard": [],
                "17_promax": []
            }
            
            # 加载iPhone 16数据（测试用）
            if os.path.exists('iphone16_hongkong.json'):
                with open('iphone16_hongkong.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    models = data.get('models', [])
                    
                    for model in models:
                        products['16_standard'].append({
                            'name': f"iPhone 16 {model.get('color', '')} {model.get('storage', '')}",
                            'part_number': model['part_number'],
                            'color': model.get('color', ''),
                            'storage': model.get('storage', ''),
                            'priority': model.get('priority', 'test')
                        })
            
            # 加载iPhone 17 Pro Max香港版数据
            if os.path.exists('iphone17_promax_hongkong_complete.json'):
                with open('iphone17_promax_hongkong_complete.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    models = data.get('models', [])
                    
                    for model in models:
                        products['17_promax'].append({
                            'name': f"iPhone 17 Pro Max {model.get('color', '')} {model.get('storage', '')}",
                            'part_number': model['part_number'],
                            'color': model.get('color', ''),
                            'storage': model.get('storage', ''),
                            'priority': model.get('priority', 'medium')
                        })
            
            total_count = len(products['16_standard']) + len(products['17_promax'])
            if total_count > 0:
                print(f"{Fore.GREEN}✅ 已加载香港产品数据: {total_count}个型号{Style.RESET_ALL}")
                if len(products['16_standard']) > 0:
                    print(f"{Fore.CYAN}   • iPhone 16: {len(products['16_standard'])}个 (测试用){Style.RESET_ALL}")
                if len(products['17_promax']) > 0:
                    print(f"   • iPhone 17 Pro Max: {len(products['17_promax'])}个")
            else:
                print(f"{Fore.YELLOW}⚠️ 未找到香港产品数据{Style.RESET_ALL}")
            
            return products
            
        except Exception as e:
            print(f"{Fore.RED}❌ 加载香港产品数据失败: {e}{Style.RESET_ALL}")
            return {"17_promax": []}
    
    def _load_hk_stores(self):
        """加载香港门店数据"""
        try:
            with open('apple_stores_hongkong.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stores = data.get('stores', [])
            
            # 分类门店（核心门店vs全部门店）
            categorized = {
                'core': [],  # 核心门店
                'all': []    # 所有门店
            }
            
            # 定义核心门店（热门位置）
            core_store_numbers = ['R409', 'R428', 'R485']  # 銅鑼灣、ifc、廣東道
            
            for store in stores:
                store_number = store.get('storeNumber')
                store_info = {
                    'store_number': store_number,
                    'name': store.get('storeNameZH', store.get('storeName', '')),
                    'name_en': store.get('storeNameEN', ''),
                    'district': store.get('district', ''),
                    'address': store.get('address', ''),
                    'is_core': store_number in core_store_numbers
                }
                
                categorized['all'].append(store_info)
                
                if store_number in core_store_numbers:
                    categorized['core'].append(store_info)
            
            print(f"{Fore.GREEN}✅ 已加载香港门店数据: {len(categorized['all'])}家门店（{len(categorized['core'])}家核心）{Style.RESET_ALL}")
            return categorized
            
        except Exception as e:
            print(f"{Fore.RED}❌ 加载香港门店数据失败: {e}{Style.RESET_ALL}")
            return {"core": [], "all": []}
    
    @property
    def IPHONE_17_PRODUCTS(self):
        """获取产品数据"""
        return self.products_data
    
    @property
    def HONGKONG_STORES(self):
        """获取门店数据"""
        return self.stores_data
    
    # 预设策略（适合香港6家门店的规模）
    STRATEGIES = {
        '1': {
            'name': '保守策略（推荐新手）',
            'stores_range': (1, 2),
            'products_range': (1, 2),
            'check_interval': 30,
            'max_requests_per_min': 8,
            'risk': '✅ 极低'
        },
        '2': {
            'name': '平衡策略（推荐）',
            'stores_range': (2, 3),
            'products_range': (2, 3),
            'check_interval': 30,
            'max_requests_per_min': 10,
            'risk': '✅ 低'
        },
        '3': {
            'name': '积极策略',
            'stores_range': (3, 4),
            'products_range': (3, 4),
            'check_interval': 25,
            'max_requests_per_min': 15,
            'risk': '⚠️ 中'
        },
        '4': {
            'name': '全店全品（高风险）',
            'stores_range': (6, 6),
            'products_range': (6, 12),
            'check_interval': 45,
            'max_requests_per_min': 25,
            'risk': '❌ 高（可能被限制）'
        }
    }
    
    def print_header(self):
        """打印标题"""
        print(f"\n{Fore.CYAN}╔{'='*68}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' '*68}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' '*20}🇭🇰 香港区域交互式配置生成器{' '*19}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{' '*68}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'='*68}╝{Style.RESET_ALL}")
    
    def select_strategy(self):
        """选择监控策略"""
        print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 步骤1: 选择监控策略{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
        
        for key, strategy in self.STRATEGIES.items():
            store_min, store_max = strategy['stores_range']
            prod_min, prod_max = strategy['products_range']
            
            print(f"  {key}. {strategy['name']}")
            print(f"     • {store_min}-{store_max}店 + {prod_min}-{prod_max}品")
            print(f"     • 随机间隔: 3-6秒")
            print(f"     • 请求频率: 约{strategy['max_requests_per_min']}次/分钟")
            print(f"     • 风险等级: {strategy['risk']}\n")
        
        print(f"  5. 自定义配置")
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
            print(f"{Fore.RED}❌ 无效选择，请输入 1-5 或 0{Style.RESET_ALL}")
    
    def select_products(self, strategy_id):
        """选择监控产品"""
        print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📱 步骤2: 选择监控产品{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
        
        iphone16_models = self.IPHONE_17_PRODUCTS.get('16_standard', [])
        promax_models = self.IPHONE_17_PRODUCTS.get('17_promax', [])
        
        if not iphone16_models and not promax_models:
            print(f"{Fore.RED}❌ 没有可用的香港产品数据{Style.RESET_ALL}")
            return []
        
        all_options = []
        index = 1
        
        # 显示iPhone 16（测试用）
        if iphone16_models:
            print(f"  {Fore.CYAN}【iPhone 16 - 测试用（有库存）】{Style.RESET_ALL}")
            for product in iphone16_models:
                print(f"  {index}. {product['name']} ({product['part_number']}) {Fore.GREEN}✅ 测试{Style.RESET_ALL}")
                all_options.append(product)
                index += 1
            print()
        
        # 显示iPhone 17 Pro Max
        if promax_models:
            print(f"{Fore.CYAN}iPhone 17 Pro Max 香港版（{len(promax_models)}个型号）:{Style.RESET_ALL}\n")
            
            # 按容量和优先级分组显示
            high_priority = [p for p in promax_models if p.get('priority') == 'high']
            medium_priority = [p for p in promax_models if p.get('priority') == 'medium']
            low_priority = [p for p in promax_models if p.get('priority') == 'low']
            
            if high_priority:
                print(f"  {Fore.GREEN}【高优先级 - 256GB 热门配置】{Style.RESET_ALL}")
                for product in high_priority:
                    print(f"  {index}. {product['name']} ({product['part_number']})")
                    all_options.append(product)
                    index += 1
                print()
            
            if medium_priority:
                print(f"  {Fore.YELLOW}【中优先级 - 512GB/1TB 配置】{Style.RESET_ALL}")
                for product in medium_priority:
                    print(f"  {index}. {product['name']} ({product['part_number']})")
                    all_options.append(product)
                    index += 1
                print()
            
            if low_priority:
                print(f"  {Fore.CYAN}【低优先级 - 2TB 配置】{Style.RESET_ALL}")
                for product in low_priority:
                    print(f"  {index}. {product['name']} ({product['part_number']})")
                    all_options.append(product)
                    index += 1
                print()
        
        print(f"  {index}. {Fore.GREEN}全选{Style.RESET_ALL}\n")
        
        # 根据策略给出建议
        if strategy_id in self.STRATEGIES:
            _, max_products = self.STRATEGIES[strategy_id]['products_range']
            print(f"{Fore.YELLOW}💡 建议最多选择 {max_products} 个产品{Style.RESET_ALL}\n")
        
        print(f"{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回上一步{Style.RESET_ALL}\n")
        
        while True:
            clean_input()  # 清理输入缓冲
            selection = input(f"{Fore.GREEN}请选择型号（多选用逗号分隔，如: 1,2,3）: {Style.RESET_ALL}").strip()
            
            # 处理特殊输入
            if selection == '0':
                print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
                return 'EXIT'
            elif selection.lower() == 'b':
                print(f"{Fore.CYAN}↩️ 返回上一步{Style.RESET_ALL}")
                return 'BACK'
            
            try:
                if selection == str(index):  # 全选
                    return all_options
                
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                
                if all(0 <= i < len(all_options) for i in indices):
                    selected = [all_options[i] for i in indices]
                    
                    # 检查是否符合策略建议
                    if strategy_id in self.STRATEGIES:
                        _, max_products = self.STRATEGIES[strategy_id]['products_range']
                        if len(selected) > max_products:
                            print(f"{Fore.YELLOW}⚠️  选择了 {len(selected)} 个产品，超过建议的 {max_products} 个{Style.RESET_ALL}")
                            confirm = input(f"{Fore.YELLOW}是否继续？(y/n): {Style.RESET_ALL}").strip().lower()
                            if confirm != 'y':
                                continue
                    
                    return selected
                else:
                    print(f"{Fore.RED}❌ 无效选择，请重新输入{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ 输入格式错误，请使用逗号分隔的数字{Style.RESET_ALL}")
    
    def select_stores(self, strategy_id):
        """选择监控门店"""
        print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🏪 步骤3: 选择监控门店{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
        
        all_stores = self.HONGKONG_STORES['all']
        core_stores = self.HONGKONG_STORES['core']
        
        if not all_stores:
            print(f"{Fore.RED}❌ 没有可用的香港门店数据{Style.RESET_ALL}")
            return []
        
        print(f"{Fore.GREEN}【核心门店（推荐）】{Style.RESET_ALL}")
        index = 1
        for store in core_stores:
            print(f"  {index}. {store['name']} ({store['district']}) ⭐")
            print(f"     {Fore.CYAN}{store['name_en']}{Style.RESET_ALL}")
            index += 1
        
        print(f"\n{Fore.CYAN}【其他门店】{Style.RESET_ALL}")
        other_stores = [s for s in all_stores if s['store_number'] not in [c['store_number'] for c in core_stores]]
        for store in other_stores:
            print(f"  {index}. {store['name']} ({store['district']})")
            print(f"     {Fore.CYAN}{store['name_en']}{Style.RESET_ALL}")
            index += 1
        
        print(f"\n  {index}. {Fore.GREEN}全选（6家门店）{Style.RESET_ALL}\n")
        
        # 根据策略给出建议
        if strategy_id in self.STRATEGIES:
            _, max_stores = self.STRATEGIES[strategy_id]['stores_range']
            print(f"{Fore.YELLOW}💡 建议最多选择 {max_stores} 个门店{Style.RESET_ALL}\n")
        
        print(f"{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回上一步{Style.RESET_ALL}\n")
        
        while True:
            clean_input()  # 清理输入缓冲
            selection = input(f"{Fore.GREEN}请选择门店（多选用逗号分隔）: {Style.RESET_ALL}").strip()
            
            # 处理特殊输入
            if selection == '0':
                print(f"{Fore.YELLOW}👋 已退出配置{Style.RESET_ALL}")
                return 'EXIT'
            elif selection.lower() == 'b':
                print(f"{Fore.CYAN}↩️ 返回上一步{Style.RESET_ALL}")
                return 'BACK'
            
            try:
                if selection == str(index):  # 全选
                    return all_stores
                
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                
                if all(0 <= i < len(all_stores) for i in indices):
                    selected = [all_stores[i] for i in indices]
                    
                    # 检查是否符合策略建议
                    if strategy_id in self.STRATEGIES:
                        _, max_stores = self.STRATEGIES[strategy_id]['stores_range']
                        if len(selected) > max_stores:
                            print(f"{Fore.YELLOW}⚠️  选择了 {len(selected)} 个门店，超过建议的 {max_stores} 个{Style.RESET_ALL}")
                            confirm = input(f"{Fore.YELLOW}是否继续？(y/n): {Style.RESET_ALL}").strip().lower()
                            if confirm != 'y':
                                continue
                    
                    return selected
                else:
                    print(f"{Fore.RED}❌ 无效选择，请重新输入{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ 输入格式错误，请使用逗号分隔的数字{Style.RESET_ALL}")
    
    def calculate_frequency(self, num_products, num_stores, check_interval):
        """计算请求频率"""
        total_requests = num_products * num_stores
        # 考虑随机延迟（平均4.5秒）
        avg_request_time = total_requests * 4.5
        total_cycle_time = avg_request_time + check_interval
        requests_per_minute = (total_requests / total_cycle_time) * 60
        return requests_per_minute
    
    def show_summary_and_confirm(self, products, stores, strategy_id):
        """显示配置摘要并确认"""
        print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 配置摘要{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}监控产品 ({len(products)}个):{Style.RESET_ALL}")
        for product in products:
            print(f"  • {product['name']}")
        
        print(f"\n{Fore.CYAN}监控门店 ({len(stores)}个):{Style.RESET_ALL}")
        for store in stores:
            core_mark = " ⭐" if store.get('is_core') else ""
            print(f"  • {store['name']} ({store['district']}){core_mark}")
        
        # 计算频率
        check_interval = self.config['check_interval']
        if strategy_id in self.STRATEGIES:
            check_interval = self.STRATEGIES[strategy_id]['check_interval']
        
        frequency = self.calculate_frequency(len(products), len(stores), check_interval)
        
        # 风险评估
        if frequency < 10:
            risk_color = Fore.GREEN
            risk_text = "✅ 安全"
        elif frequency < 15:
            risk_color = Fore.YELLOW
            risk_text = "⚠️ 中等"
        else:
            risk_color = Fore.RED
            risk_text = "❌ 高风险"
        
        print(f"\n{Fore.CYAN}监控参数:{Style.RESET_ALL}")
        print(f"  • 检查间隔: {check_interval}秒")
        print(f"  • 每轮请求: {len(products) * len(stores)}次")
        print(f"  • 请求频率: {risk_color}{frequency:.1f}次/分钟 {risk_text}{Style.RESET_ALL}")
        
        # 确认
        print(f"\n{Fore.MAGENTA}特殊选项: 0=退出程序, b=返回重新选择{Style.RESET_ALL}")
        while True:
            clean_input()  # 清理输入缓冲
            choice = input(f"\n{Fore.GREEN}确认使用此配置？(y/n/b/0): {Style.RESET_ALL}").strip().lower()
            if choice == 'y':
                return 'YES'
            elif choice == 'n':
                return 'NO'
            elif choice == 'b':
                return 'BACK'
            elif choice == '0':
                return 'EXIT'
            print(f"{Fore.RED}❌ 请输入 y/n/b/0{Style.RESET_ALL}")
    
    def generate_config(self):
        """生成配置（支持返回上一步）"""
        self.print_header()
        
        # 步骤1: 选择策略
        while True:
            strategy_id = self.select_strategy()
            if strategy_id is None:
                return None
            
            # 步骤2: 选择产品
            while True:
                products = self.select_products(strategy_id)
                if products == 'EXIT':
                    return None
                elif products == 'BACK':
                    break  # 返回步骤1
                elif not products:
                    print(f"{Fore.RED}❌ 未选择任何产品，请重新选择{Style.RESET_ALL}")
                    continue
                
                # 步骤3: 选择门店
                while True:
                    stores = self.select_stores(strategy_id)
                    if stores == 'EXIT':
                        return None
                    elif stores == 'BACK':
                        break  # 返回步骤2
                    elif not stores:
                        print(f"{Fore.RED}❌ 未选择任何门店，请重新选择{Style.RESET_ALL}")
                        continue
                    
                    # 应用策略参数
                    if strategy_id in self.STRATEGIES:
                        self.config['check_interval'] = self.STRATEGIES[strategy_id]['check_interval']
                    
                    # 步骤4: 显示摘要并确认
                    result = self.show_summary_and_confirm(products, stores, strategy_id)
                    if result == 'EXIT':
                        return None
                    elif result == 'BACK':
                        break  # 返回步骤3
                    elif result == 'NO':
                        print(f"{Fore.YELLOW}❌ 已取消配置生成{Style.RESET_ALL}")
                        return None
                    elif result == 'YES':
                        # 生成并返回配置
                        return self._save_config(products, stores)
    
    def _save_config(self, products, stores):
        """保存配置"""
        
        # 构建最终配置
        self.config['target_products'] = [
            {
                'name': p['name'],
                'part_number': p['part_number'],
                'color': p['color'],
                'storage': p['storage']
            }
            for p in products
        ]
        
        self.config['target_stores'] = [s['store_number'] for s in stores]
        
        return self.config
    
    def save_config(self, config, filename='config.json'):
        """保存配置到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}✅ 配置已保存到 {filename}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ 保存配置失败: {e}{Style.RESET_ALL}")
            return False


def main():
    """主函数"""
    generator = InteractiveConfigGeneratorHK()
    config = generator.generate_config()
    
    if config:
        generator.save_config(config)
        print(f"\n{Fore.GREEN}✅ 香港监控配置生成完成！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}可以使用以下命令启动监控：{Style.RESET_ALL}")
        print(f"  python3 main.py")
    else:
        print(f"\n{Fore.RED}❌ 配置生成失败{Style.RESET_ALL}")


if __name__ == '__main__':
    main()

