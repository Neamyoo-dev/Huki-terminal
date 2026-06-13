<!-- Best_README_template -->

# Huki terminal
<div align="center">
  <img src="icons/logo.png" alt="Logo" width="120" height="120">
</div>

A GUI terminal by Python3.

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<br />

<p align="center">
  <h3 align="center">最不像win11终端的terminal</h3>
  <p align="center">
    您可以通过目录中的信息来使用它。
    <br />
    <br />
    <a href="https://github.com/Neamyoo-dev/Huki">查看本仓库</a>
    ·
    <a href="https://github.com/Neamyoo-dev/Huki/issues">报告 Bug 或提出特性</a>
    ·
    <a href="https://github.com/Neamyoo-dev/Huki/pulls">提出拉取请求</a>
</p>

## 目录

- [目录](#目录)
- [与python-cmd的区别](#与python-cmd的区别)
- [计划](#计划)
- [上手指南](#上手指南)
- [文件说明](#文件说明)
- [作者](#作者)

### 与[python-cmd](https://github.com/CodeCrafter-TL/python-cmd)的区别
- 更快的更新速度
- 更好的代码结构
- 更好的代码注释

### 计划
- [ ] 增加更多的命令
- [x] 增加插件支持
- [ ] 增加更多的功能
- [ ] 更好的ui
- [x] 添加日志

### 上手指南
1. 在 GitHub 中下载最新的 [Release](https://github.com/Neamyoo-dev/Huki/releases) 。

2. 在工作目录中执行如下命令:
```bash
git clone https://github.com/Neamyoo-dev/Huki.git
```
#### 安装必需包
在 clone 之后的工作目录中执行如下命令:
```bash
pip install -r requirements.txt
```
如果安装较慢，可以使用如下命令切换为阿里云镜像:
```bash
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
```
等待安装完成后，使用如下命令即可开始使用 Huki cmd:
```bash
python main.py
```

### 文件说明

```
Huki-main
├── Events
│   ├── CustomPlainTextEdit.py
│   └── Event.py
├── Value
│   ├── constants.py
│   └── data.py
|── utils
│   ├── Logger_utils.py
│   └── thread_utils.py
├── README.md
├── LICENSE.txt
├── ui.py
├── main.py
```
> `README.md`: 您正在阅读的帮助文档

> `LICENSE.txt`: 关于此项目的 MIT License 信息

> `ui.py`: 由 PyQt5 UI code generator 生成的 UI 代码

> `main.py`: 主程序文件

> `constants.py`: 必需的程序字符串信息

### 作者

![github](https://img.shields.io/badge/GitHub-Neamyoo-dev-green?logo=github)

*您也可以在贡献者名单中参看所有**参与该项目的开发者**。*

### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](https://github.com/Neamyoo-dev/Huki/LICENSE.txt)

[contributors-shield]: https://img.shields.io/github/contributors/Neamyoo-dev/Huki.svg?style=square
[contributors-url]: https://github.com/Neamyoo-dev/Huki/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Neamyoo-dev/Huki.svg?style=square
[forks-url]: https://github.com/Neamyoo-dev/Huki/network/members
[stars-shield]: https://img.shields.io/github/stars/Neamyoo-dev/Huki.svg?style=square
[stars-url]: https://github.com/Neamyoo-dev/Huki/stargazers
[issues-shield]: https://img.shields.io/github/issues/Neamyoo-dev/Huki.svg?style=square
[issues-url]: https://img.shields.io/github/issues/Neamyoo-dev/Huki.svg
[license-shield]: https://img.shields.io/github/license/Neamyoo-dev/Huki.svg?style=square
[license-url]: https://github.com/Neamyoo-dev/Huki/blob/master/LICENSE.txt
