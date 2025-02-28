import uuid
from django.core.exceptions import ValidationError
from django.utils.text import slugify

def generate_unique_slug(text):
    unique_text = uuid.uuid4().hex[:5]
    slug_text = slugify(text)

    return f"{slug_text}_{unique_text}"


def validate_image_extension(value):
    allowed_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    ext = value.name.split('.')[-1].lower()

    if ext not in allowed_extensions:
        raise ValidationError(f"Extension {ext} is not allowed. Allowed Extensions: {', '.join(allowed_extensions)}")
    

def validate_image_size(value, max_size_mb=5):
    if value.size > max_size_mb*1024*1024:
        raise ValidationError(f"Image Size must be under {max_size_mb}MB.")
