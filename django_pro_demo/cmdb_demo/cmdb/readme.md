### CMDB开发日志
> 需求分析，表设计，创建项目
- 1、date:20190114
- 2、分析资产的类型，及资产之间的关系
- 3、创建项目、数据库、模型创建、数据库迁移

> 开发客户端数据收集工具
- 1、date:20190115~20190116
- 2、创建客户端项目目录结构
```python
Client/
├── bin
│   └── __main.py__
├── conf
│   └── __settings.py__
├── core
    ├── __handler.py__
    ├── __info_collection.py__
├── log
└── plugins
    ├── linux
        └── __sys_info.py__
    └── windows
        └── __sys_info.py__
```
- 3、开发收集windows系统数据，基于win32com,vmi之python模块

- 4、开发收集Linux系统数据【20190116】，
基于subprocess模块，执行操作系统命令，返回结果，
基于redhat-lsb及dmidecode之rpm模块，
基于/proc/cpuinfo文件收集cpu信息，
基于/proc/meminfo文件收集内存信息，
基于ifconfig -a 命令收集网络信息，
基于fdisk -l 命令收集硬盘信息

> 开发资产审核区资产
- 1、date:20190117
- 2、运用orm中create_or_update(id=,defaults=dict)方法，在待审核区，根据对资产进行更新或创建
