import boto3
import json
import os
import re
import time
from pathlib import Path

def parse_srt(srt_content):
    """解析SRT文件内容"""
    # 移除BOM字符
    if srt_content.startswith('\ufeff'):
        srt_content = srt_content[1:]
    
    blocks = srt_content.strip().split('\n\n')
    subtitles = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            # 移除可能的BOM字符并转换为整数
            index = int(lines[0].strip('\ufeff'))
            timing = lines[1]
            text = '\n'.join(lines[2:])
            
            subtitles.append({
                'index': index,
                'timing': timing,
                'text': text
            })
    
    return subtitles

def translate_text(bedrock, text, model="nova-lite", prompt="", source_lang="eng", target_lang="zh"):
    """使用指定的Nova模型翻译文本"""
    
    # 根据model参数选择模型ID
    model_id = {
        "nova-lite": "us.amazon.nova-lite-v1:0",
        "nova-micro": "us.amazon.nova-micro-v1:0"
    }.get(model, "us.amazon.nova-lite-v1:0")
    
    # 构建系统提示
    system_prompt = f"""你是一个专业的字幕翻译系统。请将{source_lang}字幕翻译成{target_lang}。

翻译要求：
1. 保持原文的语气和风格
2. 确保翻译自然流畅
3. 适合目标语言的观众理解
4. 保持专业术语的准确性
5. 考虑上下文连贯性

{prompt if prompt else ""}
"""
    
    system_list = [{
        "text": system_prompt
    }]
    
    message_list = [{
        "role": "user",
        "content": [
            {
                "text": f"请翻译以下文本：\n{text}"
            }
        ]
    }]

    # 配置推理参数
    inf_params = {
        "max_new_tokens": 5000,
        "top_p": 0.1,
        "top_k": 20,
        "temperature": 0
    }

    # 构建请求体
    body = json.dumps({
        "schemaVersion": "messages-v1",
        "messages": message_list,
        "system": system_list,
        "inferenceConfig": inf_params
    })

    try:
        # 调用模型
        response = bedrock.invoke_model(
            modelId=model_id,
            body=body
        )
        
        # 解析响应
        response_body = json.loads(response['body'].read())
        result = response_body['output']['message']['content'][0]['text']
        
        # 获取token统计信息
        usage = response_body.get('usage', {})
        input_tokens = usage.get('inputTokens', 'N/A')
        output_tokens = usage.get('outputTokens', 'N/A')
        
        return result.strip(), input_tokens, output_tokens
        
    except Exception as e:
        print(f"翻译错误: {str(e)}")
        return None, 0, 0

def translate_srt_file(input_file, output_file, model="nova-lite", prompt="", source_lang="eng", target_lang="zh"):
    """翻译整个SRT文件"""
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 记录开始时间
    start_time = time.time()
    
    # 创建 Bedrock Runtime 客户端
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'
    )
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析字幕
    subtitles = parse_srt(content)
    
    # 将字幕分批处理，每批100行
    batch_size = 100
    total_subtitles = len(subtitles)
    translations = {}
    total_input_tokens = 0
    total_output_tokens = 0
    
    for i in range(0, total_subtitles, batch_size):
        batch_end = min(i + batch_size, total_subtitles)
        batch_subtitles = subtitles[i:batch_end]
        
        # 构建当前批次的字幕文本
        batch_text = "\n\n".join([f"字幕 {s['index']}:\n{s['text']}" for s in batch_subtitles])
        
        print(f"\n正在翻译第 {i+1} 到 {batch_end} 行字幕...")
        translated_text, input_tokens, output_tokens = translate_text(
            bedrock,
            batch_text,
            model,
            prompt,
            source_lang,
            target_lang
        )
        
        if translated_text:
            # 解析当前批次的翻译结果
            current_index = None
            current_text = []
            
            for line in translated_text.split('\n'):
                if line.startswith('字幕 '):
                    if current_index is not None:
                        translations[current_index] = '\n'.join(current_text).strip()
                        current_text = []
                    current_index = int(line.split(':')[0].replace('字幕 ', ''))
                elif line.strip() and current_index is not None:
                    current_text.append(line.strip())
            
            if current_index is not None and current_text:
                translations[current_index] = '\n'.join(current_text).strip()
            
            # 累加token计数
            total_input_tokens += input_tokens if isinstance(input_tokens, int) else 0
            total_output_tokens += output_tokens if isinstance(output_tokens, int) else 0
            
            print(f"当前批次完成！输入tokens: {input_tokens}, 输出tokens: {output_tokens}")
    
    # 所有批次处理完成后，构建最终的翻译文件
    translated_blocks = []
    for subtitle in subtitles:
        if subtitle['index'] in translations:
            block = f"{subtitle['index']}\n{subtitle['timing']}\n{translations[subtitle['index']]}"
            translated_blocks.append(block)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(translated_blocks))
    
    print(f"\n全部翻译完成!")
    print(f"输入tokens总数: {total_input_tokens}")
    print(f"输出tokens总数: {total_output_tokens}")
    print(f"翻译结果已保存到: {output_file}")
    
    # 计算并显示总用时
    end_time = time.time()
    duration = end_time - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    print(f"总用时: {minutes}分{seconds}秒")

def main():
    # 设置输入输出文件路径
    input_file = "srts/Wolf.King.S01E01.tt31038402.eng.srt"  # 输入的SRT文件
    output_file = "srts/Wolf.King.S01E01.tt31038402.chs.srt"  # 输出的翻译文件
    
    # 自定义翻译提示词
    prompt = """请将这段字幕翻译成自然流畅的中文，保持原文的语气和风格，使其适合中文观众观看。
翻译时要注意：
1. 保持对话的自然性
2. 准确传达原文含义
3. 符合中文表达习惯
4. 保持字幕简洁明了
"""
    
    # 执行翻译
    translate_srt_file(
        input_file=input_file,
        output_file=output_file,
        model="nova-lite",
        prompt=prompt,
        source_lang="eng",
        target_lang="zh"
    )

if __name__ == "__main__":
    main()
