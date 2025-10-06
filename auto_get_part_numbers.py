#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动获取 iPhone Part Number 工具
通过解析 Apple 官网页面自动提取所有可用的 Part Number
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse, parse_qs

def get_iphone_models():
    """获取 iPhone 机型列表"""
    models = [
        {
            'name': 'iPhone 17 Pro Max',
            'url': 'https://www.apple.com.cn/shop/buy-iphone/iphone-17-pro',
            'type': 'pro_max'
        },
        {
            'name': 'iPhone 17 Pro',
            'url': 'https://www.apple.com.cn/shop/buy-iphone/iphone-17-pro',
            'type': 'pro'
        },
        {
            'name': 'iPhone 17',
            'url': 'https://www.apple.com.cn/shop/buy-iphone/iphone-17',
            'type': 'standard'
        },
        {
            'name': 'iPhone 17 Air',
            'url': 'https://www.apple.com.cn/shop/buy-iphone/iphone-17-air',
            'type': 'air'
        }
    ]
    return models

def extract_part_numbers_from_page(url):
    """
    从 Apple 官网页面提取 Part Number
    
    注意：这个方法需要实际访问页面并解析 JavaScript 生成的内容
    Apple 的页面大多是 JavaScript 渲染的，需要使用 Selenium 等工具
    """
    print(f"\n正在访问: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ 访问失败: HTTP {response.status_code}")
            return []
        
        # 查找页面中的 Part Number
        # Apple 页面通常在 JSON 数据或 data 属性中包含型号信息
        part_numbers = []
        
        # 方法 1: 查找 data-part-number 属性
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有可能包含 Part Number 的元素
        elements_with_part = soup.find_all(attrs={'data-part-number': True})
        for elem in elements_with_part:
            part_num = elem.get('data-part-number')
            if part_num and 'CH/A' in part_num:
                part_numbers.append(part_num)
        
        # 方法 2: 在 script 标签中查找 JSON 数据
        scripts = soup.find_all('script', type='application/json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                # 递归查找 JSON 中的 Part Number
                find_part_numbers_in_json(data, part_numbers)
            except:
                pass
        
        # 方法 3: 正则表达式匹配
        pattern = r'M[UX][0-9A-Z]{3,5}CH/A'
        matches = re.findall(pattern, response.text)
        part_numbers.extend(matches)
        
        # 去重
        part_numbers = list(set(part_numbers))
        
        if part_numbers:
            print(f"✅ 找到 {len(part_numbers)} 个 Part Number")
            for pn in part_numbers:
                print(f"   - {pn}")
        else:
            print("⚠️  页面中未找到 Part Number")
            print("   这可能是因为：")
            print("   1. 页面使用 JavaScript 动态加载")
            print("   2. 需要用户交互才会显示")
            print("   3. Part Number 在 API 请求中返回")
        
        return part_numbers
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        return []

def find_part_numbers_in_json(data, result_list):
    """递归在 JSON 数据中查找 Part Number"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str) and 'CH/A' in value and re.match(r'M[UX][0-9A-Z]+', value):
                result_list.append(value)
            else:
                find_part_numbers_in_json(value, result_list)
    elif isinstance(data, list):
        for item in data:
            find_part_numbers_in_json(item, result_list)

def manual_guide():
    """显示手动获取指南"""
    print("\n" + "="*70)
    print("📋 手动获取 Part Number 指南")
    print("="*70)
    print("\n由于 Apple 官网使用 JavaScript 动态加载，自动提取较困难。")
    print("建议使用以下手动方法：\n")
    
    print("【方法一：浏览器开发者工具】")
    print("1. 访问 Apple 官网: https://www.apple.com.cn/shop/buy-iphone")
    print("2. 选择 iPhone 17 系列机型")
    print("3. 按 F12 打开开发者工具")
    print("4. 切换到 Network（网络）标签")
    print("5. 选择颜色和容量配置")
    print("6. 点击 '查看店内提货情况'")
    print("7. 输入位置并搜索")
    print("8. 在 Network 中查找 'pickup' 或 'retail' 请求")
    print("9. 查看请求参数中的 parts.0 字段\n")
    
    print("【方法二：使用 Selenium 自动化】")
    print("如果需要批量获取，可以使用 Selenium + Chrome 自动化:")
    print("1. 安装: pip install selenium")
    print("2. 下载 ChromeDriver")
    print("3. 编写自动化脚本模拟用户操作")
    print("4. 自动提取所有配置的 Part Number\n")
    
    print("【方法三：直接测试】")
    print("使用已知的 Part Number 格式规律:")
    print("- iPhone 17 Pro Max: MU7xxCH/A 或 MX7xxCH/A")
    print("- iPhone 17 Pro: MU6xxCH/A 或 MX6xxCH/A")
    print("- iPhone 17: MYExxCH/A")
    print("- 不同颜色/容量使用不同的字母/数字组合\n")
    
    print("="*70)

def create_selenium_script():
    """创建 Selenium 自动化脚本"""
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用 Selenium 自动获取 iPhone Part Number
需要先安装: pip install selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

def get_part_numbers_selenium():
    """使用 Selenium 获取 Part Number"""
    
    print("正在启动浏览器...")
    
    # 配置 Chrome 选项
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 访问 iPhone 17 Pro Max 页面
        url = "https://www.apple.com.cn/shop/buy-iphone/iphone-17-pro"
        print(f"访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 这里需要根据实际页面结构编写选择逻辑
        # 例如：选择颜色、容量等
        
        # 点击查看店内提货
        # pickup_btn = driver.find_element(By.XPATH, "//button[contains(text(), '查看店内提货')]")
        # pickup_btn.click()
        
        # 监听网络请求（需要使用 Chrome DevTools Protocol）
        
        print("\\n请手动在浏览器中:")
        print("1. 选择颜色和容量")
        print("2. 点击'查看店内提货情况'")
        print("3. 输入位置并搜索")
        print("\\n然后查看浏览器开发者工具的 Network 标签")
        
        input("\\n按回车键关闭浏览器...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    get_part_numbers_selenium()
'''
    
    with open('selenium_get_part_numbers.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("\n✅ 已创建 Selenium 脚本: selenium_get_part_numbers.py")
    print("   使用方法:")
    print("   1. pip install selenium")
    print("   2. 下载 ChromeDriver: https://chromedriver.chromium.org/")
    print("   3. python selenium_get_part_numbers.py")

def main():
    """主函数"""
    print("\n" + "="*70)
    print("🍎 iPhone Part Number 自动获取工具")
    print("="*70)
    
    print("\n说明：")
    print("由于 Apple 官网使用了大量 JavaScript 和动态加载，")
    print("简单的 HTTP 请求无法获取完整的 Part Number 列表。")
    print("\n推荐的获取方法：")
    print("1. 使用浏览器开发者工具手动获取（最可靠）")
    print("2. 使用 Selenium 自动化（可批量获取）")
    print("3. 参考已知的型号规律（用于测试）")
    
    print("\n正在尝试从页面提取...")
    
    models = get_iphone_models()
    all_part_numbers = {}
    
    for model in models:
        print(f"\n{'='*70}")
        print(f"📱 {model['name']}")
        print(f"{'='*70}")
        
        part_numbers = extract_part_numbers_from_page(model['url'])
        if part_numbers:
            all_part_numbers[model['name']] = part_numbers
    
    if all_part_numbers:
        print("\n" + "="*70)
        print("📊 提取结果汇总")
        print("="*70)
        
        for model_name, pns in all_part_numbers.items():
            print(f"\n{model_name}:")
            for pn in pns:
                print(f"  - {pn}")
        
        # 保存到文件
        with open('iphone_17_part_numbers.json', 'w', encoding='utf-8') as f:
            json.dump(all_part_numbers, f, ensure_ascii=False, indent=2)
        
        print("\n✅ 已保存到: iphone_17_part_numbers.json")
    else:
        print("\n⚠️  自动提取未成功")
    
    # 显示手动指南
    manual_guide()
    
    # 询问是否创建 Selenium 脚本
    print("\n" + "="*70)
    response = input("\n是否创建 Selenium 自动化脚本？(y/n): ")
    if response.lower() == 'y':
        create_selenium_script()
    
    print("\n" + "="*70)
    print("💡 提示：")
    print("如果需要准确的 Part Number，最可靠的方法是：")
    print("1. 访问 Apple 官网")
    print("2. 使用浏览器开发者工具")
    print("3. 查看实际的 API 请求")
    print("\n详细步骤请查看: 获取Part_Number详细教程.md")
    print("="*70)

if __name__ == "__main__":
    main()








