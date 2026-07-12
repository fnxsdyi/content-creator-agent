"""
Supabase 配置说明
================

1. 访问 https://supabase.com 注册账号
2. 创建新项目
3. 在 Settings > API 中获取以下信息：
   - Project URL
   - Anon Key (public)
4. 在 SQL Editor 中执行以下 SQL 创建表：

-- 用户历史记录表
CREATE TABLE user_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    input_data TEXT,
    output_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 用户偏好表
CREATE TABLE user_preferences (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT UNIQUE NOT NULL,
    default_platform TEXT DEFAULT '微信公众号',
    default_tone TEXT DEFAULT '专业正式',
    preferred_languages TEXT[] DEFAULT ARRAY['中文', 'English'],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用 RLS
ALTER TABLE user_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

-- 创建策略
CREATE POLICY "Users can view own history" ON user_history
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can insert own history" ON user_history
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can view own preferences" ON user_preferences
    FOR SELECT USING (auth.uid()::text = user_id);

CREATE POLICY "Users can upsert own preferences" ON user_preferences
    FOR INSERT WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own preferences" ON user_preferences
    FOR UPDATE USING (auth.uid()::text = user_id);

5. 将以下信息填入 .env 文件：
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
"""
