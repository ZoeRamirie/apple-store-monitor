#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动获取iPhone 17系列香港版本的所有Part Number
从Apple香港官网提取真实的产品型号
"""

import requests
import json
import re
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


def get_iphone_models_from_page(url):
    """
    从Apple产品页面提取Part Number
    
    Args:
        url: Apple产品页面URL
    
    Returns:
        提取到的Part Number列表
    """
    print(f"\n{Fore.CYAN}正在访问: {url}{Style.RESET_ALL}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            content = response.text
            
            # 查找所有ZA/A格式的Part Number
            # 格式：字母数字组合 + ZA/A
            pattern = r'([A-Z0-9]{5,6}ZA/A)'
            matches = re.findall(pattern, content)
            
            # 去重
            unique_models = list(set(matches))
            
            print(f"{Fore.GREEN}✅ 找到 {len(unique_models)} 个Part Number{Style.RESET_ALL}\n")
            
            return unique_models
        else:
            print(f"{Fore.RED}❌ HTTP {response.status_code}{Style.RESET_ALL}\n")
            return []
    
    except Exception as e:
        print(f"{Fore.RED}❌ 错误: {e}{Style.RESET_ALL}\n")
        return []


def get_model_details_from_api(part_number):
    """
    从fulfillment API获取产品详细信息
    
    Args:
        part_number: 产品型号
    
    Returns:
        产品信息
    """
    api_url = "https://www.apple.com/hk-zh/shop/fulfillment-messages"
    
    params = {
        'fae': 'true',
        'little': 'false',
        'parts.0': part_number,
        'mts.0': 'regular',
        'mts.1': 'sticky',
        'fts': 'true'
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # 尝试提取产品名称
            try:
                product_title = data['body']['content']['pickupMessage']['pickupEligibility'][part_number]['messageTypes']['regular']['storePickupProductTitle']
                return {
                    'part_number': part_number,
                    'name': product_title,
                    'available_for_pickup': data['body']['content']['pickupMessage']['pickupEligibility'][part_number]['messageTypes']['regular'].get('storePickEligible', False)
                }
            except:
                return {
                    'part_number': part_number,
                    'name': 'Unknown',
                    'available_for_pickup': False
                }
        
        return None
    
    except Exception as e:
        return None


def manual_iphone17_models():
    """
    手动提供iPhone 17系列的常见配置
    基于iPhone产品线的通用规律
    """
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"手动生成iPhone 17系列可能的型号")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}注意：以下型号需要在Apple香港官网实际验证{Style.RESET_ALL}\n")
    
    models = {
        "iPhone 17": {
            "description": "iPhone 17 标准版",
            "colors": ["黑色", "白色", "蓝色", "粉色", "黄色"],
            "storage": ["128GB", "256GB", "512GB"],
            "note": "需要从官网获取实际Part Number"
        },
        "iPhone 17 Plus": {
            "description": "iPhone 17 Plus",
            "colors": ["黑色", "白色", "蓝色", "粉色", "黄色"],
            "storage": ["128GB", "256GB", "512GB"],
            "note": "需要从官网获取实际Part Number"
        },
        "iPhone 17 Pro": {
            "description": "iPhone 17 Pro",
            "colors": ["原色钛金属", "白色钛金属", "黑色钛金属", "蓝色钛金属"],
            "storage": ["128GB", "256GB", "512GB", "1TB"],
            "note": "需要从官网获取实际Part Number"
        },
        "iPhone 17 Pro Max": {
            "description": "iPhone 17 Pro Max",
            "colors": ["原色钛金属", "白色钛金属", "黑色钛金属", "蓝色钛金属"],
            "storage": ["256GB", "512GB", "1TB"],
            "note": "需要从官网获取实际Part Number",
            "example": "MFYP4ZA/A (256GB 深墨藍色 - 从您的数据中获取)"
        }
    }
    
    return models


def get_models_from_browser_guide():
    """
    提供浏览器手动获取Part Number的指南
    """
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"📋 如何从浏览器获取完整的iPhone 17系列型号")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    guide = """
{Fore.YELLOW}方法1：从购买页面获取{Style.RESET_ALL}

1. 访问 https://www.apple.com/hk/shop/buy-iphone

2. 选择每个iPhone 17型号（17, 17 Plus, 17 Pro, 17 Pro Max）

3. 对每个型号：
   - 选择所有颜色
   - 选择所有容量
   - F12 → Network → 查找包含Part Number的请求
   - 或查看页面源代码搜索 "ZA/A"

4. 记录所有找到的Part Number


{Fore.YELLOW}方法2：从API响应提取{Style.RESET_ALL}

1. 访问购买页面并选择产品

2. 点击"查看店内取货情况"

3. F12 → Network → 找到 fulfillment-messages 请求

4. 在Response中查找所有 Part Number

5. 响应中会包含该配置的完整型号


{Fore.YELLOW}方法3：从JSON配置文件提取{Style.RESET_ALL}

