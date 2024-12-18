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

3. Set up PostgreSQL Database:

a. Install PostgreSQL on your system if not already installed:
   - Windows: Download and install from https://www.postgresql.org/download/windows/
   - macOS: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql`

b. Create a new PostgreSQL database:
```bash
# Log into PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE financial_learning;
```

c. Create required tables:
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Game progress table
CREATE TABLE game_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    game_name VARCHAR(100) NOT NULL,
    points INTEGER DEFAULT 0,
    correct_predictions INTEGER DEFAULT 0,
    total_predictions INTEGER DEFAULT 0,
    highest_streak INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Achievements table
CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    achievement_name VARCHAR(100) NOT NULL,
    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, achievement_name)
);
```

d. Set up environment variables:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/financial_learning
```

Note: Replace `your_password` with your PostgreSQL password. The default port is usually 5432.

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
