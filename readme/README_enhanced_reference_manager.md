# 增强版论文参考文献管理MCP工具

这是一个增强版的参考文献管理MCP工具，集成了网络搜索功能，提供从搜索到管理的完整解决方案。

## 新增功能

### 1. 网络搜索功能
- **arXiv搜索** - 搜索预印本论文
- **Semantic Scholar搜索** - 学术论文搜索
- **论文详情获取** - 获取完整论文信息
- **搜索结果保存** - 多格式保存搜索结果

### 2. 原有功能（保留）
- 引用分析
- 清理未使用引用
- 保存参考文献
- 引用格式转换

## 安装依赖

```bash
python install_enhanced_dependencies.py
```

## 使用方法

### 1. 搜索论文

#### 在arXiv上搜索
```
@thesis-reference-manager search_papers_arxiv
{
    "query": "music generation transformer",
    "max_results": 5
}
```

#### 在Semantic Scholar上搜索
```
@thesis-reference-manager search_papers_semantic_scholar
{
    "query": "machine learning",
    "max_results": 5
}
```

### 2. 获取论文详情

```
@thesis-reference-manager get_paper_details
{
    "paper_id": "1809.04281",
    "source": "arxiv"
}
```

### 3. 保存搜索结果

```
@thesis-reference-manager save_search_results
{
    "results": [search_results],
    "output_dir": "references"
}
```

### 4. 原有功能

```
@thesis-reference-manager analyze_citations
@thesis-reference-manager clean_unused_references
@thesis-reference-manager save_references
@thesis-reference-manager convert_citations_to_superscript
```

## 完整工作流示例

### 步骤1：搜索相关论文
```python
# 搜索音乐生成相关论文
results = await search_papers_arxiv("music generation", 10)
```

### 步骤2：获取感兴趣论文的详情
```python
# 获取特定论文的详细信息
details = await get_paper_details("1809.04281", "arxiv")
```

### 步骤3：保存搜索结果
```python
# 保存搜索结果到本地
save_results = await save_search_results(search_results, "my_references")
```

### 步骤4：分析现有引用
```python
# 分析论文中的引用使用情况
analysis = await analyze_citations("thesis_draft.tex")
```

### 步骤5：清理未使用引用
```python
# 清理未使用的参考文献
cleanup = await clean_unused_references("thesis_draft.tex")
```

## 输出格式

### 搜索结果格式
- **JSON格式** - 结构化数据
- **BibTeX格式** - 标准引用格式
- **Markdown格式** - 可读性文档

### 论文详情格式
- 标题、作者、发表时间
- 摘要或总结
- 链接和标识符
- BibTeX引用格式

## 支持的搜索源

### arXiv
- 预印本论文
- 计算机科学、数学、物理等
- 免费访问

### Semantic Scholar
- 学术论文数据库
- 引用关系分析
- 多学科覆盖

### DOI解析
- 标准数字对象标识符
- 跨平台论文识别
- 元数据获取

## 技术特性

- **异步操作** - 高效并发处理
- **错误处理** - 完善的异常处理
- **超时控制** - 防止长时间等待
- **多格式输出** - 灵活的保存选项
- **网络优化** - 智能重试机制

## 测试验证

运行测试脚本验证功能：

```bash
python test_enhanced_reference_manager.py
```

## 注意事项

1. **网络连接** - 需要稳定的网络连接
2. **API限制** - 注意API调用频率限制
3. **数据准确性** - 验证搜索结果的准确性
4. **文件备份** - 操作前备份重要文件

## 故障排除

### 常见问题

1. **网络超时**
   - 检查网络连接
   - 增加超时时间

2. **API限制**
   - 减少搜索数量
   - 添加延迟

3. **解析错误**
   - 检查数据格式
   - 验证API响应

## 版本信息

- **版本**: 2.0.0
- **更新日期**: 2024年
- **新增功能**: 网络搜索、论文详情获取
- **兼容性**: 保持原有功能完全兼容

这个增强版工具现在提供了完整的参考文献搜索和管理解决方案，从网络搜索到本地管理，一站式服务。

