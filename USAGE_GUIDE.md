# Groover Podcast-to-Article Platform - Usage Guide

## 🎯 Complete Workflow Tutorial

### Step-by-Step: From Audio to Published Article

---

## 1️⃣ Upload & Process Audio

### What You Need
- MP3 podcast file(s)
- Files can be any size (auto-chunked if >25MB)

### Steps
1. Navigate to **"Upload & Process"** page
2. Drag & drop MP3 files or click to browse
3. Review uploaded files (shows size, duration)
4. Click **"🚀 Process Files"**
5. Wait for processing (progress bar shows status)

### What Happens
- File validation
- Audio analysis (duration, channels, sample rate)
- Automatic chunking if needed
- Files stored in session for transcription

### Tips
- ✅ Upload multiple files at once
- ✅ Check audio quality before processing
- ✅ Files are temporarily stored (cleared on refresh)

---

## 2️⃣ Transcribe Audio

### What You Need
- Processed audio files from Step 1
- OpenAI API key (in .env)

### Steps
1. Navigate to **"Transcribe"** page
2. Choose language settings:
   - **Auto-detect** (recommended) or
   - Select specific language
3. Select files to transcribe (checkboxes)
4. Click **"🚀 Transcribe X file(s)"**
5. Wait for transcription (parallel processing)

### What Happens
- Uses gpt-4o-transcribe model (best quality)
- Parallel chunk processing for speed
- Context prompts for music terminology
- Auto-reassembly of chunks
- Transcripts stored in session

### Transcription Features
- Language detection
- Word count display
- Segment information
- Download transcript (.txt)
- Preview in UI

### Tips
- ✅ Let it auto-detect language (usually accurate)
- ✅ Large files process faster (parallel chunks)
- ✅ Download transcripts as backup

---

## 3️⃣ Generate Content

### What You Need
- Transcribed audio from Step 2
- Anthropic API key (in .env)
- Optional: Custom terms/names

### Steps

#### A. Select Transcription
1. Navigate to **"Generate Content"** page
2. Choose which transcript to use (dropdown)
3. Preview transcript

#### B. Configure Correction (Optional but Recommended)
1. Check **"Apply smart correction"**
2. Add custom terms:
   - Artist names (e.g., "Billie Eilish")
   - Labels (e.g., "Universal Music")
   - Technical terms (e.g., "LoFi", "Ableton")
   - Platform names
3. Enter one per line or comma-separated

#### C. Set Content Options
1. **Article Length:**
   - Long Form (2000+ words)
   - Short Form (500-800 words)

2. **Add Groover CTAs:** ✅ (recommended)

3. **Editorial Angle** (optional):
   - Specific focus/perspective
   - Example: "Focus on independent artists"

4. **Additional Instructions** (optional):
   - Style preferences
   - Specific requirements

#### D. Generate
- Click **"🚀 Generate Article"** OR
- Click **"💡 Suggest Editorial Angles"** first

### What Happens

**If Using Correction:**
1. GPT-4 corrects transcript errors
2. Custom terms preserved exactly
3. Music glossary applied
4. Corrected transcript used for generation

**Content Generation:**
1. Claude Sonnet 4.5 analyzes transcript
2. Generates article in Groover's style
3. Creates SEO metadata
4. Generates social snippets
5. (Optional) Adds Groover CTAs

### Output Includes
- ✅ Full article (editable in UI)
- ✅ SEO title & meta description
- ✅ URL slug
- ✅ Keywords/tags
- ✅ Social media snippets (Twitter, Instagram, LinkedIn)
- ✅ Download buttons (.txt, .md)

### Editorial Angles Feature
Click "💡 Suggest Editorial Angles" to get:
- 3 different article perspectives
- Compelling titles
- Key talking points
- Target audience analysis

### Tips
- ✅ Always use correction with custom terms
- ✅ Add artist names, labels, specific terminology
- ✅ Try different editorial angles
- ✅ Edit generated content in UI before saving
- ✅ Save custom terms for reuse

---

## 4️⃣ Translate Articles

### What You Need
- Generated articles from Step 3
- Anthropic API key (in .env)

### Steps

#### A. Select Article
1. Navigate to **"Translate"** page
2. Choose article to translate (dropdown)
3. Preview article

#### B. Select Languages
- Check boxes for target languages:
  - French, Spanish, German
  - Italian, Portuguese, Dutch
  - Japanese, Korean, Chinese
- Select 1 or multiple languages

#### C. Configure Options
1. **Cultural Adaptation:** ✅ (recommended)
   - Adapts idioms and references
   - Provides cultural notes

2. **Translate SEO Metadata:** ✅
   - Translates titles, descriptions
   - Adapts keywords per language

#### D. Translate
- Click **"🚀 Translate to X Language(s)"**
- Wait for parallel processing

### What Happens
1. Parallel translation to all selected languages
2. SEO keywords preserved/adapted
3. Emojis and formatting maintained
4. Cultural references adapted
5. Technical terms handled correctly

