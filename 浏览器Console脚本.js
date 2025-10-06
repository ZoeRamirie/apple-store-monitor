/**
 * iPhone 17系列Part Number批量提取脚本
 * 在Apple香港官网的浏览器Console中运行
 * 
 * 使用方法：
 * 1. 访问 https://www.apple.com/hk/shop/buy-iphone
 * 2. F12 → Console
 * 3. 复制粘贴下面的代码并运行
 */

(function() {
    console.log('%c🍎 iPhone Part Number 提取工具', 'color: #0066CC; font-size: 16px; font-weight: bold');
    console.log('%c开始扫描页面...', 'color: #666');
    
    // 提取所有ZA/A格式的Part Number
    const content = document.body.innerHTML;
    const matches = content.match(/[A-Z0-9]{5,6}ZA\/A/g);
    
    if (!matches || matches.length === 0) {
        console.log('%c❌ 未找到Part Number', 'color: red');
        console.log('提示：请确保页面已完全加载，或尝试选择不同的产品配置');
        return;
    }
    
    // 去重
    const uniqueModels = [...new Set(matches)];
    
    console.log(`%c✅ 找到 ${uniqueModels.length} 个Part Number`, 'color: green; font-weight: bold');
    console.log('');
    
    // 显示列表
    console.log('%c📋 Part Number列表：', 'color: #0066CC; font-size: 14px');
    uniqueModels.forEach((pn, index) => {
        console.log(`  ${index + 1}. ${pn}`);
    });
    console.log('');
    
    // 生成JSON格式
    const jsonOutput = {
        region: 'Hong Kong',
        device: 'iPhone 17 Series',
        part_number_format: 'ZA/A',
        extracted_at: new Date().toISOString(),
        models: uniqueModels.map(pn => ({
            part_number: pn,
            name: 'Unknown (需要从API获取)'
        })),
        total: uniqueModels.length
    };
    
    // 复制到剪贴板
    const jsonString = JSON.stringify(jsonOutput, null, 2);
    
    // 尝试复制
    if (navigator.clipboard) {
        navigator.clipboard.writeText(jsonString).then(() => {
            console.log('%c✅ JSON已复制到剪贴板！', 'color: green; font-weight: bold');
            console.log('您可以直接粘贴保存为文件');
        }).catch(() => {
            console.log('%c⚠️  无法自动复制，请手动复制下面的内容：', 'color: orange');
            console.log(jsonString);
        });
    } else {
        console.log('%c📄 JSON输出（请手动复制）：', 'color: #0066CC');
        console.log(jsonString);
    }
    
    // 也显示简单列表格式
    console.log('');
    console.log('%c📝 简单列表格式（可直接使用）：', 'color: #0066CC');
    console.log(uniqueModels.join('\n'));
    
    // 返回结果
    return {
        models: uniqueModels,
        json: jsonOutput,
        copyToClipboard: function() {
            if (navigator.clipboard) {
                navigator.clipboard.writeText(jsonString);
                console.log('✅ 已复制');
            }
        }
    };
})();


