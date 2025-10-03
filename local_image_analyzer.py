#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本地图像分析MCP服务器
使用本地模型和规则进行图像内容理解和标题生成

特点:
1. 无需API密钥，完全本地运行
2. 基于图像特征和OCR的智能分析
3. 支持多种图像类型识别
4. 生成有意义的标题
"""

import os
import base64
import json
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
from mcp.server.fastmcp import FastMCP

# 尝试导入OCR功能
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# 初始化MCP服务器
mcp = FastMCP("local-image-analyzer")

def _get_image_info(image_path: Path) -> Dict:
    """获取图像基本信息"""
    try:
        with Image.open(image_path) as img:
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height,
                "file_size": image_path.stat().st_size
            }
    except Exception as e:
        return {"error": f"Failed to get image info: {e}"}

def _extract_text_with_ocr(image_path: Path) -> str:
    """使用OCR提取图像中的文字"""
    if not OCR_AVAILABLE:
        return ""
    
    try:
        with Image.open(image_path) as img:
            # 尝试中英文OCR
            text = pytesseract.image_to_string(img, lang='chi_sim+eng').strip()
            return text
    except Exception:
        return ""

def _analyze_image_features(image_path: Path) -> Dict:
    """分析图像特征"""
    try:
        image_info = _get_image_info(image_path)
        if "error" in image_info:
            return image_info
        
        width, height = image_info["width"], image_info["height"]
        file_size = image_info["file_size"]
        aspect_ratio = width / height if height > 0 else 1
        
        # 分析图像特征
        features = {
            "aspect_ratio": aspect_ratio,
            "file_size": file_size,
            "resolution": width * height,
            "is_landscape": aspect_ratio > 1.2,
            "is_portrait": aspect_ratio < 0.8,
            "is_square": 0.8 <= aspect_ratio <= 1.2,
            "is_high_res": width > 1000 or height > 1000,
            "is_large_file": file_size > 500000
        }
        
        return features
    except Exception as e:
        return {"error": f"Failed to analyze features: {e}"}

def _classify_image_type(features: Dict, ocr_text: str) -> str:
    """根据特征和OCR文本分类图像类型"""
    aspect_ratio = features.get("aspect_ratio", 1)
    file_size = features.get("file_size", 0)
    ocr_lower = ocr_text.lower()
    
    # 基于OCR文本的分类
    if any(keyword in ocr_lower for keyword in ["证书", "奖状", "奖", "证书", "certificate", "award"]):
        return "证书/奖状"
    elif any(keyword in ocr_lower for keyword in ["营业执照", "许可证", "执照", "license", "permit"]):
        return "营业执照/许可证"
    elif any(keyword in ocr_lower for keyword in ["合同", "协议", "contract", "agreement"]):
        return "合同/协议"
    elif any(keyword in ocr_lower for keyword in ["身份证", "护照", "证件", "id", "passport"]):
        return "身份证件"
    elif any(keyword in ocr_lower for keyword in ["发票", "收据", "invoice", "receipt"]):
        return "发票/收据"
    elif any(keyword in ocr_lower for keyword in ["报告", "报告", "report", "analysis"]):
        return "报告/分析"
    
    # 基于图像特征分类
    if aspect_ratio > 1.5:
        if file_size > 1000000:  # 大于1MB
            return "横向文档/图表"
        else:
            return "横向图像"
    elif aspect_ratio < 0.7:
        return "纵向文档"
    elif 0.8 <= aspect_ratio <= 1.2:
        if file_size > 500000:
            return "方形图像/照片"
        else:
            return "方形图像"
    else:
        return "一般图像"

def _generate_smart_title(image_type: str, ocr_text: str, features: Dict, context: str = "") -> str:
    """生成智能标题"""
    if not ocr_text.strip():
        # 没有OCR文本，基于特征生成标题
        if features.get("is_landscape"):
            return f"横向{image_type}"
        elif features.get("is_portrait"):
            return f"纵向{image_type}"
        else:
            return f"方形{image_type}"
    
    # 有OCR文本，提取关键信息
    ocr_lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    
    if image_type == "证书/奖状":
        # 提取证书关键信息
        for line in ocr_lines:
            if "奖" in line or "证书" in line:
                return line[:30]  # 限制长度
        return "证书/奖状"
    
    elif image_type == "营业执照/许可证":
        # 提取公司名称或许可证信息
        for line in ocr_lines:
            if "公司" in line or "有限" in line or "股份" in line:
                return line[:30]
        return "营业执照/许可证"
    
    elif image_type == "合同/协议":
        # 提取合同标题
        for line in ocr_lines:
            if "合同" in line or "协议" in line:
                return line[:30]
        return "合同/协议"
    
    else:
        # 使用第一行有意义的文本
        for line in ocr_lines:
            if len(line) > 5:  # 过滤太短的文本
                return line[:30]
        
        # 如果没有合适的文本，使用类型
        return image_type

def _extract_keywords(image_type: str, ocr_text: str, features: Dict) -> List[str]:
    """提取关键词"""
    keywords = [image_type]
    
    # 基于图像特征添加关键词
    if features.get("is_landscape"):
        keywords.append("横向")
    elif features.get("is_portrait"):
        keywords.append("纵向")
    else:
        keywords.append("方形")
    
    if features.get("is_high_res"):
        keywords.append("高清")
    
    if features.get("is_large_file"):
        keywords.append("大文件")
    
    # 从OCR文本中提取关键词
    if ocr_text:
        ocr_lower = ocr_text.lower()
        important_keywords = [
            "证书", "奖状", "奖", "营业执照", "许可证", "合同", "协议",
            "身份证", "护照", "发票", "收据", "报告", "分析"
        ]
        
        for keyword in important_keywords:
            if keyword in ocr_lower:
                keywords.append(keyword)
    
    return keywords

def _analyze_image_comprehensive(image_path: Path, context: str = "") -> Dict:
    """综合分析图像"""
    try:
        # 获取基本信息
        image_info = _get_image_info(image_path)
        if "error" in image_info:
            return image_info
        
        # 分析特征
        features = _analyze_image_features(image_path)
        if "error" in features:
            return features
        
        # OCR文本提取
        ocr_text = _extract_text_with_ocr(image_path)
        
        # 图像类型分类
        image_type = _classify_image_type(features, ocr_text)
        
        # 生成标题
        suggested_title = _generate_smart_title(image_type, ocr_text, features, context)
        
        # 提取关键词
        keywords = _extract_keywords(image_type, ocr_text, features)
        
        # 计算置信度
        confidence = 0.5  # 基础置信度
        if ocr_text.strip():
            confidence += 0.3  # 有OCR文本增加置信度
        if image_type != "一般图像":
            confidence += 0.2  # 能明确分类增加置信度
        
        confidence = min(confidence, 1.0)  # 限制在1.0以内
        
        return {
            "image_type": image_type,
            "main_content": ocr_text[:100] if ocr_text else f"图像尺寸: {image_info['width']}x{image_info['height']}",
            "suggested_title": suggested_title,
            "keywords": keywords,
            "confidence": confidence,
            "analysis_details": f"基于图像特征和OCR文本的综合分析，图像类型: {image_type}",
            "ocr_text": ocr_text,
            "features": features,
            "method": "local_comprehensive"
        }
        
    except Exception as e:
        return {"error": f"Comprehensive analysis failed: {e}"}

@mcp.tool()
def analyze_single_image(image_path: str, user_working_dir: str, context: str = "") -> Dict:
    """分析单个图像并生成标题
    
    Args:
        image_path: 图像文件路径
        user_working_dir: 用户工作目录
        context: 上下文信息
    
    Returns:
        dict: 分析结果
    """
    try:
        # 路径处理
        base_dir = Path(user_working_dir)
        if not base_dir.exists():
            return {"error": f"User working directory not found: {user_working_dir}"}
        
        if Path(image_path).is_absolute():
            img_path = Path(image_path)
        else:
            img_path = base_dir / image_path
        
        if not img_path.exists():
            return {"error": f"Image file not found: {image_path}"}
        
        # 检查文件格式
        if img_path.suffix.lower() not in [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp"]:
            return {"error": f"Unsupported image format: {img_path.suffix}"}
        
        # 分析图像
        analysis_result = _analyze_image_comprehensive(img_path, context)
        
        if "error" in analysis_result:
            return analysis_result
        
        # 获取图像基本信息
        image_info = _get_image_info(img_path)
        
        return {
            "success": True,
            "file_path": str(img_path),
            "file_name": img_path.name,
            "image_info": image_info,
            "analysis": analysis_result,
            "ocr_available": OCR_AVAILABLE,
            "message": f"Successfully analyzed image: {img_path.name}"
        }
        
    except Exception as e:
        return {"error": f"Failed to analyze image: {e}"}

@mcp.tool()
def batch_analyze_images(image_dir: str, user_working_dir: str, context: str = "") -> Dict:
    """批量分析目录中的图像"""
    try:
        # 路径处理
        base_dir = Path(user_working_dir)
        if not base_dir.exists():
            return {"error": f"User working directory not found: {user_working_dir}"}
        
        if Path(image_dir).is_absolute():
            dir_path = Path(image_dir)
        else:
            dir_path = base_dir / image_dir
        
        if not dir_path.exists():
            return {"error": f"Directory not found: {image_dir}"}
        if not dir_path.is_dir():
            return {"error": f"Not a directory: {image_dir}"}
        
        # 支持的图像格式
        supported_formats = [".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp"]
        
        # 分析所有图像
        results = []
        for img_file in sorted(dir_path.iterdir()):
            if not img_file.is_file():
                continue
            if img_file.suffix.lower() not in supported_formats:
                continue
            
            try:
                # 分析单个图像
                analysis_result = _analyze_image_comprehensive(img_file, context)
                image_info = _get_image_info(img_file)
                
                results.append({
                    "file_path": str(img_file),
                    "file_name": img_file.name,
                    "image_info": image_info,
                    "analysis": analysis_result,
                    "success": "error" not in analysis_result
                })
                
            except Exception as e:
                results.append({
                    "file_path": str(img_file),
                    "file_name": img_file.name,
                    "error": str(e),
                    "success": False
                })
        
        return {
            "success": True,
            "directory": str(dir_path),
            "total_images": len(results),
            "successful_analyses": len([r for r in results if r.get("success", False)]),
            "results": results,
            "ocr_available": OCR_AVAILABLE,
            "message": f"Analyzed {len(results)} images in {dir_path}"
        }
        
    except Exception as e:
        return {"error": f"Failed to batch analyze images: {e}"}

@mcp.tool()
def generate_smart_titles(image_dir: str, user_working_dir: str, title_style: str = "descriptive") -> Dict:
    """为图像生成智能标题"""
    try:
        # 先批量分析图像
        analysis_result = batch_analyze_images(image_dir, user_working_dir)
        
        if "error" in analysis_result:
            return analysis_result
        
        # 生成标题建议
        title_suggestions = []
        for result in analysis_result["results"]:
            if not result.get("success", False):
                continue
            
            analysis = result.get("analysis", {})
            file_name = result["file_name"]
            
            # 根据风格生成标题
            if title_style == "descriptive":
                suggested_title = analysis.get("suggested_title", file_name)
            elif title_style == "concise":
                main_content = analysis.get("main_content", file_name)
                suggested_title = main_content[:20] if main_content else file_name
            else:  # formal
                image_type = analysis.get("image_type", "图像")
                suggested_title = f"{image_type}_{analysis.get('suggested_title', 'unknown')}"
            
            # 清理标题中的特殊字符
            clean_title = "".join(c for c in suggested_title if c.isalnum() or c in " -_")
            clean_title = clean_title.strip()
            
            title_suggestions.append({
                "original_file": file_name,
                "suggested_title": clean_title,
                "image_type": analysis.get("image_type", "未知"),
                "confidence": analysis.get("confidence", 0.0),
                "keywords": analysis.get("keywords", []),
                "ocr_text": analysis.get("ocr_text", ""),
                "method": "local_comprehensive"
            })
        
        return {
            "success": True,
            "title_style": title_style,
            "total_suggestions": len(title_suggestions),
            "suggestions": title_suggestions,
            "ocr_available": OCR_AVAILABLE,
            "message": f"Generated {len(title_suggestions)} smart title suggestions"
        }
        
    except Exception as e:
        return {"error": f"Failed to generate smart titles: {e}"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
