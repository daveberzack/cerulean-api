# Django API Structure Guide for Beginners

This guide explains how the General Purpose Django API is organized and what each file does. The API is structured to support multiple products/sections, with Hocus Focus being one section. If you're new to Django or web APIs, this will help you understand the structure and concepts.

## What is Django?

Django is a Python web framework that helps you build web applications and APIs quickly. It follows the **Model-View-Template (MVT)** pattern, but for APIs we use **Model-View-Serializer** instead.

## Overall Project Structure

```
cerulean/                          # Root project folder
├── manage.py                      # Django's command-line utility
├── api_core/                      # Main project configuration (generic)
│   ├── __init__.py               # Makes this a Python package
│   ├── settings.py               # All project settings and configuration
│   ├── urls.py                   # Main URL routing (like a table of contents)
│   ├── wsgi.py                   # Web server gateway interface
│   └── asgi.py                   # Async server gateway interface
├── hocus_focus/                   # Hocus Focus product section
│   ├── __init__.py               # Makes this a Python package
│   └── challenges/               # Challenges app (business logic)
│       ├── __init__.py           # Makes this a Python package
│       ├── models.py             # Database structure definitions
│       ├── views.py              # API endpoint logic
│       ├── serializers.py        # Data conversion between JSON and Python
│       ├── urls.py               # App-specific URL routing
│       ├── admin.py              # Django admin interface setup
│       ├── apps.py               # App configuration
│       ├── tests.py              # Unit tests
│       └── migrations/           # Database change history
├── requirements.txt              # List of Python packages needed
├── build.sh                     # Deployment build script
├── .env.example                 # Environment variables template
└── db.sqlite3                   # Development database file
```

## Why This Structure?

Django organizes code into **projects** and **apps**, and we've added an additional **product namespace** layer:

- **Project** (`api_core/`): The overall container with settings and configuration (generic)
- **Product Namespace** (`hocus_focus/`): Groups related apps for a specific product/section
- **App** (`hocus_focus/challenges/`): A specific piece of functionality (like challenges, users, etc.)

This separation allows you to:
- Keep related code together by product
- Easily add new product sections alongside hocus_focus
- Scale by adding more apps within each product namespace
- Maintain clean, organized code with clear boundaries
- Support multiple products in a single API

## Key Files Explained

### 1. `manage.py` - The Command Center
```python
# This file lets you run Django commands like:
# python manage.py runserver    # Start the development server
# python manage.py migrate      # Update the database
# python manage.py shell        # Open Python shell with Django loaded
```

**What it does**: Acts as Django's command-line interface. You use this to start the server, create database tables, and run other Django commands.

### 2. `api_core/settings.py` - The Configuration Hub

This file contains all the settings for your Django project:

```python
# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # What type of database
        'NAME': BASE_DIR / 'db.sqlite3',         # Where the database file is
    }
}

# Installed apps - tells Django what functionality to include
INSTALLED_APPS = [
    'django.contrib.admin',      # Admin interface
    'rest_framework',            # API functionality
    'corsheaders',              # Cross-origin requests
    'hocus_focus.challenges',    # Our hocus focus challenges app
]

# CORS settings - which websites can access our API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",     # Local development
    "https://your-site.com",     # Production site
]
```

**Why it's important**: This is where you configure everything - database, security, which apps to use, API settings, etc.

### 3. `api_core/urls.py` - The Main Router

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                              # Django admin at /admin/
    path('api/auth/token/', obtain_auth_token),                   # Authentication at /api/auth/token/
    path('api/hocus-focus/', include('hocus_focus.challenges.urls')), # Hocus Focus endpoints under /api/hocus-focus/
]
```

**What it does**: Like a table of contents for your API. When someone visits `/api/hocus-focus/challenge/1`, Django looks here to figure out which code should handle that request. Notice how hocus_focus endpoints are now namespaced under `/api/hocus-focus/`.

### 4. `hocus_focus/challenges/models.py` - The Database Blueprint

Models define what data you store and how it's structured:

```python
class Challenge(models.Model):
    """A puzzle challenge in the game"""
    
    # Fields (columns in the database)
    clue = models.TextField()                    # The puzzle clue
    image_key = models.CharField(max_length=255) # Image identifier
    goals = models.JSONField(default=list)       # Time goals [30, 60, 90]
    created_at = models.DateTimeField(auto_now_add=True)  # When created
    
    # Metadata
    class Meta:
        db_table = 'challenges'     # Database table name
        ordering = ['-created_at']  # Show newest first
    
    def __str__(self):
        return f"Challenge {self.id}: {self.clue[:50]}"  # How to display in admin
