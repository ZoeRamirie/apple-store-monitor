#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控程序 - 增强版主程序
支持：单门店+多产品、香港门店、中国大陆门店
"""

import sys
import json
import signal
import time
from pathlib import Path
from threading import Event
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate

# 导入增强版监控器
from apple_store_monitor_enhanced import AppleStoreMonitorEnhanced
from notifier import Notifier
from logger_config import setup_logger

init(autoreset=True)
stop_event = Event()
logger = setup_logger()


def load_config(config_path='config.json'):
    """加载配置文件"""
    try:
        config_file = Path(config_path)
        if not config_file.exists():
            example_config = Path('config.example.json')
            if example_config.exists():
                logger.warning(f"{config_path} 不存在，使用示例配置")
                config_path = 'config.example.json'
            else:
                raise FileNotFoundError("配置文件未找到")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 验证必要字段
        required_fields = ['target_products']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"配置文件缺少必要字段: {field}")
        
        # 设置默认区域
        if 'region' not in config:
            config['region'] = 'CN'
            logger.warning("未指定区域，使用默认值：CN（中国大陆）")
        
        return config
    
    except FileNotFoundError:
        logger.error(f"配置文件未找到: {config_path}")
        logger.info("请复制配置示例文件或创建config.json")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        sys.exit(1)


def signal_handler(sig, frame):
    """处理中断信号"""
    print(f"\n{Fore.YELLOW}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}收到中断信号，正在安全退出...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*70}{Style.RESET_ALL}\n")
    stop_event.set()


def print_banner():
    """打印程序横幅"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║     🍎  Apple Store 库存实时监控系统 v2.1 (增强版)  🍎           ║
║                                                                   ║
║         ✨ 新功能：单门店+多产品、香港门店支持                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)


def print_config_summary(config: dict, monitor: AppleStoreMonitorEnhanced):
    """打印配置摘要"""
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📋 监控配置{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    
    # 区域信息
    region_name = monitor.region_config['name']
    print(f"{Fore.YELLOW}🌍 监控区域: {region_name}{Style.RESET_ALL}")
    print(f"  • API端点: {monitor.region_config['api_url']}")
    print(f"  • 语言: {monitor.region_config['language']}")
    
    # 商品列表
    products = config['target_products']
    print(f"\n{Fore.YELLOW}📱 监控商品 ({len(products)}个):{Style.RESET_ALL}")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product.get('name', 'Unknown')} - "
              f"{product.get('color', '')} {product.get('storage', '')} "
              f"({product.get('part_number', 'N/A')})")
    
    # 门店列表
    target_stores = config.get('target_stores', [])
    is_single_store = len(target_stores) == 1
    
    if is_single_store:
        print(f"\n{Fore.YELLOW}🏪 监控门店: 单门店模式{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}🏪 监控门店 ({len(target_stores)}个):{Style.RESET_ALL}")
    
    for store_number in target_stores:
        store_info = monitor.get_store_info(store_number)
        if store_info:
            if monitor.region == 'HK':
                print(f"  • {store_info['storeName']} ({store_info.get('city', '')})")
            else:
                print(f"  • {store_info['storeName']} ({store_info.get('city', '')})")
        else:
            print(f"  • {store_number} (未知门店)")
    
    # 监控参数
    check_interval = config.get('check_interval', 30)
    print(f"\n{Fore.YELLOW}⚙️  监控参数:{Style.RESET_ALL}")
    print(f"  • 检查间隔: {check_interval}秒")
    
    # 计算频率
    product_count = len(products)
    store_count = len(target_stores)
    one_round = product_count * store_count
    total_cycle = one_round + check_interval
    rate = one_round / total_cycle * 60
    
    print(f"  • 预计频率: {rate:.2f}次/分钟")
    
    if rate > 10:
        print(f"  • 安全性: {Fore.RED}⚠️  频率可能过高{Style.RESET_ALL}")
        print(f"\n{Fore.RED}建议使用 rate_calculator.py 验证配置！{Style.RESET_ALL}")
    elif rate > 8:
        print(f"  • 安全性: {Fore.YELLOW}✅ 安全（接近上限）{Style.RESET_ALL}")
    else:
        print(f"  • 安全性: {Fore.GREEN}✅ 安全{Style.RESET_ALL}")
    
    print(f"  • 桌面通知: {'✅ 开启' if config.get('enable_notification', True) else '❌ 关闭'}")
    print(f"  • 声音提醒: {'✅ 开启' if config.get('enable_sound', True) else '❌ 关闭'}")
    
    # 模式说明
    if is_single_store and product_count > 1:
        print(f"\n{Fore.CYAN}💡 当前模式: 单门店+多产品{Style.RESET_ALL}")
        print(f"   优势: 频率更低，配置更简单，更符合实际使用")
    
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")


