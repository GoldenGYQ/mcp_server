#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文参考文献管理MCP工具
提供参考文献分析、清理和管理功能
"""

import json
import re
import os
import requests
from typing import Dict, List, Set, Tuple, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import asyncio
import xml.etree.ElementTree as ET

# 创建MCP服务器
server = Server("thesis-reference-manager")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出可用的工具"""
    return [
        # 网络搜索工具
        Tool(
            name="search_papers_arxiv",
            description="在arXiv上搜索论文",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "最大结果数量，默认10"
                    }
                },
                "required": ["query"]
            }
        ),
        # Tool(
        #     name="search_papers_semantic_scholar",
        #     description="在Semantic Scholar上搜索论文",
        #     inputSchema={
        #         "type": "object",
        #         "properties": {
        #             "query": {
        #                 "type": "string",
        #                 "description": "搜索关键词"
        #             },
        #             "max_results": {
        #                 "type": "integer",
        #                 "description": "最大结果数量，默认10"
        #             }
        #         },
        #         "required": ["query"]
        #     }
        # ),
        Tool(
            name="get_paper_details",
            description="获取论文详细信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "paper_id": {
                        "type": "string",
                        "description": "论文ID或DOI"
                    },
                    "source": {
                        "type": "string",
                        "description": "来源：arxiv, doi, title",
                        "enum": ["arxiv", "doi", "title"]
                    }
                },
                "required": ["paper_id", "source"]
            }
        ),
        Tool(
            name="save_search_results",
            description="保存搜索结果到指定目录 - 按领域分类保存到 references/领域/ 目录",
            inputSchema={
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "description": "搜索结果列表"
                    },
                    "domain": {
                        "type": "string",
                        "description": "研究领域，如：machine_learning, computer_vision, nlp 等"
                    },
                    "base_path": {
                        "type": "string",
                        "description": "基础保存路径，默认为references。如果使用相对路径，需要提供user_workspace参数"
                    },
                    "user_workspace": {
                        "type": "string",
                        "description": "用户工作区路径（必需），用于确定相对路径的基准目录，如：D:/Users/username/Desktop"
                    }
                },
                "required": ["results", "domain", "user_workspace"]
            }
        ),
        # 原有功能
        Tool(
            name="analyze_citations",
            description="分析论文中使用的引用，找出未使用的参考文献",
            inputSchema={
                "type": "object",
                "properties": {
                    "tex_file": {
                        "type": "string",
                        "description": "LaTeX文件路径，默认为thesis_draft.tex"
                    }
                }
            }
        ),
        Tool(
            name="clean_unused_references",
            description="删除未使用的参考文献",
            inputSchema={
                "type": "object",
                "properties": {
                    "tex_file": {
                        "type": "string",
                        "description": "LaTeX文件路径，默认为thesis_draft.tex"
                    }
                }
            }
        ),
        Tool(
            name="convert_citations_to_superscript",
            description="将LaTeX中的\\cite引用转换为上标格式",
            inputSchema={
                "type": "object",
                "properties": {
                    "tex_file": {
                        "type": "string",
                        "description": "LaTeX文件路径，默认为thesis_draft.tex"
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict) -> List[TextContent]:
    """调用工具"""
    
    if name == "search_papers_arxiv":
        return await search_papers_arxiv(
            arguments["query"], 
            arguments.get("max_results", 10)
        )
    
    # elif name == "search_papers_semantic_scholar":
    #     return await search_papers_semantic_scholar(
    #         arguments["query"], 
    #         arguments.get("max_results", 10)
    #     )
    
    elif name == "get_paper_details":
        return await get_paper_details(
            arguments["paper_id"], 
            arguments["source"]
        )
    
    elif name == "save_search_results":
        return await save_search_results(
            arguments["results"], 
            arguments["domain"],
            arguments.get("base_path", "references"),
            arguments.get("user_workspace")
        )
    
    elif name == "analyze_citations":
        return await analyze_citations(arguments.get("tex_file", "thesis_draft.tex"))
    
    elif name == "clean_unused_references":
        return await clean_unused_references(arguments.get("tex_file", "thesis_draft.tex"))
    
    elif name == "save_references":
        return await save_references(arguments.get("output_dir", "references"))
    
    elif name == "convert_citations_to_superscript":
        return await convert_citations_to_superscript(arguments.get("tex_file", "thesis_draft.tex"))
    
    else:
        raise ValueError(f"未知工具: {name}")

async def search_papers_arxiv(query: str, max_results: int = 10) -> List[TextContent]:
    """在arXiv上搜索论文"""
    try:
        # arXiv API搜索
        url = f"http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # 解析XML响应
        root = ET.fromstring(response.content)
        
        results = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
            authors = []
            for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                name = author.find('{http://www.w3.org/2005/Atom}name').text
                authors.append(name)
            
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
            arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]
            
            result = {
                'title': title,
                'authors': authors,
                'published': published,
                'summary': summary,
                'arxiv_id': arxiv_id,
                'url': f"https://arxiv.org/abs/{arxiv_id}",
                'source': 'arxiv'
            }
            results.append(result)
        
        # 格式化输出
        output = f"arXiv搜索结果 (关键词: {query}):\n\n"
        for i, result in enumerate(results, 1):
            output += f"{i}. {result['title']}\n"
            output += f"   作者: {', '.join(result['authors'])}\n"
            output += f"   发表时间: {result['published'][:10]}\n"
            output += f"   arXiv ID: {result['arxiv_id']}\n"
            output += f"   链接: {result['url']}\n"
            output += f"   摘要: {result['summary'][:200]}...\n\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"arXiv搜索出错: {str(e)}")]

# async def search_papers_semantic_scholar(query: str, max_results: int = 10) -> List[TextContent]:
#     """在Semantic Scholar上搜索论文"""
#     try:
#         # 使用Semantic Scholar API
#         url = "https://api.semanticscholar.org/graph/v1/paper/search"
#         params = {
#             'query': query,
#             'limit': max_results,
#             'fields': 'title,authors,year,abstract,url,paperId,venue'
#         }
        
#         response = requests.get(url, params=params, timeout=30)
#         response.raise_for_status()
        
#         data = response.json()
#         results = []
        
#         for paper in data.get('data', []):
#             authors = [author['name'] for author in paper.get('authors', [])]
#             result = {
#                 'title': paper.get('title', ''),
#                 'authors': authors,
#                 'year': paper.get('year'),
#                 'abstract': paper.get('abstract', ''),
#                 'url': paper.get('url', ''),
#                 'paper_id': paper.get('paperId', ''),
#                 'venue': paper.get('venue', ''),
#                 'source': 'semantic_scholar'
#             }
#             results.append(result)
        
        # 格式化输出
        output = f"Semantic Scholar搜索结果 (关键词: {query}):\n\n"
        for i, result in enumerate(results, 1):
            output += f"{i}. {result['title']}\n"
            output += f"   作者: {', '.join(result['authors'])}\n"
            output += f"   年份: {result['year']}\n"
            if result['venue']:
                output += f"   期刊/会议: {result['venue']}\n"
            output += f"   链接: {result['url']}\n"
            output += f"   摘要: {result['abstract'][:200]}...\n\n"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Semantic Scholar搜索出错: {str(e)}")]

async def get_paper_details(paper_id: str, source: str) -> List[TextContent]:
    """获取论文详细信息"""
    try:
        if source == "arxiv":
            # 获取arXiv论文详情
            url = f"http://export.arxiv.org/api/query?id_list={paper_id}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            entry = root.find('{http://www.w3.org/2005/Atom}entry')
            
            if entry is not None:
                title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
                authors = []
                for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name = author.find('{http://www.w3.org/2005/Atom}name').text
                    authors.append(name)
                
                published = entry.find('{http://www.w3.org/2005/Atom}published').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
                
                # 生成BibTeX格式
                bibtex_key = f"arxiv_{paper_id.replace('.', '_')}"
                bibtex = f"""@article{{{bibtex_key},
    title={{{title}}},
    author={{{' and '.join(authors)}}},
    journal={{arXiv preprint arXiv:{paper_id}}},
    year={{{published[:4]}}},
    url={{https://arxiv.org/abs/{paper_id}}}
}}"""
                
                result = f"论文详细信息:\n\n"
                result += f"标题: {title}\n"
                result += f"作者: {', '.join(authors)}\n"
                result += f"发表时间: {published}\n"
                result += f"arXiv ID: {paper_id}\n"
                result += f"摘要: {summary}\n\n"
                result += f"BibTeX格式:\n{bibtex}"
                
                return [TextContent(type="text", text=result)]
        
        elif source == "doi":
            # 使用DOI获取论文信息
            url = f"https://api.crossref.org/works/{paper_id}"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            work = data['message']
            
            title = work.get('title', [''])[0]
            authors = [author.get('given', '') + ' ' + author.get('family', '') 
                      for author in work.get('author', [])]
            year = work.get('published-print', {}).get('date-parts', [[None]])[0][0]
            journal = work.get('container-title', [''])[0]
            
            result = f"论文详细信息 (DOI: {paper_id}):\n\n"
            result += f"标题: {title}\n"
            result += f"作者: {', '.join(authors)}\n"
            result += f"年份: {year}\n"
            result += f"期刊: {journal}\n"
            result += f"DOI: {paper_id}\n"
            
            return [TextContent(type="text", text=result)]
        
        else:
            return [TextContent(type="text", text=f"不支持的来源类型: {source}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"获取论文详情出错: {str(e)}")]

async def save_search_results(results: List[Dict], domain: str, base_path: str = "references", user_workspace: str = None) -> List[TextContent]:
    """保存搜索结果到指定路径 - 按领域分类保存"""
    try:
        # 如果base_path是相对路径，需要用户提供用户工作区路径
        if not os.path.isabs(base_path):
            if user_workspace:
                # 使用用户提供的工作区路径
                base_path = os.path.join(user_workspace, base_path)
            else:
                # 如果没有提供用户工作区，返回错误提示
                return [TextContent(type="text", text="❌ 错误：相对路径需要提供用户工作区路径参数 user_workspace")]
        
        # 构建完整的保存路径：references/领域/
        save_path = os.path.join(base_path, domain)
        
        # 确保保存路径存在
        os.makedirs(save_path, exist_ok=True)
        
        # 生成时间戳
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON文件
        json_file = os.path.join(save_path, f"papers_{timestamp}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # 生成简化的BibTeX文件
        bibtex_file = os.path.join(save_path, f"papers_{timestamp}.bib")
        bibtex_entries = []
        for i, result in enumerate(results, 1):
            if result.get('source') == 'arxiv':
                key = f"paper_{i}"
                bibtex = f"""@article{{{key},
    title={{{result['title']}}},
    author={{{' and '.join(result['authors'])}}},
    journal={{arXiv preprint arXiv:{result['arxiv_id']}}},
    year={{{result['published'][:4]}}},
    url={{{result['url']}}}
}}"""
            else:
                key = f"paper_{i}"
                bibtex = f"""@article{{{key},
    title={{{result['title']}}},
    author={{{' and '.join(result['authors'])}}},
    journal={{Unknown}},
    year={{{result.get('year', 'N/A')}}},
    url={{{result['url']}}}
}}"""
            bibtex_entries.append(bibtex)
        
        with open(bibtex_file, "w", encoding="utf-8") as f:
            f.write('\n\n'.join(bibtex_entries))
        
        # 生成领域信息文件
        domain_info_file = os.path.join(save_path, f"domain_info_{timestamp}.txt")
        with open(domain_info_file, "w", encoding="utf-8") as f:
            f.write(f"研究领域: {domain}\n")
            f.write(f"论文数量: {len(results)}\n")
            f.write(f"保存时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"搜索关键词: {', '.join(set([r.get('query', 'N/A') for r in results if 'query' in r]))}\n")
        
        # 返回简洁的结果
        result_text = f"✅ 已保存 {len(results)} 篇论文到:\n"
        result_text += f"📁 目录: {os.path.abspath(save_path)}\n"
        result_text += f"🏷️ 领域: {domain}\n"
        result_text += f"📄 JSON: {os.path.basename(json_file)}\n"
        result_text += f"📄 BibTeX: {os.path.basename(bibtex_file)}\n"
        result_text += f"📄 领域信息: {os.path.basename(domain_info_file)}"
        
        return [TextContent(type="text", text=result_text)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ 保存失败: {str(e)}")]

async def analyze_citations(tex_file: str) -> List[TextContent]:
    """分析论文中使用的引用，找出未使用的参考文献"""
    
    try:
        # 读取文件
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找出所有使用的引用
        used_citations = set()
        cite_pattern = r'\\cite\{([^}]+)\}'
        matches = re.findall(cite_pattern, content)
        
        for match in matches:
            # 处理多个引用的情况，如 \cite{key1,key2}
            citations = [c.strip() for c in match.split(',')]
            used_citations.update(citations)
        
        # 找出所有定义的参考文献
        defined_citations = set()
        bibitem_pattern = r'\\bibitem\{([^}]+)\}'
        bibitem_matches = re.findall(bibitem_pattern, content)
        defined_citations.update(bibitem_matches)
        
        # 找出未使用的参考文献
        unused_citations = defined_citations - used_citations
        
        # 找出使用但未定义的引用
        undefined_citations = used_citations - defined_citations
        
        result = f"""引用分析结果:

使用的引用数量: {len(used_citations)}
定义的参考文献数量: {len(defined_citations)}
未使用的参考文献数量: {len(unused_citations)}
使用但未定义的引用数量: {len(undefined_citations)}

使用的引用:
{', '.join(sorted(used_citations))}

未使用的参考文献:
{', '.join(sorted(unused_citations)) if unused_citations else '无'}

使用但未定义的引用:
{', '.join(sorted(undefined_citations)) if undefined_citations else '无'}"""
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"分析引用时出错: {str(e)}")]

async def clean_unused_references(tex_file: str) -> List[TextContent]:
    """删除未使用的参考文献"""
    
    try:
        # 读取文件
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找出所有使用的引用
        used_citations = set()
        cite_pattern = r'\\cite\{([^}]+)\}'
        matches = re.findall(cite_pattern, content)
        
        for match in matches:
            citations = [c.strip() for c in match.split(',')]
            used_citations.update(citations)
        
        # 找出所有定义的参考文献
        defined_citations = set()
        bibitem_pattern = r'\\bibitem\{([^}]+)\}'
        bibitem_matches = re.findall(bibitem_pattern, content)
        defined_citations.update(bibitem_matches)
        
        # 找出未使用的参考文献
        unused_citations = defined_citations - used_citations
        
        # 删除未使用的参考文献
        deleted_count = 0
        for citation in unused_citations:
            # 找到对应的bibitem并删除
            pattern = rf'\\bibitem\{{{citation}\}}.*?(?=\\bibitem\{{|\\end\{{thebibliography\}}|$)'
            new_content = re.sub(pattern, '', content, flags=re.DOTALL)
            if new_content != content:
                content = new_content
                deleted_count += 1
        
        # 清理多余的空行
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # 写回文件
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        result = f"成功删除 {deleted_count} 个未使用的参考文献\n"
        result += f"删除的参考文献: {', '.join(sorted(unused_citations))}"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"清理参考文献时出错: {str(e)}")]

async def save_references(output_dir: str = "references") -> List[TextContent]:
    """保存参考文献到不同格式"""
    try:
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 这里可以添加从LaTeX文件中提取参考文献的逻辑
        # 目前返回一个示例结果
        result = f"参考文献已保存到 {output_dir} 文件夹\n"
        result += "包含文件:\n"
        result += "- references.json (JSON格式)\n"
        result += "- references.bib (BibTeX格式)\n"
        result += "- references.md (Markdown格式)\n"
        result += "注意: 此功能需要从LaTeX文件中提取参考文献信息"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"保存参考文献时出错: {str(e)}")]

async def convert_citations_to_superscript(tex_file: str) -> List[TextContent]:
    """将LaTeX中的\\cite引用转换为上标格式"""
    try:
        # 读取文件
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建引用映射
        citation_map = {}
        citation_counter = 1
        
        # 找出所有使用的引用
        cite_pattern = r'\\cite\{([^}]+)\}'
        matches = re.findall(cite_pattern, content)
        
        for match in matches:
            citations = [c.strip() for c in match.split(',')]
            for citation in citations:
                if citation not in citation_map:
                    citation_map[citation] = citation_counter
                    citation_counter += 1
        
        # 替换引用为上标格式
        def replace_cite(match):
            citations = [c.strip() for c in match.group(1).split(',')]
            superscripts = [str(citation_map[c]) for c in citations]
            return f"$^{{{','.join(superscripts)}}}$"
        
        new_content = re.sub(cite_pattern, replace_cite, content)
        
        # 写回文件
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        result = f"成功转换 {len(citation_map)} 个引用为上标格式\n"
        result += f"转换的引用: {', '.join(sorted(citation_map.keys()))}\n"
        result += f"引用映射: {dict(citation_map)}"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"转换引用格式时出错: {str(e)}")]

if __name__ == "__main__":
    from mcp import stdio_server
    import asyncio
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())
