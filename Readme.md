声明：本项目是基于GPTFuzz项目在其基础上进行改进并且在OpenManus上进行实际防护应用。在OpenManus部分的代码本项目完全引用，
其次GPTFuzzer部分的代码，本项目在app/qwfuzzer/mutator_check.py中部分引用了原项目变异方法的代码，其他均为原创。

众所周知，OpenManus基于Manus强大的权力而暴露出了相当多的安全问题，本项目旨在解决提示词注入方向的提示词攻击的问题。
基于模糊测试的思想并且借鉴了GPTFuzzer项目中变异的方法，并在GPTFuzzer的基础上进行改进，由于本项目采用qwen-plus-character
作为编译器，因此我取名叫qwfuzzer。创新性的引入了黑名单机制，黑名单上会持久性的保存各种越狱提示词，而同一类型越狱提示词通过
变异的方式可以尽可能的找出所有相关的变式，然后保存在黑名单中，同时在判断越狱提示词的效果方面我们通过DeepSeek-v3-0324进行
提示词是否越狱的判断，从而实现黑名单的动态更新。并且我们在最终的输入阶段引入了黑名单+大模型的双重防护策略。首先黑名单机制通
过比较输入提示词和黑名单中已有的越狱提示词进行语义的相似度检测，设置了75%的阈值，一旦语义相似度超过75%，我们认为该提示词会
发生越狱的危险，则抛出危险信息并停止程序；而即使通过了黑名单的检测，之后还会进行DeepSeek-v3-0324大模型的检测， 只有这两种
检测均表示没有越狱风险才会继续执行程序。
