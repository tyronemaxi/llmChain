#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: setup.py
Time: 2024/9/1
"""
from setuptools import setup, find_packages

# 读取 README 文件内容作为 long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llmchain",  # 包名称
    version="0.1.0",  # 版本号
    author="tyrone",  # 作者名称
    author_email="tyronextian@gmail.com",  # 作者邮箱
    description="llm clinet for openai",  # 简短描述
    long_description=long_description,  # 从 README.md 获取详细描述
    long_description_content_type="text/markdown",  # 长描述的内容类型
    url="https://github.com/tyronemaxi/llmChain.git",  # 项目的GitHub仓库地址
    packages=find_packages(),  # 自动找到项目中的所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 使用的许可证类型
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.13',  # 兼容的Python版本
    install_requires=[
        "requests",  # 你的包依赖的其他库
        "httpx",  # 例如，httpx
        "ujson",  # 例如，ujson
    ]
)
