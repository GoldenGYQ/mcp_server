# 论文参考文献管理MCP工具

这是一个用于管理LaTeX论文参考文献的MCP工具，提供引用分析、清理和管理功能。

## 功能特性

### 1. 引用分析 (analyze_citations)
- 分析论文中使用的引用
- 找出未使用的参考文献
- 检查使用但未定义的引用
- 提供详细的统计信息

### 2. 清理未使用引用 (clean_unused_references)
- 自动删除未使用的参考文献条目
- 保持论文整洁
- 避免冗余引用

### 3. 保存参考文献 (save_references)
- 生成JSON格式的参考文献信息
- 生成BibTeX格式的参考文献
- 生成Markdown格式的参考文献文档

### 4. 引用格式转换 (convert_citations_to_superscript)
- 将LaTeX中的`\cite{}`引用转换为上标格式
- 支持单个和多个引用
- 自动生成引用映射

## 使用方法

### 在Cursor中使用

1. 确保MCP配置文件已更新
2. 重启Cursor
3. 在聊天中使用以下命令：

```
@thesis-reference-manager analyze_citations
```

```
@thesis-reference-manager clean_unused_references
```

```
@thesis-reference-manager save_references
```

```
@thesis-reference-manager convert_citations_to_superscript
```

### 参数说明

- `tex_file`: LaTeX文件路径（默认为thesis_draft.tex）
- `output_dir`: 输出目录（默认为references）

## 示例用法

### 分析引用
```
分析我的论文中的引用使用情况
```

### 清理未使用引用
```
清理论文中未使用的参考文献
```

### 保存参考文献
```
将参考文献保存到references文件夹
```

### 转换引用格式
```
将论文中的引用转换为上标格式
```

## 输出格式

### 引用分析结果
- 使用的引用数量
- 定义的参考文献数量
- 未使用的参考文献列表
- 使用但未定义的引用列表

### 清理结果
- 删除的参考文献数量
- 删除的参考文献列表

### 保存结果
- JSON格式的参考文献信息
- BibTeX格式的参考文献
- Markdown格式的参考文献文档

## 注意事项

1. 使用前请备份LaTeX文件
2. 清理操作会直接修改文件，请谨慎使用
3. 建议先使用分析功能了解引用情况
4. 转换格式前请确保引用键名正确

## 技术实现

- 基于Python正则表达式进行文本分析
- 使用MCP协议提供工具接口
- 支持异步操作
- 提供详细的错误处理

## 依赖项

- mcp
- asyncio
- json
- re
- os

## 版本信息

- 版本: 1.0.0
- 作者: AI Assistant
- 更新日期: 2024年
