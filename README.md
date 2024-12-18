# AI-Powered Financial Learning Platform 📈

An advanced AI-powered financial learning platform that transforms stock market education into an interactive, engaging experience. The application combines cutting-edge technologies to provide personalized, gamified financial literacy tools.

## Features

- 📊 Real-time Stock Data Dashboard
- 🤖 AI-Powered Market Mentor Chatbot
- 🎮 Interactive Financial Learning Games
- 📈 Technical Analysis Tools
- 💹 Portfolio Management
- 📱 Social Sharing Capabilities
- 🏆 Achievement System
- 📊 Progress Tracking

## Technologies Used

- Python 3.11
- Streamlit (UI Framework)
- YFinance (Real-time Stock Data)
- OpenAI GPT-4 (AI Chatbot)
- PostgreSQL (Database)
- Plotly (Interactive Charts)
- Pandas (Data Processing)

## Prerequisites

Before running the application, ensure you have:

1. Python 3.11 installed
2. PostgreSQL database server
3. OpenAI API key
4. Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-learning-platform
```

2. Install required packages:
```bash
pip install streamlit yfinance openai psycopg2-binary pandas plotly bcrypt
```

3. Set up environment variables:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@host:port/database
```

## Running the Application

1. Start the application:
```bash
streamlit run main.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Features Overview

### Stock Data Dashboard
- Real-time stock price data
- Interactive price charts
- Financial metrics and ratios
- AI-powered health scores
- Dividend history visualization

### Market Mentor Chatbot
- Personalized financial education
- Interactive Q&A
- Suggested learning topics
- Market analysis insights

### Financial Learning Games
- Price prediction game
- Achievement system
- Progress tracking
- Learning streaks

### Progress Dashboard
- Learning statistics
- Achievement badges
- Performance metrics
- Learning progress visualization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
