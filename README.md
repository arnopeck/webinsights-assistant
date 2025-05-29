# WebInsights Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A multi-agent system that simplifies web analytics data, making Google Analytics insights accessible and actionable for all team members.

![WebInsights Assistant Architecture](architecture_diagram.png)

## 🌟 The Problem

Google Analytics, especially after the GA4 update, has become increasingly complex and difficult to use. Even professionals struggle to extract useful information from the platform. WebInsights Assistant aims to solve this problem by providing a simplified and intuitive interface for web data analysis.

## 🚀 Our Solution

WebInsights Assistant is a multi-agent system built with Google's Agent Development Kit (ADK) that orchestrates specialized agents to extract, analyze, and present web analytics data in an intuitive way. The system makes web analytics accessible to non-technical users and facilitates collaboration between different roles involved in a web project.

## 🤖 Multi-Agent Architecture

The system consists of six specialized agents working together:

1. **Orchestration Agent**: Coordinates the workflow between other agents, manages user requests, and personalizes output based on specific needs.

2. **Data Extraction Agent**: Connects to Google Analytics APIs to extract raw data, handling authentication, query formulation, and error management.

3. **Data Processing Agent**: Processes raw data to make it more understandable, including data cleaning, derived metrics calculation, and trend identification.

4. **Insight Generation Agent**: Analyzes processed data to generate meaningful insights, identifying patterns, correlations, and improvement opportunities.

5. **Visualization Agent**: Creates intuitive visualizations of data and insights, producing charts, dashboards, and visual reports.

6. **Recommendation Agent**: Analyzes insights and trends to generate personalized strategic recommendations, suggesting concrete actions, identifying relevant emerging technologies, and providing advice on digital strategy.

## 🛠️ Technologies Used

- **Agent Development Kit (ADK)**: Framework for implementing the multi-agent architecture
- **Google Analytics Data API v1**: For accessing GA4 data
- **Google Cloud**: For hosting and deployment
- **Vertex AI**: For machine learning and advanced analysis capabilities
- **BigQuery**: For storing and analyzing large volumes of data
- **Python**: Core programming language for implementation

## ✨ Key Features

- **Simplified Dashboard**: Clear overview of key website metrics
- **Natural Language Insights**: Technical concepts translated into understandable information
- **Intuitive Visualizations**: Charts and reports that make data easily comprehensible
- **Strategic Recommendations**: Practical advice based on AI analysis of trends
- **Collaborative Reports**: Easily shareable and understandable by all team members

## 📊 Use Cases

- **Simplified Dashboard**: Get a clear overview of your website's key metrics without navigating through Google Analytics' complex interface.
- **Trend Analysis**: Easily identify and visualize trends in traffic, conversions, and user behavior.
- **Automated Reports**: Receive regular reports with meaningful insights without accessing Google Analytics.
- **Comparative Analysis**: Compare your website's performance with previous periods or industry benchmarks.
- **Practical Recommendations**: Get concrete suggestions to improve your website's performance.

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- Google Cloud account with Google Analytics access
- Google Analytics 4 property

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/webinsights-assistant.git
   cd webinsights-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure Google Analytics credentials:
   - Create a service account in Google Cloud Console
   - Download the JSON key file
   - Place it in the project directory as `ga_credentials.json`
   - Share your GA4 property with the service account email

4. Run the application:
   ```
   python main.py --property-id=YOUR_GA4_PROPERTY_ID
   ```

## 🧪 Running the Test Suite

To run the automated tests for WebInsights Assistant:

1. **Install all dependencies** (see Installation section above).
2. **Run the test suite** from the project root:
   ```sh
   python3 -m unittest discover -s tests -p 'test_*.py'
   ```
   All tests are asynchronous and use the ADK agent `run` method. The test suite covers agent orchestration, data extraction, processing, insight generation, visualization, Google Analytics integration, and end-to-end flows.

**Note:**
- The tests do not require real Google Analytics credentials; simulated data is used if credentials are missing.
- The test files are now located in the `tests/` folder, following Python best practices.

## 📖 Documentation

For detailed documentation, please see the [documentation.md](documentation.md) file.

## 🏗️ Architecture

The architecture diagram is available in [architecture_diagram.txt](architecture_diagram.txt).

## 🎯 Hackathon Presentation

Our hackathon presentation is available in [presentation.md](presentation.md).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- Developed for the Google Cloud Agent Development Kit Hackathon
- Created with a focus on simplifying technology and creating real value for users

## 📧 Contact

For any questions or feedback, please open an issue on this repository.

---

*WebInsights Assistant - Making web analytics accessible to everyone*
