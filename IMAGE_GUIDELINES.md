# Image Guidelines for SirTechify Website

## Folder Structure
```
static/
├── images/
│   ├── profile/         # Professional headshots and avatars
│   ├── projects/        # Project screenshots and thumbnails
│   ├── icons/           # Technology and skill icons
│   └── background/      # Background images and patterns
```

## Image Recommendations

### 1. Profile Images (`/static/images/profile/`)
- **File**: `profile.jpg` (or .png)
- **Size**: 400x400px (square)
- **Style**: Professional headshot with a clean background
- **Source Suggestions**:
  - Take a professional headshot
  - Use a high-quality selfie with good lighting
  - Consider using a service like [Photofeeler](https://www.photofeeler.com/) for feedback

### 2. Project Images (`/static/images/projects/`)
- **Files**:
  - `race-predictor.jpg`
  - `robo-demo-1000.jpg`
  - `project3.jpg` (or your project name)
- **Size**: 1200x630px (16:9 ratio)
- **Style**: Screenshots or professional mockups
- **Source Suggestions**:
  - Take actual screenshots of your projects
  - Use [CleanShot](https://cleanshot.com/) for clean screenshots
  - Create mockups using [Smartmockups](https://smartmockups.com/)

### 3. Icons (`/static/images/icons/`)
- **Files**:
  - `python.png`
  - `flask.png`
  - `electronics.png`
  - `ai-ml.png`
- **Size**: 64x64px or 128x128px
- **Style**: Flat, monochrome, or colored icons
- **Source Suggestions**:
  - [Simple Icons](https://simpleicons.org/)
  - [Font Awesome](https://fontawesome.com/)
  - [Material Icons](https://fonts.google.com/icons)

### 4. Background Images (`/static/images/background/`)
- **Files**:
  - `hero-bg.jpg` (for the header section)
  - `pattern.png` (subtle pattern)
- **Size**: 1920x1080px (for hero), smaller for patterns
- **Style**: Subtle, non-distracting, professional
- **Source Suggestions**:
  - [Gradient Hunt](https://gradienthunt.com/)
  - [Subtle Patterns](https://www.toptal.com/designers/subtlepatterns/)
  - [Unsplash](https://unsplash.com/backgrounds)

## Image Optimization

1. **File Formats**:
   - Use JPG for photos
   - Use PNG for graphics with transparency
   - Consider WebP for better compression

2. **Optimization Tools**:
   - [TinyPNG](https://tinypng.com/)
   - [Squoosh](https://squoosh.app/)
   - [ImageOptim](https://imageoptim.com/mac)

3. **Naming Conventions**:
   - Use lowercase with hyphens (e.g., `project-screenshot-1.jpg`)
   - Be descriptive but concise
   - Avoid spaces and special characters

## Adding Images to Your Site

1. Place images in their respective folders
2. Reference them in your HTML/CSS:
   ```html
   <!-- In HTML -->
   <img src="{{ url_for('static', filename='images/profile/profile.jpg') }}" alt="Profile Picture">
   
   /* In CSS */
   .hero {
     background-image: url("{{ url_for('static', filename='images/background/hero-bg.jpg') }}");
   }
   ```

## Next Steps

1. Create the folder structure
2. Add your images following the guidelines above
3. Update the HTML/CSS to reference these images
4. Optimize all images before final deployment

Would you like me to help you implement any of these changes or provide more specific recommendations for your projects?
