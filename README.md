# cvAnalysingTool  

cvAnalysingTool is a Python chatbot designed to efficiently parse and filter large volumes of CVs using **OpenAI APIs** along with **spaCy** and **nltk** NLP libraries. The chatbot is built with a strong focus on both **functionality** and **cost efficiency** to ensure optimal performance and scalability.

## Key Focus Areas  

### **Functional Considerations**  
- **Low Latency & Quick Response**: Optimized for minimal response time to ensure smooth interaction.  
- **Security & Topic Control**: Railguards prevent users from hijacking or straying conversations away from CV filtering and analysis.  
- **In-House OCR for CV Parsing**: A custom-built OCR system allows text extraction from various CV formats for detailed analysis.  

### **Non-Functional & Technical Considerations**  
- **Cost-Effective API Usage**: Optimized OpenAI API calls to keep costs low, preventing unnecessary expenses.  
- **Rate Limiting & API Efficiency**: Ensures controlled API usage to maintain stable performance and avoid excessive requests.  
- **Well-Defined Prompts**: Structured prompts include clear goals, expected response format, warnings, and content guidelines to keep the chatbot focused.  
- **In-House NLP for Text Extraction**: A non-LLM, in-house NLP pipeline efficiently extracts structured data from **PDFs** and **DOCX** files (e.g., name, address, experience, education). This significantly reduces costs compared to prompting an LLM for parsing at scale.  

By integrating **intelligent filtering**, **cost optimizations**, and **security mechanisms**, cvAnalysingTool offers an **efficient, scalable, and cost-effective** solution for automated CV analysis.




## Installation

As a prerequisite Docker CLI and Git should be preinstalled on your system

```bash
git clone https://github.com/kush96/cvAnalysingTool.git

cd cvAnalysingTool

docker build -t cv_analyser_build .

docker run -it -e OPENAI_API_KEY=<OPENAI_API_KEY> cv_analyser_build

```

## Usage

The bot processes CVs stored inside the `data/sample_cvs` directory.

### **Startup & Parsing Time**
Once you run the bot via Docker, it will begin analyzing the CVs. Parsing each CV takes approximately **3 seconds**, and the bot will display the following message:



```
Pls wait while CVs are being analysed.
The CVs are currently being analysed and parsed; this process may take up to a couple of minutes.
Based on our current benchmarks, parsing 1 CV takes approximately 3 seconds.
```


### **Applying Initial Filters**
Before interacting with the chatbot, you can apply some basic filters. Press **Enter** to skip any filter or input your criteria:


```
Enter required skills (comma-separated): ..... Press Enter to Skip 
java,spring

Minimum years of experience: ..... Press Enter to Skip 
4

Designations to filter by (comma-separated): ..... Press Enter to Skip:
backend developer
```

Once the initial filters are applied, the bot will generate a **shortlist** of relevant CVs:


```
The below CVs must be of interest to you 
['sample.cv.2.soft.dev.pdf', 'sample.cv.3.soft.dev.pdf']
```


### **Interacting with the Chatbot**
After filtering, you will enter a **chat session** where the bot helps you refine the selection further.


```
Robo : Hello!! I am here to help you with clearing through the clutter on CVs..
```
At any point, you can **restart filtering** or **exit the chat** simply by instructing the bot.

## Basic Working

There are 2 Majo

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
