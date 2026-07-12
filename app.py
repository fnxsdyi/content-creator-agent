from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
import streamlit as st
from datetime import datetime
from openai import OpenAI
import hashlib
import os
import json

# Setup database for storage
db = SqliteDb(db_file="agents.db")

# Config file path
CONFIG_FILE = "config.json"

def load_config():
    """Load config from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """Save config to file"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False)

# Load saved config
saved_config = load_config()

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]

def save_history(action_type, input_data, output_data):
    """Save user activity to history"""
    st.session_state.history.append({
        "id": len(st.session_state.history) + 1,
        "type": action_type,
        "input": input_data[:200] + "..." if len(input_data) > 200 else input_data,
        "output": output_data[:200] + "..." if len(output_data) > 200 else output_data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def create_agents(api_key, base_url):
    """Create agents with API configuration"""
    model_config = {"id": "gpt-4o", "api_key": api_key, "base_url": base_url}
    
    web_researcher = Agent(
        name="Web Researcher",
        role="搜索网络热点和趋势信息",
        model=OpenAIChat(**model_config),
        tools=[DuckDuckGoTools()],
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    copywriter = Agent(
        name="Copywriter",
        role="创建吸引人的文案和标题",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    social_media = Agent(
        name="Social Media Expert",
        role="优化内容适合不同社交平台",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    seo_expert = Agent(
        name="SEO Expert",
        role="优化内容的搜索排名和关键词",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    translator = Agent(
        name="Translator",
        role="专业翻译，支持中英日韩等多种语言互译",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    data_analyst = Agent(
        name="Data Analyst",
        role="分析数据趋势，生成数据报告和可视化建议",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    image_describer = Agent(
        name="Image Describer",
        role="描述图片内容，生成图片标题和Alt文本",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    video_scriptwriter = Agent(
        name="Video Scriptwriter",
        role="创作短视频脚本，包括口播稿、分镜脚本、带货文案",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    xiaohongshu_expert = Agent(
        name="Xiaohongshu Expert",
        role="创作小红书爆款笔记，擅长标题、正文、标签优化",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    english_polisher = Agent(
        name="English Polisher",
        role="润色英文内容，提升语法准确性、表达地道性和可读性",
        model=OpenAIChat(**model_config),
        db=db,
        add_history_to_context=True,
        markdown=True,
    )

    content_team = Team(
        name="Content Creation Team",
        model=OpenAIChat(**model_config),
        members=[web_researcher, copywriter, social_media, seo_expert, translator, data_analyst, image_describer, video_scriptwriter, xiaohongshu_expert, english_polisher],
        debug_mode=True,
        markdown=True,
    )

    return web_researcher, copywriter, social_media, seo_expert, translator, data_analyst, image_describer, video_scriptwriter, xiaohongshu_expert, english_polisher, content_team

def main():
    st.set_page_config(
        page_title="AI Content Creator Agent",
        page_icon="✍️",
        layout="wide"
    )
    
    st.title("✍️ AI Content Creator Agent")
    st.caption("多Agent协作的内容创作助手")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ 设置")
        
        # API Key with persistence
        api_key_value = saved_config.get("api_key", "")
        base_url_value = saved_config.get("base_url", "https://api.openai.com/v1")
        
        openai_api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            value=api_key_value,
            key="api_key_input"
        )
        api_base_url = st.text_input(
            "API Base URL", 
            placeholder="https://api.openai.com/v1",
            value=base_url_value,
            key="base_url_input"
        )
        
        # Auto-save config when values change
        if openai_api_key != api_key_value or api_base_url != base_url_value:
            save_config({"api_key": openai_api_key, "base_url": api_base_url})
        
        # Manual save button
        if st.button("💾 保存配置", type="secondary"):
            save_config({"api_key": openai_api_key, "base_url": api_base_url})
            st.success("配置已保存！")
        
        # Show status
        if openai_api_key:
            st.success("✅ API Key 已配置")
        else:
            st.warning("⚠️ 请配置 API Key")
        
        st.divider()
        st.header("📋 Agent 信息")
        st.info("""
        **Web Researcher** - 搜索热点
        **Copywriter** - 文案创作
        **Social Media** - 社媒优化
        **SEO Expert** - 搜索优化
        **Translator** - 多语言翻译
        **Data Analyst** - 数据分析
        **Video Scriptwriter** - 视频脚本
        **Xiaohongshu Expert** - 小红书爆款
        **English Polisher** - 英文润色
        """)
    
    # Main content
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "📝 内容创作", "📊 热点分析", "📅 内容日历", "🌐 多语言翻译", 
        "📈 数据分析", "🎬 视频脚本", "📱 小红书爆款", "🔤 英文润色", 
        "🔍 SEO 分析", "📜 历史记录"
    ])
    
    with tab1:
        st.header("创建内容")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("主题/产品名称", placeholder="例如：AI写作助手")
            platform = st.selectbox("目标平台", ["微信公众号", "小红书", "抖音", "知乎", "微博", "LinkedIn", "Twitter"])
        
        with col2:
            content_type = st.selectbox("内容类型", ["产品介绍", "技术博客", "营销文案", "教程指南", "行业分析", "新闻稿"])
            tone = st.selectbox("语气风格", ["专业正式", "轻松活泼", "亲切友好", "幽默搞笑", "严肃认真"])
        
        additional_info = st.text_area("补充信息", placeholder="任何需要包含的特定信息、关键词或要求...")
        
        if st.button("🚀 开始创作", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            with st.spinner("AI Agent 团队正在创作中..."):
                _, _, _, _, _, _, _, _, _, _, content_team = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请为以下内容创建完整的创作方案：
                
                主题：{topic}
                平台：{platform}
                内容类型：{content_type}
                语气风格：{tone}
                补充信息：{additional_info}
                
                请按以下步骤协作：
                1. Web Researcher: 先搜索相关热点和趋势
                2. Copywriter: 根据搜索结果创作文案
                3. Social Media Expert: 优化为适合{platform}的形式
                4. SEO Expert: 添加SEO优化建议
                
                最终输出完整的、可直接使用的{content_type}内容。
                """
                
                result = content_team.run(prompt, stream=False)
                
                st.divider()
                st.subheader("✨ 创作结果")
                st.markdown(result.content)
                
                # Save to history
                save_history("内容创作", f"{topic} - {platform}", result.content)
                
                # Download button
                st.download_button(
                    label="📥 下载内容",
                    data=result.content,
                    file_name=f"{topic}_{platform}_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    
    with tab2:
        st.header("热点分析")
        
        industry = st.text_input("行业/领域", placeholder="例如：人工智能、电商、教育")
        
        if st.button("🔍 分析热点", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            with st.spinner("正在分析热点..."):
                web_researcher, _, _, _, _, _, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请分析"{industry}"行业的当前热点和趋势：
                
                1. 搜索最新的行业动态
                2. 总结5-10个关键热点
                3. 分析每个热点的传播潜力
                4. 给出内容创作建议
                
                用清晰的列表和表格展示结果。
                """
                
                try:
                    result = web_researcher.run(prompt, stream=False)
                    
                    st.subheader("📊 热点分析结果")
                    st.markdown(result.content)
                    
                    # Save to history
                    save_history("热点分析", industry, result.content)
                except Exception as e:
                    st.error(f"分析失败：{str(e)}")
                    st.info("提示：如果网络不稳定，建议使用英文关键词进行搜索")
    
    with tab3:
        st.header("内容日历规划")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期")
        with col2:
            days = st.number_input("规划天数", min_value=7, max_value=30, value=14)
        
        industry_cal = st.text_input("行业/领域", placeholder="例如：人工智能、电商、教育", key="cal_industry")
        
        if st.button("📅 生成日历", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            with st.spinner("正在生成内容日历..."):
                _, copywriter, _, _, _, _, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请为"{industry_cal}"行业创建{days}天的内容发布日历：
                
                从{start_date}开始，每天规划：
                - 发布时间
                - 内容主题
                - 内容类型
                - 目标平台
                - 创作要点
                
                用表格形式展示，并确保内容有节奏感（不要每天都发硬广）。
                """
                
                result = copywriter.run(prompt, stream=False)
                
                st.subheader("📅 内容日历")
                st.markdown(result.content)
                
                # Save to history
                save_history("内容日历", f"{industry_cal} - {days}天", result.content)
    
    with tab4:
        st.header("🌐 多语言翻译")
        
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox("源语言", ["中文", "English", "日本語", "한국어", "Français", "Deutsch", "Español"])
        with col2:
            target_lang = st.selectbox("目标语言", ["English", "中文", "日本語", "한국어", "Français", "Deutsch", "Español"])
        
        source_text = st.text_area("输入要翻译的内容", placeholder="请粘贴或输入要翻译的文本...", height=150)
        
        if st.button("🔄 开始翻译", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            if not source_text:
                st.warning("请输入要翻译的内容")
                return
            
            with st.spinner("翻译中..."):
                _, _, _, _, translator, _, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"请将以下{source_lang}内容翻译为{target_lang}，保持原文的风格和语气：\n\n{source_text}"
                result = translator.run(prompt, stream=False)
                
                st.subheader("翻译结果")
                st.text_area("译文", value=result.content, height=200)
                
                # Save to history
                save_history("多语言翻译", f"{source_lang} → {target_lang}", result.content)
                
                st.download_button(
                    label="📥 下载译文",
                    data=result.content,
                    file_name=f"translation_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
    
    with tab5:
        st.header("📈 数据分析")
        
        data_text = st.text_area("输入数据或描述", placeholder="粘贴数据、报告内容，或描述你想分析的问题...\n\n例如：\n- 上周销售额：周一12万，周二15万，周三18万...\n- 用户反馈：40%觉得价格高，30%觉得功能不足...", height=150)
        
        analysis_type = st.selectbox("分析类型", ["趋势分析", "对比分析", "问题诊断", "建议生成", "综合分析"])
        
        if st.button("📊 开始分析", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            if not data_text:
                st.warning("请输入数据或描述")
                return
            
            with st.spinner("分析中..."):
                _, _, _, _, _, data_analyst, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请对以下内容进行{analysis_type}：
                
                {data_text}
                
                请提供：
                1. 关键发现
                2. 数据解读
                3. 趋势/模式识别
                4. 可执行建议
                
                用清晰的结构和表格展示结果。
                """
                result = data_analyst.run(prompt, stream=False)
                
                st.subheader("📊 分析报告")
                st.markdown(result.content)
                
                # Save to history
                save_history("数据分析", analysis_type, result.content)
    
    with tab6:
        st.header("🎬 视频脚本创作")
        
        video_topic = st.text_input("视频主题", placeholder="例如：AI写作助手产品介绍")
        video_type = st.selectbox("视频类型", ["口播稿", "分镜脚本", "带货文案", "教程脚本", "故事脚本"])
        video_platform = st.selectbox("目标平台", ["抖音", "快手", "B站", "YouTube", "视频号"])
        video_duration = st.selectbox("视频时长", ["15秒", "30秒", "1分钟", "3分钟", "5分钟"])
        
        video_details = st.text_area("补充说明", placeholder="视频风格、目标受众、需要包含的要点等...", height=100)
        
        if st.button("🎬 生成脚本", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            if not video_topic:
                st.warning("请输入视频主题")
                return
            
            with st.spinner("生成视频脚本中..."):
                _, _, _, _, _, _, _, video_scriptwriter, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请为以下视频创作{video_type}：
                
                主题：{video_topic}
                平台：{video_platform}
                时长：{video_duration}
                补充说明：{video_details}
                
                请提供：
                1. 开场钩子（前3秒抓住观众）
                2. 主体内容（分段展示）
                3. 结尾CTA（引导互动）
                4. 配音建议（语速、语调）
                5. 画面建议（如有分镜）
                
                确保脚本口语化、有节奏感、适合{video_platform}平台风格。
                """
                
                try:
                    result = video_scriptwriter.run(prompt, stream=False)
                    
                    st.subheader("🎬 视频脚本")
                    st.markdown(result.content)
                    
                    st.download_button(
                        label="📥 下载脚本",
                        data=result.content,
                        file_name=f"视频脚本_{video_topic}_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    
                    save_history("视频脚本", f"{video_topic} - {video_type}", result.content)
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")
    
    with tab7:
        st.header("📱 小红书爆款笔记")
        
        xhs_topic = st.text_input("笔记主题", placeholder="例如：平价好物推荐、旅行攻略、美食探店")
        xhs_type = st.selectbox("笔记类型", ["种草推荐", "经验分享", "教程攻略", "测评对比", "日常分享"])
        xhs_style = st.selectbox("风格", ["真诚分享", "干货满满", "轻松活泼", "专业权威", "搞笑幽默"])
        
        xhs_keywords = st.text_input("关键词（可选）", placeholder="例如：平价、学生党、新手友好")
        xhs_details = st.text_area("补充说明", placeholder="产品特点、使用体验、目标人群等...", height=100)
        
        if st.button("📱 生成爆款笔记", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            if not xhs_topic:
                st.warning("请输入笔记主题")
                return
            
            with st.spinner("生成小红书爆款笔记中..."):
                _, _, _, _, _, _, _, _, xiaohongshu_expert, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请为小红书创作一篇爆款{xhs_type}笔记：
                
                主题：{xhs_topic}
                风格：{xhs_style}
                关键词：{xhs_keywords}
                补充说明：{xhs_details}
                
                请提供：
                1. **爆款标题**（3个备选，含emoji，18字以内）
                2. **正文内容**（800-1200字，分段清晰）
                3. **标签推荐**（15-20个相关标签）
                4. **封面建议**（图片风格和构图）
                5. **发布时间建议**
                
                要求：
                - 标题吸引眼球，有数字或痛点
                - 正文有干货、有故事、有互动
                - 多用emoji，排版清晰
                - 结尾引导点赞收藏
                """
                
                try:
                    result = xiaohongshu_expert.run(prompt, stream=False)
                    
                    st.subheader("📱 小红书爆款笔记")
                    st.markdown(result.content)
                    
                    st.download_button(
                        label="📥 下载笔记",
                        data=result.content,
                        file_name=f"小红书笔记_{xhs_topic}_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    
                    save_history("小红书笔记", xhs_topic, result.content)
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")
    
    with tab8:
        st.header("🔤 英文润色")
        
        en_content = st.text_area("输入需要润色的英文内容", placeholder="Paste your English text here...", height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            en_style = st.selectbox("润色风格", ["学术正式", "商务专业", "日常交流", "创意写作", "技术文档"])
        with col2:
            en_level = st.selectbox("润色程度", ["轻度修改（修正语法）", "中度润色（优化表达）", "重度改写（提升质量）"])
        
        en_focus = st.text_input("特殊要求（可选）", placeholder="例如：增加专业术语、简化表达、提升可读性")
        
        if st.button("🔤 开始润色", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            if not en_content:
                st.warning("请输入需要润色的英文内容")
                return
            
            with st.spinner("润色中..."):
                _, _, _, _, _, _, _, _, _, english_polisher, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请对以下英文内容进行{en_level}：
                
                {en_content}
                
                润色风格：{en_style}
                特殊要求：{en_focus}
                
                请提供：
                1. **润色后的内容**（完整版本）
                2. **修改说明**（列出主要修改点和原因）
                3. **语法检查**（如有错误请指出）
                4. **表达建议**（提升地道性的建议）
                
                确保保持原意，同时提升表达质量。
                """
                
                try:
                    result = english_polisher.run(prompt, stream=False)
                    
                    st.subheader("🔤 润色结果")
                    st.markdown(result.content)
                    
                    st.download_button(
                        label="📥 下载润色结果",
                        data=result.content,
                        file_name=f"polished_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown"
                    )
                    
                    save_history("英文润色", en_content[:100], result.content)
                except Exception as e:
                    st.error(f"润色失败：{str(e)}")
    
    with tab9:
        st.header("🔍 SEO 分析")
        
        seo_url = st.text_input("输入网址（可选）", placeholder="例如：https://example.com")
        seo_content = st.text_area("或直接输入文章内容进行SEO分析", placeholder="粘贴文章内容...", height=200)
        
        if st.button("🔍 开始分析", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            # Combine URL and content for analysis
            input_content = ""
            if seo_url:
                input_content += f"网址：{seo_url}\n\n"
            if seo_content:
                input_content += seo_content
            
            if not input_content:
                st.warning("请输入网址或文章内容")
                return
            
            with st.spinner("SEO 分析中..."):
                _, _, _, seo_expert, _, _, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请对以下内容进行全面的 SEO 分析：
                
                {input_content}
                
                请提供：
                1. **关键词分析**：核心关键词、长尾关键词建议
                2. **标题优化**：标题长度、吸引力、关键词包含情况
                3. **内容结构**：段落划分、标题层级、可读性
                4. **Meta 描述**：建议的 meta description
                5. **SEO 评分**：0-100分，附改进建议
                6. **竞品关键词**：相关热门搜索词
                
                用清晰的结构展示，包含具体的优化建议。
                """
                
                try:
                    result = seo_expert.run(prompt, stream=False)
                    
                    st.subheader("📊 SEO 分析报告")
                    st.markdown(result.content)
                    
                    # Save to history
                    save_history("SEO分析", input_content[:100], result.content)
                except Exception as e:
                    st.error(f"分析失败：{str(e)}")
    
    with tab10:
        st.header("📜 历史记录")
        
        if st.session_state.history:
            st.write(f"共 {len(st.session_state.history)} 条记录")
            
            for record in reversed(st.session_state.history):
                with st.expander(f"**{record['type']}** - {record['timestamp']}"):
                    st.write(f"**类型：** {record['type']}")
                    st.write(f"**输入：** {record['input']}")
                    st.write(f"**输出：**")
                    st.markdown(record['output'])
            
            if st.button("🗑️ 清空历史", type="secondary"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("暂无历史记录")

if __name__ == "__main__":
    main()
