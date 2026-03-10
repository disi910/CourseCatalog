# CourseCatalog

A web application for browsing and visualizing courses at the Institute of Informatics (Institutt for Informatikk) at the University of Oslo.

Hosted at https://didriksi.com

## Features

- **Course Search** — Search and filter courses by department, level, language, and semester
- **Course Details** — View full course info including credits, prerequisites, exam form, and teaching language
- **Dependency Graph** — Interactive prerequisite visualization using node-based graphs (ReactFlow)
- **Course Map** — Overview of all course prerequisite relationships

## Tech Stack

| Layer    | Technology                                  |
|----------|---------------------------------------------|
| Frontend | React 19, TypeScript, Vite, Tailwind CSS    |
| Backend  | FastAPI (Python 3.12+)                      |
| Database | PostgreSQL with SQLAlchemy + Alembic        |
| Graphs   | ReactFlow                                   |

## Project Structure

```
CourseCatalog/
├── apps/
│   ├── api/            # FastAPI backend
│   └── web/ififag/     # React frontend
└── .github/workflows/  # CI/CD (GitHub Actions)
```

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- Node.js 18+ and npm
- PostgreSQL

---

### Backend

```bash
cd apps/api

# Install dependencies
poetry install

# Create .env file
echo "DATABASE_URL=postgresql://user:password@localhost:5432/coursecatalog" > .env
echo "SECRET_KEY=your-secret-key" >> .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

#### Key endpoints

| Method | Path                                  | Description                    |
|--------|---------------------------------------|--------------------------------|
| GET    | `/courses/`                           | List courses (with filters)    |
| GET    | `/courses/{id}`                       | Get a single course            |
| GET    | `/courses/{id}/dependencies`          | Get prerequisite graph data    |
| GET    | `/statistics/departments`             | Course counts by department    |
| GET    | `/health`                             | Health check                   |

---

### Frontend

```bash
cd apps/web/ififag

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`.

> **Note:** The frontend is currently configured to connect to `http://192.168.0.200:8000`. Update `apps/web/ififag/src/services/api.ts` if your API runs on a different host.

#### Other scripts

```bash
npm run build    # Production build
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

---

### Running Tests (Backend)

```bash
cd apps/api
pytest tests
```

## Environment Variables

| Variable       | Description                          | Default                    |
|----------------|--------------------------------------|----------------------------|
| `DATABASE_URL` | PostgreSQL connection string         | *(required)*               |
| `SECRET_KEY`   | Application secret key               | `development-secret-key`   |
