#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apple Store 库存监控器 - 优化版（随机打散策略）
"""

import requests
import json
import time
import logging
from typing import Dict, List, Optional
from datetime import datetime
import random

# 配置日志
logger = logging.getLogger(__name__)


class AppleStoreMonitor:
    """Apple Store 库存监控器"""
    
    def __init__(self, config: dict, stop_event=None):
        """
        初始化监控器
        
        Args:
            config: 配置字典
            stop_event: 停止事件（用于优雅退出）
        """
        self.config = config
        self.stop_event = stop_event
        self.session = requests.Session()
        self.stock_history = {}
        
        # API endpoints
        self.api_url = 'https://www.apple.com.cn/shop/retail/pickup-message'
        
        # 加载门店数据
        self.stores = self._load_stores()
        logger.info(f"已加载 {len(self.stores)} 个 Apple Store")
        
        # 设置请求头
        self.session.headers.update({
            'User-Agent': config.get('user_agent', 
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'),
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.apple.com.cn/'
        })
    
    def _load_stores(self) -> Dict:
        """加载门店数据"""
        try:
            with open('apple_stores_china.json', 'r', encoding='utf-8') as f:
                stores_list = json.load(f)
            
            # 转换为字典格式，以store_number为key
            stores = {}
            for store in stores_list:
                stores[store['storeNumber']] = store
            
            return stores
        except Exception as e:
            logger.error(f"加载门店数据失败: {e}")
            return {}
    
    def _interruptible_sleep(self, seconds: float):
        """可中断的sleep"""
        if not self.stop_event:
            time.sleep(seconds)
            return
        
        end_time = time.time() + seconds
        while time.time() < end_time:
            if self.stop_event.is_set():
                return
            time.sleep(min(0.1, end_time - time.time()))
    
    def check_product_availability(self, part_number: str, store_number: str) -> Dict:
        """检查单个产品在单个门店的库存"""
        try:
            params = {
                'pl': 'true',
                'mts.0': 'regular',
                'mts.1': 'compact',
                'cppart': 'UNLOCKED/US',
                'parts.0': part_number,
                'store': store_number
            }
            
            response = self.session.get(self.api_url, params=params, timeout=10)
            
            if response.status_code == 541:
                return {
                    'success': False,
                    'error': 'HTTP 541 - API访问频率限制',
                    'part_number': part_number,
                    'store_number': store_number
                }
            
            response.raise_for_status()
            data = response.json()
            
            return self._parse_availability_response(data, part_number)
            
        except Exception as e:
            logger.error(f"查询失败 {part_number} @ {store_number}: {e}")
            return {
                'success': False,
                'error': str(e),
                'part_number': part_number,
                'store_number': store_number
            }
    
    def _parse_availability_response(self, data: Dict, part_number: str) -> Dict:
        """解析API响应"""
        result = {
            'success': True,
            'part_number': part_number,
            'stores': {},
            'available_stores': []
        }
        
        try:
            body = data.get('body', {})
            stores_data = body.get('stores', [])
            
            for store in stores_data:
                store_number = store.get('storeNumber')
                if not store_number:
                    continue
                
                # 获取库存信息
                parts_availability = store.get('partsAvailability', {})
                product_info = parts_availability.get(part_number, {})
                
                pickup_display = product_info.get('pickupDisplay', 'unavailable')
                is_available = pickup_display == 'available'
                
                store_info = self.stores.get(store_number)
                
                store_result = {
                    'store_number': store_number,
                    'store_name': store_info['storeName'] if store_info else store.get('storeName', 'Unknown'),
                    'city': store_info['city'] if store_info else '',
                    'available': is_available,
                    'pickup_display': pickup_display,
                }
                
                result['stores'][store_number] = store_result
                
                if is_available:
                    result['available_stores'].append(store_result)
            
            return result
            
        except Exception as e:
            logger.error(f"解析库存数据失败: {e}")
            result['success'] = False
            result['error'] = str(e)
            return result
    
    def check_multiple_products(self, products: List[Dict], stores: List[str] = None) -> Dict:
        """
        检查多个商品在多个门店的库存（优化版：随机打散策略）
        
        Args:
            products: 商品列表，每个商品包含 part_number 等信息
            stores: 门店编号列表，None表示所有门店
            
        Returns:
            所有商品的库存信息
        """
        results = {}
        
        # 确定要查询的门店列表
        target_stores = stores if stores else list(self.stores.keys())
        
        # 步骤1: 生成所有"产品-门店"组合
        combinations = []
        for product in products:
            part_number = product.get('part_number')
            if not part_number:
                logger.warning(f"商品缺少 part_number: {product}")
                continue
            
            for store_number in target_stores:
                combinations.append({
                    'product': product,
                    'part_number': part_number,
                    'product_name': product.get('name', part_number),
                    'store_number': store_number
                })
        
        # 步骤2: 随机打散顺序（每轮都不同）
        random.shuffle(combinations)
        
        logger.info(f"\n{'='*80}")
        logger.info(f"🎲 本轮检查 {len(combinations)} 个组合（已随机打散）")
        logger.info(f"📦 {len(products)} 个产品 × {len(target_stores)} 个门店")
        logger.info(f"{'='*80}\n")
        
        # 步骤3: 逐个发送请求，随机间隔
        error_count = 0  # 连续错误计数
        
        for i, combo in enumerate(combinations, 1):
            # 检查是否收到停止信号
            if self.stop_event and self.stop_event.is_set():
                logger.info("检测到停止信号，中断查询")
                break
            
            part_number = combo['part_number']
            product_name = combo['product_name']
            store_number = combo['store_number']
            
            # 初始化该产品的结果字典
            if part_number not in results:
                results[part_number] = {
                    'part_number': part_number,
                    'name': product_name,
                    'product': combo['product'],
                    'result': {
                        'success': True,
                        'stores': {},
                        'available_stores': []
                    }
                }
            
            try:
                # 发送请求
                result = self.check_product_availability(part_number, store_number)
                
                if result.get('success') and 'stores' in result:
                    # 合并门店数据
                    results[part_number]['result']['stores'].update(result['stores'])
                    results[part_number]['result']['available_stores'].extend(result.get('available_stores', []))
                    error_count = 0  # 重置错误计数
                elif 'HTTP 541' in str(result.get('error', '')):
                    # 检测到HTTP 541错误
                    error_count += 1
                    logger.warning(f"⚠️  API限制警告 ({error_count}/3)")
                    
                    if error_count >= 3:
                        logger.error(f"🛑 连续触发限制，停止本轮剩余 {len(combinations) - i} 个请求")
                        logger.error(f"💡 建议：增加 check_interval 或减少产品/门店数量")
                        break
            
            except Exception as e:
                logger.error(f"查询失败 {product_name} @ {store_number}: {e}")
            
            # 随机延迟（最后一个不延迟）
            if i < len(combinations):
                # 随机延迟：1.5-2.5秒（正态分布更自然）
                delay = random.gauss(2.0, 0.3)  # 均值2.0秒，标准差0.3
                delay = max(1.5, min(2.5, delay))  # 限制在1.5-2.5秒
                
                logger.debug(f"⏳ [{i}/{len(combinations)}] 等待 {delay:.3f}秒 后发送下一个请求...")
                self._interruptible_sleep(delay)
        
        logger.info(f"\n✅ 本轮完成，共检查 {len(combinations)} 个组合")
        logger.info(f"📊 结果: {len(results)} 个产品")
        
        return results
    
    def _save_to_history(self, part_number: str, data: Dict):
        """保存库存历史记录"""
        if not self.config.get('save_history', True):
            return
        
        if part_number not in self.stock_history:
            self.stock_history[part_number] = []
        
        self.stock_history[part_number].append({
            'timestamp': datetime.now().isoformat(),
            'data': data
        })
        
        # 只保留最近100条记录
        if len(self.stock_history[part_number]) > 100:
            self.stock_history[part_number] = self.stock_history[part_number][-100:]
    
    def get_all_stores(self) -> List[Dict]:
        """获取所有门店列表"""
        return list(self.stores.values())
    
    def export_history(self, filename: str = None, region: str = 'CN'):
        """导出库存历史记录"""
        if not filename:
            filename = f"stock_history_{region}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.stock_history, f, ensure_ascii=False, indent=2)
            logger.info(f"历史记录已导出到: {filename}")
            return filename
        except Exception as e:
            logger.error(f"导出历史记录失败: {e}")
            return None

