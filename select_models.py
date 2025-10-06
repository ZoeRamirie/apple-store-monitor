#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iPhone 17 型号选择工具
帮助用户快速生成监控配置
"""

import json
import sys

def load_models():
    """加载所有型号"""
    with open('iphone17_all_models.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def display_models(models, series_filter=None):
    """显示型号列表"""
    series_dict = {}
    for model in models:
        series = model['series']
        if series_filter and series != series_filter:
            continue
        if series not in series_dict:
            series_dict[series] = []
        series_dict[series].append(model)
    
    idx = 1
    model_map = {}
    
    for series in ['iPhone 17', 'iPhone 17 Pro', 'iPhone 17 Pro Max']:
        if series in series_dict:
            print(f"\n📱 {series}")
            print("-" * 80)
            for model in series_dict[series]:
                part = model['part_number']
                desc = model['description']
                print(f"  {idx:2d}. {part} - {desc}")
                model_map[idx] = model
                idx += 1
    
    return model_map

def main():
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                                                                ║")
    print("║        🍎 iPhone 17 型号选择工具 🍎                           ║")
    print("║                                                                ║")
    print("╚════════════════════════════════════════════════════════════════╝\n")
    
    # 加载所有型号
    all_models = load_models()
    
    print("📊 可选型号总数: 31 个")
    print("\n选择模式:")
    print("  1. 快速模式 - 使用热门预设（推荐）")
    print("  2. 自定义模式 - 手动选择型号")
    print("  3. 按系列选择")
    
    try:
        mode = input("\n请选择模式 (1-3): ").strip()
        
        if mode == '1':
            # 快速模式
            print("\n✅ 使用热门预设配置")
            print("\n包含型号:")
            print("  • iPhone 17 Pro 256GB 银色 (MG8T4CH/A)")
            print("  • iPhone 17 Pro 256GB 深蓝色 (MG8V4CH/A)")
            print("  • iPhone 17 Pro Max 256GB 银色 (MG034CH/A)")
            print("  • iPhone 17 Pro Max 256GB 深蓝色 (MG054CH/A)")
            
            confirm = input("\n使用此配置？(y/n): ").strip().lower()
            if confirm == 'y':
                import shutil
                shutil.copy('config_iphone17_popular.json', 'config.json')
                print("\n✅ 配置已生成: config.json")
                print("\n启动命令: python3 main.py")
                return
        
        elif mode == '2':
            # 自定义模式
            print("\n📱 所有型号:")
            model_map = display_models(all_models)
            
            print("\n请输入要监控的型号编号，用逗号分隔")
            print("例如: 1,2,5  或者  10,15,20,25")
            
            selections = input("\n您的选择: ").strip()
            selected_indices = [int(x.strip()) for x in selections.split(',')]
            
            selected_models = []
            for idx in selected_indices:
                if idx in model_map:
                    model = model_map[idx]
                    # 解析描述
                    desc = model['description']
                    parts = desc.split(' ')
                    
                    # 提取容量
                    storage = ''
                    color = ''
                    for i, p in enumerate(parts):
                        if 'GB' in p:
                            storage = p
                            if i+1 < len(parts):
                                color = ' '.join(parts[i+1:])
                            break
                    
                    selected_models.append({
                        'name': f"{model['series']} {storage} {color}",
                        'part_number': model['part_number'],
                        'color': color,
                        'storage': storage,
                        'series': model['series']
                    })
            
            print(f"\n✅ 已选择 {len(selected_models)} 个型号")
            for m in selected_models:
                print(f"  • {m['name']} ({m['part_number']})")
            
            # 生成配置
            config = {
                'target_products': selected_models,
                'all_stores': False,
                'target_stores': ['R485', 'R448', 'R409', 'R388', 'R505'],
                'check_interval': 60,
                'enable_notification': True,
                'enable_sound': True,
                'notification_types': ['desktop', 'sound', 'log'],
                'max_retries': 3,
                'timeout': 10,
                'save_history': True,
                'log_level': 'INFO',
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            print("\n✅ 配置已生成: config.json")
            print("\n启动命令: python3 main.py")
        
        elif mode == '3':
            # 按系列选择
            print("\n选择系列:")
            print("  1. iPhone 17 (10个型号)")
            print("  2. iPhone 17 Pro (9个型号)")
            print("  3. iPhone 17 Pro Max (12个型号)")
            
            series_choice = input("\n请选择系列 (1-3): ").strip()
            series_map = {
                '1': 'iPhone 17',
                '2': 'iPhone 17 Pro',
                '3': 'iPhone 17 Pro Max'
            }
            
            if series_choice in series_map:
                series = series_map[series_choice]
                print(f"\n📱 {series} 型号:")
                model_map = display_models(all_models, series)
                
                print("\n请输入要监控的型号编号，用逗号分隔")
                selections = input("您的选择: ").strip()
                
                # 处理选择...（类似自定义模式）
                print("\n💡 提示: 请使用自定义模式进行详细配置")
        
    except KeyboardInterrupt:
        print("\n\n👋 已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
