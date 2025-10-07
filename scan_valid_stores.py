#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
扫描有效的Apple Store门店编号
基于最新的门店列表（2025年）
"""

import requests
import json
import time
from datetime import datetime
from logger_config import setup_logger

logger = setup_logger()

# 2025年最新门店列表（从web搜索获取）
KNOWN_STORES_2025 = {
    "上海": ["浦东", "上海环贸iapm", "环球港", "七宝", "香港广场", "五角场", "南京东路", "静安"],
    "北京": ["三里屯", "华贸购物中心", "西单大悦城", "朝阳大悦城", "王府井"],
    "广东": ["珠江新城", "天环广场", "深圳益田假日广场", "深圳万象城"],
    "江苏": ["玄武湖", "虹悦城", "新街口", "无锡恒隆广场", "苏州"],
    "浙江": ["天一广场", "西湖", "杭州万象城", "温州万象城"],
    "四川": ["成都万象城", "成都太古里"],
    "天津": ["天津万象城", "天津大悦城", "天津恒隆广场"],
    "重庆": ["重庆万象城", "重庆北城天街", "解放碑"],
    "辽宁": ["百年城", "大连恒隆广场", "沈阳万象城", "中街大悦城"],
    "其他": ["昆明", "郑州万象城", "武汉", "长沙", "厦门新生活广场", 
             "泰禾广场", "济南恒隆广场", "青岛万象城", "南宁万象城"]
}

def test_store_number(store_number, part_number="MG0G4CH/A"):
    """测试单个门店编号是否有效"""
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    session.headers.update(headers)
    
    params = {
        'pl': 'true',
        'mts.0': 'regular',
        'mts.1': 'compact',
        'cppart': 'UNLOCKED/CN',
        'parts.0': part_number,
        'store': store_number
    }
    
    url = "https://www.apple.com.cn/shop/retail/pickup-message"
    
    try:
        response = session.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查是否有stores数组（表示有效）
            if 'body' in data and 'stores' in data['body']:
                stores_data = data['body']['stores']
                if stores_data and len(stores_data) > 0:
                    store = stores_data[0]
                    return {
                        'valid': True,
                        'storeNumber': store.get('storeNumber'),
                        'storeName': store.get('storeName'),
                        'city': store.get('city'),
                        'state': store.get('state'),
                        'phoneNumber': store.get('phoneNumber'),
                        'address': store.get('address', {}).get('address2', '')
                    }
            
            # 检查是否有错误消息
            if 'body' in data and 'errorMessage' in data['body']:
                return {
                    'valid': False,
                    'error': data['body']['errorMessage']
                }
        
        return {
            'valid': False,
            'error': f'HTTP {response.status_code}'
        }
        
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def scan_store_range(start, end, delay=2, conservative=False):
    """
    扫描一个范围的门店编号
    
    Args:
        start: 起始编号
        end: 结束编号
        delay: 基础延迟（秒）
        conservative: 保守模式（更长延迟，更安全）
    """
    
    valid_stores = []
    invalid_stores = []
    error_count = 0  # 连续错误计数
    http_541_count = 0  # HTTP 541错误计数
    
    # 保守模式使用更长延迟
    if conservative:
        delay = max(delay, 3)
        print(f"\n⚠️  保守模式已启用：每次请求延迟{delay}秒，每10次额外休息30秒")
    
    print(f"\n{'='*80}")
    print(f"🔍 扫描门店编号范围: R{start:03d} - R{end:03d}")
    print(f"{'='*80}")
    print(f"⏱️  预计耗时: {(end-start+1) * delay / 60:.1f} 分钟")
    print(f"{'='*80}\n")
    
    for i in range(start, end + 1):
        store_num = f"R{i:03d}"
        
        print(f"测试 {store_num}...", end=' ', flush=True)
        
        result = test_store_number(store_num)
        
        # 检查HTTP 541错误
        if 'HTTP 541' in str(result.get('error', '')):
            http_541_count += 1
            error_count += 1
            print(f"⚠️  被限制 (HTTP 541) - 连续{http_541_count}次")
            
            # 连续3次HTTP 541，警告
            if http_541_count >= 3:
                print(f"\n{'='*80}")
                print(f"⚠️  ⚠️  ⚠️  检测到连续{http_541_count}次API限制！")
                print(f"{'='*80}")
                print(f"建议：")
                print(f"  1. 等待30-60秒后继续")
                print(f"  2. 或者暂停扫描，稍后再试")
                print(f"  3. 已扫描：{i-start+1}/{end-start+1}")
                print(f"{'='*80}\n")
                
                choice = input("输入 'c' 继续（等待60秒），'q' 退出: ").strip().lower()
                if choice == 'q':
                    print("\n⚠️  用户中止扫描")
                    break
                else:
                    print(f"\n💤 等待60秒以避免限制...")
                    time.sleep(60)
                    http_541_count = 0  # 重置计数
                    print("✅ 继续扫描...\n")
            
            invalid_stores.append({
                'storeNumber': store_num,
                'error': result.get('error', 'Unknown')
            })
        
        elif result['valid']:
            print(f"✅ 有效！{result['storeName']} ({result['city']})")
            valid_stores.append(result)
            error_count = 0  # 重置错误计数
            http_541_count = 0  # 重置541计数
            
            # 保存单个门店的详细数据
            with open(f'store_detail_{store_num}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            print(f"❌ 无效")
            invalid_stores.append({
                'storeNumber': store_num,
                'error': result.get('error', 'Unknown')
            })
            error_count = 0  # 普通无效不算错误
            http_541_count = 0
        
        # 基础延迟
        time.sleep(delay)
        
        # 每10个编号额外休息
        if (i - start + 1) % 10 == 0:
            extra_delay = 10 if not conservative else 30
            print(f"\n💤 已扫描 {i-start+1}/{end-start+1}，休息{extra_delay}秒...\n")
            time.sleep(extra_delay)
        
        # 保守模式：每5个编号额外休息
        elif conservative and (i - start + 1) % 5 == 0:
            print(f"\n💤 保守模式休息...\n")
            time.sleep(10)
    
    return valid_stores, invalid_stores


def main():
    """主函数"""
    
    print(f"\n{'='*80}")
    print(f"🍎 Apple Store 中国区门店编号扫描工具")
    print(f"{'='*80}")
    print(f"\n基于2025年最新门店列表")
    print(f"将扫描R001-R999范围的门店编号\n")
    
    # 询问用户扫描范围
    print("选择扫描模式：")
    print("  1. 快速扫描 (R001-R100) - 约5分钟")
    print("  2. 标准扫描 (R001-R500) - 约30分钟")
    print("  3. 完全扫描 (R001-R999) - 约60分钟")
    print("  4. 自定义范围")
    print("  5. 测试已知编号 (R448, R388, R485等) - 约1分钟")
    print("  6. 保守模式扫描 (更安全，但更慢)")
    
    choice = input("\n请选择 (1-6): ").strip()
    
    conservative = False
    known_numbers = None  # 初始化
    start, end = 0, 0  # 默认值
    
    if choice == '1':
        start, end = 1, 100
    elif choice == '2':
        start, end = 1, 500
    elif choice == '3':
        start, end = 1, 999
    elif choice == '4':
        print("\n💡 请输入纯数字（如：300），不要包含R或其他符号")
        while True:
            try:
                start_input = input("起始编号 (1-999): ").strip()
                start = int(start_input)
                if 1 <= start <= 999:
                    break
                else:
                    print("⚠️  请输入1-999之间的数字")
            except ValueError:
                print(f"❌ 输入错误：'{start_input}' 不是有效数字，请只输入数字（如：300）")
        
        while True:
            try:
                end_input = input("结束编号 (1-999): ").strip()
                end = int(end_input)
                if 1 <= end <= 999 and end >= start:
                    break
                elif end < start:
                    print(f"⚠️  结束编号({end})不能小于起始编号({start})")
                else:
                    print("⚠️  请输入1-999之间的数字")
            except ValueError:
                print(f"❌ 输入错误：'{end_input}' 不是有效数字，请只输入数字（如：400）")
        
        print(f"\n✅ 将扫描 R{start:03d} - R{end:03d}（共{end-start+1}个编号）")
    elif choice == '5':
        # 测试已知编号 - 特殊处理，只测试指定的编号
        known_numbers = [448, 388, 485, 409, 505, 570]
        print(f"\n将测试以下编号: {known_numbers}")
        print(f"总计: {len(known_numbers)} 个编号")
    elif choice == '6':
        conservative = True
        print("\n⚠️  保守模式：延迟更长，更安全，但更慢")
        print("  1. 快速扫描 (R001-R100) - 约10分钟")
        print("  2. 标准扫描 (R001-R500) - 约60分钟")
        sub_choice = input("请选择范围 (1-2): ").strip()
        if sub_choice == '2':
            start, end = 1, 500
            print("✅ 选择：标准扫描 R001-R500")
        elif sub_choice == '1':
            start, end = 1, 100
            print("✅ 选择：快速扫描 R001-R100")
        else:
            print("⚠️  无效选择，使用快速扫描")
            start, end = 1, 100
    else:
        print("无效选择，使用快速扫描模式")
        start, end = 1, 100
    
    # 显示警告信息
    print(f"\n{'='*80}")
    print(f"⚠️  重要提醒：")
    print(f"{'='*80}")
    print(f"1. Apple API有访问频率限制")
    print(f"2. 连续请求可能触发HTTP 541错误")
    print(f"3. 触发限制后需等待10-30分钟才能恢复")
    print(f"4. 建议从小范围开始测试")
    print(f"5. 遇到限制时程序会自动暂停并提示")
    print(f"{'='*80}\n")
    
    # 模式5特殊处理：只扫描指定的编号
    if choice == '5':
        confirm = input(f"将测试 {len(known_numbers)} 个已知门店编号。继续？(y/n): ")
        
        if confirm.lower() != 'y':
            print("已取消")
            return
        
        # 开始扫描已知编号
        start_time = datetime.now()
        valid_stores = []
        invalid_stores = []
        
        print(f"\n{'='*80}")
        print(f"🔍 测试已知门店编号")
        print(f"{'='*80}\n")
        
        for i, num in enumerate(known_numbers, 1):
            store_num = f"R{num:03d}"
            print(f"[{i}/{len(known_numbers)}] 测试 {store_num}...", end=' ', flush=True)
            
            result = test_store_number(store_num)
            
            if result['valid']:
                print(f"✅ 有效！{result['storeName']} ({result['city']})")
                valid_stores.append(result)
                
                with open(f'store_detail_{store_num}.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                print(f"❌ 无效")
                invalid_stores.append({
                    'storeNumber': store_num,
                    'error': result.get('error', 'Unknown')
                })
            
            # 延迟
            if i < len(known_numbers):
                time.sleep(3)
        
        end_time = datetime.now()
    else:
        # 其他模式：范围扫描
        confirm = input(f"将扫描 R{start:03d} 到 R{end:03d}，共 {end-start+1} 个编号。继续？(y/n): ")
        
        if confirm.lower() != 'y':
            print("已取消")
            return
        
        # 开始扫描
        start_time = datetime.now()
        valid_stores, invalid_stores = scan_store_range(start, end, conservative=conservative)
        end_time = datetime.now()
    
    # 保存结果
    if choice == '5':
        scan_range = f"已知编号({len(known_numbers)}个)"
        total_scanned = len(known_numbers)
    else:
        scan_range = f'R{start:03d}-R{end:03d}'
        total_scanned = end - start + 1
    
    results = {
        'scan_time': datetime.now().isoformat(),
        'scan_range': scan_range,
        'duration_seconds': (end_time - start_time).total_seconds(),
        'total_scanned': total_scanned,
        'valid_count': len(valid_stores),
        'invalid_count': len(invalid_stores),
        'valid_stores': valid_stores,
        'invalid_stores': invalid_stores[:20]  # 只保存前20个无效门店
    }
    
    output_file = f'valid_stores_scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 打印总结
    print(f"\n{'='*80}")
    print(f"📊 扫描完成！")
    print(f"{'='*80}\n")
    print(f"扫描范围：{scan_range}")
    print(f"总计扫描：{total_scanned} 个编号")
    print(f"有效门店：{len(valid_stores)} 个 ✅")
    print(f"无效编号：{len(invalid_stores)} 个 ❌")
    print(f"耗时：{(end_time - start_time).total_seconds():.1f} 秒")
    print(f"\n结果已保存到：{output_file}")
    
    if valid_stores:
        print(f"\n{'='*80}")
        print(f"✅ 发现的有效门店：")
        print(f"{'='*80}\n")
        
        for store in valid_stores:
            print(f"  {store['storeNumber']}: {store['storeName']} ({store['city']})")
        
        # 生成新的门店配置文件
        new_stores_config = {
            "stores": [
                {
                    "storeNumber": s['storeNumber'],
                    "storeName": s['storeName'],
                    "city": s['city'],
                    "province": s.get('state', ''),
                    "phoneNumber": s.get('phoneNumber', ''),
                    "address": s.get('address', ''),
                    "verified": True,
                    "verifiedDate": datetime.now().isoformat()
                }
                for s in valid_stores
            ]
        }
        
        new_config_file = 'apple_stores_china_verified.json'
        with open(new_config_file, 'w', encoding='utf-8') as f:
            json.dump(new_stores_config, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 已生成验证后的门店配置：{new_config_file}")
        print(f"\n💡 建议：")
        print(f"   1. 查看 {output_file} 了解详细结果")
        print(f"   2. 使用 {new_config_file} 替换旧的门店配置")
        print(f"   3. 更新 config.json 中的 target_stores")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  扫描被中断")
    except Exception as e:
        logger.error(f"扫描出错: {e}")
        print(f"\n❌ 错误: {e}")

