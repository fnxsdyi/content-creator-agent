from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
import streamlit as st
from datetime import datetime
from openai import OpenAI
import hashlib

# Setup database for storage
db = SqliteDb(db_file="agents.db")

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

    content_team = Team(
        name="Content Creation Team",
        model=OpenAIChat(**model_config),
        members=[web_researcher, copywriter, social_media, seo_expert, translator, data_analyst, image_describer],
        debug_mode=True,
        markdown=True,
    )

    return web_researcher, copywriter, social_media, seo_expert, translator, data_analyst, image_describer, content_team

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
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        api_base_url = st.text_input("API Base URL", placeholder="https://api.openai.com/v1", value="https://api.openai.com/v1")
        
        st.divider()
        st.header("📋 Agent 信息")
        st.info("""
        **Web Researcher** - 搜索热点
        **Copywriter** - 文案创作
        **Social Media** - 社媒优化
        **SEO Expert** - 搜索优化
        **Translator** - 多语言翻译
        **Data Analyst** - 数据分析
        **Image Describer** - 图片描述
        """)
    
    # Main content
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["📝 内容创作", "📊 热点分析", "📅 内容日历", "🌐 多语言翻译", "📈 数据分析", "🎨 图片生成", "🔍 SEO 分析", "📜 历史记录"])
    
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
                _, _, _, _, _, _, _, content_team = create_agents(openai_api_key, api_base_url)
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
                web_researcher, _, _, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请分析"{industry}"行业的当前热点和趋势：
                
                1. 搜索最新的行业动态
                2. 总结5-10个关键热点
                3. 分析每个热点的传播潜力
                4. 给出内容创作建议
                
                用清晰的列表和表格展示结果。
                """
                
                result = web_researcher.run(prompt, stream=False)
                
                st.subheader("📊 热点分析结果")
                st.markdown(result.content)
                
                # Save to history
                save_history("热点分析", industry, result.content)
    
    with tab3:
        st.header("内容日历规划")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期")
        with col2:
            days = st.number_input("规划天数", min_value=7, max_value=30, value=14)
        
        if st.button("📅 生成日历", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            with st.spinner("正在生成内容日历..."):
                _, copywriter, _, _, _, _, _, _ = create_agents(openai_api_key, api_base_url)
                prompt = f"""
                请为"{industry}"行业创建{days}天的内容发布日历：
                
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
                save_history("内容日历", f"{industry} - {days}天", result.content)
    
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
                _, _, _, _, translator, _, _, _ = create_agents(openai_api_key, api_base_url)
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
                _, _, _, _, _, data_analyst, _, _ = create_agents(openai_api_key, api_base_url)
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
        st.header("🎨 AI 图片生成")
        
        # Check if API provider supports image generation
        if "api2d" in api_base_url.lower():
            st.warning("⚠️ API2D 不支持图片生成功能（仅支持聊天和嵌入）")
            st.info("如需使用图片生成，请配置支持 DALL-E 的 API，例如：\n- OpenAI 官方 API\n- 其他支持 /images/generations 的代理")
        else:
            image_prompt = st.text_area("描述你想生成的图片", placeholder="例如：一只可爱的猫咪坐在窗台上，阳光洒在身上，水彩画风格...", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                image_size = st.selectbox("图片尺寸", ["1024x1024", "1024x1792", "1792x1024"])
            with col2:
                image_quality = st.selectbox("图片质量", ["standard", "hd"])
            
            if st.button("🎨 生成图片", type="primary"):
                if not openai_api_key:
                    st.error("请先输入 OpenAI API Key")
                    return
                
                if not image_prompt:
                    st.warning("请输入图片描述")
                    return
                
                with st.spinner("生成图片中..."):
                    try:
                        client = OpenAI(api_key=openai_api_key, base_url=api_base_url, timeout=180.0)
                        response = client.images.generate(
                            model="dall-e-3",
                            prompt=image_prompt,
                            size=image_size,
                            quality=image_quality,
                            n=1,
                        )
                        
                        image_url = response.data[0].url
                        revised_prompt = response.data[0].revised_prompt
                        
                        st.image(image_url, caption="AI 生成的图片", use_container_width=True)
                        st.info(f"**优化后的提示词：** {revised_prompt}")
                        
                        # Save to history
                        save_history("图片生成", image_prompt, f"已生成图片: {image_url[:50]}...")
                        
                        # Download image
                        st.markdown(f"[📥 下载图片]({image_url})")
                        
                    except Exception as e:
                        st.error(f"生成图片时出错：{str(e)}")
    
    with tab7:
        st.header("🔍 SEO 分析")
        
        seo_url = st.text_input("输入网址或内容", placeholder="输入网址或粘贴文章内容进行SEO分析...")
        seo_content = st.text_area("或直接输入文章内容", placeholder="粘贴文章内容...", height=150)
        
        if st.button("🔍 开始分析", type="primary"):
            if not openai_api_key:
                st.error("请先输入 OpenAI API Key")
                return
            
            input_content = seo_url if seo_url else seo_content
            if not input_content:
                st.warning("请输入内容")
                return
            
            with st.spinner("SEO 分析中..."):
                _, _, _, seo_expert, _, _, _, _ = create_agents(openai_api_key, api_base_url)
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
                
                result = seo_expert.run(prompt, stream=False)
                
                st.subheader("📊 SEO 分析报告")
                st.markdown(result.content)
                
                # Save to history
                save_history("SEO分析", input_content[:100], result.content)
    
    with tab8:
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
