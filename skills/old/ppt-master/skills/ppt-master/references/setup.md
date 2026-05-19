# Environment Setup

> Read this file when setting up the environment for the first time or troubleshooting dependency issues.

## Docker Mount Path Convention

- Skill directory: `/mnt/skills/public/ppt-master/skills/ppt-master` → **`SKILL_DIR`**
- User projects: `/mnt/user-data/projects/`
- User uploads: `/mnt/user-data/uploads/`
- User workspace: `/mnt/user-data/workspace/`

## Install Dependencies

```bash
pip install -r /mnt/skills/public/ppt-master/requirements.txt
```

## Key Dependency Groups

| Group | Packages | Purpose |
|-------|----------|---------|
| **SVG to PPTX** | `python-pptx`, `svglib`, `reportlab` (or `cairosvg`) | Convert SVG to PowerPoint |
| **PDF conversion** | `PyMuPDF` | Extract text/images from PDF |
| **Document conversion** | `mammoth`, `markdownify`, `ebooklib`, `nbconvert` | Convert DOCX/HTML/EPUB/IPYNB |
| **Image processing** | `Pillow`, `numpy` | Image analysis and watermark removal |
| **Web scraping** | `requests`, `beautifulsoup4`, `curl_cffi` (optional) | Web page to Markdown |
| **AI image generation** | `google-genai`, `openai` (backend-specific) | Generate images with AI |

## Environment Variables for Image Generation

```bash
# Set in Docker environment or .env file
IMAGE_BACKEND=gemini  # or openai, minimax, qwen, zhipu, etc.
GEMINI_API_KEY=your_key_here  # if using Gemini backend
OPENAI_API_KEY=your_key_here  # if using OpenAI backend
# ... other provider-specific keys
```
