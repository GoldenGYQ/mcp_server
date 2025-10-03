# 测试文件结构说明

## 目录结构

```
test/
├── install_enhanced_dependencies.py          # 增强版依赖安装脚本
├── test_enhanced_reference_manager/          # 增强版参考文献管理工具测试
│   ├── test_enhanced_reference_manager.py   # 增强版功能测试脚本
│   └── test_data/                           # 测试数据目录
│       ├── references.bib                   # BibTeX格式参考文献
│       ├── references.json                 # JSON格式参考文献
│       ├── references.md                   # Markdown格式参考文献
│       ├── search_results.bib              # 搜索结果BibTeX格式
│       ├── search_results.json             # 搜索结果JSON格式
│       └── search_results.md               # 搜索结果Markdown格式
├── test_image_tagger/                       # 图像标签工具测试
│   └── docx_img_165.jpeg                   # 测试图像文件
└── test_references/                         # 原始参考文献管理工具测试
    ├── references.md                        # 参考文献文档
    └── test_thesis_reference_manager.py    # 原始功能测试脚本
```

## 测试文件说明

### 1. 增强版参考文献管理工具测试
- **位置**: `test/test_enhanced_reference_manager/`
- **测试脚本**: `test_enhanced_reference_manager.py`
- **功能**: 测试网络搜索、论文详情获取、搜索结果保存等新功能
- **测试数据**: `test_data/` 目录包含各种格式的测试结果

### 2. 原始参考文献管理工具测试
- **位置**: `test/test_references/`
- **测试脚本**: `test_thesis_reference_manager.py`
- **功能**: 测试引用分析、清理、格式转换等基础功能

### 3. 图像标签工具测试
- **位置**: `test/test_image_tagger/`
- **测试文件**: `docx_img_165.jpeg`
- **功能**: 测试图像标签和OCR功能

## 运行测试

### 运行增强版测试
```bash
cd test/test_enhanced_reference_manager
python test_enhanced_reference_manager.py
```

### 运行原始版测试
```bash
cd test/test_references
python test_thesis_reference_manager.py
```

### 安装依赖
```bash
cd test
python install_enhanced_dependencies.py
```

## 测试数据说明

### 搜索测试数据
- **来源**: arXiv API和Semantic Scholar API
- **格式**: JSON、BibTeX、Markdown
- **内容**: 音乐生成、机器学习相关论文

### 引用测试数据
- **来源**: 模拟LaTeX文档
- **格式**: 标准BibTeX格式
- **内容**: 学术论文引用信息

## 注意事项

1. **网络依赖**: 增强版测试需要网络连接
2. **API限制**: 注意API调用频率限制
3. **数据更新**: 测试数据会随API响应变化
4. **文件路径**: 确保在正确的目录下运行测试

## 维护说明

- 定期更新测试数据
- 检查API可用性
- 验证输出格式
- 更新测试用例

