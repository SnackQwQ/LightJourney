# 旅行行程管理系统 — 项目总述提示词

> 将此提示词发送给你的本地AI（Claude Code、Cursor、Copilot等），
> AI即可全面了解本项目并协助你完成开发任务。

---

## 项目总述

我们正在开发一个**AI驱动的旅行行程管理系统**。核心理念：用户描述出行意图，AI自动生成结构化行程方案，一键保存管理。产品定位为极简、克制、AI驱动的个人工具。

**交付形态**：纯Web SPA（桌面端优先）
**MVP目标**：跑通"注册 → AI规划行程 → 浏览管理 → AI生成分享文案"的完整体验闭环
**开发周期**：1天（MVP）

---

## 技术栈

| 层 | 技术 |
|------|------|
| 前端框架 | Vue 3（Composition API）+ Vite |
| UI组件库 | Element Plus |
| 状态管理 | Pinia（仅存储token） |
| HTTP客户端 | Axios |
| 路由 | Vue Router 4（history模式） |
| 后端框架 | Python FastAPI |
| ORM | SQLAlchemy 2.0 |
| 数据库 | SQLite |
| 鉴权 | JWT（PyJWT + bcrypt，access token 24h） |
| LLM | DeepSeek API（兼容OpenAI格式，`openai` Python SDK调用） |
| 后端服务器 | Uvicorn |

---

## MVP功能范围

### 要做的基础功能（F-01 ~ F-09）
1. **注册登录**：用户名+密码注册，JWT鉴权，未登录拦截跳转登录页
2. **行程列表**：按日期分组展示，卡片式布局
3. **行程筛选**：按城市、日期范围筛选
4. **预算统计**：筛选结果总预算 + 每日小计
5. **行程CRUD**：新建/编辑/删除，表单含城市、日期、时段、标题、描述、预算
6. **时段冲突校验**：同一用户同日期，时段重叠禁止保存（结束时间=开始时间不算重叠）
7. **数据隔离**：所有行程按user_id隔离

### 要做的AI功能
8. **Skill1 行程智能规划**：用户输入天数、城市、偏好（多选：美食/自然风光/人文）、预算上限 → AI生成2-3条/天的行程JSON → 前端三步弹窗（填参数→预览编辑→确认保存）。行展开编辑，混合模式冲突检测（预览时浅黄色提示，保存时硬拦截外部冲突），逐条保存无冲突的、明确告知哪些跳过
9. **Skill2 行程文案生成**：选中行程 → AI生成4-6句口语化朋友圈文案（真实感分享型，1-2个emoji）→ 弹窗编辑+复制

---

## 数据库Schema

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    city VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT DEFAULT '',
    budget DECIMAL(10,2) DEFAULT 0.00,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_trips_user_date ON trips(user_id, date);
```

---

## API端点

**Base URL:** `http://localhost:8000/api`
**鉴权方式:** `Authorization: Bearer <jwt_token>`（除注册/登录外）

**统一响应格式：**
```json
{ "code": 200, "message": "success", "data": {} }
```

**错误码：** 200成功 | 400参数错误 | 401未登录 | 403无权限 | 409冲突 | 422验证失败 | 500服务器错误 | 502 AI服务失败

| 方法 | 端点 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/api/auth/register` | 否 | 注册，body: {username, password} |
| POST | `/api/auth/login` | 否 | 登录，返回 {access_token, token_type, username} |
| GET | `/api/trips?city=&date_from=&date_to=` | 是 | 行程列表，返回 {trips, total_budget, daily_budgets} |
| POST | `/api/trips` | 是 | 创建行程，body: {city, date, start_time, end_time, title, description?, budget?} |
| PUT | `/api/trips/:id` | 是 | 更新行程，返回403若操作他人数据 |
| DELETE | `/api/trips/:id` | 是 | 删除行程 |
| POST | `/api/ai/plan` | 是 | AI规划，body: {city, days, preferences[], budget?}，返回 {plan[], conflicts[]} |
| POST | `/api/ai/copywriting` | 是 | AI文案，body: {trip_id}，返回 {copywriting, trip_title, trip_date} |

---

## 后端项目结构

```
backend/
├── main.py              # FastAPI入口、CORS、路由注册
├── config.py             # 环境变量（DB路径、JWT密钥、DeepSeek Key/URL）
├── database.py           # SQLAlchemy引擎、Session、Base
├── dependencies.py       # get_current_user() JWT依赖注入
├── models/
│   ├── user.py           # User ORM
│   └── trip.py           # Trip ORM
├── routers/
│   ├── auth.py           # POST /api/auth/register, /api/auth/login
│   ├── trips.py          # GET/POST/PUT/DELETE /api/trips
│   └── ai.py             # POST /api/ai/plan, /api/ai/copywriting
├── services/
│   ├── auth_service.py   # 密码哈希/验证、JWT签发/验证
│   ├── trip_service.py   # 行程CRUD、冲突检测、预算统计
│   └── ai_service.py     # DeepSeek调用封装、JSON解析容错
├── prompts/
│   ├── planning.py       # Skill1 Prompt模板
│   └── copywriting.py    # Skill2 Prompt模板
└── requirements.txt
```

---

## 前端项目结构

```
frontend/
├── index.html
├── vite.config.js
├── package.json
└── src/
    ├── main.js              # Vue应用入口，注册Router/Pinia/ElementPlus
    ├── App.vue              # 根组件 <router-view>
    ├── router/index.js      # 路由表 + beforeEach鉴权守卫
    ├── api/
    │   ├── index.js         # axios实例、请求拦截器(注入token)、响应拦截器(统一错误)
    │   ├── auth.js          # login(), register()
    │   ├── trips.js         # getTrips(), getTrip(), createTrip(), updateTrip(), deleteTrip()
    │   └── ai.js            # planTrip(), generateCopywriting()
    ├── stores/user.js       # Pinia store: token存储/读取/清除
    ├── styles/variables.css # CSS变量: 颜色、字体、间距
    ├── views/
    │   ├── Login.vue        # 登录页
    │   ├── Register.vue     # 注册页
    │   └── TripList.vue     # 行程列表页（筛选栏+日期分组+卡片列表+预算统计+空状态）
    └── components/
        ├── TripCard.vue         # 行程卡片（hover显示操作按钮）
        ├── TripFormDialog.vue   # 行程新建/编辑弹窗（前端校验+提交）
        ├── AIPlanDialog.vue     # AI规划三步弹窗（参数→预览编辑→保存）
        └── AICopywritingDialog.vue  # AI文案弹窗（展示+编辑+复制）
