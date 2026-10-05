# my-indie-studio (한중 크로스보더 대구/구독 플랫폼 MVP)

한중 크로스보더 커머스 플랫폼의 MVP 개발 프로젝트입니다.

## 🛠️ Tech Stack
- **Backend**: Python 3.13, FastAPI, SQLAlchemy 2.0 (Async), Pydantic v2
- **Frontend**: Uni-app (Vue 3 + TypeScript + Vite)
- **Database**: SQLite (`aiosqlite` - 개발용) / PostgreSQL (운영 예정)

## 📁 Project Structure
```text
my-indie-studio/
├── apps/
│   ├── backend/          # FastAPI RESTful API
│   └── frontend/         # Uni-app (Vue 3) App/Web Frontend
├── docs/                 # API Specification & DB Schema Drafts
├── scripts/              # Code Generation Scripts (DeepSeek/Gemini)
└── .env.example          # Environment Variable Blueprint