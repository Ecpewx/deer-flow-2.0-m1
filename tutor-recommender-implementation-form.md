# 导师推荐模块实现形式详解

本文面向研发、测试和后续维护人员，详细说明当前“导师推荐模块”在 DeerFlow 中的实现形式，包括系统分层、核心数据流、接口契约、前后端协作方式、降级策略，以及后续可扩展方向。

## 1. 设计目标与实现取向

当前实现选择的是**分层可演进架构**，核心原则是：

- 先提供可用闭环（MVP）：用户可在工作区输入条件并拿到推荐结果
- 关键逻辑后端收敛：检索与打分在服务层，前端只做展示与交互
- 路径无环境硬编码：服务读取仓库内数据，便于本地/测试/部署一致
- 预留 LLM 增强位：默认规则理由，支持未来切换到真正 LLM 解释
- 保证联调稳定：前端支持“直连后端”和“同源代理”双模式

---

## 2. 模块分层结构

当前可以理解为 5 层：

1) **数据层（Data Layer）**  
- 来源目录：`tutor_recommender_deepflow/data`  
- 主要文件：
  - `tutors_354.json`（导师基础信息，包含导师主页 `url`）
  - `tutors_academic_full.json`（论文/项目等学术信息，也包含 `url`）
- 运行时策略：
  - 推荐服务会在返回 Top-K 导师时，按需访问对应 `url`
  - 抽取网页文本摘要（`webpage_excerpt`）用于增强展示与解释
  - 使用内存缓存避免重复抓取，失败时自动降级为空摘要，不中断推荐

2) **推荐服务层（Domain Service Layer）**  
- 文件：`backend/app/services/tutor_recommender.py`  
- 负责：
  - 数据加载与映射（导师基础信息 + 学术信息）
  - 查询匹配与打分
  - 过滤条件应用
  - 推荐理由生成（含 LLM 可选、fallback 标记）
  - 输出结构化结果 + debug 诊断信息

3) **网关 API 层（Gateway Layer）**  
- 文件：`backend/app/gateway/routers/tutor_recommendations.py`  
- 负责：
  - 对外暴露 HTTP API
  - 请求参数校验（Pydantic）
  - 调用服务层并返回稳定响应结构
  - 健康检查接口

4) **前端数据访问层（Frontend Data Layer）**  
- 文件：`frontend/src/core/tutor-recommendations/api.ts`  
- 负责：
  - 定义前端请求/响应 TypeScript 类型
  - 统一封装请求函数 `recommendTutors`
  - 统一处理错误信息

5) **前端交互展示层（UI Layer）**  
- 页面：`frontend/src/app/workspace/tutor-recommendations/page.tsx`  
- 导航入口：`frontend/src/components/workspace/workspace-nav-chat-list.tsx`  
- 负责：
  - 收集用户输入条件
  - 调用 API
  - 展示推荐结果卡片、错误提示、debug 信息

---

## 3. 后端实现形式（服务层）

服务核心对象是 `TutorRecommenderService`，实现形式是“**单服务实例 + 内存数据索引**”：

- 启动时加载数据文件到内存：
  - 导师列表 `self._tutors`
  - 学术信息映射 `self._academic_map`
- 提供 `health()` 返回就绪状态和数据统计
- `recommend()` 为主入口，参数包括：
  - `query`
  - `k`
  - `filters`
  - `llm_optional`

### 3.1 检索与打分形式

当前版本使用的是**轻量关键词命中打分**（规则检索）：

- 将导师可检索文本拼接为统一文本（姓名/职称/单位/研究方向/课程）
- 将查询词分词为 token（按空格简化切分）
- 计算 token 命中比例作为分数
- 按分数降序取 Top-K

这是一种“可运行、低依赖”的实现，优点是稳定、可解释、调试简单；后续可替换为向量召回（FAISS）而不改变 API 形状。

### 3.2 过滤条件形式

服务层在打分前进行过滤，支持：

- `school`：单位关键字匹配
- `title`：职称关键字匹配
- `has_papers`：仅保留有论文记录导师
- `has_projects`：仅保留有项目记录导师

### 3.3 推荐理由形式（LLM Optional）

当前采用“**规则理由为主，LLM 可选增强位**”：

- 默认生成规则理由（匹配等级 + 研究方向摘要）
- 输出中包含：
  - `used_llm`
  - `fallback_used`