```

**Why models matter**: 
- They define your database structure
- Django automatically creates database tables from these
- They provide an easy way to work with data in Python
- They include validation and relationships

### 5. `hocus_focus/challenges/serializers.py` - The Data Translator

Serializers convert between JSON (what APIs use) and Python objects (what Django uses):

```python
class ChallengeSerializer(serializers.ModelSerializer):
    """Converts Challenge objects to/from JSON"""
    
    class Meta:
        model = Challenge
        fields = [
            'id', 'clue', 'image_key', 'goals',     # What fields to include
            'hitareas', 'created_at', 'updated_at'  # hitareas is now a tokenized string field
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']  # Can't be changed via API
```

**What serializers do**:
- **Incoming**: Convert JSON from API requests into Python objects
- **Outgoing**: Convert Python objects into JSON for API responses
- **Validation**: Check that incoming data is valid
- **Relationships**: Handle related data (like hit areas for a challenge)

### 6. `hocus_focus/challenges/views.py` - The Business Logic

Views contain the actual logic for each API endpoint:

```python
@api_view(['POST'])                    # Only accept POST requests
@permission_classes([AllowAny])       # No authentication required
def create_challenge(request):
    """Create a new challenge"""
    try:
        # Convert JSON to Python object
        serializer = ChallengeCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save to database
            challenge = serializer.save()
            
            # Convert back to JSON and return
            response_serializer = ChallengeSerializer(challenge)
            return Response(response_serializer.data, status=201)
        else:
            # Return validation errors
            return Response(serializer.errors, status=400)
            
    except Exception as e:
        # Handle unexpected errors
        return Response({'error': str(e)}, status=500)
```

**What views do**:
- Handle HTTP requests (GET, POST, PUT, DELETE)
- Process the request data
- Interact with the database through models
- Return appropriate responses
- Handle errors gracefully

### 7. `hocus_focus/challenges/urls.py` - App-Specific Routing

```python
from django.urls import path
from . import views

urlpatterns = [
    path('challenge', views.create_challenge, name='create_challenge'),
    path('christmas', views.create_christmas_challenge, name='create_christmas_challenge'),
    path('challenge/<int:challenge_id>', views.get_challenge_by_id, name='get_challenge_by_id'),
]
```

**What it does**: Maps specific URLs to view functions. When someone visits `/api/hocus-focus/challenge/1`, it calls `views.get_challenge_by_id` with `challenge_id=1`. Note that the `/api/hocus-focus/` prefix is handled by the main `api_core/urls.py`.

## How It All Works Together

Here's what happens when someone makes an API request:

1. **Request comes in**: `POST /api/hocus-focus/challenge` with JSON data
2. **URL routing**: Django checks `api_core/urls.py`, then `hocus_focus/challenges/urls.py` to find the right view
3. **View processes**: The view function runs, using serializers to validate data
4. **Database interaction**: Models are used to save/retrieve data
5. **Response sent**: Serializers convert the result back to JSON

## The Django Philosophy

Django follows these principles:

### 1. **Don't Repeat Yourself (DRY)**
- Write code once, reuse it everywhere
- Models automatically generate database tables
- Serializers automatically handle JSON conversion

### 2. **Convention over Configuration**
- Django assumes sensible defaults
- File names and locations have meaning
- Following conventions makes code predictable

### 3. **Separation of Concerns**
- **Models**: Handle data and business rules
- **Views**: Handle request/response logic
- **Serializers**: Handle data conversion
- **URLs**: Handle routing

## Common Patterns You'll See

### 1. **Model-Serializer-View Pattern**
```
Model (data) → Serializer (conversion) → View (logic) → Response
```

### 2. **CRUD Operations**
- **Create**: POST requests to add new data
- **Read**: GET requests to retrieve data
- **Update**: PUT/PATCH requests to modify data
- **Delete**: DELETE requests to remove data

### 3. **Error Handling**
```python
try:
    # Try to do something
    result = do_something()
    return Response(result, status=200)
except ValidationError as e:
    # Handle expected errors
    return Response({'error': str(e)}, status=400)
except Exception as e:
    # Handle unexpected errors
    return Response({'error': 'Something went wrong'}, status=500)
```

## Development vs Production

### Development (what you're running locally):
- Uses SQLite database (simple file)
- DEBUG=True (shows detailed errors)
- Allows all CORS origins
- Uses Django's development server

### Production (deployed on Render.com):
- Uses PostgreSQL database (more robust)
- DEBUG=False (hides sensitive error details)
- Restricted CORS origins
- Uses Gunicorn web server

## API Endpoints Structure

With the new namespaced structure, all Hocus Focus endpoints are now under `/api/hocus-focus/`:

- `POST /api/hocus-focus/challenge` - Create a new challenge
- `POST /api/hocus-focus/christmas` - Create a Christmas challenge
- `GET /api/hocus-focus/challenge/{id}` - Get challenge by ID
- `GET /api/hocus-focus/challenges` - List all challenges
- `POST /api/hocus-focus/solve` - Create a solve record

This structure allows for easy expansion:
- `/api/other-product/` - Future product endpoints
- `/api/shared/` - Shared functionality endpoints
- `/api/auth/` - Authentication endpoints

## Next Steps for Learning

1. **Try modifying the API**: Add a new field to the Challenge model in `hocus_focus/challenges/models.py`
2. **Create a new endpoint**: Add a DELETE endpoint to remove challenges
3. **Add a new product section**: Create another directory like `hocus_focus/` for a different product
4. **Add validation**: Make certain fields required or add custom validation
5. **Explore Django admin**: Visit `/admin/` to see the built-in interface
6. **Read Django docs**: https://docs.djangoproject.com/

## Key Takeaways

- **Django organizes code into projects and apps, with an added product namespace layer**
- **The API is now general-purpose with hocus_focus as one section**
- **Models define your data structure**
- **Serializers handle JSON conversion**
- **Views contain your business logic**
- **URLs route requests to the right code with proper namespacing**
- **Everything works together to create a scalable, organized API**

This structure might seem complex at first, but it makes large, multi-product applications much easier to maintain and scale! The namespacing allows you to easily add new products or services without affecting existing functionality.