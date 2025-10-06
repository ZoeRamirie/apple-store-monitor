#!/bin/bash
# Apple Store 库存监控 - 快速启动脚本

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║         🍎 Apple Store 库存监控系统                              ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "请选择启动方式："
echo ""
echo "  1. 统一入口（推荐）- 支持香港和大陆双区域"
echo "  2. 原监控程序 - 使用config.json配置"
echo "  3. 退出"
echo ""
read -p "请选择 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "启动统一入口..."
        echo ""
        python3 main_unified.py
        ;;
    2)
        echo ""
        echo "启动原监控程序..."
        echo ""
        python3 main.py
        ;;
    3)
        echo ""
        echo "已退出"
        echo ""
        exit 0
        ;;
    *)
        echo ""
        echo "无效选择"
        echo ""
        exit 1
        ;;
esac
