from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
import streamlit as st
from datetime import datetime
import json

# Setup database for storage
db = SqliteDb(db_file="agents.db")

# Define Agents
web_researcher = Agent(
    name="Web Researcher",
    role="搜索网络热点和趋势信息",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

copywriter = Agent(
    name="Copywriter",
    role="创建吸引人的文案和标题",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    markdown=True,
)

social_media = Agent(
    name="Social Media Expert",
    role="优化内容适合不同社交平台",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    markdown=True,
)

seo_expert = Agent(
    name="SEO Expert",
    role="优化内容的搜索排名和关键词",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    markdown=True,
)

translator = Agent(
    name="Translator",
    role="专业翻译，支持中英日韩等多种语言互译",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    markdown=True,
)

data_analyst = Agent(
    name="Data Analyst",
    role="分析数据趋势，生成数据报告和可视化建议",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    add_history_to_context=True,
    markdown=True,
)

image_describer = Agent(
    name="Image Describer",
    role="描述图片内容，生成图片标题和Alt文本",
    model=OpenAIChat(id="gpt-4o", model_kwargs={"vision": True}),
    db=db,
    add_history_to_context=True,
    markdown=True,
)

# Create Agent Team
content_team = Team(
    name="Content Creation Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[web_researcher, copywriter, social_media, seo_expert, translator, data_analyst, image_describer],
    debug_mode=True,
    markdown=True,
)

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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 内容创作", "📊 热点分析", "📅 内容日历", "🌐 多语言翻译", "📈 数据分析"])
    
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
                prompt = f"请将以下{source_lang}内容翻译为{target_lang}，保持原文的风格和语气：\n\n{source_text}"
                result = translator.run(prompt, stream=False)
                
                st.subheader("翻译结果")
                st.text_area("译文", value=result.content, height=200)
                
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

if __name__ == "__main__":
    main()
