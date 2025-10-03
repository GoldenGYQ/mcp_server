# MCP Servers Collection

这是一个包含多个MCP (Model Context Protocol) 服务器的集合，为AI助手提供各种实用功能。

## 📦 包含的MCP服务器

### 1. 论文参考文献管理器 (thesis_reference_manager.py)
- **功能**: 搜索arXiv论文、管理参考文献、分析LaTeX引用
- **工具**:
  - `search_papers_arxiv`: 在arXiv上搜索论文
  - `get_paper_details`: 获取论文详细信息
  - `save_search_results`: 保存搜索结果到本地
  - `analyze_citations`: 分析LaTeX文件中的引用
  - `clean_unused_references`: 清理未使用的参考文献
  - `convert_citations_to_superscript`: 转换引用格式

### 2. 文档图片标签器 (docx_image_tagger.py)
- **功能**: 从Word文档中提取图片并生成智能标签
- **工具**:
  - `extract_docx_images`: 提取docx文件中的图片
  - `extract_docx_text`: 提取docx文件中的文本
  - `extract_docx_tables`: 提取docx文件中的表格
  - `extract_zip_assets`: 从zip文件中提取资源
  - `tag_exported_images`: 为图片生成智能标签

### 3. 本地图片分析器 (local_image_analyzer.py)
- **功能**: 分析本地图片并生成描述
- **工具**:
  - `analyze_single_image`: 分析单个图片
  - `batch_analyze_images`: 批量分析图片
  - `generate_smart_titles`: 生成智能标题

### 4. Hello World服务器 (helloworld.py)
- **功能**: 简单的测试服务器
- **工具**:
  - `helloworld`: 返回问候信息

## 🛠️ 安装和配置

### 1. 克隆仓库
```bash
git clone https://github.com/GoldenYQ/mcp-servers.git
cd mcp-servers
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置MCP客户端

#### 对于Cursor IDE:
编辑 `~/.cursor/mcp.json` 文件:

```json
{
  "mcpServers": {
    "thesis-reference-manager": {
      "command": "python",
      "args": ["path/to/mcp-servers/thesis_reference_manager.py"],
      "description": "论文参考文献管理工具"
    },
    "docx-image-tagger": {
      "command": "python", 
      "args": ["path/to/mcp-servers/docx_image_tagger.py"],
      "description": "文档图片标签器"
    },
    "local-image-analyzer": {
      "command": "python",
      "args": ["path/to/mcp-servers/local_image_analyzer.py"],
      "description": "本地图片分析器"
    },
    "hello-server": {
      "command": "python",
      "args": ["path/to/mcp-servers/helloworld.py"],
      "description": "Hello World测试服务器"
    }
  }
}
```

#### 对于其他MCP客户端:
根据您的MCP客户端文档进行配置。

## 🚀 使用方法

### 论文搜索和保存示例
```python
# 搜索论文
search_result = await search_papers_arxiv("machine learning", max_results=5)

# 保存到本地
save_result = await save_search_results(
    results=search_result,
    save_path="D:/Users/username/Desktop/references"
)
```

### 图片分析示例
```python
# 分析单个图片
analysis = await analyze_single_image(
    image_path="path/to/image.jpg",
    user_working_dir="D:/Users/username/Desktop"
)
```

## 📁 项目结构
```
mcp-servers/
├── thesis_reference_manager.py    # 论文参考文献管理器
├── docx_image_tagger.py          # 文档图片标签器
├── local_image_analyzer.py       # 本地图片分析器
├── helloworld.py                 # Hello World服务器
├── requirements.txt              # 依赖包列表
├── README.md                     # 项目说明
└── examples/                     # 使用示例
    ├── search_papers.py
    └── analyze_images.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [MCP官方文档](https://modelcontextprotocol.io/)
- [Cursor IDE](https://cursor.sh/)
