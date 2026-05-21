# Grading Skills — Routing Guide

当用户要求批改/评分/批阅学生作业时，按以下规则路由到对应技能：

## 路由表

| 任务类型 | 路由到 |
|---------|--------|
| 编程/代码/算法题批改 | `student-code-questions-grading` |
| 概念/名词解释/简答/填空/客观题批改 | `student-concept-questions-grading` |
| 案例分析问答（学生答案评估，非出题） | `student-case-questions-grading` |
| 论述/议论文/讨论回应批改 | `student-essay-questions-grading` |
| 课程论文/报告/文献综述/实验报告批改 | `student-paper-report-grading` |

## 混合题型处理

若作业包含多种题型（如"期末试卷""A 卷/B 卷""第 1 题…第 N 题""综合题""多部分作业"）：
1. 优先使用 `student-mixed-exam-grading`（编排层）
2. 该技能会自行拆分并路由到各单题型技能

## 多文件批量处理

若用户上传了多位学生的作业文件（批量批改）：
1. 优先使用 `student-batch-grading`（编排层）
2. 该技能会自行文件配对、逐学生路由、汇总

## 反馈重批处理

若教师对上一版批改结果提修改意见（"太松""重点偏了""按反馈重做"）：
1. 先读取 `student-grading-feedback-revision` 的重批协议
2. 再按题型路由到对应的 `student-*-grading` 执行

## 无法匹配时的兜底

若任务类型不明确，用通用批改逻辑：
1. 从题干推断评分维度和规则
2. 评估学生答案
3. 输出 Markdown 批改报告
