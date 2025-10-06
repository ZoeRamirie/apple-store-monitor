#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控核心模块
支持监控全国各个Apple Store的iPhone库存情况
"""

import requests
import time
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from logger_config import setup_logger

logger = setup_logger()


class AppleStoreMonitor:
    """Apple Store 库存监控器"""
    
    # Apple Store 中国区 API 端点
    BASE_URL = "https://www.apple.com.cn"
    RETAIL_API = "https://www.apple.com.cn/shop/retail/pickup-message"
    FULFILLMENT_API = "https://www.apple.com.cn/shop/fulfillment-messages"
    
    def __init__(self, config: dict, stop_event=None):
        """
        初始化监控器
        
        Args:
            config: 配置字典
            stop_event: 停止事件（用于响应用户中断）
        """
        self.config = config
        self.stop_event = stop_event
        self.session = self._create_session()
        self.stores = self._load_stores()
        self.stock_history = {}
    
    def _interruptible_sleep(self, seconds: float):
        """
        可中断的sleep，每0.1秒检查一次stop_event
        
        Args:
            seconds: 睡眠时间（秒）
        """
        if not self.stop_event:
            time.sleep(seconds)
            return
        
        # 分成小段sleep，每段检查stop_event
        end_time = time.time() + seconds
        while time.time() < end_time:
            if self.stop_event.is_set():
                return
            time.sleep(min(0.1, end_time - time.time()))
        
    def _create_session(self) -> requests.Session:
        """创建HTTP会话"""
        session = requests.Session()
        
        headers = {
            'User-Agent': self.config.get('user_agent', 
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'),
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.apple.com.cn/shop/buy-iphone',
            'Origin': 'https://www.apple.com.cn',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
        }
        session.headers.update(headers)
        
        # 设置重试策略
        adapter = requests.adapters.HTTPAdapter(
            max_retries=self.config.get('max_retries', 3),
            pool_connections=20,
            pool_maxsize=50
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        return session
    
    def _load_stores(self) -> Dict:
        """加载Apple Store列表"""
        try:
            with open('apple_stores_china.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                stores_dict = {store['storeNumber']: store for store in data['stores']}
                logger.info(f"已加载 {len(stores_dict)} 个 Apple Store")
                return stores_dict
        except FileNotFoundError:
            logger.error("找不到 apple_stores_china.json 文件")
            return {}
        except Exception as e:
            logger.error(f"加载门店列表失败: {e}")
            return {}
    
    def get_store_info(self, store_number: str) -> Optional[Dict]:
        """
        获取门店信息
        
        Args:
            store_number: 门店编号
            
        Returns:
            门店信息字典
        """
        return self.stores.get(store_number)
    
    def check_product_availability(self, part_number: str, store_number: str = None) -> Dict:
        """
        检查商品在指定门店或所有门店的库存
        
        Args:
            part_number: 商品型号编号
            store_number: 门店编号，None表示查询所有门店
            
        Returns:
            库存信息字典
        """
        try:
            # 构建查询参数
            params = {
                'pl': 'true',
                'mts.0': 'regular',
                'mts.1': 'compact',
                'cppart': 'UNLOCKED/CN',
                'parts.0': part_number,
            }
            
            # 必须指定门店才能查询
            # Apple API 不支持一次性查询所有门店
            if store_number:
                params['store'] = store_number
            else:
                # 如果没有指定门店，返回错误
                logger.warning("未指定门店编号，无法查询")
                return {'success': False, 'error': 'Store number required'}
            
            logger.debug(f"查询库存: {part_number} @ {store_number or '所有门店'}")
            
            response = self.session.get(
                self.RETAIL_API,
                params=params,
                timeout=self.config.get('timeout', 10)
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_availability_response(data, part_number)
            else:
                logger.warning(f"库存查询失败: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except requests.RequestException as e:
            logger.error(f"库存查询网络错误: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"库存查询出错: {e}")
            return {'success': False, 'error': str(e)}
    
    def _parse_availability_response(self, data: Dict, part_number: str) -> Dict:
        """
        解析库存查询响应
        
        Args:
            data: API响应数据
            part_number: 商品型号编号
            
        Returns:
            解析后的库存信息
        """
        result = {
            'success': True,
            'part_number': part_number,
            'stores': {},
            'available_stores': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 解析响应结构（根据实际API响应调整）
            if 'body' in data and 'stores' in data['body']:
                stores_data = data['body']['stores']
                
                for store in stores_data:
                    store_number = store.get('storeNumber')
                    store_info = self.get_store_info(store_number)
                    
                    # 检查该门店的商品库存
                    parts_availability = store.get('partsAvailability', {})
                    product_info = parts_availability.get(part_number, {})
                    
                    pickup_display = product_info.get('pickupDisplay', 'unavailable')
                    is_available = pickup_display == 'available'
                    
                    store_result = {
                        'store_number': store_number,
                        'store_name': store_info['storeName'] if store_info else store.get('storeName', 'Unknown'),
                        'city': store_info['city'] if store_info else '',
                        'state': store_info.get('state', store_info.get('province', '')) if store_info else '',
                        'province': store_info.get('state', store_info.get('province', '')) if store_info else '',
                        'available': is_available,
                        'pickup_display': pickup_display,
                        'pickup_quote': product_info.get('pickupSearchQuote', ''),
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
        import random
        
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
                    'stores': {},
                    'available_stores': []
                }
            
            try:
                # 发送请求
                result = self.check_product_availability(part_number, store_number)
                
                if result.get('success') and 'stores' in result:
                    # 合并门店数据
                    results[part_number]['stores'].update(result['stores'])
                    results[part_number]['available_stores'].extend(result.get('available_stores', []))
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
                # 随机延迟：3-6秒（正态分布更自然）
                delay = random.gauss(4.5, 0.8)  # 均值4.5秒，标准差0.8
                delay = max(3, min(6, delay))  # 限制在3-6秒
                
                logger.debug(f"⏳ [{i}/{len(combinations)}] 等待 {delay:.1f}秒 后发送下一个请求...")
                self._interruptible_sleep(delay)
        
        logger.info(f"\n✅ 本轮完成，共检查 {len(combinations)} 个组合")
        logger.info(f"📊 结果: {len(results)} 个产品")
        
        return results
                # 如果已决定跳过，直接跳过
                if skip_remaining:
                    logger.info(f"跳过门店 {store_number}（已触发限制保护）")
                    continue
                
                try:
                    result = self.check_product_availability(part_number, store_number)
                    
                    if result.get('success') and 'stores' in result:
                        # 合并门店数据
                        all_stores.update(result['stores'])
                        available_stores.extend(result.get('available_stores', []))
                        error_count = 0  # 重置错误计数
                    elif 'HTTP 541' in str(result.get('error', '')):
                        # 检测到HTTP 541错误
                        error_count += 1
                        
                        if error_count >= 3:
                            # 连续3次错误，跳过该产品的剩余门店
                            logger.warning(f"⚠️  连续{error_count}次遇到API限制！")
                            logger.warning(f"为保护IP，跳过该产品的剩余 {len(target_stores) - i} 个门店")
                            logger.warning(f"建议：减少监控门店数量，或增加检查间隔")
                            skip_remaining = True
                            continue
                    
                    # 基础延迟：每个门店查询后延迟
                    # 根据门店总数和当前查询数调整延迟时间
                    if len(target_stores) > 30:
                        # 大量门店时
                        if i > 30:
                            self._interruptible_sleep(2)  # 查询30个后，延迟更长
                        else:
                            self._interruptible_sleep(1.5)
                    else:
                        self._interruptible_sleep(1)
                    
                    # 每5个门店额外延迟
                    if i % 5 == 0:
                        self._interruptible_sleep(3)
                        logger.info(f"已查询 {i}/{len(target_stores)} 个门店，继续...")
                    
                    # 每查询20个门店，额外休息10秒
                    if i % 20 == 0 and i < len(target_stores):
                        logger.info(f"已查询{i}个门店，休息10秒以避免限制...")
                        self._interruptible_sleep(10)
                    
                except Exception as e:
                    logger.warning(f"查询门店 {store_number} 时出错: {e}")
                    continue
            
            results[part_number] = {
                'product': product,
                'result': {
                    'success': True,
                    'part_number': part_number,
                    'stores': all_stores,
                    'available_stores': available_stores,
                    'requested_stores_count': len(target_stores),  # 实际请求的门店数
                    'responded_stores_count': len(all_stores),     # API返回数据的门店数
                    'requested_stores': target_stores,  # 请求的门店列表
                    'timestamp': datetime.now().isoformat()
                }
            }
            
            # 记录历史
            self._save_to_history(part_number, results[part_number])
        
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
    
    def get_stores_by_city(self, city: str) -> List[Dict]:
        """获取指定城市的门店列表"""
        return [store for store in self.stores.values() if store['city'] == city]
    
    def get_stores_by_province(self, province: str) -> List[Dict]:
        """获取指定省份的门店列表"""
        return [store for store in self.stores.values() if store.get('state', store.get('province', '')) == province]
    
    def export_history(self, filename: str = None):
        """导出库存历史记录"""
        if not filename:
            filename = f"stock_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.stock_history, f, ensure_ascii=False, indent=2)
            logger.info(f"历史记录已导出到: {filename}")
            return True
        except Exception as e:
            logger.error(f"导出历史记录失败: {e}")
            return False

