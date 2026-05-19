# 导师推荐模块变更说明

本文记录本次“导师推荐模块”落地的实际代码改动，覆盖后端服务、API、Skill、前端页面、导航入口、i18n 以及校验结果。

## 1. 后端：可复用推荐服务

- 新增文件：`backend/app/services/tutor_recommender.py`
- 核心内容：
  - 抽象 `TutorRecommenderService`
  - 数据路径改为仓库相对路径（基于 `tutor_recommender_deepflow/data`）
  - 去除原始实现中的硬编码绝对路径
  - 支持推荐参数：
    - `query`
    - `k`（1-20）
    - `filters`：`school`、`title`、`has_papers`、`has_projects`
    - `llm_optional`
  - 输出结构化推荐结果：导师信息、分数、理由、论文/项目计数、标签
  - 提供 `health()` 健康检查信息
  - 返回 `debug` 元信息（matched_count、returned_count、elapsed_ms、fallback_used 等）

## 2. 后端：导师推荐 API

- 新增文件：`backend/app/gateway/routers/tutor_recommendations.py`
- 新增接口：
  - `POST /api/tutor-recommendations`
    - 入参：`query`、`k`、`filters`、`llm_optional`
    - 出参：`recommendations[]` + `debug`
  - `GET /api/tutor-recommendations/health`
- 路由注册变更：
  - 修改 `backend/app/gateway/routers/__init__.py`
  - 修改 `backend/app/gateway/app.py`（`app.include_router(tutor_recommendations.router)`）

## 3. Skill：导师推荐技能（MVP）

- 新增文件：`skills/public/tutor-recommender/SKILL.md`
- 覆盖内容：
  - 适用场景与触发意图
  - 输入字段规范（query/k/filters）
  - 执行规则（排序、降级）
  - 输出格式（结构化 Markdown）
  - 约束（不杜撰、无命中提示）

## 4. 前端：技能 mock 列表接入

- 修改文件：`frontend/src/app/mock/api/skills/route.ts`
- 新增技能条目：
  - `name: "tutor-recommender"`
  - 用于前端本地/演示环境立即可见技能入口

## 5. 前端：推荐 API 封装

- 新增文件：`frontend/src/core/tutor-recommendations/api.ts`
- 新增能力：
  - 类型定义：
    - `TutorRecommendationFilters`
    - `TutorRecommendationRequest`
    - `TutorRecommendationItem`
    - `TutorRecommendationResponse`
  - 调用函数：`recommendTutors(request)`
  - 统一错误处理（包含后端 detail）

## 6. 前端：导师推荐页面

- 新增文件：`frontend/src/app/workspace/tutor-recommendations/page.tsx`
- 页面能力：
  - 输入条件：
    - query
    - k
    - school / title
    - has_papers / has_projects
  - 调用后端推荐接口
  - 展示结果卡片（导师名、职称、单位、研究方向、匹配分、理由、论文/项目计数）
  - 展示错误信息与 debug 信息
  - 支持 loading 态

## 7. 前端：侧边栏导航入口

- 修改文件：`frontend/src/components/workspace/workspace-nav-chat-list.tsx`
- 新增导航菜单项：
  - 路径：`/workspace/tutor-recommendations`
  - 图标：`GraduationCapIcon`
  - 文案：`t.sidebar.tutorRecommendations`

## 8. i18n 国际化

- 修改文件：`frontend/src/core/i18n/locales/types.ts`
  - 新增 `sidebar.tutorRecommendations`
  - 新增 `tutorRecommendation` 文案类型定义
- 修改文件：`frontend/src/core/i18n/locales/zh-CN.ts`
  - 补齐中文文案（标题、描述、输入占位、筛选、按钮、错误、字段标签）
- 修改文件：`frontend/src/core/i18n/locales/en-US.ts`
  - 补齐英文文案（对应中文字段）

## 9. 质量检查与修复

- 已执行相关文件的 linter 检查
- 修复点：
  - 原页面引用不存在的 `@/components/ui/checkbox`、`@/components/ui/label`
  - 调整为原生 `input type="checkbox"` 与 `label`，消除类型错误
- 最终结果：
  - 本次新增/修改的导师推荐模块文件无 linter 报错

## 10. 本次改动文件清单（导师推荐相关）

- `backend/app/services/tutor_recommender.py`（新增）
- `backend/app/gateway/routers/tutor_recommendations.py`（新增）
- `backend/app/gateway/routers/__init__.py`（修改）
- `backend/app/gateway/app.py`（修改）
- `skills/public/tutor-recommender/SKILL.md`（新增）
- `frontend/src/app/mock/api/skills/route.ts`（修改）
- `frontend/src/core/tutor-recommendations/api.ts`（新增）
- `frontend/src/app/workspace/tutor-recommendations/page.tsx`（新增）
- `frontend/src/components/workspace/workspace-nav-chat-list.tsx`（修改）
- `frontend/src/core/i18n/locales/types.ts`（修改）
- `frontend/src/core/i18n/locales/zh-CN.ts`（修改）
- `frontend/src/core/i18n/locales/en-US.ts`（修改）

## 11. 问题修复记录：前端点击“开始推荐”返回 404

- 现象：
  - 点击“开始推荐”后报错：`Failed to recommend tutors: Not Found`
  - 控制台请求：`POST http://127.0.0.1:3006/api/tutor-recommendations 404`
- 原因：
  - 请求发往 Next 前端服务（3006），但当时前端没有对应的 API 路由进行转发
- 修复方案：
  1. 新增前端代理路由：`frontend/src/app/api/tutor-recommendations/route.ts`
     - `POST /api/tutor-recommendations` 代理到后端 `/api/tutor-recommendations`
     - `GET /api/tutor-recommendations` 代理到后端 `/api/tutor-recommendations/health`
  2. 更新前端请求策略：`frontend/src/core/tutor-recommendations/api.ts`
     - 若配置 `NEXT_PUBLIC_BACKEND_BASE_URL`，前端直连后端
     - 若未配置，则自动走同源代理 `/api/tutor-recommendations`
- 结果：
  - 解决 404 Not Found
  - 本地开发环境在未配置后端 base URL 时也可正常调用推荐接口

## 12. 数据层增强：读取导师主页 URL 内容

- 背景：
  - `tutors_354.json` 与 `tutors_academic_full.json` 中都包含导师主页 `url`
  - 仅展示 URL 不足以体现数据价值，需要在推荐时读取网页内容
- 实现：
  1. 后端服务新增 URL 内容抓取能力（`backend/app/services/tutor_recommender.py`）
     - 新增 `fetch_web_content` 控制参数（默认 `true`）
     - 对 Top-K 导师按需请求 `url`（短超时、User-Agent、HTML 文本抽取）
     - 生成 `webpage_excerpt`（网页摘要）
     - 内存缓存 URL 抓取结果，避免重复抓取
     - 抓取失败自动降级为空字符串，不影响推荐主流程
  2. API 响应结构扩展（`backend/app/gateway/routers/tutor_recommendations.py`）
     - 请求体支持 `fetch_web_content`
     - 推荐项增加 `webpage_excerpt`
  3. 前端类型与展示扩展
     - `frontend/src/core/tutor-recommendations/api.ts` 增加 `fetch_web_content` 入参与 `webpage_excerpt` 字段
     - `frontend/src/app/workspace/tutor-recommendations/page.tsx` 结果卡片展示“主页摘要”
- 结果：
  - 推荐结果不仅包含结构化静态字段，也可附带导师主页实时文本摘要
  - 数据层实现从“URL 字段展示”升级为“URL 内容读取 + 摘要利用”

