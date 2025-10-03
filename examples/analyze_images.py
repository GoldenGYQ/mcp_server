#!/usr/bin/env python3
"""
图片分析示例
演示如何使用local_image_analyzer MCP服务器
"""

import asyncio
from local_image_analyzer import analyze_single_image, batch_analyze_images

async def main():
    """分析图片的示例"""
    
    # 1. 分析单个图片
    print("🖼️ 分析单个图片...")
    result = await analyze_single_image(
        image_path="path/to/your/image.jpg",
        user_working_dir="D:/Users/username/Desktop"
    )
    print(f"分析结果: {result}")
    
    # 2. 批量分析图片
    print("📁 批量分析图片...")
    batch_result = await batch_analyze_images(
        image_dir="path/to/image/folder",
        user_working_dir="D:/Users/username/Desktop"
    )
    print(f"批量分析结果: {batch_result}")
    
    print("✅ 完成!")

if __name__ == "__main__":
    asyncio.run(main())
