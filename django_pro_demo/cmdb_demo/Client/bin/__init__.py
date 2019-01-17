#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2019/1/15
"""启动脚本的所在目录"""

dic = {
    "ram": [
        {
            "solt": "DIMM0",
            "capacity": 4,
            "manufacturer": "Samsung",
            "sn": "178EA60D"
        },
        {
            "solt": "DIMM2",
            "capacity": 4,
            "manufacturer": "Samsung",
            "sn": "67557876"
        }
    ],
}
ram_size = 0
for x in dic.get('ram'):
    ram_size += x.get('capacity')
print(ram_size)

