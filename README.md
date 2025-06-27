### 说明

用于获取 Steam 游戏评论

### 环境信息

**1.** 使用的 Python 版本：Python 3.13.5
**2.** 第三方依赖
| 类型 | 名称 |
| -------- | ------------------ |
| Python 包 | selenium |
| 外部程序 | Chrome for Testing |
| 外部程序 | ChromeDriver |

**3.** 其他环境依赖
能够畅通访问 steamcommunity.com

### 结果储存：

**文件名**

1. \<GameName\> - \<GameAppId\>.csv（csv 文件）
1. \<GameName\> - \<GameAppId\>.db（sqlite 文件）

**表结构**
| 字段名 | 说明 | 类型 |
| ------------- | ---------------------- | ------------------------------ |
| author | 评测作者名 | 字符串 |
| posted_date | 评测时间 | 格式为“xxxx 年 xx 月 xx 日”的字符串 |
| played_hours | 游玩时间 | 浮点数 |
| helpful_count | 觉得此评测有价值的人数 | 整数 |
| is_recommend | 是否推荐 | 整数（1=推荐，0=不推荐） |
| main_content | 评测文本 | 字符串 |

### 代码文件说明

| 文件名               | 作用简述                       |
| -------------------- | ------------------------------ |
| GameReview.py        | 游戏评测的模型类               |
| GameReviewFetcher.py | 主类，用于爬取游戏评论         |
| StorageHelper.py     | 用于保存抓取结果至文件的工具类 |
| ConsoleHelper.py     | 用于打印控制台信息工具类       |
| \_\_main\_\_.py      | 程序入口                       |

### 使用方法

查看并修改\_\_main\_\_.py 文件，并在\_\_main\_\_.py 所在的目录运行

```shell
python __main__.py
```

### 性能信息

1. 速率：约 ? 条评论/秒<del>（懒得测，纯占位）</del>

### 附加地址：

1. Chrome for Testing 及 ChromeDriver 下载: https://googlechromelabs.github.io/chrome-for-testing/
