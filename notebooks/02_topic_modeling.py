import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 加载论文数据
df = pd.read_csv('../data/raw/arxiv_papers.csv')
texts = df['summary'].dropna().tolist()

print(f"加载了 {len(texts)} 篇论文")

# 尝试使用BERTopic
try:
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer
    
    vectorizer = CountVectorizer(ngram_range=(1, 2), stop_words="english", min_df=2)
    
    topic_model = BERTopic(
        vectorizer_model=vectorizer,
        language="english",
        nr_topics=8,
        min_topic_size=5,
        verbose=True
    )
    
    topics, probs = topic_model.fit_transform(texts)
    
    # 查看主题
    topic_info = topic_model.get_topic_info()
    print("\n主题信息:")
    print(topic_info.head(10))
    
    # 为每个主题命名（手工标注）
    topic_names = {
        -1: "Other",
        0: "VLA_Models",
        1: "Dexterous_Manipulation",
        2: "Humanoid_Control",
        3: "Sim_to_Real",
        4: "Robot_Learning",
        5: "Grasping",
        6: "Navigation",
        7: "Multi_Modal"
    }
    
    # 将主题映射到论文
    df['topic_id'] = topics
    df['tech_route'] = df['topic_id'].map(topic_names)
    
    # 保存结果
    df.to_csv('../data/processed/papers_with_topics.csv', index=False)
    topic_model.save('../data/processed/bertopic_model')
    print(f"\n主题模型已保存。论文已分类并保存到 ../data/processed/papers_with_topics.csv")
    print(df[['title', 'topic_id', 'tech_route']].head(10))
    
except Exception as e:
    print(f"BERTopic运行失败: {e}")
    print("降级为关键词匹配分类...")
    
    # 降级方案：关键词匹配
    keywords_map = {
        'VLA_Models': ['vision-language-action', 'VLA', 'multimodal policy', 'language-conditioned'],
        'Dexterous_Manipulation': ['dexterous', 'tactile', 'in-hand', 'multi-fingered', 'shadow hand'],
        'Humanoid_Control': ['humanoid', 'bipedal', 'whole-body', 'Atlas', 'Optimus', 'H1', 'locomotion'],
        'Sim_to_Real': ['sim-to-real', 'domain randomization', 'simulation', 'Isaac Sim', 'transfer'],
        'Robot_Learning': ['reinforcement learning', 'imitation learning', 'behavioral cloning', 'policy'],
        'Grasping': ['grasp', 'grasping', 'pick-and-place', 'grasp detection', 'grasp quality'],
        'Navigation': ['navigation', 'path planning', 'SLAM', 'exploration', 'mobile robot'],
        'Multi_Modal': ['multi-modal', 'vision-language', 'perception', 'scene understanding']
    }
    
    def classify_by_keywords(text):
        text_lower = str(text).lower()
        scores = {}
        for route, keywords in keywords_map.items():
            scores[route] = sum(1 for kw in keywords if kw.lower() in text_lower)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else 'Other'
    
    df['tech_route'] = df['summary'].apply(classify_by_keywords)
    df['topic_id'] = pd.Categorical(df['tech_route']).codes
    
    df.to_csv('../data/processed/papers_with_topics.csv', index=False)
    print(f"\n关键词分类完成。论文已保存到 ../data/processed/papers_with_topics.csv")
    print(df['tech_route'].value_counts())
