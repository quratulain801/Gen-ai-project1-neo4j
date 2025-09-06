# Neo4j Knowledge Graph for Automated Resume Screening

## 📌 Project Objective  
This project demonstrates how **Neo4j Graph Database** can be integrated with **LLMs (Large Language Models)** to build a smart, automated resume screening system.  
The system extracts candidate information from resumes, organizes it in a **knowledge graph**, and enables natural language queries to quickly identify the best-fit candidates.  

---

## 🏗️ Data Model  
The knowledge graph is designed with three main entities:  

- **Candidate** → stores applicant details (name, email, experience, etc.)  
- **Skill** → technical and soft skills extracted from resumes  
- **Job** → requirements of a job position  

**Relationships**:  
- `(:Candidate)-[:HAS_SKILL]->(:Skill)`  
- `(:Candidate)-[:APPLIED_FOR]->(:Job)`  
- `(:Job)-[:REQUIRES_SKILL]->(:Skill)`  

👉 *(Insert your data model diagram image here)*


---

## ✨ Features  
- Upload and process resumes (PDFs).  
- Extract structured information using **LangChain & OpenAI Embeddings**.  
- Store candidates, jobs, and skills in **Neo4j Graph Database**.  
- Run **natural language queries** (via LLM → Cypher) to find suitable candidates.  
- Compare candidate skills with job requirements for **automated scoring**.  

---

## ⚙️ How to Run  

### 1. Clone the repository  
```bash
git clone https://github.com/your-username/genai-neo4j-resume-screening.git
cd genai-neo4j-resume-screening
Install dependencies
pip install -r requirements.txt
Setup environment variables

Create a .env file with:

OPENAI_API_KEY=your_api_key
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
Run the script
python main.py
Example Queries

“Find candidates with Python and SQL skills.”

“Which candidates are the best match for Data Analyst role?”

“List candidates with more than 3 years of experience in Machine Learning.”

The system will translate these into Cypher queries and fetch results from Neo4j.

📊 Results / Scoring

Candidates are ranked based on skill overlap with job requirements.

A matching score (0–100%) is calculated using embeddings.

Example:

Candidate	Applied For	Match Score
Ali Khan	Data Analyst	92%
Sara Ahmed	Data Analyst	75%
🚀 Future Improvements

Integration with ATS (Applicant Tracking Systems).

Add support for multiple file formats (DOCX, TXT).

Multi-language resume parsing.

Real-time job matching dashboard.
##[Knowledge Graph](neo4j_resume_graph.png)##


