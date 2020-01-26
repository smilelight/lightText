# lightText
文本处理相关库，目前包括新词发现等功能。

## 功能

1. 新词发现

## 安装

```bash
pip install lightText
```
建议使用国内源来安装，如使用以下命令：

```bash
pip install -i https://pypi.douban.com/simple/ lightText
```

## 使用

### 1.新词发现

#### 使用示例

```python
from pprint import pprint

from lighttext import NewWordDetector

detector = NewWordDetector()
detector.load_file('new_word/test_new_word3.txt')
pprint(detector.get_top_k(10))
```

其中，文本内容如下：

```text
知识图谱（Knowledge Graph），在图书情报界称为知识域可视化或知识领域映射地图，是显示知识发展进程与结构关系的一系列各种不同的图形，用可视化技术描述知识资源及其载体，挖掘、分析、构建、绘制和显示知识及它们之间的相互联系。
知识图谱是通过将应用数学、图形学、信息可视化技术、信息科学等学科的理论与方法与计量学引文分析、共现分析等方法结合，并利用可视化的图谱形象地展示学科的核心结构、发展历史、前沿领域以及整体知识架构达到多学科融合目的的现代理论。它能为学科研究提供切实的、有价值的参考。
具体来说，知识图谱是通过将应用数学、图形学、信息可视化技术、信息科学等学科的理论与方法与计量学引文分析、共现分析等方法结合，并利用可视化的图谱形象地展示学科的核心结构、发展历史、前沿领域以及整体知识架构达到多学科融合目的的现代理论。它把复杂的知识领域通过数据挖掘、信息处理、知识计量和图形绘制而显示出来，揭示知识领域的动态发展规律，为学科研究提供切实的、有价值的参考。迄今为止，其实际应用在发达国家已经逐步拓展并取得了较好的效果，但它在我国仍属研究的起步阶段。
```

执行结果如下所示：

```bash
[('知识_图谱', 0.4920544676085099),
 ('可视化_技术', 0.4818782843526798),
 ('计量学_引文', 0.4262552853165825),
 ('知识_领域', 0.3902233812935824),
 ('共现_分析', 0.389030837989985),
 ('信息_可视化', 0.33426621501923115),
 ('利用_可视化', 0.3324330079992808),
 ('图谱_形象', 0.3301218104431901),
 ('引文_分析', 0.3267139032681375),
 ('知识_架构', 0.30243479556626457)]
```

## 参考

### NLP

1. [基于互信息和左右信息熵的短语提取识别-码农场](https://www.hankcs.com/nlp/extraction-and-identification-of-mutual-information-about-the-phrase-based-on-information-entropy.html)
2. [互联网时代的社会语言学：基于SNS的文本数据挖掘 | Matrix67: The Aha Moments](http://www.matrix67.com/blog/archives/5044)
3. [python3实现互信息和左右熵的新词发现 - 简书](https://www.jianshu.com/p/e9313fd692ef)

### 源码

1. [xylander23/New-Word-Detection: 新词发现算法(NewWordDetection)](https://github.com/xylander23/New-Word-Detection)
2. [zhanzecheng/Chinese_segment_augment: python3实现互信息和左右熵的新词发现](https://github.com/zhanzecheng/Chinese_segment_augment)

### Python

1. [Can't pickle local object 'DataLoader.__init__.<locals>.<lambda>' - vision - PyTorch Forums](https://discuss.pytorch.org/t/cant-pickle-local-object-dataloader-init-locals-lambda/31857)
2. [python3.X中pickle类的用法（cPickle模块移除了）_python,pickle_lanqiu5ge的专栏-CSDN博客](https://blog.csdn.net/lanqiu5ge/article/details/25136909)
3. [python - copy.deepcopy vs pickle - Stack Overflow](https://stackoverflow.com/questions/1410615/copy-deepcopy-vs-pickle)
4. [Python中collections.defaultdict()使用 - 简书](https://www.jianshu.com/p/26df28b3bfc8)

### 数据结构

1. [Trie树（字典树）](https://github.com/zhanzecheng/The-Art-Of-Programming-By-July/blob/master/ebook/zh/06.09.md)

## 打赏

如果该项目对您有所帮助，欢迎打赏~

![UTOOLS1578660899400.jpg](https://lightsmile-img.oss-cn-beijing.aliyuncs.com/UTOOLS1578660899400.jpg)




