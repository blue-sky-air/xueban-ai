import httpx
import json
import re
from app.core.config import AI_API_KEY, AI_BASE_URL, AI_MODEL
from app.services.prompt_templates import PROMPTS

async def call_ai(prompt: str) -> str:
    """调用大模型API"""
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": AI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    url = f"{AI_BASE_URL}/v1/chat/completions"
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except httpx.TimeoutException:
            return '{"error": "AI服务响应超时，请稍后重试"}'
        except httpx.HTTPStatusError as e:
            return f'{{"error": "AI服务返回错误: {e.response.status_code}"}}'
        except Exception as e:
            return f'{{"error": "AI服务异常: {str(e)}"}}'

def parse_json(text: str) -> dict:
    """从AI回复中提取JSON"""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {"raw": text}

async def generate_study_plan(major, grade, goal, basics=None, target_school=None):
    prompt = PROMPTS["study_plan"].format(
        major=major, grade=grade, goal=goal,
        basics=", ".join(basics) if basics else "无",
        target_school=target_school or "无"
    )
    result = await call_ai(prompt)
    return parse_json(result)

async def generate_competition_guide(competition, role, time_remaining, level):
    prompt = PROMPTS["competition_guide"].format(
        competition=competition, role=role,
        time_remaining=time_remaining, level=level
    )
    result = await call_ai(prompt)
    return parse_json(result)

async def generate_project_name(direction, project_type, tech_preference, keywords):
    prompt = PROMPTS["project_name"].format(
        direction=direction, project_type=project_type,
        tech_preference=tech_preference, keywords=keywords or "无"
    )
    result = await call_ai(prompt)
    return parse_json(result)

async def generate_project_summary(project_name, subtitle, direction, project_type):
    prompt = PROMPTS["project_summary"].format(
        project_name=project_name, subtitle=subtitle,
        direction=direction, project_type=project_type
    )
    result = await call_ai(prompt)
    return parse_json(result)

async def generate_tech_route(project_name, direction, tech_preference, team_size):
    prompt = PROMPTS["tech_route"].format(
        project_name=project_name, direction=direction,
        tech_preference=tech_preference, team_size=team_size
    )
    result = await call_ai(prompt)
    return parse_json(result)

async def generate_business_model(project_name, direction, project_type):
    prompt = PROMPTS["business_model"].format(
        project_name=project_name, direction=direction, project_type=project_type
    )
    result = await call_ai(prompt)
    return parse_json(result)

async def generate_feasibility(project_name, direction, project_type, team_size):
    prompt = PROMPTS["feasibility"].format(
        project_name=project_name, direction=direction,
        project_type=project_type, team_size=team_size
    )
    result = await call_ai(prompt)
    return parse_json(result)
