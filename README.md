# SSPanelBomb
![logo](https://pic.rmb.bdstatic.com/bjh/f52f22e8921d1b3e6787ae1a6b0aa196.png)

## 简介
一款用于SSPanel面板的压力测试脚本，支持多种常见接口。  
**仅供学习测试之用，请勿用于恶意攻击！**

## 特性
- 简单易懂的配置
- 方便的修改请求时的HttpHeader数据
- 支持设置自定义延迟/超时时间
- 详细的工作状态显示
- 支持http/s代理
- 在Linux/Windows上均测试可用

目前支持对以下接口进行压力测试：

- 注册接口
- 邮件接口

未来预计会增加更多模式。

## 依赖
脚本依赖以下程序：
- Python3
- pip(用于安装requests模块)
- requests

仅需安装上述依赖即可工作。

## 使用
在你的VPS或任何支持Python的设备上安装python3并使用pip安装依赖的模块，

然后下载脚本，用任意文本编辑器打开`sspbomb.py`，按照注释中的说明设置目标url和其他参数最后运行脚本即可！

如需使用代理ip特性，需要准备可用的http/s代理，在脚本同目录下新建`ip.txt`，将你的代理写入此文件即可。

**Tips：设置更低的延迟和多开脚本可造成更大的压力，但您的IP可能会更容易被目标的WAF/CDN规则封禁！**

## 更新
- V1：支持对邮件接口请求，并支持http/s代理
- V2：支持对注册接口请求
- V2.5: 重构代码，两个模式均支持使用代理