```

---

## UI设计原则

**极简旅行质感** — 大面积浅色留白，克制使用颜色，安静高级感。

**色彩：**
- 页面底色 `#F7F8FA`、卡片白色 `#FFFFFF`
- 主文字 `#1A1A2E`、次要文字 `#8C8C8C`、分割线 `#EBEBEB`
- 强调色：`#7D9B76`（鼠尾草绿）— 仅用于主按钮、选中状态等高亮元素
- 同一页面可见颜色不超过3种（含灰度）

**字体：** PingFang SC / Microsoft YaHei，字重300-600，字号不超过4档（18/16/14/12px）

**动效：** `transition: all 0.2s ease`，无弹跳/缩放。Loading使用骨架屏或细线进度条。

**卡片：** 纯白、极细边框、微投影 `box-shadow: 0 1px 3px rgba(0,0,0,0.04)`，操作按钮hover显示。

**弹窗：** 圆角12px、蒙层 `rgba(0,0,0,0.3)`、无多余装饰线。

---

## 关键算法

### 时段冲突检测
```
A和B重叠 ⟺ A.start < B.end AND A.end > B.start
注意：12:00结束 vs 12:00开始 → 不冲突（等于不算重叠）
```

### AI规划批量保存
逐条检测冲突 → 无冲突的直接写入 → 有外部冲突的跳过 → 返回 {saved_count, failed_count, failed_items}

---

## 团队分工（5人）

| 成员 | 角色 | 核心产出 |
|------|------|------|
| P1 BE-Lead | 后端负责人 | FastAPI初始化、数据库建表、JWT鉴权（注册/登录/拦截器）、统一响应格式 |
| P2 BE-AI | 后端开发 | 行程CRUD+冲突校验、DeepSeek封装、Skill1+Skill2 Prompt与接口 |
| P3 FE-Lead | 前端负责人 | Vue3初始化、路由守卫、axios拦截器、Pinia store、登录页、注册页、CSS变量 |
| P4 FE-Trip | 前端开发 | 行程列表页（筛选/分组/统计/空状态）、TripCard组件、TripFormDialog弹窗 |
| P5 FE-AI | 前端开发 | AIPlanDialog三步弹窗（行展开编辑+冲突标记+批量保存）、AICopywritingDialog弹窗 |

---

## AI Skill Prompt设计要点

### Skill1 行程规划
- 角色：专业旅行规划师
- 输出：纯JSON数组，不输出任何解释文字
- 每字段：date(YYYY-MM-DD), start_time(HH:MM), end_time(HH:MM), title, description(50-100字), budget(数字，人均元)
- 约束：每天2-3条（上午/下午/晚上各一），每条≥2小时，相邻行程≥1小时间隔，景点地理位置相近
- 交互：三步弹窗 → 预览可编辑 → 逐条保存无冲突的 → 明确告知保存结果

### Skill2 文案生成
- 角色：真实旅行博主
- 风格：口语化、有情绪、4-6句串联当天行程、1-2个贴切emoji
- 上下文：传入目标行程 + 当天同城所有其他行程
- 交互：弹窗展示 → 可编辑 → 一键复制

**AI生成内容绝不直接写库，必须经过用户预览确认。**

---

## 开发环境

| 项 | 要求 |
|------|------|
| Python | 3.10+ |
| Node.js | 18+ |
| 后端端口 | 8000 |
| 前端端口 | 5173 |
| 代码管理 | Git（功能分支→合并main） |
| 命名 | 后端snake_case，前端组件PascalCase，CSS类名BEM风格kebab-case |

---

## 验收标准（10条）

1. 能注册新用户、登录获取token、token过期拦截到登录页
2. 能新建/编辑/删除行程，操作即时反映在列表页
3. 同日期时段重叠时禁止保存，明确提示
4. 按城市/日期筛选结果正确，预算统计自动更新
5. AI规划：输入参数→返回可用JSON→预览可编辑→确认后批量保存成功
6. 文案生成：点击生成→返回口语化文案→可编辑→可复制
7. 用户A无法看到用户B的行程
8. 新用户空列表展示引导内容
9. 网络异常、AI超时、输入非法时有明确提示，不崩溃
10. AI生成内容必须先经过预览和用户确认才能写入数据库
