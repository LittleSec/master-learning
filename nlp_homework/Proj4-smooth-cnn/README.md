### 一、问题分析
1. 自然语言通顺与否的判定，即给定一个句子，要求判定所给的句子是否通顺，0通顺，1不通顺。
2. 二分类问题，通顺为正例，不通顺为负例
3. n-gram模型，对句子计算概率，打分从而判断正确与否
4. 一维**cnn**，作用于句子上的卷积滤波器一次学习几个词，并将结果最大化池化来创建一个句子向量。**本次作业采用这个方案**！


### 二、步骤，遇到的问题以及解决方案
1. 分词，用pkuseg库，该库北大的一个开源的中文分词工具包，它在多个分词数据集上都有非常高的分词准确率。
    + 不用jieba分词库的原因：jieba分词库算是中文分词里比较入门级的库，易用性来说对用户很友好，但是对非中文（如数字、英文、其他语言等）分词效果很糟糕，例如`hello world!`则会分成`['hello', ' ', 'world', '!']`，空格也算做词！（不过速度还是jieba快，毕竟jieba返回的是迭代器，pkuseg直接返回列表）
    + 我认为这次作业关注的是中文，因此英文、数字、其他语言（韩文日文等）会转换成一个标签，对应的英文（不仅仅是词，包括英文句子）为`<ENG>`，数字为`<NUM>`，英文数字组合为`<NAE>`，其他语言为`<OTHER>`。
    + 对标点符号的处理分为中文标点和英文标点，和上面一样，统一替换成一个标签`<PUN>`。
    + 从人的角度而言，标点符号应该是有区别的对待，例如逗号和句号，应该分别对待。但是发现训练集对标点好像并不是特别的敏感。例如通顺的句子并非一定以句号感叹号等结尾，也有用逗号结尾，或者没有标点的。因此在此对符号统一处理。
2. 词向量，对分好的词进行词频统计，按照出现次数升序从1开始自增编号，编号作为该词的id，并将中文句子转化成对应的id序列，长度按照最长的句子来，不够长的在前面补0。测试集中未出现在训练集中的词统一用一个id（紧接着编号）。
3. 训练模型，用keras库，参数见代码。


### 三、文件说明
>以下程序都是直接运行即可：`python3 filename.py`
>所有程序运行都会输出运行时间。
1. `preprocess.py`，数据预处理，主要是分词。
    + input: `train.txt` or `test_v3.txt`，需要在代码最后修改要处理的文件
    + output: `pre_train.txt` or `pre_test_v3.txt`，生成分好词的文本，文件名为在输入文件名前加上pre_前缀
2. `fixmodel.py`，生成word-id映射，训练模型。
    + `getIdMapWord()`函数用于生成word-id映射，若存在文件`idmapword.pkl`则从该文件中读取，否则通过分好词的txt中生成并存入`idmapword.pkl`二进制文件中。
    + `trainAndSaveModel(Xtrain, Ytrain)`函数，Xtrain是词向量，Ytrain是对应的标签，通过`getXandY(word2index)`函数生成。该函数用于生成模型，并将模型存储为文件`model1.h5`
    + 总得来说：
        - input: `pre_train.txt`(and `idmapword.pkl`)
        - output: (`idmapword.pkl` and) `model1.h5`
3. `predict.py`，读入模型，并预测
    + input: `model1.h5` and `idmapword.pkl` and `pre_test_v3.txt`
    + output: `MF1833026.txt`
4. 输出文件依赖性，一旦`preprocess.py`预处理的行为发生变化，那么需要删除`idmapword.pkl`，否则运行`fixmodel.py`并不会生成（或覆盖）新的pkl文件。其他输出文件重新运行程序会被覆盖。


### 四、运行环境
1. Windows 10 64-bit
2. no GPU
3. CPU: I7-4790, 4 core, 3.6GHz
4. Memory: 16G
5. Python 3.6.5
6. 文件运行顺序：`preprocess.py`-->`fixmodel.py`-->`predict.py`


### 五、关于成绩
虽然和baseline一样，但是真的不是全1，我的提交里没有一个是全1的提交。