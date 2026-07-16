from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
import streamlit as st
from datetime import datetime
import hashlib

# ── Translations ──────────────────────────────────────────────────────────────

T = {
    "zh": {
        # App
        "title": "✍️ AI 内容创作助手",
        "subtitle": "多Agent协作的内容创作助手",
        # Sidebar
        "settings": "⚙️ 设置",
        "api_key_label": "API Key",
        "api_key_placeholder": "输入你的 API Key",
        "base_url_label": "API Base URL",
        "api_configured": "✅ API Key 已配置",
        "api_warning": "⚠️ 请配置 API Key",
        "agents_info": "📋 Agent 信息",
        "agent_web": "**Web Researcher** - 搜索热点",
        "agent_copy": "**Copywriter** - 文案创作",
        "agent_social": "**Social Media** - 社媒优化",
        "agent_seo": "**SEO Expert** - 搜索优化",
        "agent_translate": "**Translator** - 多语言翻译",
        "agent_data": "**Data Analyst** - 数据分析",
        "agent_video": "**Video Scriptwriter** - 视频脚本",
        "agent_xhs": "**Xiaohongshu Expert** - 小红书爆款",
        "agent_polish": "**English Polisher** - 英文润色",
        # Tabs
        "tab1": "📝 内容创作",
        "tab2": "📊 热点分析",
        "tab3": "📅 内容日历",
        "tab4": "🌐 多语言翻译",
        "tab5": "📈 数据分析",
        "tab6": "🎬 视频脚本",
        "tab7": "📱 小红书爆款",
        "tab8": "🔤 英文润色",
        "tab9": "🔍 SEO 分析",
        "tab10": "📜 历史记录",
        # Tab 1: Content Creation
        "create_title": "创建内容",
        "topic_label": "主题/产品名称",
        "topic_placeholder": "例如：AI写作助手",
        "platform_label": "目标平台",
        "platforms": ["微信公众号", "小红书", "抖音", "知乎", "微博", "LinkedIn", "Twitter"],
        "content_type_label": "内容类型",
        "content_types": ["产品介绍", "技术博客", "营销文案", "教程指南", "行业分析", "新闻稿"],
        "tone_label": "语气风格",
        "tones": ["专业正式", "轻松活泼", "亲切友好", "幽默搞笑", "严肃认真"],
        "additional_label": "补充信息",
        "additional_placeholder": "任何需要包含的特定信息、关键词或要求...",
        "btn_create": "🚀 开始创作",
        "creating": "AI Agent 团队正在创作中...",
        "result_title": "✨ 创作结果",
        "btn_download": "📥 下载内容",
        # Tab 2: Trend Analysis
        "trend_title": "热点分析",
        "industry_label": "行业/领域",
        "industry_placeholder": "例如：人工智能、电商、教育",
        "btn_trend": "🔍 分析热点",
        "analyzing": "正在分析热点...",
        "trend_result": "📊 热点分析结果",
        "trend_hint": "提示：如果网络不稳定，建议使用英文关键词进行搜索",
        # Tab 3: Content Calendar
        "calendar_title": "内容日历规划",
        "start_date": "开始日期",
        "days_label": "规划天数",
        "btn_calendar": "📅 生成日历",
        "generating_calendar": "正在生成内容日历...",
        "calendar_result": "📅 内容日历",
        # Tab 4: Translation
        "translate_title": "🌐 多语言翻译",
        "source_lang": "源语言",
        "target_lang": "目标语言",
        "source_text_label": "输入要翻译的内容",
        "source_text_placeholder": "请粘贴或输入要翻译的文本...",
        "btn_translate": "🔄 开始翻译",
        "translating": "翻译中...",
        "translate_result": "翻译结果",
        "translation_label": "译文",
        "btn_download_translation": "📥 下载译文",
        # Tab 5: Data Analysis
        "data_title": "📈 数据分析",
        "data_label": "输入数据或描述",
        "data_placeholder": "粘贴数据、报告内容，或描述你想分析的问题...",
        "analysis_type_label": "分析类型",
        "analysis_types": ["趋势分析", "对比分析", "问题诊断", "建议生成", "综合分析"],
        "btn_analyze": "📊 开始分析",
        "analyzing_data": "分析中...",
        "data_result": "📊 分析报告",
        # Tab 6: Video Script
        "video_title": "🎬 视频脚本创作",
        "video_topic_label": "视频主题",
        "video_topic_placeholder": "例如：AI写作助手产品介绍",
        "video_type_label": "视频类型",
        "video_types": ["口播稿", "分镜脚本", "带货文案", "教程脚本", "故事脚本"],
        "video_platform_label": "目标平台",
        "video_platforms": ["抖音", "快手", "B站", "YouTube", "视频号"],
        "video_duration_label": "视频时长",
        "video_durations": ["15秒", "30秒", "1分钟", "3分钟", "5分钟"],
        "video_details_label": "补充说明",
        "video_details_placeholder": "视频风格、目标受众、需要包含的要点等...",
        "btn_video": "🎬 生成脚本",
        "generating_video": "生成视频脚本中...",
        "video_result": "🎬 视频脚本",
        "btn_download_video": "📥 下载脚本",
        # Tab 7: Xiaohongshu
        "xhs_title": "📱 小红书爆款笔记",
        "xhs_topic_label": "笔记主题",
        "xhs_topic_placeholder": "例如：平价好物推荐、旅行攻略、美食探店",
        "xhs_type_label": "笔记类型",
        "xhs_types": ["种草推荐", "经验分享", "教程攻略", "测评对比", "日常分享"],
        "xhs_style_label": "风格",
        "xhs_styles": ["真诚分享", "干货满满", "轻松活泼", "专业权威", "搞笑幽默"],
        "xhs_keywords_label": "关键词（可选）",
        "xhs_keywords_placeholder": "例如：平价、学生党、新手友好",
        "xhs_details_label": "补充说明",
        "xhs_details_placeholder": "产品特点、使用体验、目标人群等...",
        "btn_xhs": "📱 生成爆款笔记",
        "generating_xhs": "生成小红书爆款笔记中...",
        "xhs_result": "📱 小红书爆款笔记",
        "btn_download_xhs": "📥 下载笔记",
        # Tab 8: English Polish
        "polish_title": "🔤 英文润色",
        "polish_input_label": "输入需要润色的英文内容",
        "polish_input_placeholder": "Paste your English text here...",
        "polish_style_label": "润色风格",
        "polish_styles": ["学术正式", "商务专业", "日常交流", "创意写作", "技术文档"],
        "polish_level_label": "润色程度",
        "polish_levels": ["轻度修改（修正语法）", "中度润色（优化表达）", "重度改写（提升质量）"],
        "polish_focus_label": "特殊要求（可选）",
        "polish_focus_placeholder": "例如：增加专业术语、简化表达、提升可读性",
        "btn_polish": "🔤 开始润色",
        "polishing": "润色中...",
        "polish_result": "🔤 润色结果",
        "btn_download_polish": "📥 下载润色结果",
        # Tab 9: SEO
        "seo_title": "🔍 SEO 分析",
        "seo_url_label": "输入网址（可选）",
        "seo_url_placeholder": "例如：https://example.com",
        "seo_content_label": "或直接输入文章内容进行SEO分析",
        "seo_content_placeholder": "粘贴文章内容...",
        "btn_seo": "🔍 开始分析",
        "analyzing_seo": "SEO 分析中...",
        "seo_result": "📊 SEO 分析报告",
        # Tab 10: History
        "history_title": "📜 历史记录",
        "history_count": "共 {n} 条记录",
        "history_type": "类型：",
        "history_input": "输入：",
        "history_output": "输出：",
        "btn_clear_history": "🗑️ 清空历史",
        "no_history": "暂无历史记录",
        # Tab 11: Video Production
        "tab11": "🎥 视频制作",
        "video_gen_title": "🎥 AI 视频制作",
        "video_gen_subtitle": "选择视频生成平台，输入内容即可生成短视频",
        "video_provider_label": "选择平台",
        "jimeng_api_key_label": "即梦 API Key",
        "jimeng_api_key_placeholder": "输入即梦 API Key",
        "kling_api_key_label": "可灵 API Key",
        "kling_api_key_placeholder": "输入可灵 API Key",
        "cogvideox_api_key_label": "智谱 API Key",
        "cogvideox_api_key_placeholder": "输入智谱 API Key",
        "provider_configured": "✅ {provider} API Key 已配置",
        "provider_warning": "⚠️ 请配置 {provider} API Key（用于视频生成）",
        "provider_not_configured": "未配置 API Key",
        "video_mode_label": "制作模式",
        "video_modes": ["文字转视频", "图片转视频", "脚本转视频", "数字分身"],
        "video_text_label": "视频描述",
        "video_text_placeholder": "输入视频的描述文字，越详细效果越好...\n例如：一个阳光明媚的海滩，海浪轻轻拍打着沙滩，远处有几棵棕榈树",
        "video_image_label": "上传首帧图片",
        "video_image_help": "支持 JPG、PNG 格式，建议 16:9 比例",
        "video_prompt_label": "视频提示词（可选）",
        "video_prompt_placeholder": "补充视频的运动、风格等描述...",
        "video_duration_label": "视频时长",
        "video_durations": ["3秒", "5秒", "10秒"],
        "video_aspect_label": "画面比例",
        "video_aspects": ["16:9 横屏", "9:16 竖屏", "1:1 方形"],
        "btn_generate_video": "🎬 生成视频",
        "generating_video": "正在生成视频，请稍候（约1-3分钟）...",
        "video_result": "🎬 视频预览",
        "btn_download_video": "📥 下载视频",
        "video_status_ready": "✅ 视频已就绪",
        "video_status_processing": "⏳ 视频生成中...",
        "video_status_failed": "❌ 视频生成失败",
        "script_segments_label": "脚本段落数",
        "segment": "段落",
        "segment_prompt_label": "本段视频描述",
        "segment_prompt_placeholder": "描述这一段视频的内容...",
        "script_video_info": "💡 脚本转视频：输入多个视频片段描述，系统将逐段生成并拼接成完整视频。",
        "avatar_select_label": "选择数字分身",
        "avatar_script_label": "数字分身要说的话",
        "avatar_script_placeholder": "输入数字分身要说的内容...\n例如：大家好，我是AI助手，今天给大家介绍一款新产品...",
        "avatar_loading": "正在加载数字分身列表...",
        "avatar_no_available": "当前平台不支持数字分身功能，请选择可灵 (Kling) 平台",
        "avatar_not_configured": "请先配置可灵 API Key 以使用数字分身功能",
        # Errors
        "error_api_key": "请先输入 API Key",
        "error_input_required": "请输入内容",
        "error_generic": "操作失败：{error}",
    },
    "en": {
        # App
        "title": "✍️ AI Content Creator Agent",
        "subtitle": "Multi-Agent collaborative content creation assistant",
        # Sidebar
        "settings": "⚙️ Settings",
        "api_key_label": "API Key",
        "api_key_placeholder": "Enter your API Key",
        "base_url_label": "API Base URL",
        "api_configured": "✅ API Key configured",
        "api_warning": "⚠️ Please configure API Key",
        "agents_info": "📋 Agent Info",
        "agent_web": "**Web Researcher** - Trend research",
        "agent_copy": "**Copywriter** - Content creation",
        "agent_social": "**Social Media** - Platform optimization",
        "agent_seo": "**SEO Expert** - Search optimization",
        "agent_translate": "**Translator** - Multi-language translation",
        "agent_data": "**Data Analyst** - Data analysis",
        "agent_video": "**Video Scriptwriter** - Video scripts",
        "agent_xhs": "**Xiaohongshu Expert** - Xiaohongshu posts",
        "agent_polish": "**English Polisher** - English polishing",
        # Tabs
        "tab1": "📝 Content",
        "tab2": "📊 Trends",
        "tab3": "📅 Calendar",
        "tab4": "🌐 Translation",
        "tab5": "📈 Data Analysis",
        "tab6": "🎬 Video Script",
        "tab7": "📱 Xiaohongshu",
        "tab8": "🔤 English Polish",
        "tab9": "🔍 SEO Analysis",
        "tab10": "📜 History",
        # Tab 1: Content Creation
        "create_title": "Create Content",
        "topic_label": "Topic / Product Name",
        "topic_placeholder": "e.g., AI Writing Assistant",
        "platform_label": "Target Platform",
        "platforms": ["WeChat", "Xiaohongshu", "Douyin", "Zhihu", "Weibo", "LinkedIn", "Twitter"],
        "content_type_label": "Content Type",
        "content_types": ["Product Intro", "Tech Blog", "Marketing Copy", "Tutorial", "Industry Analysis", "Press Release"],
        "tone_label": "Tone Style",
        "tones": ["Professional", "Casual", "Friendly", "Humorous", "Serious"],
        "additional_label": "Additional Info",
        "additional_placeholder": "Any specific info, keywords, or requirements...",
        "btn_create": "🚀 Start Creating",
        "creating": "AI Agent team is working on it...",
        "result_title": "✨ Result",
        "btn_download": "📥 Download",
        # Tab 2: Trend Analysis
        "trend_title": "Trend Analysis",
        "industry_label": "Industry / Field",
        "industry_placeholder": "e.g., AI, E-commerce, Education",
        "btn_trend": "🔍 Analyze Trends",
        "analyzing": "Analyzing trends...",
        "trend_result": "📊 Trend Analysis Result",
        "trend_hint": "Tip: If the network is unstable, try using English keywords",
        # Tab 3: Content Calendar
        "calendar_title": "Content Calendar Planning",
        "start_date": "Start Date",
        "days_label": "Number of Days",
        "btn_calendar": "📅 Generate Calendar",
        "generating_calendar": "Generating content calendar...",
        "calendar_result": "📅 Content Calendar",
        # Tab 4: Translation
        "translate_title": "🌐 Multi-language Translation",
        "source_lang": "Source Language",
        "target_lang": "Target Language",
        "source_text_label": "Enter text to translate",
        "source_text_placeholder": "Paste or type text to translate...",
        "btn_translate": "🔄 Start Translation",
        "translating": "Translating...",
        "translate_result": "Translation Result",
        "translation_label": "Translation",
        "btn_download_translation": "📥 Download Translation",
        # Tab 5: Data Analysis
        "data_title": "📈 Data Analysis",
        "data_label": "Enter data or description",
        "data_placeholder": "Paste data, reports, or describe your analysis question...",
        "analysis_type_label": "Analysis Type",
        "analysis_types": ["Trend Analysis", "Comparison", "Problem Diagnosis", "Recommendations", "Comprehensive"],
        "btn_analyze": "📊 Start Analysis",
        "analyzing_data": "Analyzing...",
        "data_result": "📊 Analysis Report",
        # Tab 6: Video Script
        "video_title": "🎬 Video Script Writer",
        "video_topic_label": "Video Topic",
        "video_topic_placeholder": "e.g., AI Writing Assistant product intro",
        "video_type_label": "Video Type",
        "video_types": ["Voiceover Script", "Storyboard", "Sales Copy", "Tutorial Script", "Story Script"],
        "video_platform_label": "Target Platform",
        "video_platforms": ["Douyin", "Kuaishou", "Bilibili", "YouTube", "WeChat Video"],
        "video_duration_label": "Duration",
        "video_durations": ["15s", "30s", "1 min", "3 min", "5 min"],
        "video_details_label": "Additional Details",
        "video_details_placeholder": "Video style, target audience, key points to include...",
        "btn_video": "🎬 Generate Script",
        "generating_video": "Generating video script...",
        "video_result": "🎬 Video Script",
        "btn_download_video": "📥 Download Script",
        # Tab 7: Xiaohongshu
        "xhs_title": "📱 Xiaohongshu Viral Post",
        "xhs_topic_label": "Post Topic",
        "xhs_topic_placeholder": "e.g., Budget finds, travel guide, food review",
        "xhs_type_label": "Post Type",
        "xhs_types": ["Product Recommendation", "Experience Share", "Tutorial", "Review", "Daily Share"],
        "xhs_style_label": "Style",
        "xhs_styles": ["Sincere Sharing", "Info-packed", "Casual & Fun", "Professional", "Humorous"],
        "xhs_keywords_label": "Keywords (optional)",
        "xhs_keywords_placeholder": "e.g., budget-friendly, student-friendly, beginner-friendly",
        "xhs_details_label": "Additional Details",
        "xhs_details_placeholder": "Product features, user experience, target audience...",
        "btn_xhs": "📱 Generate Post",
        "generating_xhs": "Generating Xiaohongshu post...",
        "xhs_result": "📱 Xiaohongshu Viral Post",
        "btn_download_xhs": "📥 Download Post",
        # Tab 8: English Polish
        "polish_title": "🔤 English Polish",
        "polish_input_label": "Enter English text to polish",
        "polish_input_placeholder": "Paste your English text here...",
        "polish_style_label": "Polish Style",
        "polish_styles": ["Academic", "Business", "Casual", "Creative Writing", "Technical"],
        "polish_level_label": "Polish Level",
        "polish_levels": ["Light (fix grammar)", "Medium (improve expression)", "Heavy (rewrite for quality)"],
        "polish_focus_label": "Special Requirements (optional)",
        "polish_focus_placeholder": "e.g., add technical terms, simplify, improve readability",
        "btn_polish": "🔤 Start Polishing",
        "polishing": "Polishing...",
        "polish_result": "🔤 Polish Result",
        "btn_download_polish": "📥 Download Result",
        # Tab 9: SEO
        "seo_title": "🔍 SEO Analysis",
        "seo_url_label": "Enter URL (optional)",
        "seo_url_placeholder": "e.g., https://example.com",
        "seo_content_label": "Or paste article content for SEO analysis",
        "seo_content_placeholder": "Paste article content...",
        "btn_seo": "🔍 Start Analysis",
        "analyzing_seo": "Analyzing SEO...",
        "seo_result": "📊 SEO Analysis Report",
        # Tab 10: History
        "history_title": "📜 History",
        "history_count": "Total {n} records",
        "history_type": "Type: ",
        "history_input": "Input: ",
        "history_output": "Output: ",
        "btn_clear_history": "🗑️ Clear History",
        "no_history": "No history yet",
        # Tab 11: Video Production
        "tab11": "🎥 Video Production",
        "video_gen_title": "🎥 AI Video Production",
        "video_gen_subtitle": "Select a video generation platform, enter content to generate videos",
        "video_provider_label": "Select Platform",
        "jimeng_api_key_label": "Jimeng API Key",
        "jimeng_api_key_placeholder": "Enter Jimeng API Key",
        "kling_api_key_label": "Kling API Key",
        "kling_api_key_placeholder": "Enter Kling API Key",
        "cogvideox_api_key_label": "CogVideoX API Key",
        "cogvideox_api_key_placeholder": "Enter CogVideoX API Key",
        "provider_configured": "✅ {provider} API Key configured",
        "provider_warning": "⚠️ Please configure {provider} API Key (for video generation)",
        "provider_not_configured": "API Key not configured",
        "video_mode_label": "Production Mode",
        "video_modes": ["Text to Video", "Image to Video", "Script to Video", "Digital Avatar"],
        "video_text_label": "Video Description",
        "video_text_placeholder": "Enter video description, more details = better results...\nExample: A sunny beach with gentle waves, palm trees in the distance",
        "video_image_label": "Upload First Frame Image",
        "video_image_help": "Supports JPG, PNG format, 16:9 aspect ratio recommended",
        "video_prompt_label": "Video Prompt (Optional)",
        "video_prompt_placeholder": "Add motion, style descriptions...",
        "video_duration_label": "Video Duration",
        "video_durations": ["3s", "5s", "10s"],
        "video_aspect_label": "Aspect Ratio",
        "video_aspects": ["16:9 Landscape", "9:16 Portrait", "1:1 Square"],
        "btn_generate_video": "🎬 Generate Video",
        "generating_video": "Generating video, please wait (approx. 1-3 minutes)...",
        "video_result": "🎬 Video Preview",
        "btn_download_video": "📥 Download Video",
        "video_status_ready": "✅ Video Ready",
        "video_status_processing": "⏳ Processing...",
        "video_status_failed": "❌ Generation Failed",
        "script_segments_label": "Number of Segments",
        "segment": "Segment",
        "segment_prompt_label": "Video Description for This Segment",
        "segment_prompt_placeholder": "Describe the content of this video segment...",
        "script_video_info": "💡 Script to Video: Enter multiple video segment descriptions, and the system will generate each segment and combine them into a complete video.",
        "avatar_select_label": "Select Digital Avatar",
        "avatar_script_label": "What the avatar will say",
        "avatar_script_placeholder": "Enter the script for the digital avatar...\nExample: Hello everyone, I'm your AI assistant. Today I'll introduce a new product...",
        "avatar_loading": "Loading digital avatars...",
        "avatar_no_available": "Current platform does not support digital avatars. Please select Kling platform.",
        "avatar_not_configured": "Please configure Kling API Key first to use digital avatar feature",
        # Errors
        "error_api_key": "Please enter your API Key first",
        "error_input_required": "Please enter content",
        "error_generic": "Operation failed: {error}",
    },
}

