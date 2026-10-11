# LLM-Reasoning-Experiment
A comparative study of direct prompting and structured reasoning prompting using a large language model.
# Comparative Analysis of Direct Prompting and Structured Reasoning Prompting in Large Language Models

## 📌 Project Overview

This project investigates how different prompting strategies affect the performance of Large Language Models (LLMs).

It compares two prompting approaches:

- **Direct Prompting:** The model is asked to provide the final answer directly.
- **Structured Reasoning Prompting:** The model is asked to provide an organized explanation before giving its final answer.

The experiment evaluates answer accuracy, error rate, response time, and token usage to understand the trade-offs between these approaches.

## 🎯 Research Question

Does structured reasoning prompting improve answer accuracy enough to justify its additional response time and token usage?

## 🔬 Research Hypotheses

- **H1:** Structured reasoning prompting may improve accuracy on multi-step problems.
- **H2:** Structured reasoning prompting may increase response length and response time.
- **H3:** The effectiveness of each prompting strategy may vary depending on the type of problem.

These are hypotheses to investigate, not assumed conclusions.

## 📊 Dataset

The dataset contains 12 questions across four categories:

| Category | Number of Questions |
|---|---:|
| Mathematics | 3 |
| Logical Reasoning | 3 |
| Aptitude | 3 |
| Algorithms | 3 |
| **Total** | **12** |

Each question includes its category, difficulty level, question text, and expected correct answer.

Dataset file: `data/questions.csv`

## ⚙️ Methodology

1. Prepare a dataset of mathematical, logical, aptitude, and algorithmic questions.
2. Submit each question using direct prompting.
3. Submit the same question using structured reasoning prompting.
4. Record the model's response and relevant performance measurements.
5. Compare the results for both prompting methods.
6. Analyze observed differences, failures, and limitations.

## 📏 Evaluation Metrics

- **Accuracy:** Percentage of evaluated answers that are correct.
- **Error Rate:** Percentage of evaluated answers that are incorrect.
- **Response Time:** Time taken for a successful model request, in seconds.
- **Input Tokens:** Number of tokens used in the request.
- **Output Tokens:** Number of tokens generated in the response.
- **API Success Rate:** Percentage of API requests that completed successfully.

API request failures are tracked separately from incorrect answers.

## 🛠️ Technologies Used

- Python
- Google Gemini API
- Pandas
- Jupyter Notebook
- Matplotlib
- Visual Studio Code
- Git and GitHub

## 📁 Project Structure

```text
LLM-Reasoning-Experiment/
├── data/
│   └── questions.csv
├── notebooks/
│   └── experiment.ipynb
├── presentation/
│   └── Prompting_Comparison_BIT_Mesra.pptx
├── results/
│   ├── pilot_results.csv
│   ├── results.csv
│   └── results_partial.csv
├── src/
│   └── model.py
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚧 Experimental Status and Limitations

The initial experiment recorded 24 API attempts: 12 questions evaluated using two prompting methods.

Thirteen requests succeeded, while eleven failed because the Gemini API free-tier request quota was exhausted.

Consequently, the current results are preliminary and incomplete. Accuracy calculations must be interpreted using only the successfully evaluated responses, and the incomplete sample does not establish which prompting method is generally more accurate.

Other limitations include the small dataset, evaluation using a single model, and the variability of response times.

## 🔮 Future Work

- Complete the missing API requests when quota becomes available.
- Expand the dataset with more questions and difficulty levels.
- Evaluate additional language models.
- Repeat experiments to account for response variability.
- Compare performance across different problem categories.
- Investigate the relationship between reasoning quality, accuracy, latency, and token usage.

## 🔐 Security

API credentials are stored locally in a `.env` file and excluded from version control using `.gitignore`.

**Never publish API keys, passwords, or other secrets in this repository.**
