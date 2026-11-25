# Rachel Backend

Gin service for **Rachel** — chat storage and API (agent loop & hardware tools coming soon).

## Techs

- **Go**: Programming language
- **Gin**: Backend framework
- **GORM**: ORM
- **SQLite**: Database
- **godotenv**: Environment variables

## Setup

First go inside directory:

```bash
cd backend
```

Download dependencies:

```bash
go mod tidy
```

### Configure `.env`

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then edit it:

```env
APP_ENV=development
```

> Default environment is production if `APP_ENV` is not set.
> Database file is created automatically as `rachel.db` in the backend directory.

### Run

```bash
go run main.go
```

- API: `http://127.0.0.1:8000`
