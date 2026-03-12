from PIL import Image, ImageDraw, ImageFilter

# Load the image and convert to RGBA (supports transparency)
original = Image.open("krystal-ng-O07o2Cd_vX0-unsplash.jpg").convert("RGBA")

# Step 1: Blur the background for dreamy depth
blurred = original.filter(ImageFilter.GaussianBlur(radius=15))

# Step 2: Calculate a centered panel size
img_width, img_height = blurred.size
panel_width = int(img_width * 0.6)
panel_height = int(img_height * 0.4)
panel_x = (img_width - panel_width) // 2
panel_y = (img_height - panel_height) // 2

# Step 3: Add the glassmorphism rectangle
def add_glassmorphism(image, position, size, radius=25, fill=(255, 255, 255, 40), outline=(255, 255, 255, 80)):
    glass = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(glass)
    
    x, y = position
    w, h = size
    
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline)
    return Image.alpha_composite(image, glass)

# Apply the glass panel
final_image = add_glassmorphism(blurred, (panel_x, panel_y), (panel_width, panel_height))

# Save and display the frosted result
final_image.save("glassmorphism_centered.png")
# final_image.show()
