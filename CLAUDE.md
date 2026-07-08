# LightJourney — AI驱动的旅行行程管理系统

> **一句话定位**：用户描述出行意图，AI 生成结构化行程，一键保存管理。极简、克制、不做社区/电商/社交。

---

## 技术栈

| 层 | 技术 |
|------|------|
| 前端 | Vue 3 (Composition API) + Vite + Element Plus |
| 状态/路由 | Pinia (仅存token) + Vue Router 4 (history模式) |
| HTTP | Axios（拦截器注入token，统一错误处理） |
| 后端 | Python FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.0 + SQLite |
| 鉴权 | JWT (PyJWT + bcrypt, access token 24h) |
| LLM | DeepSeek API（openai Python SDK 调用，兼容格式） |

---

## 当前范围：MVP（Skill1 + Skill2）

### 基础功能（F-01 ~ F-09）
1. 注册登录（用户名+密码，JWT 鉴权，未登录拦截跳转）
2. 行程列表（按日期分组，卡片式布局）
3. 行程筛选（按城市、日期范围）
4. 预算统计（总预算 + 每日小计，筛选联动）
5. 行程 CRUD（新建/编辑/删除，含时段冲突校验）
6. 数据隔离（所有查询强制按 user_id 过滤）

### AI 功能
- **Skill1 行程智能规划**：用户输入天数+城市+偏好+预算 → AI 生成每日 2-3 条行程 JSON → 前端三步弹窗（填参数→预览编辑→确认保存）→ 冲突的跳过、无冲突的逐条保存
- **Skill2 行程文案生成**：选中行程 → AI 生成 4-6 句口语化朋友圈文案 → 弹窗编辑+复制

### 明确不做
- 打包物品清单、AI 打包推荐、风险校验、雨天备选方案、海报导出
- 社交/评论/点赞、酒店机票预订、多人协作、第三方登录、移动端 App、地图可视化

---

## 项目目录结构

```
LightJourney/
├── backend/
│   ├── main.py              # FastAPI入口、CORS、路由注册
│   ├── config.py            # 环境变量（DB路径、JWT密钥、DeepSeek Key/URL）
│   ├── database.py          # SQLAlchemy引擎、Session、Base
│   ├── dependencies.py      # get_current_user() JWT依赖注入
│   ├── models/
│   │   ├── user.py          # User ORM
│   │   └── trip.py          # Trip ORM
│   ├── routers/
│   │   ├── auth.py          # POST /api/auth/register, /api/auth/login
│   │   ├── trips.py         # GET/POST/PUT/DELETE /api/trips
│   │   └── ai.py            # POST /api/ai/plan, /api/ai/copywriting
│   ├── services/
│   │   ├── auth_service.py  # 密码哈希/验证、JWT签发/验证
│   │   ├── trip_service.py  # 行程CRUD、冲突检测、预算统计
│   │   └── ai_service.py    # DeepSeek调用封装、JSON解析容错
│   ├── prompts/
│   │   ├── planning.py      # Skill1 Prompt模板
│   │   └── copywriting.py   # Skill2 Prompt模板
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.js              # Vue应用入口，注册Router/Pinia/ElementPlus
│       ├── App.vue              # 根组件 <router-view>
│       ├── router/index.js      # 路由表 + beforeEach鉴权守卫
│       ├── api/
│       │   ├── index.js         # axios实例、请求拦截器、响应拦截器
│       │   ├── auth.js          # login(), register()
│       │   ├── trips.js         # CRUD封装
│       │   └── ai.js            # planTrip(), generateCopywriting()
│       ├── stores/user.js       # Pinia store: token存储/读取/清除
│       ├── styles/variables.css # CSS变量
│       ├── views/
│       │   ├── Login.vue
│       │   ├── Register.vue
│       │   └── TripList.vue
│       └── components/
│           ├── TripCard.vue
│           ├── TripFormDialog.vue
│           ├── AIPlanDialog.vue
│           └── AICopywritingDialog.vue
└── docs/
    ├── REQUIREMENTS.md
    ├── HIGH_LEVEL_DESIGN.md
    └── PROJECT_PROMPT.md
```

---

## 数据库 Schema

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

## API 契约

**Base URL:** `http://localhost:8000/api`
**鉴权:** `Authorization: Bearer <jwt_token>`（除注册/登录外所有接口）
**统一响应:** `{ "code": 200, "message": "success", "data": {} }`

