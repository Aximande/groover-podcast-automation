# 🎙️ Groover Podcast-to-Article Automation Platform

Transform podcast audio files into engaging, multilingual blog articles optimized for Groover's content strategy.

![Groover Logo](Logo_GROOVER.png)

## ✨ Features

- **🎤 Audio Transcription** - Whisper API with intelligent chunking (10-minute segments)
- **🔧 Smart Correction** - GPT-4o-mini post-processing with custom terminology
- **✍️ Content Generation** - Claude Sonnet 4.5 for Groover-style articles
- **🔬 A/B Testing** - Compare content with/without reference articles
- **🌍 Multi-Language Translation** - 10 languages with cultural adaptation
- **📤 Multi-Format Export** - Markdown, HTML, WordPress, JSON
- **📊 SEO Optimization** - Auto-generated metadata and social snippets

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/groover_podcast_article_maker.git
cd groover_podcast_article_maker
```

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Configure API Keys

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### 4. Run the Application

```bash
streamlit run main.py
```

Open your browser at `http://localhost:8501`

## 📋 Requirements

- Python 3.9+
- OpenAI API key (for Whisper transcription)
- Anthropic API key (for Claude content generation)
- FFmpeg (for audio processing)

## 🎯 Workflow

1. **Upload & Process** - Upload MP3 files, automatic chunking for large files
2. **Transcribe** - Whisper API transcription with language detection
3. **Generate Content** - Claude-powered article generation with Groover's tone
4. **Translate** (Optional) - Translate to 10 languages
5. **Export** - Download in multiple formats

## 🔧 Configuration

### Custom Terms

Add specific artist names, labels, or terminology in the "Custom Terms" section to ensure proper spelling and preservation during correction.

### A/B Testing

Enable "Use Example Articles" to include Groover's reference articles in the generation prompt for better style matching.

### Article Styles

- **Long Form**: 2000-2500 words
- **Short Form**: 500-800 words

## 📊 Cost Estimates

### Transcription (Whisper API)
- $0.006 per minute of audio
- Example: 60-minute podcast = $0.36

### Correction (GPT-4o-mini)
- ~$0.01 per 10,000 words
- Example: 12,000 words = $0.012

### Content Generation (Claude Sonnet 4.5)
- Input: $3.00 per million tokens
- Output: $15.00 per million tokens
- Example: Long article (2,500 words) ≈ $0.15-0.30

## 🗂️ Project Structure

```
groover_podcast_article_maker/
├── main.py                      # Streamlit app entry point
├── requirements.txt             # Python dependencies
├── Logo_GROOVER.png            # Groover logo
├── .env.example                # API keys template
├── src/
│   ├── audio_processing.py     # Audio chunking (10-min segments)
│   ├── transcription.py        # Whisper API integration
│   ├── correction.py           # GPT-4 post-processing
│   ├── content_generation.py   # Claude article generation
│   ├── translation.py          # Multi-language translation
│   ├── export_formats.py       # Export functionality
│   ├── groover_examples.py     # Reference articles loader
│   └── pages/                  # Streamlit UI pages
├── data/
│   └── music_glossary.json     # Music industry terminology
├── groover_tone_of_voice/      # Reference articles (10 examples)
├── tests/                      # Unit tests
└── docs/                       # Documentation

```

## 🌍 Supported Languages

- English (en)
- French (fr)
- Spanish (es)
- German (de)
- Italian (it)
- Portuguese (pt)
- Dutch (nl)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## 📝 Documentation

- [Usage Guide](USAGE_GUIDE.md) - Complete workflow tutorial
- [A/B Testing Guide](AB_TESTING_GUIDE.md) - Reference articles feature
- [Smart Correction Explained](SMART_CORRECTION_EXPLAINED.md) - How correction works
- [Development Status](DEVELOPMENT_STATUS.md) - Project progress

## 🐛 Troubleshooting

### Transcription Fails
- Check OpenAI API key in `.env`
- Ensure audio file is valid MP3/M4A
- Check API quota/billing

### Generation Fails
- Check Anthropic API key in `.env`
- Ensure sufficient API credits
- Check transcript length (very long = skip correction)

### Import Errors
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`
- Download spaCy model: `python -m spacy download en_core_web_sm`

## 🚀 Deployment on Streamlit Cloud

1. Push code to GitHub (public repo)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets in Streamlit Cloud dashboard:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
5. Deploy!

## 🔒 Security Notes

- **Never commit `.env` file** (contains API keys)
- Use Streamlit Secrets for deployment
- Make repo private after testing if desired

## 📈 Features Implemented (Tasks 1-8)

✅ Task 1: Project Setup & Environment  
✅ Task 2: Audio Processing & Chunking (10-min segments)  
✅ Task 3: Whisper API Transcription  
✅ Task 4: Smart Correction System  
✅ Task 5: Claude Content Generation  
✅ Task 6: Multi-Format Export  
✅ Task 7: Multi-Language Translation  
✅ Task 8: Streamlit User Interface  

## 🔮 Future Enhancements (Tasks 9-12)

⏳ Task 9: Database Storage (PostgreSQL)  
⏳ Task 10: WordPress Integration  
⏳ Task 11: Analytics & Reporting  
⏳ Task 12: System Integration & Deployment  

## 📄 License

Proprietary - Groover Internal Tool

## 🙏 Credits

Built with:
- [OpenAI Whisper](https://openai.com/research/whisper) - Speech-to-text
- [Anthropic Claude](https://www.anthropic.com/) - Content generation
- [Streamlit](https://streamlit.io/) - Web interface
- [spaCy](https://spacy.io/) - NLP
- [pydub](https://github.com/jiaaro/pydub) - Audio processing

---

**Made with ❤️ for Groover**