某些页面会加载包含所有型号的JSON配置文件，查找：
- product-config.json
- skus.json
- variants.json


{Fore.CYAN}提取到的Part Number应该是这样的格式：{Style.RESET_ALL}

XXXXX{Fore.GREEN}ZA/A{Style.RESET_ALL}

例如：
- MFYP4ZA/A
- MFYQ3ZA/A
- MFYR2ZA/A

{Fore.YELLOW}请将找到的所有Part Number保存到文件或告诉我！{Style.RESET_ALL}
""".format(Fore=Fore, Style=Style)
    
    print(guide)


def create_detection_script():
    """
    创建一个交互式脚本来收集Part Number
    """
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"📝 请提供iPhone 17系列的Part Number")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"请输入Part Number（每行一个，输入'done'完成）：\n")
    
    models = []
    
    try:
        while True:
            line = input(f"{Fore.GREEN}>{Style.RESET_ALL} ").strip()
            
            if line.lower() == 'done':
                break
            
            if line and 'ZA/A' in line.upper():
                # 提取Part Number
                match = re.search(r'([A-Z0-9]{5,6}ZA/A)', line.upper())
                if match:
                    part_number = match.group(1)
                    models.append(part_number)
                    print(f"  ✅ 已添加: {part_number}")
                else:
                    print(f"  ⚠️  格式不正确，请重新输入")
            elif line:
                print(f"  ⚠️  Part Number应包含'ZA/A'")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
        return []
    
    return models


def save_models_config(models):
    """
    保存iPhone 17型号配置
    """
    if not models:
        print(f"\n{Fore.YELLOW}没有型号数据，跳过保存{Style.RESET_ALL}\n")
        return
    
    config = {
        'region': 'Hong Kong',
        'device': 'iPhone 17 Series',
        'part_number_format': 'ZA/A',
        'models': models,
        'total_models': len(models),
        'last_updated': datetime.now().isoformat(),
        'source': 'User provided / Apple HK Official',
        'note': '香港版Part Number与大陆版不同，请使用ZA/A结尾的型号'
    }
    
    filename = 'iphone17_all_models_hk.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Fore.GREEN}✅ 型号配置已保存到: {filename}{Style.RESET_ALL}\n")


def main():
    """
    主函数
    """
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║                                                                   ║")
    print(f"║           🔍 iPhone 17系列香港版型号检测工具                      ║")
    print(f"║                                                                   ║")
    print(f"╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}重要提示：{Style.RESET_ALL}")
    print(f"  • 香港Part Number格式：{Fore.GREEN}XXXXXZA/A{Style.RESET_ALL}")
    print(f"  • 大陆Part Number格式：{Fore.YELLOW}XXXXXCH/A{Style.RESET_ALL}")
    print(f"  • 同样的配置，不同地区Part Number不同！\n")
    
    print(f"选择操作：")
    print(f"  1. 查看iPhone 17系列产品线（手动参考）")
    print(f"  2. 查看如何从浏览器获取Part Number")
    print(f"  3. 手动输入已知的Part Number")
    print(f"  4. 从您之前提供的数据（示例）")
    print(f"  5. 退出")
    
    try:
        choice = input(f"\n请选择 (1-5): ").strip()
        
        if choice == '1':
            models = manual_iphone17_models()
            print(f"\n{Fore.CYAN}iPhone 17系列产品线：{Style.RESET_ALL}\n")
            for series, info in models.items():
                print(f"{Fore.GREEN}{series}{Style.RESET_ALL}")
                print(f"  描述: {info['description']}")
                print(f"  颜色: {', '.join(info['colors'])}")
                print(f"  容量: {', '.join(info['storage'])}")
                if 'example' in info:
                    print(f"  示例: {Fore.YELLOW}{info['example']}{Style.RESET_ALL}")
                print()
        
        elif choice == '2':
            get_models_from_browser_guide()
        
        elif choice == '3':
            models = create_detection_script()
            if models:
                print(f"\n{Fore.GREEN}收集到 {len(models)} 个Part Number：{Style.RESET_ALL}\n")
                for i, model in enumerate(models, 1):
                    print(f"  {i}. {model}")
                
                save = input(f"\n保存到配置文件？(y/n): ").strip().lower()
                if save == 'y':
                    save_models_config(models)
        
        elif choice == '4':
            print(f"\n{Fore.CYAN}从您提供的数据中提取的型号：{Style.RESET_ALL}\n")
            print(f"  • MFYP4ZA/A - iPhone 17 Pro Max 256GB 深墨藍色\n")
            print(f"{Fore.YELLOW}这只是一个示例，需要获取完整系列的所有型号{Style.RESET_ALL}\n")
        
        elif choice == '5':
            print(f"\n{Fore.CYAN}已退出{Style.RESET_ALL}\n")
        
        else:
            print(f"\n{Fore.RED}无效选择{Style.RESET_ALL}\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}错误: {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()


