from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许所有前端域名访问

# 文物鉴定专业知识库
ANTIQUE_KNOWLEDGE = {
    "青花瓷": {
        "明代特征": "使用苏麻离青料，发色浓艳，有铁锈斑，纹饰疏朗大气",
        "清代特征": "采用浙料，发色纯蓝，纹饰繁密精细，层次丰富",
        "鉴定要点": "一看青料发色，二观胎体质地，三辨纹饰风格，四识款识年代"
    },
    "青铜器": {
        "商周特征": "形制古朴厚重，纹饰神秘庄严，多饕餮纹、云雷纹",
        "春秋战国特征": "工艺精湛细腻，出现失蜡法，纹饰更加写实",
        "鉴定要点": "一看锈色层次，二听敲击声音，三辨纹饰工艺，四识铭文内容"
    },
    "书画": {
        "唐代风格": "以人物画为主，线条流畅有力，色彩富丽堂皇",
        "宋代风格": "重视写实意境，山水画成就最高，讲究笔墨韵味",
        "鉴定要点": "一看笔墨功力，二观纸绢材质，三识款印特征，四辨时代风格"
    },
    "玉器": {
        "新石器时代": "造型古朴神秘，多为祭祀礼器，工艺简单粗犷",
        "明清时期": "工艺精湛细腻，题材丰富多样，多为陈设玩赏",
        "鉴定要点": "一看玉质温润度，二观雕工精细度，三识纹饰时代性，四辨沁色自然度"
    }
}

@app.route('/')
def home():
    """首页欢迎信息"""
    return jsonify({
        "message": "🎉 文鉴通助手Flask后端API运行正常",
        "status": "success",
        "version": "2.0.0",
        "service": "文物鉴定专业API"
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "文鉴通助手Flask API",
        "timestamp": "2024",
        "endpoints": {
            "chat": "/api/chat (POST)",
            "health": "/api/health (GET)"
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """智能文物鉴定对话接口"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({
                "reply": "请提供有效的JSON数据",
                "status": "error"
            }), 400
            
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message:
            return jsonify({
                "reply": "请输入您要咨询的文物问题",
                "status": "error"
            }), 400
        
        logger.info(f"用户 {user_id} 咨询: {user_message}")
        
        # 智能回复逻辑
        user_message_lower = user_message.lower()
        
        if any(keyword in user_message_lower for keyword in ["青花瓷", "瓷器", "陶瓷"]):
            knowledge = ANTIQUE_KNOWLEDGE["青花瓷"]
            reply = "🏺 **青花瓷专业鉴定指南**\n\n"
            for key, value in knowledge.items():
                reply += f"**{key}**: {value}\n"
            reply += "\n💡 **温馨提示**: 青花瓷鉴定需要结合实物观察，建议找专业机构检测。"
            
        elif any(keyword in user_message_lower for keyword in ["青铜", "铜器", "青铜器"]):
            knowledge = ANTIQUE_KNOWLEDGE["青铜器"]
            reply = "⚱️ **青铜器专业鉴定指南**\n\n"
            for key, value in knowledge.items():
                reply += f"**{key}**: {value}\n"
            reply += "\n💡 **温馨提示**: 青铜器鉴定要注意锈色的自然程度和铸造工艺。"
            
        elif any(keyword in user_message_lower for keyword in ["书画", "字画", "绘画", "国画"]):
            knowledge = ANTIQUE_KNOWLEDGE["书画"]
            reply = "🖼️ **书画专业鉴定指南**\n\n"
            for key, value in knowledge.items():
                reply += f"**{key}**: {value}\n"
            reply += "\n💡 **温馨提示**: 书画鉴定需要丰富的经验和专业知识，建议多方求证。"
            
        elif any(keyword in user_message_lower for keyword in ["玉器", "玉石", "玉雕", "古玉"]):
            knowledge = ANTIQUE_KNOWLEDGE["玉器"]
            reply = "💎 **玉器专业鉴定指南**\n\n"
            for key, value in knowledge.items():
                reply += f"**{key}**: {value}\n"
            reply += "\n💡 **温馨提示**: 玉器鉴定要注意材质、工艺和沁色的自然变化。"
            
        elif any(keyword in user_message_lower for keyword in ["鉴定", "真伪", "真假", "鉴别", "评估"]):
            reply = """🔍 **文物鉴定综合指南**

**鉴定五大要素**:
1️⃣ **材质分析** - 通过科学仪器检测材料成分和年代
2️⃣ **工艺特征** - 观察制作工艺是否符合时代特点
3️⃣ **艺术风格** - 对比同时期同类文物的艺术特征
4️⃣ **款识考证** - 研究款识、铭文的时代特征和内容
5️⃣ **传承脉络** - 了解文物的收藏历史和流传经历

**建议步骤**:
• 提供清晰的多角度照片
• 描述文物的具体尺寸和重量
• 说明获得途径和已知历史
• 必要时寻求专业检测机构帮助

💎 **专业建议**: 珍贵文物建议找国家认可的鉴定机构进行科学检测。"""
            
        elif any(keyword in user_message_lower for keyword in ["你好", "您好", "hello", "hi"]):
            reply = "👋 您好！我是文鉴通助手，专注于文物鉴定的专业AI助手。我可以为您提供：\n\n• 🏺 陶瓷类文物鉴定\n• ⚱️ 青铜器鉴定  \n• 🖼️ 书画类鉴定\n• 💎 玉器类鉴定\n• 🔍 综合鉴定方法\n\n请告诉我您想了解的具体文物类型或鉴定问题！"
            
        elif any(keyword in user_message_lower for keyword in ["谢谢", "感谢", "thank"]):
            reply = "🙏 不客气！能为您提供文物鉴定方面的帮助是我的荣幸。如果您还有其他问题，随时欢迎咨询！"
            
        else:
            reply = """🤔 **文物鉴定咨询**

我主要擅长以下文物类型的鉴定咨询：

**🏺 陶瓷类**
• 青花瓷年代鉴定
• 彩瓷真伪辨别
• 陶器工艺分析

**⚱️ 金属类**  
• 青铜器时代判断
• 铜器工艺特征
• 金银器材质鉴定

**🖼️ 书画类**
• 字画年代判断
• 画家风格识别
• 纸质材质分析

**💎 玉器类**
• 玉材质地鉴定
• 雕工时代特征
• 沁色自然判断

**🔍 请具体描述**：
您想鉴定的文物类型、特征和具体问题，我会给您专业的解答！"""

        logger.info(f"回复用户 {user_id}: {reply[:100]}...")
        
        return jsonify({
            "reply": reply,
            "status": "success",
            "user_id": user_id,
            "timestamp": "2024"
        })
        
    except Exception as e:
        logger.error(f"处理消息时出错: {str(e)}")
        return jsonify({
            "reply": "❌ 抱歉，服务暂时遇到问题，请稍后重试。",
            "status": "error",
            "error": str(e)
        }), 500

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "接口不存在",
        "status": "error"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "服务器内部错误",
        "status": "error"
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)