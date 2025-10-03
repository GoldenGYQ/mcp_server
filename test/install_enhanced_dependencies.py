#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装增强版参考文献管理工具的依赖项
"""

import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ 成功安装 {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 安装 {package} 失败: {e}")
        return False

def main():
    """主函数"""
    print("开始安装增强版参考文献管理工具的依赖项...")
    
    # 必需的依赖项
    dependencies = [
        "requests",  # HTTP请求库
        "mcp",       # MCP协议支持
    ]
    
    # 可选的依赖项
    optional_dependencies = [
        "bibtexparser",  # BibTeX解析
        "lxml",          # XML解析优化
    ]
    
    print("\n安装必需依赖项...")
    required_success = 0
    for dep in dependencies:
        if install_package(dep):
            required_success += 1
    
    print(f"\n必需依赖项安装结果: {required_success}/{len(dependencies)}")
    
    print("\n安装可选依赖项...")
    optional_success = 0
    for dep in optional_dependencies:
        if install_package(dep):
            optional_success += 1
    
    print(f"\n可选依赖项安装结果: {optional_success}/{len(optional_dependencies)}")
    
    print("\n=== 安装完成 ===")
    print("增强版参考文献管理工具现在支持以下功能:")
    print("• arXiv论文搜索")
    print("• Semantic Scholar论文搜索")
    print("• 论文详情获取")
    print("• 搜索结果保存")
    print("• 原有参考文献管理功能")
    
    if required_success == len(dependencies):
        print("\n🎉 所有必需依赖项安装成功！工具可以正常使用。")
    else:
        print("\n⚠️  部分必需依赖项安装失败，请手动安装。")

if __name__ == "__main__":
    main()
