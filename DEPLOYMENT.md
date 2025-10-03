# 🚀 GitHub发布和本地配置指南

## 第一步：创建GitHub仓库

### 1. 在GitHub上创建新仓库
```bash
# 在GitHub网站上创建新仓库，命名为 "mcp-servers"
```

### 2. 初始化本地Git仓库
```bash
# 在项目目录中执行
git init
git add .
git commit -m "Initial commit: MCP servers collection"
git branch -M main
git remote add origin https://github.com/GoldenYQ/mcp-servers.git
git push -u origin main
```

## 第二步：本地配置MCP客户端

### 方法1：使用Git克隆（推荐）

#### 1. 克隆仓库到本地
```bash
git clone https://github.com/GoldenYQ/mcp-servers.git
cd mcp-servers
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 配置Cursor IDE
编辑 `~/.cursor/mcp.json` 文件：

```json
{
  "mcpServers": {
    "thesis-reference-manager": {
      "command": "python",
      "args": ["D:/path/to/mcp-servers/thesis_reference_manager.py"],
      "env": {
        "PYTHONPATH": "D:/path/to/mcp-servers"
      },
      "description": "论文参考文献管理工具"
    },
    "docx-image-tagger": {
      "command": "python",
      "args": ["D:/path/to/mcp-servers/docx_image_tagger.py"],
      "env": {
        "PYTHONPATH": "D:/path/to/mcp-servers"
      },
      "description": "文档图片标签器"
    },
    "local-image-analyzer": {
      "command": "python",
      "args": ["D:/path/to/mcp-servers/local_image_analyzer.py"],
      "env": {
        "PYTHONPATH": "D:/path/to/mcp-servers"
      },
      "description": "本地图片分析器"
    },
    "hello-server": {
      "command": "python",
      "args": ["D:/path/to/mcp-servers/helloworld.py"],
      "description": "Hello World测试服务器"
    }
  }
}
```

### 方法2：使用pip安装（高级）

#### 1. 创建setup.py
```python
from setuptools import setup, find_packages

setup(
    name="mcp-servers",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-thesis-manager=thesis_reference_manager:main",
            "mcp-docx-tagger=docx_image_tagger:main",
            "mcp-image-analyzer=local_image_analyzer:main",
        ],
    },
)
```

#### 2. 安装到系统
```bash
pip install -e .
```

## 第三步：验证配置

### 1. 重启Cursor IDE
```bash
# 重启Cursor IDE以加载新的MCP配置
```

### 2. 测试MCP服务器
在Cursor中测试：
```
@thesis-reference-manager search_papers_arxiv query="machine learning" max_results=3
```

### 3. 检查日志
如果出现问题，检查Cursor的MCP日志。

## 第四步：更新和维护

### 1. 更新代码
```bash
git pull origin main
```

### 2. 更新依赖
```bash
pip install -r requirements.txt --upgrade
```

### 3. 提交更改
```bash
git add .
git commit -m "Update MCP servers"
git push origin main
```

## 故障排除

### 常见问题

1. **MCP服务器无法启动**
   - 检查Python路径是否正确
   - 确认依赖包已安装
   - 查看错误日志

2. **工具调用失败**
   - 验证参数格式
   - 检查网络连接
   - 确认文件路径存在

3. **权限问题**
   - 确保有文件读写权限
   - 检查目录是否存在

### 调试命令
```bash
# 测试单个MCP服务器
python thesis_reference_manager.py

# 检查依赖
pip list | grep mcp

# 查看Python路径
python -c "import sys; print(sys.path)"
```

## 高级配置

### 使用虚拟环境
```bash
# 创建虚拟环境
python -m venv mcp-env
source mcp-env/bin/activate  # Linux/Mac
# 或
mcp-env\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 在mcp.json中使用虚拟环境的Python路径
```

### 多环境配置
```json
{
  "mcpServers": {
    "thesis-reference-manager-dev": {
      "command": "D:/path/to/dev-env/python.exe",
      "args": ["D:/path/to/mcp-servers/thesis_reference_manager.py"],
      "description": "开发环境"
    },
    "thesis-reference-manager-prod": {
      "command": "D:/path/to/prod-env/python.exe", 
      "args": ["D:/path/to/mcp-servers/thesis_reference_manager.py"],
      "description": "生产环境"
    }
  }
}
```
