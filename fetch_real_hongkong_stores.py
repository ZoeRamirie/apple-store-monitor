#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
从Apple官方API获取香港真实门店列表
使用官方store-list API确保门店编号准确
"""

import requests
import json
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


def fetch_store_list(region='zh_HK'):
    """
    从Apple官方API获取门店列表
    
    Args:
        region: 区域代码（zh_HK=香港, zh_CN=中国大陆）
    
    Returns:
        门店列表数据
    """
    url = f"https://www.apple.com/rsp-web/store-list?locale={region}"
    
    print(f"{Fore.CYAN}正在从Apple官方API获取门店列表...{Style.RESET_ALL}")
    print(f"API: {url}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{Fore.GREEN}✅ API响应成功{Style.RESET_ALL}\n")
            return data
        else:
            print(f"{Fore.RED}❌ API响应失败: HTTP {response.status_code}{Style.RESET_ALL}\n")
            return None
    
    except Exception as e:
        print(f"{Fore.RED}❌ 请求失败: {e}{Style.RESET_ALL}\n")
        return None


def extract_hongkong_stores(data):
    """
    从API数据中提取香港门店信息
    
    Args:
        data: API返回的数据
    
    Returns:
        香港门店列表
    """
    print(f"{Fore.CYAN}正在解析香港门店数据...{Style.RESET_ALL}\n")
    
    hongkong_stores = []
    
    try:
        # 根据API结构解析数据
        if 'storeListData' in data:
            store_list_data = data['storeListData']
            
            # 查找香港数据
            for region_data in store_list_data:
                locale = region_data.get('locale', '')
                
                # 香港数据可能在 zh_HK 或其他locale下
                if 'state' in region_data:
                    for state in region_data['state']:
                        state_name = state.get('stateName', '')
                        
                        # 检查是否是香港
                        if '香港' in state_name or 'Hong Kong' in state_name or state_name == 'HK':
                            stores = state.get('store', [])
                            
                            print(f"{Fore.GREEN}✅ 找到香港门店数据！{Style.RESET_ALL}")
                            print(f"   区域: {state_name}")
                            print(f"   门店数: {len(stores)}\n")
                            
                            for store in stores:
                                store_info = {
                                    'storeNumber': store.get('id', ''),
                                    'storeName': store.get('name', ''),
                                    'storeNameEN': store.get('name', ''),
                                    'city': store.get('city', ''),
                                    'address': store.get('address', {}).get('address', ''),
                                    'phoneNumber': store.get('phoneNumber', ''),
                                    'latitude': store.get('latitude', 0),
                                    'longitude': store.get('longitude', 0),
                                    'verified': True,
                                    'verified_at': datetime.now().isoformat(),
                                    'source': 'Apple Official API'
                                }
                                
                                hongkong_stores.append(store_info)
                                
                                print(f"  • {store_info['storeNumber']}: {store_info['storeName']}")
        
        if not hongkong_stores:
            print(f"{Fore.YELLOW}⚠️  未找到香港门店数据{Style.RESET_ALL}\n")
            print(f"尝试其他方式...\n")
            
            # 尝试直接搜索包含香港门店的数据
            data_str = json.dumps(data)
            if 'Hong Kong' in data_str or '香港' in data_str:
                print(f"{Fore.CYAN}检测到数据中包含香港信息，但结构可能不同{Style.RESET_ALL}")
                print(f"需要手动检查API响应结构\n")
        
        return hongkong_stores
    
    except Exception as e:
        print(f"{Fore.RED}❌ 解析失败: {e}{Style.RESET_ALL}\n")
        return []


def verify_store_with_api(store_number, store_name):
    """
    使用fulfillment API验证门店编号
    
    Args:
        store_number: 门店编号
        store_name: 门店名称
    
    Returns:
        验证结果
    """
    print(f"  验证 {store_number} ({store_name})...", end=' ', flush=True)
    
    # 使用fulfillment API验证
    url = 'https://www.apple.com/hk/shop/fulfillment-messages'
    
    params = {
        'pl': 'true',
        'parts.0': 'MYD83ZP/A',  # iPhone 14 Pro Max香港版测试
        'store': store_number
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查响应是否包含门店信息
            if 'body' in data and 'pickupMessage' in data['body']:
                print(f"{Fore.GREEN}✅ 有效{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️  响应格式异常{Style.RESET_ALL}")
                return False
        else:
            print(f"{Fore.RED}❌ HTTP {response.status_code}{Style.RESET_ALL}")
            return False
    
    except Exception as e:
        print(f"{Fore.RED}❌ {str(e)}{Style.RESET_ALL}")
        return False


def main():
    """主函数"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║                                                                   ║")
    print(f"║       🔍 从Apple官方API获取香港真实门店列表                       ║")
    print(f"║                                                                   ║")
    print(f"╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # 获取门店列表
    data = fetch_store_list('zh_HK')
    
    if not data:
        print(f"{Fore.RED}无法获取门店数据{Style.RESET_ALL}\n")
        
        # 尝试使用zh_CN
        print(f"{Fore.YELLOW}尝试使用zh_CN区域...{Style.RESET_ALL}\n")
        data = fetch_store_list('zh_CN')
    
    if not data:
        print(f"{Fore.RED}❌ 无法获取门店数据，请检查网络连接{Style.RESET_ALL}\n")
        return
    
    # 保存原始响应（用于调试）
    with open('store_list_api_response.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"{Fore.GREEN}✅ 原始API响应已保存到: store_list_api_response.json{Style.RESET_ALL}\n")
    
    # 提取香港门店
    hongkong_stores = extract_hongkong_stores(data)
    
    if not hongkong_stores:
        print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}未能自动提取香港门店数据{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
        print(f"建议：")
        print(f"  1. 查看 store_list_api_response.json 文件")
        print(f"  2. 手动查找香港门店数据")
        print(f"  3. 或访问 Apple 香港官网查询门店列表\n")
        return
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"📊 提取结果")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"✅ 找到 {len(hongkong_stores)} 个香港Apple Store\n")
    
    # 验证门店编号（可选）
    print(f"{Fore.CYAN}是否验证这些门店编号的有效性？{Style.RESET_ALL}")
    print(f"（将实际调用API测试，需要一些时间）\n")
    
    try:
        verify = input("验证门店？(y/n): ").strip().lower()
        
        if verify == 'y':
            print(f"\n{Fore.CYAN}开始验证门店编号...{Style.RESET_ALL}\n")
            
            verified_stores = []
            for store in hongkong_stores:
                result = verify_store_with_api(
                    store['storeNumber'],
                    store['storeName']
                )
                
                if result:
                    verified_stores.append(store)
                
                # 延迟避免限制
                import time
                time.sleep(2)
            
            print(f"\n{Fore.GREEN}✅ 验证完成！{Style.RESET_ALL}")
            print(f"有效门店: {len(verified_stores)}/{len(hongkong_stores)}\n")
            
            hongkong_stores = verified_stores
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已跳过验证{Style.RESET_ALL}\n")
    
    # 生成配置文件
    config = {
        'region': 'Hong Kong',
        'region_code': 'HK',
        'api_base_url': 'https://www.apple.com/hk',
        'api_language': 'zh-HK',
        'stores': hongkong_stores,
        'total_stores': len(hongkong_stores),
        'last_updated': datetime.now().isoformat(),
        'source': 'Apple Official Store List API',
        'api_notes': {
            'store_list_api': 'https://www.apple.com/rsp-web/store-list',
            'pickup_api': 'https://www.apple.com/hk/shop/retail/pickup-message',
            'fulfillment_api': 'https://www.apple.com/hk/shop/fulfillment-messages',
            'language_param': 'zh-HK',
            'currency': 'HKD',
            'timezone': 'Asia/Hong_Kong'
        }
    }
    
    output_file = 'apple_stores_hongkong_official.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"{Fore.GREEN}✅ 香港门店配置已生成: {output_file}{Style.RESET_ALL}\n")
    
    # 显示使用方法
    print(f"{Fore.CYAN}{'='*70}")
    print(f"💡 使用方法")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"1. 备份当前配置：")
    print(f"   cp apple_stores_hongkong.json apple_stores_hongkong.json.backup\n")
    
    print(f"2. 使用新配置：")
    print(f"   cp {output_file} apple_stores_hongkong.json\n")
    
    print(f"3. 运行增强版监控器：")
    print(f"   python3 main_enhanced.py\n")


if __name__ == "__main__":
    main()