### Output Per Language
- ✅ Translated article (full)
- ✅ Cultural adaptation notes
- ✅ Translated SEO metadata
- ✅ Adapted keywords
- ✅ Download button

### Translation Features
- Language detection
- Parallel processing (fast)
- Cultural notes explaining changes
- SEO character limits respected
- History of all translations

### Tips
- ✅ Enable cultural adaptation
- ✅ Translate SEO metadata too
- ✅ Review cultural notes
- ✅ Download all versions
- ✅ Translate to multiple languages at once (faster)

---

## 5️⃣ Export & Download

### What You Need
- Generated/translated articles

### Steps

#### A. Select Article
1. Navigate to **"Export"** page
2. Choose article to export
3. Preview article

#### B. Choose Format(s)

**Text Formats:**
- 📥 Markdown (.md) - Original format
- 📥 Plain Text (.txt) - No formatting

**Web Formats:**
- 📥 HTML (styled) - With CSS
- 📥 HTML (no CSS) - Plain HTML

**Data Formats:**
- 📥 JSON - Structured data
- 📥 WordPress JSON - Import-ready

#### C. Content Components

**Key Quotes Tab:**
- Extracted quotes (up to 5)
- Perfect for social graphics
- Download as .txt

**Main Insights Tab:**
- Key takeaways (up to 3)
- Bullet-point format
- Download as .txt

**Social Graphics Tab:**
- Header cards
- Quote cards
- Tip cards
- Download as JSON

#### D. WordPress Preview
- View WordPress-ready data
- Title, excerpt, categories, tags
- SEO metadata
- HTML content preview

#### E. Batch Export
If you have multiple articles:
1. Select format (Markdown, HTML, JSON, WordPress)
2. Click **"📥 Export All Articles"**
3. Download combined file

### Export Formats Explained

**Markdown (.md)**
- Original format
- Best for editing
- Version control friendly

**HTML (styled)**
- Complete webpage
- Includes CSS
- Ready to publish

**HTML (no CSS)**
- Clean HTML only
- For CMS import

**JSON**
- Structured data
- Includes all metadata
- API-friendly

**WordPress JSON**
- Direct import format
- Categories & tags included
- SEO fields populated

### Tips
- ✅ Export to multiple formats
- ✅ Use WordPress JSON for easy import
- ✅ Download quotes/insights separately
- ✅ Use JSON for custom integrations
- ✅ Batch export saves time

---

## 🎨 Custom Terms Best Practices

### When to Use Custom Terms

**Always add:**
- Artist names mentioned
- Record label names
- Specific product names
- Custom terminology
- Industry-specific acronyms

### How to Format

**Line-separated:**
```
Billie Eilish
Universal Music Group
Ableton Live
LoFi
A&R
```

**Comma-separated:**
```
Billie Eilish, Universal Music Group, Ableton Live, LoFi, A&R
```

### Examples

**For Electronic Music Podcast:**
```
Ableton Live
Serum
Splice
deadmau5
Eric Prydz
Progressive House
```

**For Hip-Hop Podcast:**
```
J. Cole
Dreamville
808
TR-808
boom bap
sampling
```

**For Industry Podcast:**
```
Spotify for Artists
DistroKid
ASCAP
BMI
sync licensing
360 deal
```

### Tips
- ✅ Include exact capitalization
- ✅ Add variations (e.g., "Hip-Hop" and "hip-hop")
- ✅ Include acronyms and full names
- ✅ Update glossary for frequent terms
- ✅ Save your custom terms list for reuse

---

## 🌍 Multi-Language Strategy

### Recommended Language Sets

**European Markets:**
- French (fr)
- Spanish (es)
- German (de)
- Italian (it)

**Global Reach:**
- English (en) - default
- Spanish (es)
- French (fr)
- Portuguese (pt)
- Japanese (ja)

**Full Coverage:**
- All 10 supported languages

### Cultural Adaptation Tips

**When to enable:**
- ✅ Content with idioms
- ✅ Cultural references
- ✅ Local music scenes
- ✅ Regional terminology

**Review cultural notes for:**
- Changed expressions
- Adapted references
- Local equivalents
- Regional preferences

### SEO Per Language

**Keywords adapt to:**
- Search behavior per market
- Local terminology
- Regional preferences
- Character limits (titles, descriptions)

---

## ⚙️ Configuration Guide

### Environment Variables (.env)

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...     # Claude API
OPENAI_API_KEY=sk-proj-...       # Whisper API

