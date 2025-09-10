# Hocus Focus API

A Django REST API for the Hocus Focus puzzle game, providing endpoints for challenge management and user interactions.

## Features

- **Challenge Management**: Create and retrieve puzzle challenges
- **Christmas Challenges**: Special endpoint for holiday-themed puzzles
- **Solve Tracking**: Record and track user puzzle completions
- **CORS Enabled**: Ready for frontend integration
- **Authentication**: Token-based auth system
- **PostgreSQL Ready**: Configured for production databases

## Quick Start

### Development Setup

1. **Clone and setup**:
   ```bash
   cd cerulean
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **Run development server**:
   ```bash
   python manage.py runserver
   ```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/challenge` | Create a new challenge |
| POST | `/christmas` | Create Christmas challenge |
| GET | `/challenge/{id}` | Get challenge by ID |
| GET | `/challenges` | List all challenges |
| POST | `/solve` | Record a solve |
| POST | `/api/auth/token/` | Get auth token |

### Example Usage

**Create a Challenge**:
```bash
curl -X POST http://localhost:8000/challenge \
  -H "Content-Type: application/json" \
  -d '{
    "clue": "Find the hidden treasure",
    "image_key": "treasure_map_001",
    "goals": [30, 60, 90, 120, 150]
  }'
```

**Get a Challenge**:
```bash
curl http://localhost:8000/challenge/1
```

## Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed instructions on deploying to Render.com.

## Project Structure

```
cerulean/
├── challenges/          # Main app
│   ├── models.py       # Database models
│   ├── serializers.py  # API serializers
│   ├── views.py        # API endpoints
│   └── urls.py         # URL routing
├── hocus_focus_api/    # Django project
│   ├── settings.py     # Configuration
│   └── urls.py         # Main URL config
├── requirements.txt    # Dependencies
├── build.sh           # Render build script
└── manage.py          # Django management
```

## Models

- **Challenge**: Main puzzle data with clues, goals, before message fields, and metadata
- **HitArea**: Clickable areas within challenges
- **Solve**: User completion records

## Configuration

Key settings in `settings.py`:
- REST Framework configuration
- CORS settings for frontend integration
- Database configuration (SQLite dev, PostgreSQL prod)
- Authentication setup

## Development

- Python 3.8+
- Django 5.2.6
- Django REST Framework 3.16.1
- PostgreSQL (production)
- SQLite (development)

## License

This project is part of the Hocus Focus game suite.