- 现阶段 `llm_optional` 作为扩展开关占位，便于后续接入真实 LLM 推理逻辑

---

## 4. 后端实现形式（API 层）

### 4.1 接口定义

- `POST /api/tutor-recommendations`
- `GET /api/tutor-recommendations/health`

`POST` 请求结构：

- `query: string`
- `k: number (1~20)`
- `filters?: { school?, title?, has_papers?, has_projects? }`
- `llm_optional?: boolean`

`POST` 响应结构：

- `query`
- `recommendations[]`
  - `teacher`, `title`, `school`, `research`, `email`, `url`
  - `score`, `reason`
  - `papers_count`, `projects_count`
  - `tags`
- `debug`
  - `matched_count`, `returned_count`, `elapsed_ms`
  - `used_llm`, `fallback_used` 等

### 4.2 路由挂载形式

通过以下改动接入网关：

- `backend/app/gateway/routers/__init__.py` 注册模块
- `backend/app/gateway/app.py` `include_router(tutor_recommendations.router)`

---

## 5. 前端实现形式

### 5.1 页面交互形式

页面 `workspace/tutor-recommendations` 采用“**表单 + 结果卡片**”模式：

- 输入区：
  - query
  - k
  - school/title
  - has_papers / has_projects
- 操作：
  - 点击“开始推荐”触发请求
- 展示：
  - 每个导师独立卡片展示核心字段
  - 页面底部展示 debug JSON（便于联调）

### 5.2 导航入口形式

在工作区侧边栏新增一级入口：

- 文案：`t.sidebar.tutorRecommendations`
- 路径：`/workspace/tutor-recommendations`
- 图标：`GraduationCapIcon`

### 5.3 多语言形式

i18n 采用“类型先行”策略：

- 在 `types.ts` 扩展 `tutorRecommendation` 文案结构
- 在 `zh-CN.ts` 与 `en-US.ts` 同步实现，避免缺失键导致类型错误

---

## 6. 前后端联调与代理形式

本模块兼容两种调用路径：

1) **直连后端模式**  
- 当配置了 `NEXT_PUBLIC_BACKEND_BASE_URL` 时  
- 前端直接请求 `${BACKEND_BASE_URL}/api/tutor-recommendations`

2) **同源代理模式（默认兜底）**  
- 未配置 backend base URL 时  
- 前端请求 `/api/tutor-recommendations`  
- 由 Next Route Handler 代理到后端（默认 `127.0.0.1:8001`）

新增代理文件：

- `frontend/src/app/api/tutor-recommendations/route.ts`

这样解决了此前“请求打到前端 3006 但无对应路由”导致的 404 问题。

---

## 7. Skill 接入形式

Skill 文件：`skills/public/tutor-recommender/SKILL.md`

该文件主要承担“**能力声明 + 路由提示 + 输出规范**”角色：

- 告诉系统何时调用导师推荐技能
- 约束输入字段与输出结构
- 明确降级行为（LLM 不可用时不可阻断主流程）

这是 DeerFlow 技能生态中的标准接入方式，便于后续策略路由和提示工程持续优化。

---

## 8. 当前实现的边界与后续演进

### 8.1 当前边界

- 检索为规则匹配，不是向量召回
- `llm_optional` 已有协议位，但尚未接真实模型调用
- debug 当前以字符串展示，后续可更友好可视化

### 8.2 推荐的下一步演进

1. 用 FAISS + Embedding 替换规则匹配，保留现有 API 结构不变  
2. 接入真实 LLM 解释层，并缓存理由（减少重复推理）  
3. 增加排序/导出/复制能力（按分数、按论文数、按项目数）  
4. 增加后端单测与前端 E2E 用例（尤其过滤条件组合场景）  
5. 引入可观测指标（QPS、P95、命中率、fallback 比例）

---

## 9. 实现总结

本次实现采用了“**先稳定闭环，再能力增强**”的工程策略。  
在不破坏现有 DeerFlow 架构的前提下，导师推荐模块已具备完整产品链路：

- 可访问入口
- 可提交条件
- 可获得结果
- 可诊断问题
- 可持续扩展

这意味着该模块已从“概念能力”进入“可用能力”阶段，后续可以逐步升级算法质量与推荐体验。