def display_stock_status(results: dict, monitor: AppleStoreMonitorEnhanced):
    """显示库存状态"""
    print(f"\n{Fore.CYAN}{'='*100}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📊 库存查询结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")
    
    for part_number, data in results.items():
        product = data.get('product', {})
        product_name = f"{product.get('name', 'Unknown')} {product.get('color', '')} {product.get('storage', '')}"
        
        print(f"{Fore.YELLOW}📱 {product_name}{Style.RESET_ALL}")
        print(f"   型号: {part_number}\n")
        
        result = data.get('result', {})
        if not result.get('success', False):
            print(f"   {Fore.RED}❌ 查询失败: {result.get('error', 'Unknown')}{Style.RESET_ALL}\n")
            continue
        
        available_stores = result.get('available_stores', [])
        requested_stores_count = result.get('requested_stores_count', 0)
        
        if available_stores:
            print(f"   {Fore.GREEN}✅ 有货! 共 {len(available_stores)} 个门店有货{Style.RESET_ALL}\n")
            
            # 创建表格
            table_data = []
            for store in available_stores:
                table_data.append([
                    store.get('store_name', 'Unknown'),
                    store.get('city', ''),
                    store.get('district', store.get('state', '')),
                    f"{Fore.GREEN}✓ 可取货{Style.RESET_ALL}",
                    store.get('pickup_quote', '')
                ])
            
            headers = ['门店名称', '城市', '区域', '状态', '备注']
            print(tabulate(table_data, headers=headers, tablefmt='simple'))
            print()
        else:
            print(f"   {Fore.RED}❌ 暂无库存 (已查询 {requested_stores_count} 个门店){Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")


def monitor_loop(monitor: AppleStoreMonitorEnhanced, notifier: Notifier, config: dict):
    """主监控循环"""
    products = config['target_products']
    target_stores = config.get('target_stores', [])
    check_interval = config.get('check_interval', 30)
    
    iteration = 0
    
    while not stop_event.is_set():
        try:
            iteration += 1
            logger.info(f"开始第 {iteration} 轮库存检查...")
            
            # 检查所有商品
            results = monitor.check_multiple_products(products, target_stores)
            
            # 显示结果
            display_stock_status(results, monitor)
            
            # 检查库存并发送通知
            for part_number, data in results.items():
                product = data.get('product', {})
                result = data.get('result', {})
                
                if not result.get('success'):
                    continue
                
                available_stores = result.get('available_stores', [])
                
                if available_stores:
                    if len(available_stores) == 1:
                        notifier.notify_stock_available(product, available_stores[0])
                    else:
                        notifier.notify_multiple_stores_available(product, available_stores)
                    
                    logger.info(f"🎉 {product.get('name')} 在 {len(available_stores)} 个门店有货！")
            
            # 等待下次检查
            logger.info(f"本轮检查完成，{check_interval}秒后进行下一轮...")
            stop_event.wait(check_interval)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"监控循环出错: {e}")
            notifier.notify_error(str(e))
            stop_event.wait(5)
    
    logger.info("监控循环已退出")


def main():
    """主函数"""
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 打印横幅
    print_banner()
    
    # 加载配置
    logger.info("正在加载配置...")
    config = load_config()
    
    # 初始化增强版监控器
    try:
        logger.info("正在初始化增强版监控器...")
        monitor = AppleStoreMonitorEnhanced(config, stop_event)
    except Exception as e:
        logger.error(f"初始化监控器失败: {e}")
        print(f"\n{Fore.RED}❌ 初始化失败！{Style.RESET_ALL}")
        print(f"错误: {e}\n")
        print(f"请检查：")
        print(f"  1. region配置是否正确（CN或HK）")
        print(f"  2. 门店数据文件是否存在")
        print(f"  3. Part Number格式是否正确\n")
        sys.exit(1)
    
    # 打印配置摘要
    print_config_summary(config, monitor)
    
    # 初始化通知器
    notifier = Notifier(config)
    
    # 计算监控范围
    product_count = len(config['target_products'])
    store_count = len(config.get('target_stores', []))
    
    # 发送启动通知
    notifier.notify_monitoring_started(product_count, store_count)
    
    print(f"{Fore.GREEN}✨ 监控已启动！正在实时检查库存...{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}💡 提示: 按 Ctrl+C 可随时停止监控{Style.RESET_ALL}\n")
    
    # 开始监控
    try:
        monitor_loop(monitor, notifier, config)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"程序异常: {e}")
        notifier.notify_error(str(e))
    
    # 导出历史记录
    if config.get('save_history', True):
        logger.info("正在导出历史记录...")
        monitor.export_history()
    
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}程序已退出。感谢使用 Apple Store 库存监控系统！{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    
    logger.info("程序正常退出")


if __name__ == "__main__":
    main()


