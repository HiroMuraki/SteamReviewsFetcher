### 说明
用于获取Steam游戏评论

### 环境信息
**1.** 使用的Python版本：Python 3.13.0
**2.** 第三方依赖
| 类型     | 名称               |
| -------- | ------------------ |
| Python包 | seleinum           |
| 外部程序 | Chrome for Testing |
| 外部程序 | ChromeDriver       |

**3.** 其他环境依赖
能够畅通访问 steamcommunity.com

### 结果储存：
**文件名**
1. \<GameName\> - \<GameAppId\>.csv（csv文件）
1. \<GameName\> - \<GameAppId\>.db（sqlite文件）
   
**表结构**
| 字段名        | 说明                   | 类型                           |
| ------------- | ---------------------- | ------------------------------ |
| author        | 评测作者名             | 字符串                         |
| posted_date   | 评测时间               | 格式为“xxxx年xx月xx日”的字符串 |
| played_hours  | 游玩时间               | 浮点数                         |
| helpful_count | 觉得此评测有价值的人数 | 整数                           |
| is_recommend  | 是否推荐               | 整数（1=推荐，0=不推荐）       |
| main_content  | 评测文本               | 字符串                         |

### 代码文件说明
| 文件名               | 作用简述                       |
| -------------------- | ------------------------------ |
| AsyncHelper.py       | 用于并发执行的工具类           |
| ElementExtractor.py  | 用于从HTML中抽取所需字段       |
| GameReview.py        | 游戏评测的模型类               |
| GameReviewFetcher.py | 主类，用于爬取游戏评论         |
| StorageHelper.py     | 用于保存抓取结果至文件的工具类 |
| ConsoleHelper.py     | 用于打印控制台信息工具类       |
| main.py              | 程序入口                       |


### 使用方法
查看并修改main.py文件，并在main.py所在的目录运行
```shell
python main.py
```


### 性能信息
1. 速率：约5条评论/秒<del>（懒得优化了）</del>

### 附加地址：
1. Chrome for Testing及ChromeDriver下载: https://googlechromelabs.github.io/chrome-for-testing/

