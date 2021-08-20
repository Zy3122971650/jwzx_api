# 辽宁工程技术大学教务在线API

提供一组辽宁工程技术大学教务在线的API，让大家可以方便的构建自己的教务在线软件，以在享受便利的同时保护自己的信息。

## 为什么做这个

因为工大Plus小程序拿我的分数信息做了专业、学校的排名...

所以我萌生了做一个自己的获取教务在线信息的软件的想法。并且给广大同学提供可被审查，安全食用的API。

## 使用
安装依赖`pip install -r requirements.txt`

在你的脚本中导入jwzx，开始使用

    from jwzx import JWZX

## API手册

参考[`/docs/api.md`](docs/api.md)

## 参与贡献

参考[`/docs/contribute.md`](docs/api.md)

## 特性

- [x] 获取课程信息
- [x] 获取考试安排信息
- [x] 获取考试成绩信息
- [x] 计算GAP
- [x] 学籍信息
- [x] 空闲教室查询

## TODO
- [ ] 构建成pip包的形式