def t(key: str, **kwargs) -> str:
    lang = st.session_state.get("lang", "zh")
    text = T.get(lang, T["en"]).get(key, T["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text

# Prompt templates — zh/en pairs for each feature
P = {
    "create": {
        "zh": "请为以下内容创建完整的创作方案：\n\n主题：{topic}\n平台：{platform}\n内容类型：{content_type}\n语气风格：{tone}\n补充信息：{additional_info}\n\n请按以下步骤协作：\n1. Web Researcher: 先搜索相关热点和趋势\n2. Copywriter: 根据搜索结果创作文案\n3. Social Media Expert: 优化为适合{platform}的形式\n4. SEO Expert: 添加SEO优化建议\n\n最终输出完整的、可直接使用的{content_type}内容。",
        "en": "Create a complete content plan:\n\nTopic: {topic}\nPlatform: {platform}\nType: {content_type}\nTone: {tone}\nAdditional: {additional_info}\n\nCollaborate:\n1. Web Researcher: search trends\n2. Copywriter: write copy\n3. Social Media Expert: optimize for {platform}\n4. SEO Expert: add SEO suggestions\n\nOutput ready-to-use {content_type} content.",
    },
    "trend": {
        "zh": "请分析\"{industry}\"行业的当前热点和趋势：\n\n1. 搜索最新的行业动态\n2. 总结5-10个关键热点\n3. 分析每个热点的传播潜力\n4. 给出内容创作建议\n\n用清晰的列表和表格展示结果。",
        "en": 'Analyze current trends in the "{industry}" industry:\n1. Search latest industry news\n2. Summarize 5-10 key trends\n3. Analyze viral potential\n4. Give content creation suggestions\nUse clear lists and tables.',
    },
    "calendar": {
        "zh": "请为\"{industry_cal}\"行业创建{days}天的内容发布日历：\n\n从{start_date}开始，每天规划：\n- 发布时间\n- 内容主题\n- 内容类型\n- 目标平台\n- 创作要点\n\n用表格形式展示，并确保内容有节奏感（不要每天都发硬广）。",
        "en": 'Create a {days}-day content calendar for the "{industry_cal}" industry starting from {start_date}:\nFor each day: time, topic, type, platform, key points.\nUse table format. Vary content types (not all promotional).',
    },
    "video": {
        "zh": "请为以下视频创作{video_type}：\n\n主题：{video_topic}\n平台：{video_platform}\n时长：{video_duration}\n补充说明：{video_details}\n\n请提供：\n1. 开场钩子（前3秒抓住观众）\n2. 主体内容（分段展示）\n3. 结尾CTA（引导互动）\n4. 配音建议（语速、语调）\n5. 画面建议（如有分镜）\n\n确保脚本口语化、有节奏感、适合{video_platform}平台风格。",
        "en": "Create a {video_type} for a video:\n\nTopic: {video_topic}\nPlatform: {video_platform}\nDuration: {video_duration}\nDetails: {video_details}\n\nProvide:\n1. Opening hook (first 3 seconds)\n2. Main content (segmented)\n3. Closing CTA\n4. Voiceover suggestions\n5. Visual suggestions (if storyboard)\n\nMake it conversational and suited for {video_platform}.",
    },
    "xhs": {
        "zh": "请为小红书创作一篇爆款{xhs_type}笔记：\n\n主题：{xhs_topic}\n风格：{xhs_style}\n关键词：{xhs_keywords}\n补充说明：{xhs_details}\n\n请提供：\n1. **爆款标题**（3个备选，含emoji，18字以内）\n2. **正文内容**（800-1200字，分段清晰）\n3. **标签推荐**（15-20个相关标签）\n4. **封面建议**（图片风格和构图）\n5. **发布时间建议**\n\n要求：\n- 标题吸引眼球，有数字或痛点\n- 正文有干货、有故事、有互动\n- 多用emoji，排版清晰\n- 结尾引导点赞收藏",
        "en": "Create a viral Xiaohongshu {xhs_type} post:\n\nTopic: {xhs_topic}\nStyle: {xhs_style}\nKeywords: {xhs_keywords}\nDetails: {xhs_details}\n\nProvide:\n1. **3 viral title options** (with emoji, under 18 chars)\n2. **Main content** (800-1200 words, well-structured)\n3. **15-20 hashtags**\n4. **Cover image suggestion**\n5. **Best posting time**\n\nRequirements:\n- Eye-catching titles with numbers or pain points\n- Useful content with stories and engagement\n- Use emojis, clear formatting\n- End with call-to-action for likes and saves",
    },
    "polish": {
        "zh": "请对以下英文内容进行{en_level}：\n\n{en_content}\n\n润色风格：{en_style}\n特殊要求：{en_focus}\n\n请提供：\n1. **润色后的内容**（完整版本）\n2. **修改说明**（列出主要修改点和原因）\n3. **语法检查**（如有错误请指出）\n4. **表达建议**（提升地道性的建议）\n\n确保保持原意，同时提升表达质量。",
        "en": "Apply {en_level} to the following English text:\n\n{en_content}\n\nStyle: {en_style}\nSpecial requirements: {en_focus}\n\nProvide:\n1. **Polished version** (complete)\n2. **Change notes** (list key changes and reasons)\n3. **Grammar check** (flag any errors)\n4. **Expression suggestions** (improve naturalness)\n\nPreserve the original meaning while improving quality.",
    },
    "seo": {
        "zh": "请对以下内容进行全面的 SEO 分析：\n\n{input_content}\n\n请提供：\n1. **关键词分析**：核心关键词、长尾关键词建议\n2. **标题优化**：标题长度、吸引力、关键词包含情况\n3. **内容结构**：段落划分、标题层级、可读性\n4. **Meta 描述**：建议的 meta description\n5. **SEO 评分**：0-100分，附改进建议\n6. **竞品关键词**：相关热门搜索词\n\n用清晰的结构展示，包含具体的优化建议。",
        "en": "Perform comprehensive SEO analysis on:\n\n{input_content}\n\nProvide:\n1. **Keyword analysis**: core + long-tail keywords\n2. **Title optimization**: length, appeal, keyword inclusion\n3. **Content structure**: paragraphs, headings, readability\n4. **Meta description**: suggested\n5. **SEO score**: 0-100 with improvement tips\n6. **Competitor keywords**: related popular searches\nUse clear structure with specific optimization advice.",
    },
    "data": {
        "zh": "请对以下内容进行{analysis_type}：\n\n{data_text}\n\n请提供：\n1. 关键发现\n2. 数据解读\n3. 趋势/模式识别\n4. 可执行建议\n\n用清晰的结构和表格展示结果。",
        "en": "Perform {analysis_type} on the following:\n\n{data_text}\n\nProvide:\n1. Key findings\n2. Data interpretation\n3. Trends/patterns\n4. Actionable recommendations\nUse clear structure and tables.",
    },
}

def prompt(key: str, **kwargs) -> str:
    lang = st.session_state.get("lang", "zh")
    template = P.get(key, {}).get(lang, P.get(key, {}).get("en", ""))
    return template.format(**kwargs)

# ── Setup ─────────────────────────────────────────────────────────────────────

db = SqliteDb(db_file="agents.db")

def load_config():
    try:
        return {
            "api_key": st.secrets.get("api_key", ""),
            "base_url": st.secrets.get("base_url", "https://oa.api2d.net"),
        }
    except FileNotFoundError:
        return {"api_key": "", "base_url": "https://oa.api2d.net"}

saved_config = load_config()

if 'history' not in st.session_state:
    st.session_state.history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
if 'lang' not in st.session_state:
    st.session_state.lang = "zh"

def save_history(action_type, input_data, output_data):
    st.session_state.history.append({
        "id": len(st.session_state.history) + 1,
        "type": action_type,
        "input": input_data[:200] + "..." if len(input_data) > 200 else input_data,
        "output": output_data[:200] + "..." if len(output_data) > 200 else output_data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def get_agents(api_key, base_url):
    cache_key = f"{api_key}_{base_url}"
    if "agents" in st.session_state and st.session_state.get("agents_key") == cache_key:
        return st.session_state.agents

    model_config = {"id": "gpt-4o", "api_key": api_key, "base_url": base_url}

    web_researcher = Agent(
        name="Web Researcher", role="搜索网络热点和趋势信息",
        model=OpenAIChat(**model_config), tools=[DuckDuckGoTools()],
        db=db, add_history_to_context=True, markdown=True,
    )
    copywriter = Agent(
        name="Copywriter", role="创建吸引人的文案和标题",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    social_media = Agent(
        name="Social Media Expert", role="优化内容适合不同社交平台",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    seo_expert = Agent(
        name="SEO Expert", role="优化内容的搜索排名和关键词",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    translator = Agent(
        name="Translator", role="专业翻译，支持中英日韩等多种语言互译",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    data_analyst = Agent(
        name="Data Analyst", role="分析数据趋势，生成数据报告和可视化建议",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    video_scriptwriter = Agent(
        name="Video Scriptwriter", role="创作短视频脚本，包括口播稿、分镜脚本、带货文案",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    xiaohongshu_expert = Agent(
        name="Xiaohongshu Expert", role="创作小红书爆款笔记，擅长标题、正文、标签优化",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    english_polisher = Agent(
        name="English Polisher", role="润色英文内容，提升语法准确性、表达地道性和可读性",
        model=OpenAIChat(**model_config), db=db, add_history_to_context=True, markdown=True,
    )
    content_team = Team(
        name="Content Creation Team", model=OpenAIChat(**model_config),
        members=[web_researcher, copywriter, social_media, seo_expert, translator, data_analyst, video_scriptwriter, xiaohongshu_expert, english_polisher],
        markdown=True,
    )

    agents = {
        "web_researcher": web_researcher, "copywriter": copywriter,
        "social_media": social_media, "seo_expert": seo_expert,
        "translator": translator, "data_analyst": data_analyst,
        "video_scriptwriter": video_scriptwriter, "xiaohongshu_expert": xiaohongshu_expert,
        "english_polisher": english_polisher, "content_team": content_team,
    }
    st.session_state.agents = agents
    st.session_state.agents_key = cache_key
    return agents

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="AI Content Creator Agent", page_icon="✍️", layout="wide")

    st.title(t("title"))
    st.caption(t("subtitle"))

    # Sidebar
    with st.sidebar:
        # Language switcher
        lang = st.radio("Language / 语言", ["zh", "en"], index=0 if st.session_state.lang == "zh" else 1, horizontal=True, key="lang_radio")
        if lang != st.session_state.lang:
            st.session_state.lang = lang
            st.rerun()

        st.header(t("settings"))

        # Persist API key across reruns (e.g. language switch)
        if "api_key" not in st.session_state:
            st.session_state.api_key = saved_config.get("api_key", "")
        if "base_url" not in st.session_state:
            st.session_state.base_url = saved_config.get("base_url", "https://oa.api2d.net")

        openai_api_key = st.text_input(t("api_key_label"), type="password", value=st.session_state.api_key, key="api_key_input", placeholder=t("api_key_placeholder"))
        api_base_url = st.text_input(t("base_url_label"), placeholder="https://oa.api2d.net", value=st.session_state.base_url, key="base_url_input")

        # Save to session_state on change
        if openai_api_key != st.session_state.api_key:
            st.session_state.api_key = openai_api_key
        if api_base_url != st.session_state.base_url:
            st.session_state.base_url = api_base_url

        if openai_api_key:
            st.success(t("api_configured"))
        else:
            st.warning(t("api_warning"))

        st.divider()

        # Video Generation API Keys
        st.header("🎥 " + t("tab11").split(" ")[-1])

        if "jimeng_api_key" not in st.session_state:
            st.session_state.jimeng_api_key = ""
        if "kling_api_key" not in st.session_state:
            st.session_state.kling_api_key = ""
        if "cogvideox_api_key" not in st.session_state:
            st.session_state.cogvideox_api_key = ""

        jimeng_api_key = st.text_input(
            t("jimeng_api_key_label"),
            type="password",
            value=st.session_state.jimeng_api_key,
            key="jimeng_api_key_input",
            placeholder=t("jimeng_api_key_placeholder")
        )
        if jimeng_api_key != st.session_state.jimeng_api_key:
            st.session_state.jimeng_api_key = jimeng_api_key

        kling_api_key = st.text_input(
            t("kling_api_key_label"),
            type="password",
            value=st.session_state.kling_api_key,
            key="kling_api_key_input",
            placeholder=t("kling_api_key_placeholder")
        )
        if kling_api_key != st.session_state.kling_api_key:
            st.session_state.kling_api_key = kling_api_key

        cogvideox_api_key = st.text_input(
            t("cogvideox_api_key_label"),
            type="password",
            value=st.session_state.cogvideox_api_key,
            key="cogvideox_api_key_input",
            placeholder=t("cogvideox_api_key_placeholder")
        )
        if cogvideox_api_key != st.session_state.cogvideox_api_key:
            st.session_state.cogvideox_api_key = cogvideox_api_key

        # 显示配置状态
        any_configured = jimeng_api_key or kling_api_key or cogvideox_api_key
        if any_configured:
            configured = []
            if jimeng_api_key:
                configured.append("即梦")
            if kling_api_key:
                configured.append("可灵")
            if cogvideox_api_key:
                configured.append("智谱")
            st.success(f"✅ 已配置: {', '.join(configured)}")
        else:
            st.warning("⚠️ 请配置至少一个视频生成平台的 API Key")

        st.divider()
        st.header(t("agents_info"))
        st.info("\n".join([
            t("agent_web"), t("agent_copy"), t("agent_social"), t("agent_seo"),
            t("agent_translate"), t("agent_data"), t("agent_video"), t("agent_xhs"), t("agent_polish"),
        ]))

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        t("tab1"), t("tab2"), t("tab3"), t("tab4"),
        t("tab5"), t("tab6"), t("tab7"), t("tab8"),
        t("tab9"), t("tab10"), t("tab11"),
    ])

    # ── Tab 1: Content Creation ───────────────────────────────────────────────
    with tab1:
        st.header(t("create_title"))
        col1, col2 = st.columns(2)
        with col1:
            topic = st.text_input(t("topic_label"), placeholder=t("topic_placeholder"))
            platform = st.selectbox(t("platform_label"), t("platforms"))
        with col2:
            content_type = st.selectbox(t("content_type_label"), t("content_types"))
            tone = st.selectbox(t("tone_label"), t("tones"))
        additional_info = st.text_area(t("additional_label"), placeholder=t("additional_placeholder"))

        if st.button(t("btn_create"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            with st.spinner(t("creating")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("create", topic=topic, platform=platform, content_type=content_type, tone=tone, additional_info=additional_info)
                try:
                    result = agents["content_team"].run(p, stream=False)
                    st.divider()
                    st.subheader(t("result_title"))
                    st.markdown(result.content)
                    save_history(t("tab1").split(" ", 1)[-1], f"{topic} - {platform}", result.content)
                    st.download_button(t("btn_download"), data=result.content, file_name=f"{topic}_{platform}_{datetime.now().strftime('%Y%m%d')}.md", mime="text/markdown")
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 2: Trend Analysis ─────────────────────────────────────────────────
    with tab2:
        st.header(t("trend_title"))
        industry = st.text_input(t("industry_label"), placeholder=t("industry_placeholder"))
        if st.button(t("btn_trend"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            with st.spinner(t("analyzing")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("trend", industry=industry)
                try:
                    result = agents["web_researcher"].run(p, stream=False)
                    st.subheader(t("trend_result"))
                    st.markdown(result.content)
                    save_history(t("tab2").split(" ", 1)[-1], industry, result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))
                    st.info(t("trend_hint"))

    # ── Tab 3: Content Calendar ───────────────────────────────────────────────
    with tab3:
        st.header(t("calendar_title"))
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(t("start_date"))
        with col2:
            days = st.number_input(t("days_label"), min_value=7, max_value=30, value=14)
        industry_cal = st.text_input(t("industry_label"), placeholder=t("industry_placeholder"), key="cal_industry")
        if st.button(t("btn_calendar"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            with st.spinner(t("generating_calendar")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("calendar", industry_cal=industry_cal, days=days, start_date=start_date)
                try:
                    result = agents["copywriter"].run(p, stream=False)
                    st.subheader(t("calendar_result"))
                    st.markdown(result.content)
                    save_history(t("tab3").split(" ", 1)[-1], f"{industry_cal} - {days}d", result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 4: Translation ────────────────────────────────────────────────────
    with tab4:
        st.header(t("translate_title"))
        col1, col2 = st.columns(2)
        lang_list = ["中文", "English", "日本語", "한국어", "Français", "Deutsch", "Español"]
        with col1:
            source_lang = st.selectbox(t("source_lang"), lang_list, index=0)
        with col2:
            target_lang = st.selectbox(t("target_lang"), lang_list, index=1)
        source_text = st.text_area(t("source_text_label"), placeholder=t("source_text_placeholder"), height=150)
        if st.button(t("btn_translate"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            if not source_text:
                st.warning(t("error_input_required")); return
            with st.spinner(t("translating")):
                agents = get_agents(openai_api_key, api_base_url)
                p = f"Translate the following {source_lang} text to {target_lang}, preserving the original style and tone:\n\n{source_text}"
                try:
                    result = agents["translator"].run(p, stream=False)
                    st.subheader(t("translate_result"))
                    st.text_area(t("translation_label"), value=result.content, height=200)
                    save_history(t("tab4").split(" ", 1)[-1], f"{source_lang} → {target_lang}", result.content)
                    st.download_button(t("btn_download_translation"), data=result.content, file_name=f"translation_{datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain")
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 5: Data Analysis ──────────────────────────────────────────────────
    with tab5:
        st.header(t("data_title"))
        data_text = st.text_area(t("data_label"), placeholder=t("data_placeholder"), height=150)
        analysis_type = st.selectbox(t("analysis_type_label"), t("analysis_types"))
        if st.button(t("btn_analyze"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            if not data_text:
                st.warning(t("error_input_required")); return
            with st.spinner(t("analyzing_data")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("data", analysis_type=analysis_type, data_text=data_text)
                try:
                    result = agents["data_analyst"].run(p, stream=False)
                    st.subheader(t("data_result"))
                    st.markdown(result.content)
                    save_history(t("tab5").split(" ", 1)[-1], analysis_type, result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 6: Video Script ───────────────────────────────────────────────────
    with tab6:
        st.header(t("video_title"))
        video_topic = st.text_input(t("video_topic_label"), placeholder=t("video_topic_placeholder"))
        video_type = st.selectbox(t("video_type_label"), t("video_types"))
        video_platform = st.selectbox(t("video_platform_label"), t("video_platforms"))
        video_duration = st.selectbox(t("video_duration_label"), t("video_durations"))
        video_details = st.text_area(t("video_details_label"), placeholder=t("video_details_placeholder"), height=100)
        if st.button(t("btn_video"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            if not video_topic:
                st.warning(t("error_input_required")); return
            with st.spinner(t("generating_video")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("video", video_type=video_type, video_topic=video_topic, video_platform=video_platform, video_duration=video_duration, video_details=video_details)
                try:
                    result = agents["video_scriptwriter"].run(p, stream=False)
                    st.subheader(t("video_result"))
                    st.markdown(result.content)
                    st.download_button(t("btn_download_video"), data=result.content, file_name=f"video_script_{datetime.now().strftime('%Y%m%d')}.md", mime="text/markdown")
                    save_history(t("tab6").split(" ", 1)[-1], f"{video_topic} - {video_type}", result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 7: Xiaohongshu ────────────────────────────────────────────────────
    with tab7:
        st.header(t("xhs_title"))
        xhs_topic = st.text_input(t("xhs_topic_label"), placeholder=t("xhs_topic_placeholder"))
        xhs_type = st.selectbox(t("xhs_type_label"), t("xhs_types"))
        xhs_style = st.selectbox(t("xhs_style_label"), t("xhs_styles"))
        xhs_keywords = st.text_input(t("xhs_keywords_label"), placeholder=t("xhs_keywords_placeholder"))
        xhs_details = st.text_area(t("xhs_details_label"), placeholder=t("xhs_details_placeholder"), height=100)
        if st.button(t("btn_xhs"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            if not xhs_topic:
                st.warning(t("error_input_required")); return
            with st.spinner(t("generating_xhs")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("xhs", xhs_type=xhs_type, xhs_topic=xhs_topic, xhs_style=xhs_style, xhs_keywords=xhs_keywords, xhs_details=xhs_details)
                try:
                    result = agents["xiaohongshu_expert"].run(p, stream=False)
                    st.subheader(t("xhs_result"))
                    st.markdown(result.content)
                    st.download_button(t("btn_download_xhs"), data=result.content, file_name=f"xhs_{datetime.now().strftime('%Y%m%d')}.md", mime="text/markdown")
                    save_history(t("tab7").split(" ", 1)[-1], xhs_topic, result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 8: English Polish ─────────────────────────────────────────────────
    with tab8:
        st.header(t("polish_title"))
        en_content = st.text_area(t("polish_input_label"), placeholder=t("polish_input_placeholder"), height=200)
        col1, col2 = st.columns(2)
        with col1:
            en_style = st.selectbox(t("polish_style_label"), t("polish_styles"))
        with col2:
            en_level = st.selectbox(t("polish_level_label"), t("polish_levels"))
        en_focus = st.text_input(t("polish_focus_label"), placeholder=t("polish_focus_placeholder"))
        if st.button(t("btn_polish"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            if not en_content:
                st.warning(t("error_input_required")); return
            with st.spinner(t("polishing")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("polish", en_level=en_level, en_content=en_content, en_style=en_style, en_focus=en_focus)
                try:
                    result = agents["english_polisher"].run(p, stream=False)
                    st.subheader(t("polish_result"))
                    st.markdown(result.content)
                    st.download_button(t("btn_download_polish"), data=result.content, file_name=f"polished_{datetime.now().strftime('%Y%m%d')}.md", mime="text/markdown")
                    save_history(t("tab8").split(" ", 1)[-1], en_content[:100], result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 9: SEO ────────────────────────────────────────────────────────────
    with tab9:
        st.header(t("seo_title"))
        seo_url = st.text_input(t("seo_url_label"), placeholder=t("seo_url_placeholder"))
        seo_content = st.text_area(t("seo_content_label"), placeholder=t("seo_content_placeholder"), height=200)
        if st.button(t("btn_seo"), type="primary"):
            if not openai_api_key:
                st.error(t("error_api_key")); return
            input_content = ""
            if seo_url:
                input_content += f"URL: {seo_url}\n\n"
            if seo_content:
                input_content += seo_content
            if not input_content:
                st.warning(t("error_input_required")); return
            with st.spinner(t("analyzing_seo")):
                agents = get_agents(openai_api_key, api_base_url)
                p = prompt("seo", input_content=input_content)
                try:
                    result = agents["seo_expert"].run(p, stream=False)
                    st.subheader(t("seo_result"))
                    st.markdown(result.content)
                    save_history(t("tab9").split(" ", 1)[-1], input_content[:100], result.content)
                except Exception as e:
                    st.error(t("error_generic", error=str(e)))

    # ── Tab 10: History ───────────────────────────────────────────────────────
    with tab10:
        st.header(t("history_title"))
        if st.session_state.history:
            st.write(t("history_count", n=len(st.session_state.history)))
            for record in reversed(st.session_state.history):
                with st.expander(f"**{record['type']}** - {record['timestamp']}"):
                    st.write(f"**{t('history_type')}** {record['type']}")
                    st.write(f"**{t('history_input')}** {record['input']}")
                    st.write(f"**{t('history_output')}**")
                    st.markdown(record['output'])
            if st.button(t("btn_clear_history"), type="secondary"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info(t("no_history"))

    # ── Tab 11: Video Production ──────────────────────────────────────────────
    with tab11:
        st.header(t("video_gen_title"))
        st.caption(t("video_gen_subtitle"))

        try:
            from video_providers import get_provider, VIDEO_PROVIDERS
        except ImportError:
            st.error("video_providers.py 模块未找到，请确保文件存在。")
            st.stop()

        # 检查哪些平台已配置 API Key
        jimeng_key = st.session_state.get("jimeng_api_key", "")
        kling_key = st.session_state.get("kling_api_key", "")
        cogvideox_key = st.session_state.get("cogvideox_api_key", "")

        available_providers = []
        if jimeng_key:
            available_providers.append(("jimeng", "即梦 (Jimeng)"))
        if kling_key:
            available_providers.append(("kling", "可灵 (Kling)"))
        if cogvideox_key:
            available_providers.append(("cogvideox", "智谱 (CogVideoX)"))

        if not available_providers:
            st.warning("⚠️ 请在左侧边栏配置至少一个视频生成平台的 API Key")
            st.info("支持的平台：即梦、可灵、智谱")
        else:
            # Platform selection
            provider_names = [p[1] for p in available_providers]
            provider_keys = [p[0] for p in available_providers]
            selected_idx = st.selectbox(
                t("video_provider_label"),
                options=range(len(provider_names)),
                format_func=lambda x: provider_names[x]
            )
            selected_provider_key = provider_keys[selected_idx]
            provider_info = VIDEO_PROVIDERS[selected_provider_key]
            st.caption(provider_info["description"])

            # 获取对应的 API Key
            api_key_map = {
                "jimeng": jimeng_key,
                "kling": kling_key,
                "cogvideox": cogvideox_key
            }
            client = get_provider(selected_provider_key, api_key_map[selected_provider_key])

            # Mode selection
            video_mode = st.radio(
                t("video_mode_label"),
                t("video_modes"),
                horizontal=True
            )

            # Common parameters
            duration_options = {"3秒": 3, "5秒": 5, "10秒": 10}
            duration = st.selectbox(t("video_duration_label"), options=t("video_durations"))
            duration_seconds = duration_options[duration]

            aspect_options = {"16:9 横屏": "16:9", "9:16 竖屏": "9:16", "1:1 方形": "1:1"}
            aspect = st.selectbox(t("video_aspect_label"), options=t("video_aspects"))
            aspect_ratio = aspect_options[aspect]

            # ── Mode: Text to Video ────────────────────────────────────────
            if video_mode == t("video_modes")[0]:
                video_text = st.text_area(
                    t("video_text_label"),
                    placeholder=t("video_text_placeholder"),
                    height=150
                )

                if st.button(t("btn_generate_video"), type="primary", key="btn_text2video"):
                    if not video_text:
                        st.error(t("error_input_required"))
                    else:
                        with st.spinner(t("generating_video")):
                            try:
                                import requests as req
                                task_id = client.text_to_video(
                                    prompt=video_text,
                                    duration=duration_seconds,
                                    aspect_ratio=aspect_ratio
                                )
                                status = client.wait_for_video(task_id)

                                if status.get("status") == "completed":
                                    video_url = status.get("video_url")
                                    st.subheader(t("video_result"))
                                    st.video(video_url)
                                    st.success(t("video_status_ready"))

                                    st.download_button(
                                        t("btn_download_video"),
                                        data=req.get(video_url).content,
                                        file_name=f"video_{task_id}.mp4",
                                        mime="video/mp4"
                                    )
                                    save_history(t("tab11").split(" ", 1)[-1], video_text[:100], f"Video: {video_url}")
                                else:
                                    st.error(t("video_status_failed"))
                            except Exception as e:
                                st.error(t("error_generic", error=str(e)))

            # ── Mode: Image to Video ───────────────────────────────────────
            elif video_mode == t("video_modes")[1]:
                uploaded_image = st.file_uploader(
                    t("video_image_label"),
                    type=["jpg", "jpeg", "png"],
                    help=t("video_image_help")
                )
                if uploaded_image:
                    st.image(uploaded_image, caption="首帧图片预览", use_container_width=True)

                prompt = st.text_input(
                    t("video_prompt_label"),
                    placeholder=t("video_prompt_placeholder")
                )

                if st.button(t("btn_generate_video"), type="primary", key="btn_img2video"):
                    if not uploaded_image:
                        st.error(t("error_input_required"))
                    else:
                        with st.spinner(t("generating_video")):
                            try:
                                import requests as req
                                import base64
                                img_bytes = uploaded_image.read()
                                b64 = base64.b64encode(img_bytes).decode()
                                mime = "image/jpeg" if uploaded_image.type == "image/jpeg" else "image/png"
                                image_url = f"data:{mime};base64,{b64}"

                                task_id = client.image_to_video(
                                    image_url=image_url,
                                    prompt=prompt,
                                    duration=duration_seconds,
                                    aspect_ratio=aspect_ratio
                                )
                                status = client.wait_for_video(task_id)

                                if status.get("status") == "completed":
                                    video_url = status.get("video_url")
                                    st.subheader(t("video_result"))
                                    st.video(video_url)
                                    st.success(t("video_status_ready"))

                                    st.download_button(
                                        t("btn_download_video"),
                                        data=req.get(video_url).content,
                                        file_name=f"video_{task_id}.mp4",
                                        mime="video/mp4"
                                    )
                                    save_history(t("tab11").split(" ", 1)[-1], f"Image: {uploaded_image.name}", f"Video: {video_url}")
                                else:
                                    st.error(t("video_status_failed"))
                            except Exception as e:
                                st.error(t("error_generic", error=str(e)))

            # ── Mode: Script to Video ──────────────────────────────────────
            elif video_mode == t("video_modes")[2]:
                st.info(t("script_video_info"))

                num_segments = st.number_input(
                    t("script_segments_label"),
                    min_value=1,
                    max_value=10,
                    value=3
                )

                segments = []
                for i in range(num_segments):
                    with st.expander(f"{t('segment')} {i + 1}"):
                        segment_prompt = st.text_area(
                            t("segment_prompt_label"),
                            placeholder=t("segment_prompt_placeholder"),
                            key=f"segment_prompt_{i}"
                        )
                        segments.append({"prompt": segment_prompt})

                if st.button(t("btn_generate_video"), type="primary", key="btn_script2video"):
                    valid_segments = [s for s in segments if s.get("prompt")]
                    if not valid_segments:
                        st.error(t("error_input_required"))
                    else:
                        with st.spinner(t("generating_video")):
                            try:
                                import requests as req
                                # 逐段生成视频
                                task_ids = []
                                for seg in valid_segments:
                                    task_id = client.text_to_video(
                                        prompt=seg["prompt"],
                                        duration=duration_seconds,
                                        aspect_ratio=aspect_ratio
                                    )
                                    task_ids.append(task_id)

                                st.info(f"已提交 {len(task_ids)} 个视频片段，正在逐段生成...")

                                results = client.wait_for_videos(task_ids)

                                completed = [r for r in results if r.get("status") == "completed"]
                                if completed:
                                    st.subheader(t("video_result"))
                                    for idx, r in enumerate(completed):
                                        video_url = r.get("video_url")
                                        if video_url:
                                            st.markdown(f"**{t('segment')} {idx + 1}**")
                                            st.video(video_url)

                                    st.success(t("video_status_ready"))
                                    save_history(
                                        t("tab11").split(" ", 1)[-1],
                                        f"Script: {len(valid_segments)} segments",
                                        f"Videos: {len(completed)} generated"
                                    )
                                else:
                                    st.error(t("video_status_failed"))
                            except Exception as e:
                                st.error(t("error_generic", error=str(e)))

            # ── Mode: Digital Avatar ─────────────────────────────────────
            else:
                if selected_provider_key != "kling":
                    st.warning(t("avatar_no_available"))
                    st.info("数字分身功能目前仅支持可灵 (Kling) 平台。请在左侧边栏配置可灵 API Key。")
                else:
                    st.info("🎭 数字分身：输入文字，让数字分身为你说话")

                    # 加载数字分身列表
                    with st.spinner(t("avatar_loading")):
                        try:
                            avatars = client.get_avatars()
                        except Exception:
                            avatars = []

                    if not avatars:
                        st.warning("未找到可用的数字分身。请先在可灵平台创建数字分身。")
                        st.markdown("""
**如何创建数字分身：**
1. 访问 [可灵AI官网](https://klingai.com)
2. 登录后进入"数字分身"功能
3. 上传照片或视频，创建你的数字分身
4. 创建完成后，返回此页面刷新即可看到
                        """)
                    else:
                        # 选择数字分身
                        avatar_options = {a["avatar_id"]: a.get("name", a["avatar_id"]) for a in avatars}
                        selected_avatar = st.selectbox(
                            t("avatar_select_label"),
                            options=list(avatar_options.keys()),
                            format_func=lambda x: avatar_options[x]
                        )

                        # 输入脚本
                        avatar_script = st.text_area(
                            t("avatar_script_label"),
                            placeholder=t("avatar_script_placeholder"),
                            height=150
                        )

                        if st.button(t("btn_generate_video"), type="primary", key="btn_avatar"):
                            if not avatar_script:
                                st.error(t("error_input_required"))
                            else:
                                with st.spinner(t("generating_video")):
                                    try:
                                        import requests as req
                                        task_id = client.avatar_video(
                                            avatar_id=selected_avatar,
                                            script=avatar_script,
                                            aspect_ratio=aspect_ratio
                                        )
                                        status = client.wait_for_video(task_id)

                                        if status.get("status") == "completed":
                                            video_url = status.get("video_url")
                                            st.subheader(t("video_result"))
                                            st.video(video_url)
                                            st.success(t("video_status_ready"))

                                            st.download_button(
                                                t("btn_download_video"),
                                                data=req.get(video_url).content,
                                                file_name=f"avatar_video_{task_id}.mp4",
                                                mime="video/mp4"
                                            )
                                            save_history(t("tab11").split(" ", 1)[-1], f"Avatar: {avatar_script[:50]}", f"Video: {video_url}")
                                        else:
                                            st.error(t("video_status_failed"))
                                    except Exception as e:
                                        st.error(t("error_generic", error=str(e)))

if __name__ == "__main__":
    main()
