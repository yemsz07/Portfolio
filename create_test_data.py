import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysites.settings')
django.setup()

from django.contrib.auth import get_user_model
from mywebsite.models import myweb

User = get_user_model()

# Create a test user if it doesn't exist
try:
    user = User.objects.get(username='admin')
    print(f"Using existing user: {user.username}")
except User.DoesNotExist:
    user = User.objects.create_user(username='admin', password='admin123')
    print(f"Created user: {user.username}")

# Create some test data
test_posts = [
    {'description': 'First test post with image', 'image': 'test1.jpg'},
    {'description': 'Second test post with different content', 'image': 'test2.jpg'},
    {'description': 'Third post for testing API', 'image': 'test3.jpg'},
]

for i, post_data in enumerate(test_posts, 1):
    # Create a dummy image file path (you'll need to upload actual images later)
    myweb_obj = myweb.objects.create(
        user=user,
        description=post_data['description'],
        image=post_data['image']  # This should be a real image file
    )
    print(f"Created post {i}: ID={myweb_obj.id}, Description={post_data['description']}")

print(f"\nTotal posts created: {myweb.objects.count()}")
