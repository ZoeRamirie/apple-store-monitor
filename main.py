#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控程序 - 主程序入口
实时监控全国各个 Apple Store 的 iPhone 库存情况
"""

import sys
import json
import time
import signal
from pathlib import Path
from threading import Thread, Event, Lock
from datetime import datetime
from colorama import init, Fore, Style
from tabulate import tabulate

try:
    from apple_store_monitor_enhanced import AppleStoreMonitorEnhanced as AppleStoreMonitor
    USING_ENHANCED = True
except ImportError:
    from apple_store_monitor import AppleStoreMonitor
    USING_ENHANCED = False
from notifier import Notifier
from logger_config import setup_logger

# 初始化colorama
init(autoreset=True)

# 全局停止事件
stop_event = Event()
# 线程锁
print_lock = Lock()

logger = setup_logger()


def load_config(config_path='config.json'):
    """加载配置文件"""
    try:
        # 如果config.json不存在，尝试使用示例配置
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
        
        return config
    
    except FileNotFoundError:
        logger.error(f"配置文件未找到: {config_path}")
        logger.info("请复制 config.example.json 为 config.json 并根据需要修改")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"配置文件格式错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        sys.exit(1)


def signal_handler(sig, frame):
    """处理中断信号"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}收到中断信号，正在安全退出...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    stop_event.set()


def print_banner():
    """打印程序横幅"""
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🍎  Apple Store 库存实时监控系统 v2.0  🍎                 ║
║                                                               ║
║         实时监控全国 Apple Store iPhone 库存情况               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)


