# MCP Servers Collection

这是一个MCP (Model Context Protocol) 服务器集合，包含多个实用的工具服务器。

## 🚀 包含的服务器

### 1. **thesis-reference-manager** - 论文参考文献管理工具
- **功能**：搜索arXiv论文、保存搜索结果、分析LaTeX引用
- **文件**：`thesis_reference_manager.py`
- **工具**：
  - `search_papers_arxiv`: 在arXiv上搜索论文
  - `get_paper_details`: 获取论文详细信息
  - `save_search_results`: 保存搜索结果到本地
  - `analyze_citations`: 分析LaTeX引用
  - `clean_unused_references`: 清理未使用的参考文献
  - `convert_citations_to_superscript`: 转换引用格式

### 2. **docx-image-tagger** - DOCX图片标签工具
- **功能**：从DOCX文件中提取图片并生成标签
- **文件**：`docx_image_tagger.py`

### 3. **local-image-analyzer** - 本地图片分析工具
- **功能**：分析本地图片并生成智能标题
- **文件**：`local_image_analyzer.py`

### 4. **helloworld** - 简单示例服务器
- **功能**：MCP服务器基础示例
- **文件**：`helloworld.py`

## 📦 安装和配置

### 1. **环境要求**
```bash
# 创建conda环境
conda create -n docx-mcp python=3.9
conda activate docx-mcp

# 安装依赖
pip install mcp requests
```

### 2. **配置Cursor**
在 `~/.cursor/mcp.json` 中添加服务器配置：

```json
{
  "mcpServers": {
    "thesis-reference-manager": {
      "command": "python",
      "args": ["path/to/thesis_reference_manager.py"],
      "description": "论文参考文献管理工具"
    }
  }
}
```

## 🎯 使用示例

### 搜索和保存论文
```python
# 1. 搜索论文
results = await search_papers_arxiv("machine learning", max_results=5)

# 2. 保存到本地
await save_search_results(results, "D:/Users/username/Desktop/references")
```

### 分析LaTeX引用
```python
# 分析引用
await analyze_citations("thesis_draft.tex")

# 清理未使用的参考文献
await clean_unused_references("thesis_draft.tex")
```

## 🔧 开发

### 运行服务器
```bash
# 激活环境
conda activate docx-mcp

# 运行服务器
python thesis_reference_manager.py
```

### 测试服务器
```bash
# 测试初始化
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}' | python thesis_reference_manager.py
```

## 📁 项目结构

```
mcp_servers/
├── thesis_reference_manager.py    # 论文管理服务器
├── docx_image_tagger.py          # DOCX图片标签服务器
├── local_image_analyzer.py       # 图片分析服务器
├── helloworld.py                 # 示例服务器
├── readme/                       # 文档目录
├── test/                         # 测试目录
└── README.md                     # 项目说明
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

感谢MCP协议和Cursor团队提供的支持！
