# 🤖 RockyBot: News Research Tool

A beautiful and intelligent news research tool powered by Google Gemini AI that allows you to analyze multiple news articles and ask questions about their content.

## ✨ Features

- **Google Gemini AI Integration**: Powered by Google's latest Gemini Pro model for accurate and intelligent responses
- **Beautiful UI**: Modern, animated interface with gradient backgrounds and smooth transitions
- **Multi-URL Processing**: Analyze up to 3 news articles simultaneously
- **Intelligent Q&A**: Ask questions about the processed articles and get detailed answers with sources
- **Vector Search**: Uses FAISS for efficient similarity search and retrieval
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key

### Installation

1. **Clone or download the project files**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google Gemini API key**
   
   Edit the `.env` file and replace `your_google_gemini_api_key_here` with your actual Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   
   To get a Google Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key and paste it in the `.env` file

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser**
   
   The application will automatically open in your default browser at `http://localhost:8501`

## 📖 How to Use

1. **Add News Article URLs**: In the sidebar, paste up to 3 news article URLs that you want to analyze

2. **Process URLs**: Click the "🚀 Process URLs" button to load and process the articles

3. **Ask Questions**: Once processing is complete, type your questions in the main input field

4. **Get Answers**: The AI will provide detailed answers along with source references

## 🎨 UI Features

- **Animated Header**: Beautiful gradient text animation
- **Hover Effects**: Interactive buttons with smooth hover transitions
- **Loading Animations**: Elegant loading spinners and progress indicators
- **Gradient Backgrounds**: Modern gradient designs for better visual appeal
- **Responsive Layout**: Optimized for both desktop and mobile viewing

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS animations
- **AI Model**: Google Gemini Pro for text generation
- **Embeddings**: Google Generative AI Embeddings (models/embedding-001)
- **Vector Store**: FAISS for efficient similarity search
- **Text Processing**: LangChain for document processing and retrieval

### Key Components
- **Document Loading**: UnstructuredURLLoader for web content extraction
- **Text Splitting**: RecursiveCharacterTextSplitter for optimal chunk sizes
- **Retrieval Chain**: RetrievalQAWithSourcesChain for question-answering with sources

## 📁 Project Structure

```
├── main.py              # Main Streamlit application
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (API keys)
├── README.md           # This file
└── faiss_store_gemini.pkl  # Generated vector store (after first use)
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Google Gemini API key is correctly set in the `.env` file

2. **Module Not Found**: Ensure all dependencies are installed with `pip install -r requirements.txt`

3. **URL Processing Fails**: Check that the URLs are accessible and contain readable content

4. **Slow Processing**: Large articles may take time to process; this is normal

### Performance Tips

- Use articles with clear, readable content for best results
- Avoid very long articles (>10,000 words) for faster processing
- Process articles one batch at a time for optimal performance

## 🔒 Privacy & Security

- Your API key is stored locally in the `.env` file
- Article content is processed locally and not stored permanently
- Vector embeddings are saved locally in `faiss_store_gemini.pkl`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## 📞 Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.

---

**Powered by Google Gemini AI 🚀 | Built with ❤️ using Streamlit**

