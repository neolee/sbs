# 智能书籍标准 1.1

## 变更历史

### Version 1.0 (2025-09-20)

- 初始版本发布，定义了基本的书籍结构和核心语法扩展。

### Version 1.1 (2025-12-15)

- 书籍目录 `toc.yaml` 文件支持更灵活的章节结构。
- 更标准、更灵活的扩展语法架构设计。

## 概述

智能书籍标准（*SBS*）是智能学习平台（*SLP*）开发使用并开源的新一代数字书籍格式标准，该标准遵循开放、易于扩展和面向智能化未来的设计理念，充分利用现有技术标准，最大限度满足各种不同应用场景的需要。

## 基本结构

本标准定义的“书”是一个自解释的目录，里面包含书的四个组成部分：**元数据**、**目录结构定义**、**正文文件**和**附加资源文件**。

### 元数据和目录结构定义

元数据和目录结构定义置于根目录下的 `toc.yaml` 文件内，遵循 [YAML](https://yaml.org/) 文件格式标准。

下面是 `toc.yaml` 文件的内容结构：

```yaml
book_name: "编程思维与实践"
book_author: "DL4ALL"
book_introduction: "为零基础人士准备的编程思维与实践入门教材"

chapters:
  - name: "前言"
    path: 00/README.md
  - name: "第一章 基础篇"
    chapters:
      - name: "理解编程语言"
        path: 01/01.md
      - name: "程序的基本结构"
        path: 01/02.md
      - name: "理解对象与类"
        path: 01/03.md
  - name: "第二章 进阶篇"
    chapters:
      - name: "函数定义再探"
        path: 02/01.md
      - name: "程序中的模块与文档"
        path: 02/02.md
      - name: "数据容器"
        chapters:
        - name: "列表与元组"
          path: 02/03-1.md
        - name: "字典与集合"
          path: 02/03-2.md
      - name: "自定义数据类型"
        path: 02/04.md
...
```

其中：

- `book_name`：书名，必须字段；
- `book_author`：作者名，可选字段，如无则会将创建本书的用户视为作者；
- `book_introduction`：简要介绍，可选字段，目前只支持纯文本；
- `chapters`：书的目录结构，下面是若干**章**（`chapter`）的列表，每个 `chapter`：
  - 必须包含 `name` 字段，代表章的标题，仅用于目录展示，不会出现在正文展示中；
  - 可以包含 `path` 字段，代表该章对应的正文文件路径（相对路径），这代表该章没有子节；
  - 否则，就必须包含 `chapters` 字段，代表该章下的子章节列表；
- 每个 `path` 字段对应一个 `.md` 文件，通过相对路径引用具体的 `.md` 文件，具体目录结构和位置可由作者自行组织。

### 正文文件

一组由作者组织和命名的 Markdown 格式（`.md`）文本文件，其相对路径可由 `toc.yaml` 文件自行定制。

这些文件的内容遵循本标准定义的格式，这是一种基于 Markdown 标准扩展的文本格式，详见下面相关章节描述。

### 附加资源文件

在正文中用到的各种附加资源文件（图片、音频/视频文件、数据文件等），置于 `assets` 子目录下，此目录下可以依作者的设计建立子目录，正文中使用正确的相对路径引用相应资源文件即可。

正文中包含的可运行程序代码也可以使用这些附加资源文件。

## SBS 语法

SBS 语法基于现有 Markdown 标准并添加了扩展，具有以下特点：

- 支持所有 Markdown 标准元素；
- 兼容 CommonMark 的扩展元素。

在此基础上，SBS 提供一致、简洁且符合 Markdown 原生习惯的三种扩展语法，分别是：
1. **围栏代码块** *fenced code blocks*，也称为**组件块** *widget block*；
2. **容器** *containers*；
3. **属性** *attributes*。

### 1. 组件块 *widget blocks*

用于嵌入富交互组件（如棋牌、图表、互动小程序等），使用带有特定语言标识符的围栏代码块，语法如下：
````markdown
```sbs-<component>
<configuration/data>
```
````

**示例** 嵌入 Bridge 牌局组件：
````markdown
```sbs-bridge
[Event "World Cup"]
[Deal "N:AKQ..."]
```
````

### 2. 布局容器 *layout containers*

用于控制内容的布局结构（如左右对照、多栏排版等），使用 `:::` 包裹的容器语法：
```markdown
::: sbs-<layout>
<content>
:::
```

**示例** 与特定文本对照浮动显示的 widget：
````markdown
::: sbs-sticky
```sbs-bridge
...
```
这里是针对该牌局的分析文字...
:::
````

### 3. 属性修饰 *attributes*

用于对标准 Markdown 元素（如图片、代码块）进行参数修饰，使用 `{}` 包裹的属性语法：
```markdown
![alt](src){ key=value }
```

````markdown
```lang { key=value } 
...
```
````

## 内建功能

本节列出 SBS 内建支持的一些功能。

### 可运行代码块

*语法类型：属性修饰*

通过给代码块添加 `{ runnable=true }` 属性来实现。

**示例**
````markdown
```python { runnable=true }
println("Hello world!")
```
````

`runnable` 属性设置为 `true` 表示该代码块是可以编辑并可运行的，前提是所使用的 SLP 实现支持该语言的代码执行功能。

### 图片显示属性

*语法类型：属性修饰*

通过给图片元素添加 `{ align=..., scale=..., width=..., height=... }` 属性来实现。

**示例**
```markdown
![beautiful pic](https://images.com/pic.jpg){ align=center, width=300 }
```

支持的参数包括（均为可选）：
- `align`：图片对齐，可以取值 `left` `center` `right`，分别实现图片的靠左、居中和靠右对齐；
- `scale`：图片缩放比例，可以取大于 0 的浮点数值，为图片显示的缩放比率；
- `width`, `height`：指定图片显示的宽和高像素（*pixel*）值，可以取大于0的整数值，注意：
  - 如果前面指定了 `scale` 参数，此二参数会被忽略；
  - 如果只指定了此二参数之一，图片会按指定的宽或高以及图片原始宽高比缩放显示；
  - 如果同时指定了此二参数，图片会按指定的宽和高像素值显示，而忽略图片的原宽高比。

## 标准扩展

由项目 [sbs-ext](https://github.com/neolee/sbs-ext) 提供的扩展语法，包含更多高级功能和自定义扩展。

目前该项目支持的扩展语法包括：

*TBD*