# Optional (for future features)
DB_USER=your_db_user
DB_PASSWORD=your_db_password
WP_USERNAME=your_wp_user
WP_PASSWORD=your_wp_password
```

### API Key Setup

**Anthropic API Key:**
1. Visit console.anthropic.com
2. Create API key
3. Add to .env as ANTHROPIC_API_KEY

**OpenAI API Key:**
1. Visit platform.openai.com
2. Create API key
3. Add to .env as OPENAI_API_KEY

### Model Configuration

**Default Models (Recommended):**
- Transcription: `gpt-4o-transcribe`
- Content/Translation: `claude-sonnet-4-5-20250929`
- Correction: `gpt-4`

**Alternative Models:**
- Transcription: `gpt-4o-mini-transcribe` (faster, cheaper)
- Translation: Same model as content (consistent)

---

## 🔍 Troubleshooting

### Common Issues

**"No processed audio files found"**
- Go back to Upload & Process
- Upload and process files first

**"ANTHROPIC_API_KEY not found"**
- Check .env file exists
- Verify API key format
- Restart Streamlit

**"Transcription failed"**
- Check OpenAI API key
- Verify file isn't corrupted
- Check audio file size/format

**"Translation error"**
- Check Anthropic API key
- Verify language code
- Check API rate limits

**Session data lost**
- Data clears on page refresh
- Download important content
- Database coming in Task 9

### Best Practices

**File Management:**
- ✅ Process files in batches
- ✅ Download transcripts immediately
- ✅ Export articles regularly
- ✅ Keep backup of important content

**API Usage:**
- ✅ Monitor usage/costs
- ✅ Use appropriate models
- ✅ Handle rate limits
- ✅ Test with small files first

**Workflow:**
- ✅ Follow sequential steps
- ✅ Review corrections before generation
- ✅ Edit articles before translation
- ✅ Export to multiple formats

---

## 📊 Understanding Output

### Metrics Explained

**Audio Processing:**
- Duration: Length in minutes
- Chunks: Number of 25MB segments
- Size: File size in MB

**Transcription:**
- Language: Detected/selected language
- Words: Word count
- Segments: Number of time-stamped segments
- Duration: Audio duration in seconds

**Content Generation:**
- Word Count: Total words in article
- Style: Long-form or short-form
- Custom Terms: Number of terms preserved

**Translation:**
- Total Translations: All successful translations
- Languages Covered: Unique languages
- Articles Translated: Source articles

### Quality Indicators

**Good Transcription:**
- ✅ Detected language is correct
- ✅ Technical terms are accurate
- ✅ Proper punctuation
- ✅ Clear speaker distinction

**Good Article:**
- ✅ Groover tone maintained
- ✅ Emojis used strategically
- ✅ Clear structure with headers
- ✅ Actionable insights
- ✅ SEO optimized

**Good Translation:**
- ✅ Formatting preserved
- ✅ Cultural notes make sense
- ✅ SEO metadata adapted
- ✅ Natural reading flow

---

## 🚀 Advanced Features

### Batch Operations

**Batch Processing:**
- Upload multiple MP3s
- Process all at once
- Parallel transcription
- Faster workflow

**Batch Export:**
- Export all articles
- Single download
- Combined file
- All formats supported

### Editorial Angles

**Use Cases:**
- Generate 3 different perspectives
- A/B test different approaches
- Target different audiences
- Maximize content from one podcast

**How to Use:**
1. Transcribe podcast
2. Click "Suggest Editorial Angles"
3. Review 3 suggested angles
4. Generate article for each angle
5. Publish all or choose best

### Social Media Optimization

**Generated Snippets:**
- Twitter/X: 280 chars + hashtags
- Instagram: Engaging caption + emojis
- LinkedIn: Professional tone
- Quotes: Graphic-ready text

**Best Practice:**
- Use quotes for image posts
- Use insights for carousel posts
- Use snippets for text posts
- Maintain consistent branding

---

## 💡 Pro Tips

### Workflow Optimization

1. **Prepare Audio:**
   - Clean audio quality
   - Remove long silences
   - Normalize volume
   - Convert to MP3

2. **Custom Terms Library:**
   - Maintain a master list
   - Update after each podcast
   - Include common misspellings
   - Organize by category

3. **Template Angles:**
   - Save successful angles
   - Reuse for similar content
   - A/B test variations
   - Track performance

4. **Translation Strategy:**
   - Translate proven articles
   - Start with key markets
   - Expand gradually
   - Monitor engagement per language

### Content Strategy

**Article Types:**
- **How-to** (tactical, actionable)
- **Industry insights** (trends, analysis)
- **Artist stories** (inspiration, case studies)
- **Tool reviews** (products, platforms)

**SEO Strategy:**
- Focus keywords per article
- Optimize for long-tail
- Internal linking (manual step)
- Update keywords per language

**Publishing Cadence:**
- 2-3 articles per podcast
- Different angles/lengths
- Stagger publication
- Repurpose across channels

---

## 📈 Success Metrics

### Track These KPIs

**Production:**
- Podcasts processed
- Articles generated
- Languages covered
- Total word count

**Quality:**
- Correction accuracy
- Translation quality
- SEO score (external tool)
- Readability score

**Engagement:**
- Page views (Google Analytics)
- Time on page
- Social shares
- Downloads/exports

### Optimization Goals

**Speed:**
- < 2 min processing per podcast
- < 3 min transcription
- < 1 min article generation
- < 30 sec per translation

**Quality:**
- 95%+ transcription accuracy
- 100% custom term preservation
- Natural translation flow
- SEO score > 80

---

**Last Updated:** 2025-10-06
**Version:** 1.0
**For Support:** Check DEVELOPMENT_STATUS.md or GitHub issues
