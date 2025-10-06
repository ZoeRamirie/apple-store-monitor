#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最终方案：从Apple官方Store List API获取香港门店
使用多种API端点尝试
"""

import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


def try_api(url, description):
    """
    尝试调用API
    """
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"尝试: {description}")
    print(f"URL: {url}")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
        }
        
        print(f"正在请求...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"HTTP状态码: {response.status_code}\n")
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # 保存响应
                filename = f"api_response_{int(time.time())}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"{Fore.GREEN}✅ 成功！响应已保存到: {filename}{Style.RESET_ALL}\n")
                
                # 尝试查找香港门店
                hongkong_stores = find_hongkong_stores(data)
                
                if hongkong_stores:
                    print(f"{Fore.GREEN}✅ 找到 {len(hongkong_stores)} 个香港门店！{Style.RESET_ALL}\n")
                    
                    for i, store in enumerate(hongkong_stores, 1):
                        print(f"{i}. {store.get('storeName')} ({store.get('storeNumber')})")
                        print(f"   城市: {store.get('city', 'N/A')}")
                        print(f"   地址: {store.get('address', 'N/A')[:50]}...")
                        print()
                    
                    # 生成配置文件
                    save_hongkong_config(hongkong_stores)
                    
                    return True
                else:
                    print(f"{Fore.YELLOW}⚠️  未在响应中找到香港门店{Style.RESET_ALL}\n")
                    print(f"响应结构预览:")
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                    print(f"\n...（查看完整内容请打开 {filename}）\n")
                    
                    return False
                
            except json.JSONDecodeError:
                print(f"{Fore.YELLOW}⚠️  响应不是JSON格式{Style.RESET_ALL}\n")
                print(f"响应内容预览:")
                print(response.text[:500])
                return False
        
        else:
            print(f"{Fore.RED}❌ 请求失败: HTTP {response.status_code}{Style.RESET_ALL}\n")
            return False
    
    except Exception as e:
        print(f"{Fore.RED}❌ 错误: {e}{Style.RESET_ALL}\n")
        return False


def find_hongkong_stores(data):
    """
    从API响应中查找香港门店
    """
    hongkong_stores = []
    
    try:
        # 尝试不同的数据结构
        
        # 结构1: storeListData
        if 'storeListData' in data:
            for region_data in data['storeListData']:
                if 'state' in region_data:
                    for state in region_data['state']:
                        state_name = state.get('stateName', '')
                        
                        # 查找香港
                        if any(kw in state_name for kw in ['香港', 'Hong Kong', 'HK', 'Hongkong']):
                            stores = state.get('store', [])
                            
                            for store in stores:
                                hongkong_stores.append({
                                    'storeNumber': store.get('storeId', store.get('id', '')),
                                    'storeName': store.get('name', ''),
                                    'city': store.get('city', ''),
                                    'address': store.get('address', {}).get('address', ''),
                                    'phoneNumber': store.get('phoneNumber', ''),
                                    'latitude': store.get('latitude', 0),
                                    'longitude': store.get('longitude', 0)
                                })
        
        # 结构2: stores 数组
        if 'stores' in data and isinstance(data['stores'], list):
            for store in data['stores']:
                # 检查是否是香港门店
                country = store.get('country', '')
                state = store.get('state', '')
                city = store.get('city', '')
                
                if any(kw in str(country) + str(state) + str(city) 
                       for kw in ['香港', 'Hong Kong', 'HK']):
                    hongkong_stores.append({
                        'storeNumber': store.get('storeId', store.get('id', store.get('storeNumber', ''))),
                        'storeName': store.get('name', store.get('storeName', '')),
                        'city': city,
                        'address': store.get('address', ''),
                        'phoneNumber': store.get('phoneNumber', ''),
                        'latitude': store.get('latitude', 0),
                        'longitude': store.get('longitude', 0)
                    })
        
        # 结构3: 直接在data中
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    location = str(item.get('location', '')) + str(item.get('city', ''))
                    if '香港' in location or 'Hong Kong' in location:
                        hongkong_stores.append({
                            'storeNumber': item.get('storeId', item.get('id', '')),
                            'storeName': item.get('name', ''),
                            'city': item.get('city', ''),
                            'address': item.get('address', ''),
                            'phoneNumber': item.get('phoneNumber', ''),
                            'latitude': item.get('latitude', 0),
                            'longitude': item.get('longitude', 0)
                        })
    
    except Exception as e:
        print(f"{Fore.YELLOW}解析数据时出错: {e}{Style.RESET_ALL}\n")
    
    return hongkong_stores


def save_hongkong_config(stores):
    """
    保存香港门店配置
    """
    config = {
        'region': 'Hong Kong',
        'region_code': 'HK',
        'api_base_url': 'https://www.apple.com/hk-zh',
        'api_language': 'zh-HK',
        'stores': stores,
        'total_stores': len(stores),
        'verified': True,
        'last_updated': datetime.now().isoformat(),
        'source': 'Apple Official Store List API',
        'api_notes': {
            'fulfillment_api': 'https://www.apple.com/hk-zh/shop/fulfillment-messages',
            'part_number_format': 'ZA/A',
            'note': 'Part Number应使用ZA/A结尾，如MFYP4ZA/A'
        }
    }
    
    output_file = 'apple_stores_hongkong_verified.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Fore.GREEN}✅ 配置文件已生成: {output_file}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'='*70}")
    print(f"下一步操作")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    print(f"1. 备份当前配置：")
    print(f"   cp apple_stores_hongkong.json apple_stores_hongkong.json.backup\n")
    print(f"2. 使用新配置：")
    print(f"   cp {output_file} apple_stores_hongkong.json\n")
    print(f"3. 测试监控：")
    print(f"   python3 main_enhanced.py\n")


def main():
    """
    主函数
    """
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║                                                                   ║")
    print(f"║         🔍 获取香港Apple Store门店列表 - 最终方案                ║")
    print(f"║                                                                   ║")
    print(f"╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # 尝试多个API端点
    apis = [
        {
            'url': 'https://www.apple.com/rsp-web/store-list?locale=zh_HK',
            'description': 'Apple Store List API (zh_HK)'
        },
        {
            'url': 'https://www.apple.com/rsp-web/store-list?locale=zh_CN',
            'description': 'Apple Store List API (zh_CN) - 包含香港'
        },
        {
            'url': 'https://www.apple.com/rsp-web/store-list?locale=en_HK',
            'description': 'Apple Store List API (en_HK)'
        }
    ]
    
    for i, api in enumerate(apis, 1):
        print(f"\n{Fore.YELLOW}尝试方案 {i}/{len(apis)}...{Style.RESET_ALL}")
        
        success = try_api(api['url'], api['description'])
        
        if success:
            print(f"\n{Fore.GREEN}{'='*70}")
            print(f"🎉 成功获取香港门店列表！")
            print(f"{'='*70}{Style.RESET_ALL}\n")
            break
        
        # 延迟避免频率限制
        if i < len(apis):
            print(f"\n等待5秒后尝试下一个API...\n")
            time.sleep(5)
    else:
        print(f"\n{Fore.YELLOW}{'='*70}")
        print(f"所有API尝试完成")
        print(f"{'='*70}{Style.RESET_ALL}\n")
        print(f"如果都失败了，请尝试：")
        print(f"1. 等待30分钟后重试（避免频率限制）")
        print(f"2. 或使用浏览器手动查看门店列表")
        print(f"3. 访问 https://www.apple.com/hk/retail/ 并手动记录门店信息\n")


if __name__ == "__main__":
    main()


