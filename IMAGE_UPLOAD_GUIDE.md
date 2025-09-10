# Image Upload Implementation Guide

## Overview

The Challenge model now supports storing images directly in the database instead of using image keys. Images are stored as binary data with metadata, supporting files up to 100KB in size.

## Database Changes

### New Model Fields

The `Challenge` model now includes these image-related fields:

- `image_data` - BinaryField storing the actual image bytes
- `image_name` - CharField storing the original filename
- `image_content_type` - CharField storing the MIME type (e.g., "image/jpeg")
- `image_size` - PositiveIntegerField storing file size in bytes

### Removed Fields

- `image_key` - No longer needed as images are stored directly

## API Endpoints

### 1. Create Challenge with Image Upload

**Endpoint:** `POST /api/hocus-focus/challenge`

**Content-Type:** `multipart/form-data` (for file uploads) or `application/json` (without image)

**Form Fields:**
```
clue: string (required)
credit: string (optional)
credit_url: string (optional)
image: file (optional, max 100KB)
goals: JSON array (optional)
hit_areas: JSON array (optional)
before_message_body: string (optional)
before_message_title: string (optional)
before_message_button: string (optional)
before_message_background_image_url: string (optional)
is_test: boolean (optional)
is_permanent: boolean (optional)
is_tutorial: boolean (optional)
```

**Example using curl:**
```bash
curl -X POST http://localhost:8000/api/hocus-focus/challenge \
  -F "clue=Find the hidden object" \
  -F "credit=John Doe" \
  -F "image=@/path/to/image.jpg" \
  -F "goals=[30,60,90]"
```

**Example using JavaScript/FormData:**
```javascript
const formData = new FormData();
formData.append('clue', 'Find the hidden object');
formData.append('credit', 'John Doe');
formData.append('image', fileInput.files[0]); // File from input element
formData.append('goals', JSON.stringify([30, 60, 90]));

fetch('/api/hocus-focus/challenge', {
  method: 'POST',
  body: formData
});
```

### 2. Get Challenge with Image Data

**Endpoint:** `GET /api/hocus-focus/challenge/{id}`

**Response includes:**
```json
{
  "id": 1,
  "clue": "Find the hidden object",
  "credit": "John Doe",
  "image_name": "puzzle.jpg",
  "image_content_type": "image/jpeg",
  "image_size": 45678,
  "has_image": true,
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD...",
  "goals": [30, 60, 90],
  "hit_areas": [],
  "created_at": "2025-01-01T12:00:00Z"
}
```

### 3. Get Raw Image Data

**Endpoint:** `GET /api/hocus-focus/challenge/{id}/image`

**Response:** Raw image data with proper Content-Type header

**Example:**
```bash
curl http://localhost:8000/api/hocus-focus/challenge/1/image -o downloaded_image.jpg
```

**Use in HTML:**
```html
<img src="/api/hocus-focus/challenge/1/image" alt="Challenge Image" />
```

## Image Validation

### File Size Limit
- Maximum size: 100KB (102,400 bytes)
- Validation occurs during serialization

### Supported Formats
- JPEG (`image/jpeg`)
- PNG (`image/png`)
- GIF (`image/gif`)
- WebP (`image/webp`)

### Error Responses

**File too large:**
```json
{
  "image": ["Image file too large. Maximum size is 100KB. Current size is 150KB."]
}
```

**Unsupported format:**
```json
{
  "image": ["Unsupported image type: image/bmp. Allowed types: image/jpeg, image/png, image/gif, image/webp"]
}
```

## Model Methods

### Challenge Model Methods

```python
# Check if challenge has an image
challenge.has_image  # Property returning boolean

# Get base64 encoded image for API responses
challenge.get_image_base64()  # Returns base64 string or None

# Set image from uploaded file
challenge.set_image_from_file(uploaded_file)  # Handles file processing
```

## Admin Interface

The Django admin now displays:
- Image preview (thumbnail)
- Image filename
- File size in KB
- "Has Image" status

## Database Migration

When you run migrations, Django will:
1. Add new image fields to the Challenge table
2. Remove the old `image_key` field
3. Preserve existing challenge data

**Migration commands:**
```bash
# Since existing migrations use the original app name, use 'challenges' for migrations
python3 manage.py makemigrations challenges
python3 manage.py migrate

# Or if you're using a virtual environment:
# source your_venv/bin/activate
# python manage.py makemigrations challenges
# python manage.py migrate
```

**Note:** Even though the app is now located at `hocus_focus/challenges/`, Django migrations still reference it as 'challenges' because that's how the original migrations were created. The app name in `INSTALLED_APPS` is `'hocus_focus.challenges'` but for migrations, use just `challenges`.

## Frontend Integration Examples

### HTML Form
```html
<form method="post" enctype="multipart/form-data" action="/api/hocus-focus/challenge">
  <input type="text" name="clue" placeholder="Challenge clue" required>
  <input type="text" name="credit" placeholder="Image credit">
  <input type="file" name="image" accept="image/*">
  <input type="text" name="goals" placeholder="[30,60,90]">
  <button type="submit">Create Challenge</button>
</form>
```

### React Component
```jsx
function ChallengeUpload() {
  const [formData, setFormData] = useState({
    clue: '',
    credit: '',
    image: null
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append('clue', formData.clue);
    data.append('credit', formData.credit);
    if (formData.image) {
      data.append('image', formData.image);
    }

    const response = await fetch('/api/hocus-focus/challenge', {
      method: 'POST',
      body: data
    });

    const result = await response.json();
    console.log('Challenge created:', result);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={formData.clue}
        onChange={(e) => setFormData({...formData, clue: e.target.value})}
        placeholder="Challenge clue"
        required
      />
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFormData({...formData, image: e.target.files[0]})}
      />
      <button type="submit">Create Challenge</button>
    </form>
  );
}
```

## Performance Considerations

### Database Storage
- Images are stored as BLOB data in the database
- Consider database size limits for production
- 100KB limit helps prevent excessive database growth

### API Performance
- Base64 encoding increases response size by ~33%
- Consider pagination for endpoints returning multiple challenges
- Use the raw image endpoint (`/challenge/{id}/image`) for direct image display

### Caching
- Consider implementing caching for frequently accessed images
- Raw image endpoint can be cached by browsers
- Add appropriate cache headers in production

## Security Considerations

- File type validation prevents malicious uploads
- Size limits prevent DoS attacks
- Consider adding virus scanning in production
- Validate image content, not just file extension

## Troubleshooting

### Common Issues

1. **"No module named 'PIL'"**
   - Install Pillow: `pip install Pillow`

2. **File upload not working**
   - Ensure `enctype="multipart/form-data"` in HTML forms
   - Check Content-Type header in API requests

3. **Image not displaying**
   - Verify image was uploaded successfully
   - Check the `/challenge/{id}/image` endpoint directly
   - Ensure proper Content-Type headers

4. **Database migration errors**
   - Backup database before migration
   - Check for existing data conflicts
   - Run migrations in development first