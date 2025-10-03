#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试论文参考文献管理MCP工具
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径，以便导入thesis_reference_manager模块
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from thesis_reference_manager import analyze_citations, clean_unused_references, save_references, convert_citations_to_superscript

async def test_tools():
    """测试所有工具功能"""
    
    print("=== 测试论文参考文献管理MCP工具 ===\n")
    
    # 测试1: 分析引用
    print("1. 测试引用分析功能...")
    try:
        result = await analyze_citations("thesis_draft.tex")
        print("✓ 引用分析功能正常")
        print(f"结果: {result[0].text[:200]}...")
    except Exception as e:
        print(f"✗ 引用分析功能出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试2: 保存参考文献
    print("2. 测试保存参考文献功能...")
    try:
        result = await save_references("test_references")
        print("✓ 保存参考文献功能正常")
        print(f"结果: {result[0].text}")
    except Exception as e:
        print(f"✗ 保存参考文献功能出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试3: 转换引用格式
    print("3. 测试转换引用格式功能...")
    try:
        # 创建一个测试文件
        test_content = """
\\documentclass{article}
\\begin{document}
这是一个测试文档\\cite{test1,test2}。
另一个引用\\cite{test3}。
\\end{document}
"""
        with open("test_document.tex", "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = await convert_citations_to_superscript("test_document.tex")
        print("✓ 转换引用格式功能正常")
        print(f"结果: {result[0].text}")
        
        # 清理测试文件
        os.remove("test_document.tex")
        
    except Exception as e:
        print(f"✗ 转换引用格式功能出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    print("测试完成！")

if __name__ == "__main__":
    asyncio.run(test_tools())
