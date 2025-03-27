#!/usr/bin/env python3
from translate_srt import translate_srt_file

def test_eng_to_zh():
    """测试英文翻译为中文"""
    print("\n=== 测试英文翻译为中文 ===")
    
    # 使用Claude 3.5 Haiku模型翻译
    print("\n使用Claude 3.5 Haiku模型翻译...")
    translate_srt_file(
        input_file="srts/origin/Wolf.King.S01E01.tt31038402.eng.srt",
        output_file="srts/translated/Wolf.King.S01E01.tt31038402.chs.haiku.srt",
        model="anthropic.claude-3-5-haiku-20241022-v1:0",
        source_lang="eng",
        target_lang="zh",
        prompt="""请将这段字幕翻译成自然流畅的中文，保持原文的语气和风格，使其适合中文观众观看。
翻译时要注意：
1. 保持对话的自然性
2. 准确传达原文含义
3. 符合中文表达习惯
4. 保持字幕简洁明了
"""
    )
    
    # 使用nova-lite模型翻译
    print("\n使用nova-lite模型翻译...")
    translate_srt_file(
        input_file="srts/origin/Wolf.King.S01E01.tt31038402.eng.srt",
        output_file="srts/translated/Wolf.King.S01E01.tt31038402.chs.lite.srt",
        model="nova-lite",
        source_lang="eng",
        target_lang="zh",
        prompt="""请将这段字幕翻译成自然流畅的中文，保持原文的语气和风格，使其适合中文观众观看。
翻译时要注意：
1. 保持对话的自然性
2. 准确传达原文含义
3. 符合中文表达习惯
4. 保持字幕简洁明了
"""
    )
    
    # 使用nova-micro模型翻译
    print("\n使用nova-micro模型翻译...")
    translate_srt_file(
        input_file="srts/origin/Wolf.King.S01E01.tt31038402.eng.srt",
        output_file="srts/translated/Wolf.King.S01E01.tt31038402.chs.micro.srt",
        model="nova-micro",
        source_lang="eng",
        target_lang="zh",
        prompt="""请将这段字幕翻译成自然流畅的中文，保持原文的语气和风格，使其适合中文观众观看。
翻译时要注意：
1. 保持对话的自然性
2. 准确传达原文含义
3. 符合中文表达习惯
4. 保持字幕简洁明了
"""
    )

def test_fre_to_eng():
    """测试法文翻译为英文"""
    print("\n=== 测试法文翻译为英文 ===")
    
    # 使用Claude 3.5 Haiku模型翻译
    print("\n使用Claude 3.5 Haiku模型翻译...")
    translate_srt_file(
        input_file="srts/origin/Wolf.King.S01E01.tt31038402.fre.srt",
        output_file="srts/translated/Wolf.King.S01E01.tt31038402.eng.haiku.srt",
        model="anthropic.claude-3-5-haiku-20241022-v1:0",
        source_lang="fre",
        target_lang="eng",
        prompt="""Please translate these subtitles into natural and fluent English while maintaining the original tone and style.
Translation requirements:
1. Maintain natural dialogue flow
2. Accurately convey the original meaning
3. Follow English language conventions
4. Keep subtitles concise and clear
"""
    )
    
    # 使用nova-lite模型翻译
    print("\n使用nova-lite模型翻译...")
    translate_srt_file(
        input_file="srts/origin/Wolf.King.S01E01.tt31038402.fre.srt",
        output_file="srts/translated/Wolf.King.S01E01.tt31038402.eng.lite.srt",
        model="nova-lite",
        source_lang="fre",
        target_lang="eng",
        prompt="""Please translate these subtitles into natural and fluent English while maintaining the original tone and style.
Translation requirements:
1. Maintain natural dialogue flow
2. Accurately convey the original meaning
3. Follow English language conventions
4. Keep subtitles concise and clear
"""
    )
    
    # 使用nova-micro模型翻译
    print("\n使用nova-micro模型翻译...")
    translate_srt_file(
        input_file="srts/origin/Wolf.King.S01E01.tt31038402.fre.srt",
        output_file="srts/translated/Wolf.King.S01E01.tt31038402.eng.micro.srt",
        model="nova-micro",
        source_lang="fre",
        target_lang="eng",
        prompt="""Please translate these subtitles into natural and fluent English while maintaining the original tone and style.
Translation requirements:
1. Maintain natural dialogue flow
2. Accurately convey the original meaning
3. Follow English language conventions
4. Keep subtitles concise and clear
"""
    )

def main():
    """运行所有测试用例"""
    print("开始运行翻译测试...")
    
    # 运行测试用例
    test_eng_to_zh()
    test_fre_to_eng()
    
    print("\n所有测试完成!")

if __name__ == "__main__":
    main()
