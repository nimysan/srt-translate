# 字幕翻译测试结果总结

| 翻译任务 | 模型 | 输入Tokens | 输出Tokens | 用时(秒) | 价格(USD) | 输出文件 |
|---------|------|------------|------------|---------|-----------|----------|
| 英文到中文 | Claude 3.5 Haiku | 9,420 | 10,673 | 62 | $0.050 | Wolf.King.S01E01.tt31038402.chs.haiku.srt |
| 英文到中文 | nova-lite | 9,420 | 10,679 | 61 | $0.003 | Wolf.King.S01E01.tt31038402.chs.lite.srt |
| 英文到中文 | nova-micro | 9,420 | 10,293 | 48 | $0.002 | Wolf.King.S01E01.tt31038402.chs.micro.srt |
| 法文到英文 | Claude 3.5 Haiku | 5,309 | 3,966 | 20 | $0.020 | Wolf.King.S01E01.tt31038402.eng.haiku.srt |
| 法文到英文 | nova-lite | 5,309 | 3,966 | 21 | $0.001 | Wolf.King.S01E01.tt31038402.eng.lite.srt |
| 法文到英文 | nova-micro | 5,309 | 3,803 | 16 | $0.001 | Wolf.King.S01E01.tt31038402.eng.micro.srt |

注：价格计算方式
- Claude 3.5 Haiku: 输入 $0.0008/1K tokens, 输出 $0.004/1K tokens
- nova-lite: 输入 $0.00006/1K tokens, 输出 $0.00024/1K tokens
- nova-micro: 输入 $0.000035/1K tokens, 输出 $0.00014/1K tokens

## 主要发现
1. 性能对比：
   - nova-micro模型在处理速度上最快
   - Claude 3.5 Haiku和nova-lite速度相近
2. tokens使用情况：
   - 英文到中文的翻译输出tokens数量大于输入
   - 法文到英文的翻译输出tokens数量小于输入
   - 三个模型的输出tokens数量略有差异
3. 价格对比：
   - Claude 3.5 Haiku价格最高，但单价是nova-lite的13倍左右
   - nova-micro价格最低，且性能表现优于其他两个模型
   - nova-lite价格适中，性能与Claude相近
4. 翻译时长：
   - 法文到英文的翻译比英文到中文的翻译用时更短（约316行 vs 534行）
   - 英文到中文任务：micro 48秒，lite 61秒，haiku 62秒
   - 法文到英文任务：micro 16秒，lite 21秒，haiku 20秒
