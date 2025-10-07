#!/bin/bash

# iPhone 16 交互式配置测试脚本
# 用于验证iPhone 16是否能在交互式配置中正常选择

cd "$(dirname "$0")"

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║         📱 iPhone 16 交互式配置测试                               ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# 测试1: 检查数据文件
echo "测试1: 检查iPhone 16是否在数据文件中..."
if grep -q "MYEV3CH/A" iphone17_all_models.json; then
    echo "  ✅ iPhone 16 (MYEV3CH/A) 已在数据文件中"
else
    echo "  ❌ iPhone 16 未找到"
    exit 1
fi

# 测试2: 加载测试
echo ""
echo "测试2: 测试交互式配置加载..."
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from interactive_config import InteractiveConfigGenerator
    generator = InteractiveConfigGenerator()
    
    iphone16_count = len(generator.products_data.get('16_standard', []))
    
    if iphone16_count > 0:
        print(f"  ✅ 成功加载 {iphone16_count} 个iPhone 16机型")
        
        # 显示机型信息
        for product in generator.products_data.get('16_standard', []):
            print(f"     • {product['name']} ({product['part_number']})")
    else:
        print("  ❌ 未加载到iPhone 16机型")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ 加载失败: {e}")
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 测试失败"
    exit 1
fi

# 测试3: API测试
echo ""
echo "测试3: 测试API查询iPhone 16..."
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from apple_store_monitor_enhanced import AppleStoreMonitorEnhanced
    
    config = {
        'region': 'CN',
        'target_products': [{'name': 'iPhone 16 黑色 128GB', 'part_number': 'MYEV3CH/A'}],
        'target_stores': ['R448']
    }
    
    monitor = AppleStoreMonitorEnhanced(config)
    result = monitor.check_product_availability('MYEV3CH/A', 'R448')
    
    if result.get('success'):
        stores = result.get('stores', {})
        for store_num, store_data in stores.items():
            status = "有货" if store_data['available'] else "无货"
            print(f"  ✅ API查询成功: {store_data['store_name']} - {status}")
            print(f"     提示: {store_data.get('pickup_quote', 'N/A')}")
    else:
        print(f"  ❌ API查询失败: {result.get('error')}")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 测试失败"
    exit 1
fi

# 全部成功
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 所有测试通过！"
echo ""
echo "iPhone 16 现在可以在交互式配置中使用："
echo ""
echo "  python3 start.py"
echo ""
echo "  然后选择:"
echo "    1. 区域: 1 (中国大陆)"
echo "    2. 配置: 1 (交互式配置)"
echo "    3. 策略: 任意"
echo "    4. 产品系列: 1 (iPhone 16 标准版)"
echo "    5. 型号: 1 (iPhone 16 黑色 128GB)"
echo "    6. 门店: 任意"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"




