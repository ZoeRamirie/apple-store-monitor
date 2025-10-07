#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apple Store 库存监控核心模块 - 增强版
支持多区域（中国大陆、香港）、单门店+多产品
"""

import requests
import time
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from logger_config import setup_logger

logger = setup_logger()


class AppleStoreMonitorEnhanced:
    """Apple Store 库存监控器 - 增强版"""
    
    # 区域配置
    REGIONS = {
        'CN': {
            'name': '中国大陆',
            'base_url': 'https://www.apple.com.cn',
            'api_url': 'https://www.apple.com.cn/shop/retail/pickup-message',
            'stores_file': 'apple_stores_china.json',
            'language': 'zh-CN',
            'api_type': 'pickup-message'
        },
        'HK': {
            'name': '香港',
            'base_url': 'https://www.apple.com/hk-zh',
            'api_url': 'https://www.apple.com/hk-zh/shop/retail/pickup-message',  # ✅ 已修复：使用pickup-message
            'stores_file': 'apple_stores_hongkong.json',
            'language': 'zh-HK',
            'api_type': 'pickup-message'  # ✅ 已修复：使用pickup-message
        }
    }
    
    def __init__(self, config: dict, stop_event=None):
        """
        初始化监控器
        
        Args:
            config: 配置字典
            stop_event: 停止事件（用于响应用户中断）
        """
        self.config = config
        self.stop_event = stop_event
        self.region = config.get('region', 'CN')  # 默认中国大陆
        
        # 验证区域
        if self.region not in self.REGIONS:
            raise ValueError(f"不支持的区域: {self.region}，仅支持: {list(self.REGIONS.keys())}")
        
        self.region_config = self.REGIONS[self.region]
        logger.info(f"初始化监控器 - 区域: {self.region_config['name']}")
        
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
            'Accept-Language': f"{self.region_config['language']},zh;q=0.9,en;q=0.8",
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': f"{self.region_config['base_url']}/shop/buy-iphone",
            'Origin': self.region_config['base_url'],
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
            stores_file = self.region_config['stores_file']
            with open(stores_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                stores_list = data.get('stores', [])
                stores_dict = {store['storeNumber']: store for store in stores_list}
                logger.info(f"已加载 {len(stores_dict)} 个 {self.region_config['name']} Apple Store")
                return stores_dict
        except FileNotFoundError:
            logger.error(f"找不到 {stores_file} 文件")
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
        检查商品在指定门店的库存
        
        Args:
            part_number: 商品型号编号
            store_number: 门店编号，None表示查询所有门店
            
        Returns:
            库存信息字典
        """
        try:
            # 香港和大陆现在都使用 pickup-message API（参数相同）
            params = {
                'pl': 'true',
                'mts.0': 'regular',
                'mts.1': 'compact',
                'cppart': 'UNLOCKED/WW',  # 使用全球解锁版
                'parts.0': part_number,
            }
            
            # 指定门店（如果提供）
            if store_number:
                params['store'] = store_number
            else:
                logger.warning("未指定门店编号，无法查询")
                return {'success': False, 'error': 'Store number required'}
            
            logger.debug(f"查询库存: {part_number} @ {store_number or '全部门店'} ({self.region_config['name']})")
            
            response = self.session.get(
                self.region_config['api_url'],
                params=params,
                timeout=self.config.get('timeout', 10)
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_availability_response(data, part_number, store_number)
            else:
                logger.warning(f"库存查询失败: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except requests.RequestException as e:
            logger.error(f"库存查询网络错误: {e}")
            return {'success': False, 'error': str(e)}
        except Exception as e:
            logger.error(f"库存查询出错: {e}")
            return {'success': False, 'error': str(e)}
    
    def _parse_availability_response(self, data: Dict, part_number: str, store_number: str = None) -> Dict:
        """
        解析库存查询响应
        
        Args:
            data: API响应数据
            part_number: 商品型号编号
            store_number: 门店编号（可选，用于香港API过滤）
            
        Returns:
            解析后的库存信息
        """
        result = {
            'success': True,
            'part_number': part_number,
            'stores': {},
            'available_stores': [],
            'timestamp': datetime.now().isoformat(),
            'region': self.region
        }
        
        try:
            # 香港和大陆都使用 pickup-message API，响应格式相同
            if 'body' in data and 'stores' in data['body']:
                stores_data = data['body']['stores']
                
                for store in stores_data:
                    store_num = store.get('storeNumber')
                    store_info = self.get_store_info(store_num)
                    
                    # 检查该门店的商品库存
                    parts_availability = store.get('partsAvailability', {})
                    product_info = parts_availability.get(part_number, {})
                    
                    pickup_display = product_info.get('pickupDisplay', 'unavailable')
                    is_available = pickup_display == 'available'
                    
                    store_result = {
                        'store_number': store_num,
                        'store_name': store_info['storeName'] if store_info else store.get('storeName', 'Unknown'),
                        'city': store_info.get('city', '') if store_info else '',
                        'district': store_info.get('district', '') if store_info else '',
                        'available': is_available,
                        'pickup_display': pickup_display,
                        'pickup_quote': product_info.get('pickupSearchQuote', ''),
                        'region': self.region
                    }
                    
                    result['stores'][store_num] = store_result
                    
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
        logger.info(f"📦 {len(products)} 个产品 × {len(target_stores)} 个门店 - 区域: {self.region}")
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
            
            # 初始化该产品的结果字典（包含所有必要的统计字段）
            if part_number not in results:
                results[part_number] = {
                    'part_number': part_number,
                    'name': product_name,
                    'product': combo['product'],
                    'result': {
                        'success': True,
                        'stores': {},
                        'available_stores': [],
                        'requested_stores': target_stores,  # 添加
                        'requested_stores_count': len(target_stores),  # 添加
                        'responded_stores_count': 0  # 添加，稍后更新
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
                
                logger.info(f"⏳ [{i}/{len(combinations)}] 等待 {delay:.3f}秒 后发送下一个请求...")
                self._interruptible_sleep(delay)
        
        # 步骤4: 更新响应门店数量
        for part_number in results:
            responded_count = len(results[part_number]['result']['stores'])
            results[part_number]['result']['responded_stores_count'] = responded_count
        
        logger.info(f"\n✅ 本轮完成，共检查 {len(combinations)} 个组合")
        logger.info(f"📊 结果: {len(results)} 个产品")
        
        return results
    
    def check_multiple_products_old(self, products: List[Dict], stores: List[str] = None) -> Dict:
        """
        检查多个商品在多个门店的库存（支持单门店+多产品）
        
        Args:
            products: 商品列表，每个商品包含 part_number 等信息
            stores: 门店编号列表，None表示所有门店
            
        Returns:
            所有商品的库存信息
        """
        results = {}
        
        # 确定要查询的门店列表
        target_stores = stores if stores else list(self.stores.keys())
        is_single_store = len(target_stores) == 1
        
        if is_single_store:
            logger.info(f"单门店模式：监控 {len(products)} 个产品在门店 {target_stores[0]}")
        else:
            logger.info(f"多门店模式：监控 {len(products)} 个产品在 {len(target_stores)} 个门店")
        
        # 香港API：一次查询返回所有门店
        if self.region == 'HK':
            logger.info(f"香港区域：使用优化查询（每个产品一次API调用）")
            
            for i, product in enumerate(products, 1):
                # 检查是否收到停止信号
                if self.stop_event and self.stop_event.is_set():
                    logger.info("检测到停止信号，中断商品查询")
                    break
                
                part_number = product.get('part_number')
                if not part_number:
                    logger.warning(f"商品缺少 part_number: {product}")
                    continue
                
                product_name = product.get('name', part_number)
                logger.info(f"[{i}/{len(products)}] 检查商品: {product_name} ({part_number})")
                
                try:
                    # 香港API：一次调用返回所有门店
                    result = self.check_product_availability(part_number, None)
                    
                    if result.get('success'):
                        # 过滤出目标门店（如果指定了）
                        all_stores = result.get('stores', {})
                        if stores:  # 如果指定了目标门店，只保留这些门店
                            all_stores = {k: v for k, v in all_stores.items() if k in stores}
                        
                        available_stores = [s for s in all_stores.values() if s.get('available')]
                        
                        results[part_number] = {
                            'product': product,
                            'all_stores': all_stores,
                            'available_stores': available_stores,
                            'timestamp': result.get('timestamp'),
                            'region': self.region
                        }
                        
                        if available_stores:
                            logger.info(f"✅ 找到库存！{len(available_stores)} 个门店有货")
                    else:
                        logger.warning(f"查询失败: {result.get('error', 'Unknown error')}")
                    
                    # 产品间延迟（香港API已经很高效了，延迟可以更短）
                    if i < len(products):
                        self._interruptible_sleep(2)
                        
                except Exception as e:
                    logger.error(f"查询产品 {part_number} 时出错: {e}")
                    continue
            
            return results
        
        # 大陆API：需要逐个门店查询
        for product in products:
            # 检查是否收到停止信号
            if self.stop_event and self.stop_event.is_set():
                logger.info("检测到停止信号，中断商品查询")
                break
            
            part_number = product.get('part_number')
            if not part_number:
                logger.warning(f"商品缺少 part_number: {product}")
                continue
            
            product_name = product.get('name', part_number)
            logger.info(f"检查商品: {product_name} ({part_number})")
            
            # 合并所有门店的查询结果
            all_stores = {}
            available_stores = []
            
            # 逐个门店查询
            error_count = 0
            skip_remaining = False
            
            for i, store_number in enumerate(target_stores, 1):
                # 检查是否收到停止信号
                if self.stop_event and self.stop_event.is_set():
                    logger.info("检测到停止信号，中断门店查询")
                    break
                
                if skip_remaining:
                    logger.info(f"跳过门店 {store_number}（已触发限制保护）")
                    continue
                
                try:
                    result = self.check_product_availability(part_number, store_number)
                    
                    if result.get('success') and 'stores' in result:
                        all_stores.update(result['stores'])
                        available_stores.extend(result.get('available_stores', []))
                        error_count = 0
                    elif 'HTTP 541' in str(result.get('error', '')):
                        error_count += 1
                        
                        if error_count >= 3:
                            logger.warning(f"⚠️  连续{error_count}次遇到API限制！")
                            logger.warning(f"为保护IP，跳过该产品的剩余查询")
                            skip_remaining = True
                            continue
                    
                    # 单门店模式：产品间延迟
                    # 多门店模式：门店间延迟
                    if is_single_store:
                        # 单门店：产品间延迟1秒
                        if i < len(target_stores):  # 不是最后一个
                            self._interruptible_sleep(1)
                    else:
                        # 多门店：按原逻辑
                        if len(target_stores) > 30:
                            if i > 30:
                                self._interruptible_sleep(2)
                            else:
                                self._interruptible_sleep(1.5)
                        else:
                            self._interruptible_sleep(1)
                        
                        if i % 5 == 0:
                            self._interruptible_sleep(3)
                            logger.info(f"已查询 {i}/{len(target_stores)} 个门店，继续...")
                        
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
                    'requested_stores_count': len(target_stores),
                    'responded_stores_count': len(all_stores),
                    'requested_stores': target_stores,
                    'timestamp': datetime.now().isoformat(),
                    'region': self.region,
                    'mode': 'single_store' if is_single_store else 'multi_store'
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
        return [store for store in self.stores.values() if store.get('city') == city]
    
    def get_stores_by_district(self, district: str) -> List[Dict]:
        """获取指定区域的门店列表（香港特有）"""
        return [store for store in self.stores.values() if store.get('district') == district]
    
    def export_history(self, filename: str = None):
        """导出库存历史记录"""
        if not filename:
            filename = f"stock_history_{self.region}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.stock_history, f, ensure_ascii=False, indent=2)
            logger.info(f"历史记录已导出到: {filename}")
            return True
        except Exception as e:
            logger.error(f"导出历史记录失败: {e}")
            return False


