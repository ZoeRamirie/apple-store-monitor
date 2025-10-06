#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
通知模块 - 支持多种通知方式
"""

import os
import sys
import platform
from datetime import datetime
from typing import List, Dict
from logger_config import setup_logger

logger = setup_logger()

# 尝试导入通知库
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    logger.warning("plyer 未安装，桌面通知将不可用")


class Notifier:
    """多功能通知器"""
    
    def __init__(self, config: dict):
        """
        初始化通知器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.enable_notification = config.get('enable_notification', True)
        self.enable_sound = config.get('enable_sound', True)
        self.notification_types = config.get('notification_types', ['desktop', 'sound', 'log'])
        self.system = platform.system()
        
        # 通知历史
        self.notification_history = []
    
    def notify_stock_available(self, product_info: Dict, store_info: Dict):
        """
        发送有货通知
        
        Args:
            product_info: 商品信息
            store_info: 门店信息
        """
        product_name = product_info.get('name', 'Unknown')
        store_name = store_info.get('store_name', 'Unknown')
        city = store_info.get('city', '')
        
        title = "🎉 Apple Store 有货提醒"
        message = f"{product_name}\n{store_name} ({city})\n立即可取！"
        
        self._send_notification(title, message, urgency='high')
        self._play_sound(sound_type='success')
        
        # 记录通知
        self._log_notification('stock_available', {
            'product': product_name,
            'store': store_name,
            'city': city
        })
    
    def notify_multiple_stores_available(self, product_info: Dict, available_stores: List[Dict]):
        """
        发送多个门店有货通知
        
        Args:
            product_info: 商品信息
            available_stores: 有货门店列表
        """
        product_name = product_info.get('name', 'Unknown')
        store_count = len(available_stores)
        
        title = f"🎉 {store_count}个门店有货！"
        
        # 列出前3个门店
        store_list = []
        for i, store in enumerate(available_stores[:3]):
            store_list.append(f"{store.get('store_name')} ({store.get('city')})")
        
        message = f"{product_name}\n" + "\n".join(store_list)
        if store_count > 3:
            message += f"\n还有{store_count - 3}个门店..."
        
        self._send_notification(title, message, urgency='high')
        self._play_sound(sound_type='success')
        
        # 记录通知
        self._log_notification('multiple_stores', {
            'product': product_name,
            'store_count': store_count,
            'stores': [s.get('store_name') for s in available_stores]
        })
    
    def notify_monitoring_started(self, product_count: int, store_count: int):
        """
        发送监控启动通知
        
        Args:
            product_count: 监控商品数量
            store_count: 监控门店数量
        """
        title = "✅ 监控已启动"
        message = f"正在监控 {product_count} 个商品\n覆盖 {store_count} 个门店"
        
        self._send_notification(title, message, urgency='normal')
        logger.info(f"监控已启动: {product_count}个商品, {store_count}个门店")
    
    def notify_error(self, error_msg: str):
        """
        发送错误通知
        
        Args:
            error_msg: 错误消息
        """
        title = "❌ 监控错误"
        message = f"发生错误: {error_msg}"
        
        self._send_notification(title, message, urgency='normal')
        logger.error(error_msg)
    
    def _send_notification(self, title: str, message: str, urgency: str = 'normal'):
        """
        发送桌面通知
        
        Args:
            title: 通知标题
            message: 通知内容
            urgency: 紧急程度 (low/normal/high)
        """
        if not self.enable_notification or 'desktop' not in self.notification_types:
            return
        
        try:
            if PLYER_AVAILABLE:
                # 使用 plyer 发送跨平台通知
                notification.notify(
                    title=title,
                    message=message,
                    app_name='Apple Store Monitor',
                    timeout=15 if urgency == 'high' else 10
                )
                logger.debug(f"已发送桌面通知: {title}")
            
            elif self.system == 'Darwin':  # macOS
                # 使用 AppleScript 发送通知
                sound = 'sound name "Glass"' if self.enable_sound else ''
                os.system(f'''
                    osascript -e 'display notification "{message}" with title "{title}" {sound}'
                ''')
                logger.debug(f"已发送macOS通知: {title}")
            
            elif self.system == 'Linux':
                # 使用 notify-send
                urgency_arg = f'-u {urgency}'
                os.system(f'notify-send {urgency_arg} "{title}" "{message}"')
                logger.debug(f"已发送Linux通知: {title}")
            
            elif self.system == 'Windows':
                # Windows 10/11 toast notification
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(title, message, duration=10, threaded=True)
                    logger.debug(f"已发送Windows通知: {title}")
                except ImportError:
                    logger.warning("win10toast 未安装，无法发送Windows通知")
        
        except Exception as e:
            logger.error(f"发送桌面通知失败: {e}")
    
    def _play_sound(self, sound_type: str = 'default'):
        """
        播放提醒声音
        
        Args:
            sound_type: 声音类型 (default/success/error)
        """
        if not self.enable_sound or 'sound' not in self.notification_types:
            return
        
        try:
            if self.system == 'Darwin':  # macOS
                sounds = {
                    'default': '/System/Library/Sounds/Glass.aiff',
                    'success': '/System/Library/Sounds/Hero.aiff',
                    'error': '/System/Library/Sounds/Basso.aiff'
                }
                sound_file = sounds.get(sound_type, sounds['default'])
                os.system(f'afplay {sound_file}')
            
            elif self.system == 'Linux':
                os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null')
            
            elif self.system == 'Windows':
                import winsound
                frequencies = {
                    'default': 1000,
                    'success': 1500,
                    'error': 500
                }
                freq = frequencies.get(sound_type, frequencies['default'])
                winsound.Beep(freq, 500)
        
        except Exception as e:
            logger.debug(f"播放声音失败: {e}")
    
    def _log_notification(self, notification_type: str, data: Dict):
        """
        记录通知历史
        
        Args:
            notification_type: 通知类型
            data: 通知数据
        """
        if 'log' not in self.notification_types:
            return
        
        record = {
            'type': notification_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        self.notification_history.append(record)
        
        # 只保留最近50条记录
        if len(self.notification_history) > 50:
            self.notification_history = self.notification_history[-50:]
    
    def get_notification_history(self) -> List[Dict]:
        """获取通知历史"""
        return self.notification_history
    
    def clear_notification_history(self):
        """清空通知历史"""
        self.notification_history = []
        logger.info("通知历史已清空")


