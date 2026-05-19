import {
  CompassIcon,
  GraduationCapIcon,
  ImageIcon,
  MicroscopeIcon,
  PenLineIcon,
  ShapesIcon,
  SparklesIcon,
  VideoIcon,
  FileTextIcon,
  BookOpenIcon,
} from "lucide-react";

import type { Translations } from "./types";

export const zhCN: Translations = {
  // Locale meta
  locale: {
    localName: "中文",
  },

  // Common
  common: {
    home: "首页",
    settings: "设置",
    delete: "删除",
    edit: "编辑",
    rename: "重命名",
    share: "分享",
    openInNewWindow: "在新窗口打开",
    close: "关闭",
    more: "更多",
    search: "搜索",
    download: "下载",
    thinking: "思考",
    artifacts: "文件",
    public: "公共",
    custom: "自定义",
    notAvailableInDemoMode: "在演示模式下不可用",
    loading: "加载中...",
    version: "版本",
    lastUpdated: "最后更新",
    code: "代码",
    preview: "预览",
    cancel: "取消",
    save: "保存",
    install: "安装",
    create: "创建",
    import: "导入",
    export: "导出",
    exportAsMarkdown: "导出为 Markdown",
    exportAsJSON: "导出为 JSON",
    exportSuccess: "对话已导出",
  },

  // Home
  home: {
    docs: "文档",
    blog: "博客",
  },

  // Welcome
  welcome: {
    greeting: "欢迎使用 浙财SMILE",
    description:
      "可以帮你生成案例、批改作业、推荐导师、生成试卷，生成课件，更多惊喜值得期待！",

    createYourOwnSkill: "创建你自己的 Agent SKill",
    createYourOwnSkillDescription:
      "创建你的 Agent Skill 来释放 😋浙财SMILE 的潜力。通过自定义技能，😋浙财SMILE\n可以帮你搜索网络、分析数据，还能为你生成幻灯片、\n网页等作品，几乎可以做任何事情。",
  },

  // Clipboard
  clipboard: {
    copyToClipboard: "复制到剪贴板",
    copiedToClipboard: "已复制到剪贴板",
    failedToCopyToClipboard: "复制到剪贴板失败",
    linkCopied: "链接已复制到剪贴板",
  },

  // Input Box
  inputBox: {
    placeholder: "今天我能为你做些什么？",
    createSkillPrompt:
      "我们一起用 skill-creator 技能来创建一个技能吧。先问问我希望这个技能能做什么。",
    addAttachments: "添加附件",
    mode: "模式",
    flashMode: "闪速",
    flashModeDescription: "快速且高效的完成任务，但可能不够精准",
    reasoningMode: "思考",
    reasoningModeDescription: "思考后再行动，在时间与准确性之间取得平衡",
    proMode: "Pro",
    proModeDescription: "思考、计划再执行，获得更精准的结果，可能需要更多时间",
    ultraMode: "Ultra",
    ultraModeDescription:
      "继承自 Pro 模式，可调用子代理分工协作，适合复杂多步骤任务，能力最强",
    reasoningEffort: "推理深度",
    reasoningEffortMinimal: "最低",
    reasoningEffortMinimalDescription: "检索 + 直接输出",
    reasoningEffortLow: "低",
    reasoningEffortLowDescription: "简单逻辑校验 + 浅层推演",
    reasoningEffortMedium: "中",
    reasoningEffortMediumDescription: "多层逻辑分析 + 基础验证",
    reasoningEffortHigh: "高",
    reasoningEffortHighDescription: "全维度逻辑推演 + 多路径验证 + 反推校验",
    searchModels: "搜索模型...",
    surpriseMe: "小惊喜",
    surpriseMePrompt: "给我一个小惊喜吧",
    followupLoading: "正在生成可能的后续问题...",
    followupConfirmTitle: "发送建议问题？",
    followupConfirmDescription: "当前输入框已有内容，选择发送方式。",
    followupConfirmAppend: "追加并发送",
    followupConfirmReplace: "替换并发送",
    suggestions: [
      {
        suggestion: "案例生成",
        prompt:"生成研究生案例分析题。\n我只提供关键信息：\n- 学科：管理学\n- 主题：[必填]\n- 知识点：[选填，1-2条]\n\n其余请按高阶难度自动补全。\n默认不输出文档，网页只输出：\n1. 案例材料\n2. 问题（4题，含分值8/8/7/7）\n3. 参考答案（按题给分点）。",
        icon: PenLineIcon,
      },
      {
        suggestion: "批改作业",
        href: "/workspace/agents/grading-assistant/chats/new",
        icon: MicroscopeIcon,
      },
      {
        suggestion: "导师推荐",
        prompt: "推荐[专业]导师。",
        icon: GraduationCapIcon,
      },
      {
        suggestion: "试卷生成",
        prompt: `生成一套试卷。 \n我只提供关键信息： \n- 学科：[必填] \n- 主题：[必填] \n- 知识点：[可后续补充，或提供相关文件] \n其余请按高阶难度自动补全。\n默认输出格式要求： \n1. 试卷格式：[总分100分，建议用时120分钟，难度比例基础/中等/综合为3:5:2。] \n2. 题型包含：[可选：单选、多选、判断、填空、简答和计算题…] \n3. 输出内容：[可选：”默认格式含完整题目卷、答案卷与评分标准，答案卷中标注每道题的考察知识点（题目卷不标注）；浙财学堂格式以导入浙财学堂模版输出，题目答案放在一起；自定义需提供输出模板。] \n4. 导出格式：[可选：Word（.docx）；PDF（.pdf）。] \n5. 额外要求：[知识点覆盖尽量全面且不重复，若提供文件参考，则题目来源覆盖所有文件，若需调整题型比例，请先提示我确认。]`,
        icon: FileTextIcon,
      },
      {
        suggestion: "课件生成",
        prompt: `你是一位专业教学设计师与资深教师，请根据老师上传的论文、教材、讲义或参考资料，自动生成一份高质量课件（PPT）内容。
老师需提供以下其中一种或多种资料：
论文（PDF / Word）
 教材章节
 研究报告
 课程讲义
 教学大纲
 补充阅读资料
并提供基础信息：
 学科：[必填]
 主题：[必填]
 年级 / 学习对象：[选填]
 课时长度：[选填]
 教学目标：[选填]
 任务要求
请先解析上传资料内容，并完成以下工作：
1. 提炼核心概念、重点知识、关键结论
2. 转换为适合课堂教学的表达方式
3. 将学术内容简化为学生可理解的层次
4. 保留重要专业术语，并附必要说明
5. 若资料内容过深，请自动调整为对应年级难度
 默认输出要求
1. 输出为完整课件结构（适用于 PPT）
2. 自动规划页数（建议 10～20 页）
3. 每页包含：
    页标题
    简报内容
    教师讲解提示（备注）
4. 内容结构建议包含：
 封面页
 学习目标
 导入页
 背景介绍
 核心知识讲解
 图表 / 数据说明（如论文含数据）
 案例分析
 课堂互动题
 总结页
 延伸思考 / 作业页
 特殊规则（上传论文时）
1. 不直接复制论文原文
2. 优先摘要重点并教学化表达
3. 数据结果需转成图表建议
4. 方法论内容需简化说明
5. 若论文内容不适合学生程度，请说明并自动重构
风格要求
 专业、清晰、易懂
 适合投影片展示
 避免大段文字
 重点突出，逻辑清楚
`,
        icon: BookOpenIcon,
      }
    ],
    suggestionsCreate: [
      {
        suggestion: "网页",
        prompt: "生成一个关于[主题]的网页",
        icon: CompassIcon,
      },
      {
        suggestion: "图片",
        prompt: "生成一个关于[主题]的图片",
        icon: ImageIcon,
      },
      {
        suggestion: "视频",
        prompt: "生成一个关于[主题]的视频",
        icon: VideoIcon,
      },
      {
        type: "separator",
      },
      {
        suggestion: "技能",
        prompt:
          "我们一起用 skill-creator 技能来创建一个技能吧。先问问我希望这个技能能做什么。",
        icon: SparklesIcon,
      },
    ],
  },

  // Sidebar
  sidebar: {
    newChat: "新对话",
    chats: "对话",
    recentChats: "最近的对话",
    demoChats: "演示对话",
    agents: "智能体",
  },

  // Agents
  agents: {
    title: "智能体",
    description: "创建和管理具有专属 Prompt 与能力的自定义智能体。",
    newAgent: "新建智能体",
    emptyTitle: "还没有自定义智能体",
    emptyDescription: "创建你的第一个自定义智能体，设置专属系统提示词。",
    chat: "对话",
    delete: "删除",
    deleteConfirm: "确定要删除该智能体吗？此操作不可撤销。",
    deleteSuccess: "智能体已删除",
    newChat: "新对话",
    createPageTitle: "设计你的智能体",
    createPageSubtitle: "描述你想要的智能体，我来帮你通过对话创建。",
    nameStepTitle: "给新智能体起个名字",
    nameStepHint:
      "只允许字母、数字和连字符，存储时自动转为小写（例如 code-reviewer）",
    nameStepPlaceholder: "例如 code-reviewer",
    nameStepContinue: "继续",
    nameStepInvalidError: "名称无效，只允许字母、数字和连字符",
    nameStepAlreadyExistsError: "已存在同名智能体",
    nameStepNetworkError: "网络请求失败，请检查网络或后端连接",
    nameStepCheckError: "无法验证名称可用性，请稍后重试",
    nameStepBootstrapMessage:
      "新智能体的名称是 {name}，现在开始为它生成 **SOUL**。",
    save: "保存智能体",
    saving: "正在保存智能体...",
    saveRequested:
      "已提交保存请求，浙财SMILE 正在根据当前对话生成并保存初版智能体。",
    saveHint:
      "你可以在右上角的菜单里随时保存这个智能体，就算目前还只是初稿也可以。",
    saveCommandMessage:
      "请现在根据我们目前已经讨论的全部内容保存这个自定义智能体。这就是我明确的保存确认。如果仍有少量细节缺失，请根据上下文做出合理假设，生成一份简洁的英文初始 SOUL.md，并直接调用 setup_agent，不要再向我索要额外确认。",
    agentCreatedPendingRefresh:
      "智能体已创建，但 浙财SMILE 暂时还无法读取到它。请稍后刷新当前页面。",
    more: "更多操作",
    agentCreated: "智能体已创建！",
    startChatting: "开始对话",
    backToGallery: "返回 Gallery",
  },

  // Breadcrumb
  breadcrumb: {
    workspace: "工作区",
    chats: "对话",
  },

  // Workspace
  workspace: {
    officialWebsite: "访问 浙财SMILE 官方网站",
    githubTooltip: "访问 浙财SMILE 的 Github 仓库",
    settingsAndMore: "设置和更多",
    visitGithub: "在 Github 上查看 浙财SMILE",
    reportIssue: "报告问题",
    contactUs: "联系我们",
    about: "关于 浙财SMILE",
  },

  // Conversation
  conversation: {
    noMessages: "还没有消息",
    startConversation: "开始新的对话以查看消息",
  },

  // Chats
  chats: {
    searchChats: "搜索对话",
  },

  // Page titles (document title)
  pages: {
    appName: "浙财SMILE",
    chats: "对话",
    newChat: "新对话",
    untitled: "未命名",
  },

  // Tool calls
  toolCalls: {
    moreSteps: (count: number) => `查看其他 ${count} 个步骤`,
    lessSteps: "隐藏步骤",
    executeCommand: "执行命令",
    presentFiles: "展示文件",
    needYourHelp: "需要你的协助",
    useTool: (toolName: string) => `使用 “${toolName}” 工具`,
    searchFor: (query: string) => `搜索 “${query}”`,
    searchForRelatedInfo: "搜索相关信息",
    searchForRelatedImages: "搜索相关图片",
    searchForRelatedImagesFor: (query: string) => `搜索相关图片 “${query}”`,
    searchOnWebFor: (query: string) => `在网络上搜索 “${query}”`,
    viewWebPage: "查看网页",
    listFolder: "列出文件夹",
    readFile: "读取文件",
    writeFile: "写入文件",
    clickToViewContent: "点击查看文件内容",
    writeTodos: "更新 To-do 列表",
    skillInstallTooltip: "安装技能并使其可在 浙财SMILE 中使用",
  },

  uploads: {
    uploading: "上传中...",
    uploadingFiles: "文件上传中，请稍候...",
  },

  subtasks: {
    subtask: "子任务",
    executing: (count: number) =>
      `${count > 1 ? "并行" : ""}执行 ${count} 个子任务`,
    in_progress: "子任务运行中",
    completed: "子任务已完成",
    failed: "子任务失败",
  },

  // Token Usage
  tokenUsage: {
    title: "Token 用量",
    input: "输入",
    output: "输出",
    total: "总计",
  },

  // Shortcuts
  shortcuts: {
    searchActions: "搜索操作...",
    noResults: "未找到结果。",
    actions: "操作",
    keyboardShortcuts: "键盘快捷键",
    keyboardShortcutsDescription: "使用键盘快捷键更快地操作 浙财SMILE。",
    openCommandPalette: "打开命令面板",
    toggleSidebar: "切换侧边栏",
  },

  // Settings
  settings: {
    title: "设置",
    description: "根据你的偏好调整 浙财SMILE 的界面和行为。",
    sections: {
      appearance: "外观",
      memory: "记忆",
      tools: "工具",
      skills: "技能",
      notification: "通知",
      about: "关于",
    },
    memory: {
      title: "记忆",
      description:
        "浙财SMILE 会在后台不断从你的对话中自动学习。这些记忆能帮助 浙财SMILE 更好地理解你，并提供更个性化的体验。",
      empty: "暂无可展示的记忆数据。",
      rawJson: "原始 JSON",
      exportButton: "导出记忆",
      exportSuccess: "记忆已导出",
      importButton: "导入记忆",
      importConfirmTitle: "导入记忆？",
      importConfirmDescription: "这会用选中的 JSON 备份覆盖当前记忆。",
      importFileLabel: "已选择文件",
      importInvalidFile: "读取记忆文件失败，请选择有效的 JSON 导出文件。",
      importSuccess: "记忆已导入",
      manualFactSource: "手动添加",
      addFact: "添加事实",
      addFactTitle: "添加记忆事实",
      editFactTitle: "编辑记忆事实",
      addFactSuccess: "事实已创建",
      editFactSuccess: "事实已更新",
      clearAll: "清空全部记忆",
      clearAllConfirmTitle: "要清空全部记忆吗？",
      clearAllConfirmDescription:
        "这会删除所有已保存的摘要和事实。此操作无法撤销。",
      clearAllSuccess: "已清空全部记忆",
      factDeleteConfirmTitle: "要删除这条事实吗？",
      factDeleteConfirmDescription:
        "这条事实会立即从记忆中删除。此操作无法撤销。",
      factDeleteSuccess: "事实已删除",
      factContentLabel: "内容",
      factCategoryLabel: "类别",
      factConfidenceLabel: "置信度",
      factContentPlaceholder: "描述你想保存的记忆事实",
      factCategoryPlaceholder: "context",
      factConfidenceHint: "请输入 0 到 1 之间的数字。",
      factSave: "保存事实",
      factValidationContent: "事实内容不能为空。",
      factValidationConfidence: "置信度必须是 0 到 1 之间的数字。",
      noFacts: "还没有保存的事实。",
      summaryReadOnly:
        "摘要分区当前仍为只读。现在你可以清空全部记忆或删除单条事实。",
      memoryFullyEmpty: "还没有保存任何记忆。",
      factPreviewLabel: "即将删除的事实",
      searchPlaceholder: "搜索记忆",
      filterAll: "全部",
      filterFacts: "事实",
      filterSummaries: "摘要",
      noMatches: "没有找到匹配的记忆。",
      markdown: {
        overview: "概览",
        userContext: "用户上下文",
        work: "工作",
        personal: "个人",
        topOfMind: "近期关注（Top of mind）",
        historyBackground: "历史背景",
        recentMonths: "近几个月",
        earlierContext: "更早上下文",
        longTermBackground: "长期背景",
        updatedAt: "更新于",
        facts: "事实",
        empty: "（空）",
        table: {
          category: "类别",
          confidence: "置信度",
          confidenceLevel: {
            veryHigh: "极高",
            high: "较高",
            normal: "一般",
            unknown: "未知",
          },
          content: "内容",
          source: "来源",
          createdAt: "创建时间",
          view: "查看",
        },
      },
    },
    appearance: {
      themeTitle: "主题",
      themeDescription: "跟随系统或选择固定的界面模式。",
      system: "系统",
      light: "浅色",
      dark: "深色",
      systemDescription: "自动跟随系统主题。",
      lightDescription: "更明亮的配色，适合日间使用。",
      darkDescription: "更暗的配色，减少眩光方便专注。",
      zufeBlue: "浙财蓝",
      zufeBlueDescription: "以浙财蓝为主色的主题风格。",
      languageTitle: "语言",
      languageDescription: "在不同语言之间切换。",
    },
    tools: {
      title: "工具",
      description: "管理 MCP 工具的配置和启用状态。",
    },
    skills: {
      title: "技能",
      description: "管理 Agent Skill 配置和启用状态。",
      createSkill: "新建技能",
      emptyTitle: "还没有技能",
      emptyDescription:
        "将你的 Agent Skill 文件夹放在 浙财SMILE 根目录下的 `/skills/custom` 文件夹中。",
      emptyButton: "创建你的第一个技能",
    },
    notification: {
      title: "通知",
      description:
        "浙财SMILE 只会在窗口不活跃时发送完成通知，特别适合长时间任务：你可以先去做别的事，完成后会收到提醒。",
      requestPermission: "请求通知权限",
      deniedHint:
        "通知权限已被拒绝。可在浏览器的网站设置中重新开启，以接收完成提醒。",
      testButton: "发送测试通知",
      testTitle: "浙财SMILE",
      testBody: "这是一条测试通知。",
      notSupported: "当前浏览器不支持通知功能。",
      disableNotification: "关闭通知",
    },
    acknowledge: {
      emptyTitle: "致谢",
      emptyDescription: "相关的致谢信息会展示在这里。",
    },
  },
};