| 方法 | 端点 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/api/auth/register` | 否 | 注册 `{username, password}` |
| POST | `/api/auth/login` | 否 | 登录，返回 `{access_token, token_type, username}` |
| GET | `/api/trips?city=&date_from=&date_to=` | 是 | 列表，返回 `{trips, total_budget, daily_budgets}` |
| POST | `/api/trips` | 是 | 创建 `{city, date, start_time, end_time, title, description?, budget?}` |
| PUT | `/api/trips/:id` | 是 | 更新，403若操作他人数据 |
| DELETE | `/api/trips/:id` | 是 | 删除 |
| POST | `/api/ai/plan` | 是 | AI规划 `{city, days, preferences[], budget?}` → `{plan[], conflicts[]}` |
| POST | `/api/ai/copywriting` | 是 | AI文案 `{trip_id}` → `{copywriting, trip_title, trip_date}` |

---

## 关键算法

### 时段冲突检测
```
A和B重叠 ⟺ A.start < B.end AND A.end > B.start
注意：12:00结束 vs 12:00开始 → 不冲突（等于不算重叠）
```

### AI 规划批量保存
1. 逐条检测与已有行程的时段冲突
2. 无冲突的直接写入数据库
3. 有冲突的跳过，记录原因
4. 返回 `{saved_count, failed_count, failed_items}`

---

## 开发规范

| 项 | 规范 |
|------|------|
| 后端文件命名 | snake_case（`trip_service.py`） |
| 后端类命名 | PascalCase（`TripService`） |
| 后端函数命名 | snake_case（`check_conflict()`） |
| 前端组件命名 | PascalCase（`TripFormDialog.vue`） |
| CSS 类命名 | kebab-case（`.trip-card__title`） |
| Git commit | 中文，动词开头（`feat: 添加行程冲突校验`） |
| 后端端口 | 8000 |
| 前端端口 | 5173 |

---

## UI 设计原则

- **色彩**：页面底色 `#F7F8FA`、卡片白色 `#FFFFFF`、主文字 `#1A1A2E`、次要文字 `#8C8C8C`、强调色 `#7D9B76`（鼠尾草绿）
- **字体**：PingFang SC / Microsoft YaHei，字重 300-600，字号 ≤4 档（18/16/14/12px）
- **卡片**：白色、极细边框、微投影 `0 1px 3px rgba(0,0,0,0.04)`，操作按钮 hover 显示
- **弹窗**：圆角 12px、蒙层 `rgba(0,0,0,0.3)`
- **动效**：`transition: all 0.2s ease`，无弹跳/缩放
- **同一页面可见颜色不超过 3 种**

---

## 关键约束

1. **AI 生成内容绝不直接写库** — 必须经过用户预览确认后才能保存
2. **数据隔离** — 所有行程查询从 JWT 解析 user_id，强制按 user_id 过滤
3. **前后端双重校验** — 前端即时校验 + 后端兜底校验
4. **DeepSeek API Key 仅存后端环境变量** — 前端不可见
5. **AI 请求超时 30 秒** — 超时后允许重试
6. **密码 bcrypt 哈希存储** — 不存明文
7. **时段冲突仅校验同用户同日期** — 跨天不校验

---

## 完整文档

| 文档 | 用途 |
|------|------|
| [REQUIREMENTS.md](docs/REQUIREMENTS.md) | 需求分析：功能清单、用户流程、数据字典、验收标准 |
| [HIGH_LEVEL_DESIGN.md](docs/HIGH_LEVEL_DESIGN.md) | 概要设计：架构、模块划分、API契约、5人分工、关键流程 |
| [PROJECT_PROMPT.md](docs/PROJECT_PROMPT.md) | AI提示词：完整项目上下文，可复制给新对话的AI |

---

## 5人团队分工

| 成员 | 角色 | 核心产出 |
|------|------|------|
| P1 BE-Lead | 后端负责人 | FastAPI初始化、数据库建表、JWT鉴权（注册/登录/拦截器） |
| P2 BE-AI | 后端开发 | 行程CRUD+冲突校验、DeepSeek封装、Skill1+Skill2 Prompt与接口 |
| P3 FE-Lead | 前端负责人 | Vue3初始化、路由守卫、axios拦截器、Pinia store、登录页、注册页、CSS变量 |
| P4 FE-Trip | 前端开发 | 行程列表页（筛选/分组/统计/空状态）、TripCard、TripFormDialog |
| P5 FE-AI | 前端开发 | AIPlanDialog三步弹窗、AICopywritingDialog弹窗 |

---

## 开发者使用指南

当开发者说出自己的角色编号时，AI 应：

1. **读取详细任务清单**：[docs/HIGH_LEVEL_DESIGN.md](docs/HIGH_LEVEL_DESIGN.md) §8.2 中有每个人的任务ID、产出文件、预计耗时和前置依赖
2. **按依赖顺序执行**：先做无前置依赖的任务，完成后做下一项
3. **严格遵循规范**：API 契约、数据库 Schema、命名规范、UI 设计原则均以本文档为准
4. **标记 TODO**：代码中留有 `TODO: Px 实现` 标记处即为待补充的业务逻辑

各角色一句话启动指令：
- **P1**：我是 P1(BE-Lead)，读 HIGH_LEVEL_DESIGN.md §8.2 我的任务清单，从 BE-01 开始
- **P2**：我是 P2(BE-AI)，读 HIGH_LEVEL_DESIGN.md §8.2 我的任务清单，等 P1 完成 BE-03 后开始
- **P3**：我是 P3(FE-Lead)，读 HIGH_LEVEL_DESIGN.md §8.2 我的任务清单，从 FE-01 开始
- **P4**：我是 P4(FE-Trip)，读 HIGH_LEVEL_DESIGN.md §8.2 我的任务清单，等 P3 完成 FE-06 后开始
- **P5**：我是 P5(FE-AI)，读 HIGH_LEVEL_DESIGN.md §8.2 我的任务清单，等 P3 完成 FE-06 后开始
