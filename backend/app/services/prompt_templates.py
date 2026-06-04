PROMPTS = {
    "study_plan": """你是一位资深的大学生学习规划顾问。请根据以下学生信息，生成一份详细的学习规划。

学生信息：
- 专业：{major}
- 年级：{grade}
- 学习目标：{goal}
- 已有基础：{basics}
- 目标院校：{target_school}

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "overview": "一段简洁的学习规划总述（50字以内）",
  "phases": [
    {{
      "title": "阶段名称",
      "period": "时间段",
      "tasks": ["任务1", "任务2", "任务3"],
      "resources": ["推荐资源1", "推荐资源2"]
    }}
  ],
  "daily_plan": "每日学习计划模板建议",
  "tips": ["建议1", "建议2", "建议3"]
}}

要求：
1. 分3-4个阶段，每阶段2个月左右
2. 任务具体可执行，不要空泛
3. 推荐真实存在的课程/书籍/网站
4. 结合当前年级给出合理建议""",

    "competition_guide": """你是一位经验丰富的竞赛辅导教练。请为以下竞赛生成详细的备赛方案。

竞赛信息：
- 竞赛名称：{competition}
- 参赛角色：{role}
- 距离比赛：{time_remaining}
- 当前水平：{level}

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "intro": "竞赛简介（含时间、赛制、含金量，100字以内）",
  "timeline": [
    {{
      "title": "阶段名称",
      "period": "时间段",
      "tasks": ["具体任务1", "具体任务2", "具体任务3"]
    }}
  ],
  "resources": [
    {{
      "type": "书籍/视频/网站/工具",
      "name": "资源名称",
      "desc": "简要说明"
    }}
  ],
  "tips": ["获奖技巧1", "获奖技巧2", "获奖技巧3"],
  "team_advice": "组队建议（如适用）"
}}

要求：
1. 时间线要与距比赛时间匹配
2. 资源推荐真实存在
3. 技巧要实用具体""",

    "project_name": """你是一位大学生创新创业项目命名专家。

项目方向：{direction}
项目类型：{project_type}
技术偏好：{tech_preference}
关键词：{keywords}

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "name": "项目主名称（4-8个字）",
  "subtitle": "副标题（说明技术路线和应用场景）",
  "reasoning": "命名逻辑解释（50字以内）"
}}

要求：名称简洁有力，体现创新性和技术感。""",

    "project_summary": """你是一位创新创业项目方案撰写专家。

项目名称：{project_name}
副标题：{subtitle}
项目方向：{direction}
项目类型：{project_type}

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "background": "项目背景（用数据说话，100字以内）",
  "pain_points": ["痛点1", "痛点2", "痛点3"],
  "solution": "解决方案描述（150字以内）",
  "innovations": ["创新点1", "创新点2", "创新点3"]
}}

要求：语言专业，逻辑清晰，数据真实可查。""",

    "tech_route": """你是一位技术架构师，擅长为大学生创新项目规划技术路线。

项目名称：{project_name}
项目方向：{direction}
技术偏好：{tech_preference}
团队规模：{team_size}人

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "tech_stack": {{
    "frontend": "前端技术栈",
    "backend": "后端技术栈",
    "ai": "AI/模型相关",
    "database": "数据库",
    "other": "其他工具"
  }},
  "architecture": "架构描述（用文字描述分层架构，100字以内）",
  "phases": [
    {{
      "name": "阶段名称",
      "duration": "时长",
      "tasks": ["任务1", "任务2"]
    }}
  ]
}}

要求：技术栈要合理，适合大学生团队水平和项目周期。""",

    "business_model": """你是一位创业导师，擅长为大学生项目设计商业模式。

项目名称：{project_name}
项目方向：{direction}
项目类型：{project_type}

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "value_proposition": "核心价值主张（30字以内）",
  "customer_segments": ["目标用户群1", "目标用户群2"],
  "revenue_streams": [
    {{
      "name": "收入来源",
      "desc": "说明"
    }}
  ],
  "cost_structure": ["主要成本1", "主要成本2"],
  "competitive_advantage": ["竞争优势1", "竞争优势2", "竞争优势3"]
}}

要求：商业模式务实可行，适合大学生项目特点。""",

    "feasibility": """你是一位项目评审专家，请评估以下项目的可行性。

项目名称：{project_name}
项目方向：{direction}
项目类型：{project_type}
团队规模：{team_size}人

请按以下JSON格式输出（直接输出JSON，不要markdown代码块）：
{{
  "scores": {{
    "technical": {{"score": 4, "reason": "评分理由"}},
    "market": {{"score": 4, "reason": "评分理由"}},
    "team": {{"score": 3, "reason": "评分理由"}},
    "business": {{"score": 4, "reason": "评分理由"}}
  }},
  "overall_score": 4.0,
  "risks": [
    {{"risk": "风险描述", "mitigation": "应对策略"}}
  ],
  "suggestion": "总体建议（50字以内）"
}}

评分标准：1-5分，5分最高。要客观公正。"""
}
