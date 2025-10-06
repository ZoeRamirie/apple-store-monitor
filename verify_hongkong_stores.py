#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
香港门店编号验证脚本
实际调用Apple API验证门店编号的有效性
"""

import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)


def test_store_api(store_number, region='HK'):
    """
    测试单个门店编号是否有效
    
    Args:
        store_number: 门店编号
        region: 区域（HK=香港, CN=中国大陆）
    
    Returns:
        dict: 测试结果
    """
    # API配置
    if region == 'HK':
        api_url = 'https://www.apple.com/hk/shop/retail/pickup-message'
        language = 'zh-HK'
        test_part_number = 'MYD83ZP/A'  # iPhone 14 Pro Max的香港Part Number
    else:
        api_url = 'https://www.apple.com.cn/shop/retail/pickup-message'
        language = 'zh-CN'
        test_part_number = 'MQ8E3CH/A'  # iPhone 14 Pro Max的大陆Part Number
    
    # 构建请求
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': f'{language},zh;q=0.9,en;q=0.8',
    }
    session.headers.update(headers)
    
    params = {
        'pl': 'true',
        'mts.0': 'regular',
        'mts.1': 'compact',
        'cppart': f'UNLOCKED/{region}',
        'parts.0': test_part_number,
        'store': store_number
    }
    
    try:
        print(f"  正在测试 {store_number}...", end=' ', flush=True)
        
        response = session.get(api_url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查响应结构
            if 'body' in data and 'stores' in data['body']:
                stores_data = data['body']['stores']
                
                if stores_data and len(stores_data) > 0:
                    store = stores_data[0]
                    store_name = store.get('storeName', 'Unknown')
                    
                    # 验证返回的门店编号是否匹配
                    returned_number = store.get('storeNumber', '')
                    
                    if returned_number == store_number:
                        print(f"{Fore.GREEN}✅ 有效{Style.RESET_ALL}")
                        return {
                            'valid': True,
                            'store_number': store_number,
                            'store_name': store_name,
                            'city': store.get('city', ''),
                            'response_code': 200,
                            'has_data': True
                        }
                    else:
                        print(f"{Fore.YELLOW}⚠️  编号不匹配{Style.RESET_ALL}")
                        return {
                            'valid': False,
                            'store_number': store_number,
                            'error': f'返回编号不匹配: {returned_number}',
                            'response_code': 200
                        }
                else:
                    print(f"{Fore.RED}❌ 无数据返回{Style.RESET_ALL}")
                    return {
                        'valid': False,
                        'store_number': store_number,
                        'error': 'API返回空数据',
                        'response_code': 200
                    }
            else:
                print(f"{Fore.RED}❌ 响应格式错误{Style.RESET_ALL}")
                return {
                    'valid': False,
                    'store_number': store_number,
                    'error': '响应结构不正确',
                    'response_code': 200,
                    'response_data': data
                }
        else:
            print(f"{Fore.RED}❌ HTTP {response.status_code}{Style.RESET_ALL}")
            return {
                'valid': False,
                'store_number': store_number,
                'error': f'HTTP {response.status_code}',
                'response_code': response.status_code
            }
    
    except requests.Timeout:
        print(f"{Fore.RED}❌ 超时{Style.RESET_ALL}")
        return {
            'valid': False,
            'store_number': store_number,
            'error': '请求超时'
        }
    except Exception as e:
        print(f"{Fore.RED}❌ 错误: {str(e)}{Style.RESET_ALL}")
        return {
            'valid': False,
            'store_number': store_number,
            'error': str(e)
        }


def verify_hongkong_stores():
    """验证香港门店数据"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"🔍 香港Apple Store门店编号验证")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # 加载香港门店数据
    try:
        with open('apple_stores_hongkong.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stores = data.get('stores', [])
        print(f"📋 已加载 {len(stores)} 个香港门店数据\n")
        
    except FileNotFoundError:
        print(f"{Fore.RED}❌ 找不到 apple_stores_hongkong.json{Style.RESET_ALL}\n")
        return
    except Exception as e:
        print(f"{Fore.RED}❌ 读取文件失败: {e}{Style.RESET_ALL}\n")
        return
    
    # 逐个验证门店
    results = []
    valid_stores = []
    invalid_stores = []
    
    print(f"{Fore.CYAN}开始验证（请稍候，每次测试间隔3秒以避免限制）...{Style.RESET_ALL}\n")
    
    for i, store in enumerate(stores, 1):
        store_number = store.get('storeNumber', 'N/A')
        store_name = store.get('storeName', 'Unknown')
        
        print(f"[{i}/{len(stores)}] {store_name} ({store_number})")
        
        result = test_store_api(store_number, region='HK')
        results.append(result)
        
        if result['valid']:
            valid_stores.append({
                'storeNumber': store_number,
                'storeName': result['store_name'],
                'city': result.get('city', ''),
                'verified': True,
                'verified_at': datetime.now().isoformat()
            })
        else:
            invalid_stores.append({
                'storeNumber': store_number,
                'storeName': store_name,
                'error': result.get('error', 'Unknown'),
                'verified': False
            })
        
        # 延迟避免限制
        if i < len(stores):
            time.sleep(3)
    
    # 打印结果
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"📊 验证结果")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"✅ 有效门店: {Fore.GREEN}{len(valid_stores)}{Style.RESET_ALL} 个")
    print(f"❌ 无效门店: {Fore.RED}{len(invalid_stores)}{Style.RESET_ALL} 个")
    print(f"📈 成功率: {len(valid_stores)/len(stores)*100:.1f}%\n")
    
    # 显示有效门店
    if valid_stores:
        print(f"{Fore.GREEN}✅ 有效的香港门店：{Style.RESET_ALL}\n")
        for store in valid_stores:
            print(f"  • {store['storeNumber']}: {store['storeName']} ({store.get('city', 'N/A')})")
        print()
    
    # 显示无效门店
    if invalid_stores:
        print(f"{Fore.RED}❌ 无效的门店（需要修正）：{Style.RESET_ALL}\n")
        for store in invalid_stores:
            print(f"  • {store['storeNumber']}: {store['storeName']}")
            print(f"    错误: {store.get('error', 'Unknown')}")
        print()
    
    # 保存验证结果
    verification_result = {
        'verification_time': datetime.now().isoformat(),
        'total_stores': len(stores),
        'valid_count': len(valid_stores),
        'invalid_count': len(invalid_stores),
        'success_rate': len(valid_stores)/len(stores)*100,
        'valid_stores': valid_stores,
        'invalid_stores': invalid_stores,
        'all_results': results
    }
    
    output_file = f'hongkong_stores_verification_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(verification_result, f, indent=2, ensure_ascii=False)
    
    print(f"{Fore.CYAN}📄 验证结果已保存到: {output_file}{Style.RESET_ALL}\n")
    
    # 建议
    print(f"{Fore.CYAN}{'='*70}")
    print(f"💡 建议")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    if len(invalid_stores) == 0:
        print(f"{Fore.GREEN}✅ 所有门店编号都有效，可以放心使用！{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}⚠️  发现 {len(invalid_stores)} 个无效门店编号{Style.RESET_ALL}")
        print(f"\n建议：")
        print(f"  1. 从配置文件中移除这些门店编号")
        print(f"  2. 或到Apple香港官网确认正确的门店编号")
        print(f"  3. 更新 apple_stores_hongkong.json 文件\n")
        
        # 生成更正后的配置
        if valid_stores:
            corrected_config = {
                'region': 'Hong Kong',
                'region_code': 'HK',
                'api_base_url': 'https://www.apple.com/hk',
                'api_language': 'zh-HK',
                'stores': valid_stores,
                'total_stores': len(valid_stores),
                'last_updated': datetime.now().isoformat(),
                'verified': True,
                'api_notes': {
                    'pickup_api': 'https://www.apple.com/hk/shop/retail/pickup-message',
                    'language_param': 'zh-HK',
                    'currency': 'HKD',
                    'timezone': 'Asia/Hong_Kong'
                }
            }
            
            corrected_file = 'apple_stores_hongkong_verified.json'
            with open(corrected_file, 'w', encoding='utf-8') as f:
                json.dump(corrected_config, f, indent=2, ensure_ascii=False)
            
            print(f"{Fore.GREEN}✅ 已生成验证后的门店配置: {corrected_file}{Style.RESET_ALL}\n")
    
    return verification_result


