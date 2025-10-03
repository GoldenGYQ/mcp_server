#!/usr/bin/env python3
"""
论文搜索示例
演示如何使用thesis_reference_manager MCP服务器
"""

import asyncio
import json
from thesis_reference_manager import search_papers_arxiv, save_search_results

async def main():
    """搜索并保存论文的示例"""
    
    # 1. 搜索论文
    print("🔍 搜索论文...")
    search_results = await search_papers_arxiv("machine learning", max_results=3)
    
    # 2. 解析搜索结果
    results_data = []
    for result in search_results:
        if hasattr(result, 'text'):
            # 这里需要解析文本结果，实际使用中MCP会自动处理
            print(f"找到论文: {result.text[:100]}...")
    
    # 3. 保存结果
    print("💾 保存论文...")
    save_path = "D:/Users/username/Desktop/references"
    save_result = await save_search_results(results_data, save_path)
    
    print("✅ 完成!")

if __name__ == "__main__":
    asyncio.run(main())
