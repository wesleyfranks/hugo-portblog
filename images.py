import os
import re
import shutil

# Paths
posts_dir = "/Users/wesleyfranks/Documents/Obsidian Vault/Posts/"
attachments_dir = "/Users/wesleyfranks/Documents/Obsidian Vault/Attachments/"
obsidian_images_dir = "/Users/wesleyfranks/Documents/Obsidian Vault/images/"  # New images folder
static_images_dir = "/Users/wesleyfranks/Projects/Web/portblog/static/images/"

# Ensure the new images folder exists in Obsidian
os.makedirs(obsidian_images_dir, exist_ok=True)

# Step 1: Process each Markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        # Read the Markdown file content
        with open(filepath, "r") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format [[image_name.png]]
        images = re.findall(r'\[\[([^]]*\.(?:png|jpg|jpeg))\]\]', content, re.IGNORECASE)

        # Debug: Print found images for the current Markdown file
        print(f"Processing file: {filename}")
        print(f"Found images: {images}")

        # Step 3: Process each image found
        for image in images:
            # Normalize the image name (replace spaces with %20)
            markdown_image = f"![Image Description](images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)

            # Paths for copying the image
            image_source = os.path.join(attachments_dir, image)
            obsidian_image_target = os.path.join(obsidian_images_dir, image)
            static_image_target = os.path.join(static_images_dir, image)

            # Copy the image to Obsidian's images folder
            if os.path.exists(image_source):
                shutil.copy(image_source, obsidian_image_target)
                print(f"Copied: {image_source} to {obsidian_image_target}")
                
                # Copy the same image to Hugo's static/images directory
                shutil.copy(image_source, static_image_target)
                print(f"Copied: {image_source} to {static_image_target}")
            else:
                print(f"Warning: {image_source} not found.")

        # Step 5: Write the updated content back to the Markdown file
        with open(filepath, "w") as file:
            file.write(content)

print("Markdown files processed, images copied to Obsidian and Hugo successfully.")