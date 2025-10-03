# MCP服务器项目结构

## 项目根目录
```
mcp_servers/
├── thesis_reference_manager.py              # 增强版参考文献管理工具（主文件）
├── local_image_analyzer.py                  # 图像分析工具
├── docx_image_tagger.py                     # 文档图像标签工具
├── helloworld.py                            # 示例MCP工具
├── PROJECT_STRUCTURE.md                     # 项目结构说明（本文件）
├── readme/                                  # 文档目录
│   ├── README_thesis_reference_manager.md   # 原始参考文献管理工具文档
│   ├── README_enhanced_reference_manager.md # 增强版参考文献管理工具文档
│   └── SUMMARY.md                           # 项目总结文档
└── test/                                    # 测试目录
    ├── install_enhanced_dependencies.py     # 增强版依赖安装脚本
    ├── README_test_structure.md             # 测试结构说明
    ├── test_enhanced_reference_manager/     # 增强版参考文献管理工具测试
    │   ├── test_enhanced_reference_manager.py # 增强版功能测试脚本
    │   └── test_data/                        # 测试数据目录
    │       ├── references.bib               # BibTeX格式参考文献
    │       ├── references.json              # JSON格式参考文献
    │       ├── references.md                # Markdown格式参考文献
    │       ├── search_results.bib           # 搜索结果BibTeX格式
    │       ├── search_results.json          # 搜索结果JSON格式
    │       └── search_results.md             # 搜索结果Markdown格式
    ├── test_image_tagger/                   # 图像标签工具测试
    │   └── docx_img_165.jpeg               # 测试图像文件
    └── test_references/                     # 原始参考文献管理工具测试
        ├── references.md                    # 参考文献文档
        └── test_thesis_reference_manager.py # 原始功能测试脚本
```

## 工具功能分类

### 1. 参考文献管理工具
- **主文件**: `thesis_reference_manager.py`
- **功能**: 
  - 网络搜索（arXiv、Semantic Scholar）
  - 论文详情获取
  - 引用分析和管理
  - 多格式输出（JSON、BibTeX、Markdown）
- **测试**: `test/test_enhanced_reference_manager/`

### 2. 图像分析工具
- **主文件**: `local_image_analyzer.py`
- **功能**: 图像分析和OCR
- **测试**: `test/test_image_tagger/`

### 3. 文档图像标签工具
- **主文件**: `docx_image_tagger.py`
- **功能**: 文档图像提取和标签
- **测试**: `test/test_image_tagger/`

### 4. 示例工具
- **主文件**: `helloworld.py`
- **功能**: MCP工具示例

## 测试结构说明

### 增强版参考文献管理工具测试
```
test/test_enhanced_reference_manager/
├── test_enhanced_reference_manager.py  # 主测试脚本
└── test_data/                         # 测试数据
    ├── references.*                   # 参考文献数据
    └── search_results.*               # 搜索结果数据
```

### 原始参考文献管理工具测试
```
test/test_references/
├── test_thesis_reference_manager.py   # 原始功能测试
└── references.md                      # 参考文献文档
```

### 图像工具测试
```
test/test_image_tagger/
└── docx_img_165.jpeg                 # 测试图像文件
```

## 运行测试

### 1. 运行增强版测试
```bash
cd test/test_enhanced_reference_manager
python test_enhanced_reference_manager.py
```

### 2. 运行原始版测试
```bash
cd test/test_references
python test_thesis_reference_manager.py
```

### 3. 安装依赖
```bash
cd test
python install_enhanced_dependencies.py
```

## 文档结构

### 主要文档
- `readme/README_thesis_reference_manager.md` - 原始工具文档
- `readme/README_enhanced_reference_manager.md` - 增强版工具文档
- `readme/SUMMARY.md` - 项目总结
- `test/README_test_structure.md` - 测试结构说明

## 维护说明

1. **测试数据更新**: 定期更新测试数据以反映最新的API响应
2. **依赖管理**: 使用 `install_enhanced_dependencies.py` 管理依赖
3. **文档同步**: 保持文档与代码同步更新
4. **测试验证**: 定期运行测试确保功能正常

## 注意事项

- 增强版工具需要网络连接
- 注意API调用频率限制
- 测试数据会随API响应变化
- 确保在正确的目录下运行测试