def search_real_hongkong_stores():
    """搜索实际有效的香港门店编号"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"🔍 搜索香港实际有效的门店编号")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"正在扫描 R400-R700 范围...\n")
    
    valid_stores = []
    test_range = list(range(400, 700))
    
    for i, num in enumerate(test_range):
        store_number = f"R{num}"
        
        if (i + 1) % 10 == 0:
            print(f"\n已扫描 {i+1}/{len(test_range)} 个编号...\n")
        
        result = test_store_api(store_number, region='HK')
        
        if result['valid']:
            valid_stores.append(result)
            print(f"  {Fore.GREEN}发现有效门店！{Style.RESET_ALL}")
        
        # 延迟避免限制
        time.sleep(2)
        
        # 每扫描20个休息10秒
        if (i + 1) % 20 == 0:
            print(f"\n💤 休息10秒避免限制...\n")
            time.sleep(10)
    
    print(f"\n{Fore.GREEN}✅ 发现 {len(valid_stores)} 个有效的香港门店{Style.RESET_ALL}\n")
    
    for store in valid_stores:
        print(f"  • {store['store_number']}: {store['store_name']}")
    
    return valid_stores


def main():
    """主函数"""
    print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"║                                                                   ║")
    print(f"║          🔍 香港Apple Store门店编号验证工具                       ║")
    print(f"║                                                                   ║")
    print(f"╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    print(f"选择操作：")
    print(f"  1. 验证现有的香港门店数据")
    print(f"  2. 搜索实际有效的门店编号（R400-R700）")
    print(f"  3. 退出")
    
    try:
        choice = input(f"\n请选择 (1-3): ").strip()
        
        if choice == '1':
            verify_hongkong_stores()
        elif choice == '2':
            search_real_hongkong_stores()
        elif choice == '3':
            print(f"\n已退出\n")
        else:
            print(f"\n{Fore.YELLOW}无效选择{Style.RESET_ALL}\n")
    
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}已取消{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}错误: {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()


