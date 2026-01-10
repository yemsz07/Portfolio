import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysites.settings')
django.setup()

from mywebsite.models import myweb

def fix_image_paths():
    # Get all myweb objects
    items = myweb.objects.all()
    
    for item in items:
        # Get the current image path
        current_path = item.image.name
        
        # Check if the path needs to be updated
        if 'web_images' not in current_path:
            # Extract the filename from the path
            filename = os.path.basename(current_path)
            # Create the new path
            new_path = f'web_images/{filename}'
            
            # Check if the file exists in the new location
            full_path = os.path.join('media', new_path)
            if os.path.exists(full_path):
                # Update the image field
                item.image.name = new_path
                item.save()
                print(f'Updated: {current_path} -> {new_path}')
            else:
                print(f'File not found: {full_path}')
    
    print('Image path update complete!')

if __name__ == '__main__':
    fix_image_paths()
