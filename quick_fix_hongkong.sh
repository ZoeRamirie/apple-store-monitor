#!/bin/bash

# 香港门店快速修复脚本
# 快速验证和修复香港门店配置

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║            🔧 香港门店快速修复脚本                               ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

echo "📋 检测到的问题："
echo "   当前4个香港门店编号可能不正确"
echo ""

echo "🔍 开始快速诊断..."
echo ""

# 检查文件是否存在
if [ ! -f "apple_stores_hongkong.json" ]; then
    echo "❌ 错误：找不到 apple_stores_hongkong.json"
    exit 1
fi

echo "✅ 配置文件存在"
echo ""

# 显示当前门店
echo "📍 当前配置的香港门店："
cat apple_stores_hongkong.json | grep "storeNumber" | head -4
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🛠️  提供3个修复方案："
echo ""
echo "方案1：使用Apple官方API获取（推荐）⭐"
echo "   python3 fetch_real_hongkong_stores.py"
echo ""
echo "方案2：手动验证门店编号"
echo "   访问：https://www.apple.com/hk/retail/"
echo "   查看每个门店页面的实际编号"
echo ""
echo "方案3：扫描有效编号（耗时15分钟）"
echo "   python3 verify_hongkong_stores.py"
echo "   选择选项2"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "是否现在运行方案1？(y/n): " choice

if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
    echo ""
    echo "▶️  正在运行方案1..."
    echo ""
    python3 fetch_real_hongkong_stores.py
    
    if [ -f "apple_stores_hongkong_official.json" ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "✅ 成功获取官方门店数据！"
        echo ""
        read -p "是否替换当前配置？(y/n): " replace
        
        if [ "$replace" = "y" ] || [ "$replace" = "Y" ]; then
            # 备份原配置
            cp apple_stores_hongkong.json apple_stores_hongkong.json.backup
            echo "✅ 已备份原配置到 apple_stores_hongkong.json.backup"
            
            # 替换配置
            cp apple_stores_hongkong_official.json apple_stores_hongkong.json
            echo "✅ 已更新配置文件"
            echo ""
            echo "🎉 香港门店配置已更新！"
        else
            echo ""
            echo "ℹ️  配置未替换，您可以手动操作："
            echo "   cp apple_stores_hongkong_official.json apple_stores_hongkong.json"
        fi
    else
        echo ""
        echo "⚠️  未生成官方配置文件"
        echo ""
        echo "建议：查看详细报告"
        echo "   cat 香港门店验证报告.md"
    fi
else
    echo ""
    echo "ℹ️  您可以稍后手动运行："
    echo "   python3 fetch_real_hongkong_stores.py"
    echo ""
    echo "或查看完整报告："
    echo "   cat 香港门店验证报告.md"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 相关文档："
echo "   • 香港门店验证报告.md - 详细问题分析"
echo "   • verify_hongkong_stores.py - 验证工具"
echo "   • fetch_real_hongkong_stores.py - 官方API获取工具"
echo ""
echo "✅ 完成！"
echo ""