def print_config_summary(config: dict, monitor):
    """打印配置摘要"""
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📋 监控配置{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    
    # 显示区域信息（如果使用增强版）
    if USING_ENHANCED and hasattr(monitor, 'region'):
        region_name = monitor.region_config['name'] if hasattr(monitor, 'region_config') else monitor.region
        print(f"{Fore.YELLOW}🌍 监控区域: {region_name} ({monitor.region}){Style.RESET_ALL}\n")
    
    # 商品列表
    products = config['target_products']
    print(f"{Fore.YELLOW}📱 监控商品 ({len(products)}个):{Style.RESET_ALL}")
    for i, product in enumerate(products, 1):
        print(f"  {i}. {product.get('name', 'Unknown')} - "
              f"{product.get('color', '')} {product.get('storage', '')} "
              f"({product.get('part_number', 'N/A')})")
    
    # 门店列表
    if config.get('all_stores', False):
        stores = monitor.get_all_stores()
        print(f"\n{Fore.YELLOW}🏪 监控门店: 全部 ({len(stores)}个){Style.RESET_ALL}")
        
        # 按省份统计
        provinces = {}
        for store in stores:
            province = store.get('province', 'Unknown')
            provinces[province] = provinces.get(province, 0) + 1
        
        print(f"  覆盖省份/直辖市: {len(provinces)}个")
        for province, count in sorted(provinces.items()):
            print(f"    • {province}: {count}家")
    else:
        target_stores = config.get('target_stores', [])
        print(f"\n{Fore.YELLOW}🏪 监控门店 ({len(target_stores)}个):{Style.RESET_ALL}")
        for store_number in target_stores:
            store_info = monitor.get_store_info(store_number)
            if store_info:
                print(f"  • {store_info['storeName']} ({store_info['city']}, {store_info.get('state', store_info.get('province', ''))})")
            else:
                print(f"  • {store_number} (未知门店)")
    
    # 监控参数
    print(f"\n{Fore.YELLOW}⚙️  监控参数:{Style.RESET_ALL}")
    print(f"  • 检查间隔: {config.get('check_interval', 3)}秒")
    print(f"  • 桌面通知: {'✅ 开启' if config.get('enable_notification', True) else '❌ 关闭'}")
    print(f"  • 声音提醒: {'✅ 开启' if config.get('enable_sound', True) else '❌ 关闭'}")
    print(f"  • 保存历史: {'✅ 开启' if config.get('save_history', True) else '❌ 关闭'}")
    
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")


def display_stock_status(results: dict, monitor: AppleStoreMonitor):
    """
    显示库存状态
    
    Args:
        results: 查询结果
        monitor: 监控器实例
    """
    with print_lock:
        # 清屏（可选）
        # os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"\n{Fore.CYAN}{'='*100}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 库存查询结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")
        
        for part_number, data in results.items():
            product = data.get('product', {})
            product_name = f"{product.get('name', 'Unknown')} {product.get('color', '')} {product.get('storage', '')}"
            
            print(f"{Fore.YELLOW}📱 {product_name}{Style.RESET_ALL}")
            print(f"   型号: {part_number}\n")
            
            # 获取结果
            result = data.get('result', {})
            if not result.get('success', False):
                print(f"   {Fore.RED}❌ 查询失败: {result.get('error', 'Unknown')}{Style.RESET_ALL}\n")
                continue
            
            available_stores = result.get('available_stores', [])
            requested_stores_count = result.get('requested_stores_count', 0)
            responded_stores_count = result.get('responded_stores_count', 0)
            requested_stores_list = result.get('requested_stores', [])
            all_stores_data = result.get('stores', {})
            
            # 构建有响应和无响应的门店列表
            responded_stores = []
            no_response_stores = []
            
            for store_num in requested_stores_list:
                store_info = monitor.stores.get(store_num, {})
                store_name = store_info.get('storeName', store_num)
                city = store_info.get('city', '')
                
                if store_num in all_stores_data:
                    responded_stores.append(f"{store_name} ({city})")
                else:
                    no_response_stores.append(f"{store_name} ({city})")
            
            if available_stores:
                print(f"   {Fore.GREEN}✅ 有货! 共 {len(available_stores)} 个门店有货 (已查询 {requested_stores_count} 个门店){Style.RESET_ALL}\n")
                
                # 创建表格
                table_data = []
                for store in available_stores:
                    table_data.append([
                        store.get('store_name', 'Unknown'),
                        store.get('city', ''),
                        store.get('state', store.get('province', '')),
                        f"{Fore.GREEN}✓ 可取货{Style.RESET_ALL}",
                        store.get('pickup_quote', '')
                    ])
                
                headers = ['门店名称', '城市', '省份', '状态', '备注']
                print(tabulate(table_data, headers=headers, tablefmt='simple'))
                print()
            else:
                # 如果请求和响应门店数不一致，提示用户
                if requested_stores_count > responded_stores_count:
                    print(f"   {Fore.RED}❌ 暂无库存 (已查询 {requested_stores_count} 个门店，收到 {responded_stores_count} 个门店响应){Style.RESET_ALL}\n")
                else:
                    print(f"   {Fore.RED}❌ 暂无库存 (已查询 {requested_stores_count} 个门店){Style.RESET_ALL}\n")
            
            # 显示详细的门店响应情况
            if responded_stores:
                print(f"   {Fore.CYAN}📡 有响应的门店 ({len(responded_stores)}个):{Style.RESET_ALL}")
                for store in responded_stores:
                    print(f"      {Fore.GREEN}✓{Style.RESET_ALL} {store}")
                print()
            
            if no_response_stores:
                print(f"   {Fore.YELLOW}⚠️  未响应的门店 ({len(no_response_stores)}个):{Style.RESET_ALL}")
                for store in no_response_stores:
                    print(f"      {Fore.YELLOW}○{Style.RESET_ALL} {store}")
                print()
        
        print(f"{Fore.CYAN}{'='*100}{Style.RESET_ALL}\n")


def monitor_loop(monitor: AppleStoreMonitor, notifier: Notifier, config: dict):
    """
    主监控循环
    
    Args:
        monitor: 监控器实例
        notifier: 通知器实例
        config: 配置字典
    """
    products = config['target_products']
    target_stores = config.get('target_stores', []) if not config.get('all_stores', False) else None
    check_interval = config.get('check_interval', 3)
    
    iteration = 0
    
    while not stop_event.is_set():
        try:
            iteration += 1
            logger.info(f"开始第 {iteration} 轮库存检查...")
            
            # 检查所有商品
            results = monitor.check_multiple_products(products, target_stores)
            
            # 显示结果
            display_stock_status(results, monitor)
            
            # 检查库存并发送通知（持续提醒模式）
            for part_number, data in results.items():
                product = data.get('product', {})
                result = data.get('result', {})
                
                if not result.get('success'):
                    continue
                
                available_stores = result.get('available_stores', [])
                
                if available_stores:
                    # 持续提醒模式：只要有货就通知
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
    
    # 初始化监控器
    logger.info("正在初始化监控器...")
    monitor = AppleStoreMonitor(config, stop_event)
    
    # 打印配置摘要
    print_config_summary(config, monitor)
    
    # 初始化通知器
    notifier = Notifier(config)
    
    # 计算监控范围
    product_count = len(config['target_products'])
    if config.get('all_stores', False):
        store_count = len(monitor.get_all_stores())
    else:
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

