import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


# Function to ingest candidate + resume + skills
def ingest_candidate(tx, candidate_id, name, resume_id, raw_text, skills):
    query = """
    MERGE (c:Candidate {candidate_id:$candidate_id})
    ON CREATE SET c.name=$name, c.created_at = datetime()

    CREATE (r:Resume {resume_id:$resume_id, uploaded_at: datetime(), text:$raw_text})
    CREATE (c)-[:HAS_RESUME]->(r)

    WITH r
    UNWIND $skills AS s
      MERGE (sk:Skill {name:s.name})
      MERGE (r)-[m:MENTIONS]->(sk)
      ON CREATE SET m.confidence = s.confidence, m.proficiency = s.proficiency
    """
    tx.run(query,
           candidate_id=candidate_id,
           name=name,
           resume_id=resume_id,
           raw_text=raw_text,
           skills=skills)


# Function to ingest job opening
def ingest_job(tx, job_id, title, required_skills, min_experience):
    query = """
    MERGE (j:JobOpening {job_id:$job_id})
    ON CREATE SET j.title=$title, j.min_experience_years=$min_experience, j.posted_at=datetime()

    WITH j
    UNWIND $required_skills AS s
      MERGE (sk:Skill {name:s})
      MERGE (j)-[:REQUIRES]->(sk)
    """
    tx.run(query, job_id=job_id, title=title,
           required_skills=required_skills,
           min_experience=min_experience)


# Function to query top candidates
def top_candidates(tx, job_id, topN=5):
    query = """
    MATCH (job:JobOpening {job_id:$job_id})-[:REQUIRES]->(req:Skill)
    WITH job, collect(req.name) AS reqSkills

    MATCH (c:Candidate)-[:HAS_RESUME]->(r:Resume)-[m:MENTIONS]->(s:Skill)
    WHERE s.name IN reqSkills
    WITH c, collect(DISTINCT s.name) AS matchedSkills, job

    WITH c, size(matchedSkills) AS matchedCount, size(reqSkills) AS reqCount, job
    WITH c, (toFloat(matchedCount)/toFloat(reqCount)) AS skill_score

    OPTIONAL MATCH (c)-[:WORKED_AS]->(e:Experience)
    WITH c, skill_score, coalesce(sum(e.years),0) AS total_years, job
    WITH c, skill_score,
         CASE WHEN job.min_experience_years > 0
              THEN apoc.math.min([total_years / job.min_experience_years, 1.0])
              ELSE 0.0 END AS experience_score

    WITH c, (0.6*skill_score + 0.4*experience_score) AS score
    RETURN c.candidate_id AS candidate, score
    ORDER BY score DESC
    LIMIT $topN
    """
    result = tx.run(query, job_id=job_id, topN=topN)
    return [record.data() for record in result]


# Example usage
if __name__ == "__main__":
    with driver.session() as session:
        # Insert one candidate
        session.execute_write(
            ingest_candidate,
            "C123", "Alice Khan", "R123",
            "Experienced Python developer with Neo4j knowledge",
            [
                {"name": "Python", "confidence": 0.95, "proficiency": 0.9},
                {"name": "Neo4j", "confidence": 0.9, "proficiency": 0.8}
            ]
        )

        # Insert job opening
        session.execute_write(
            ingest_job,
            "J100", "Data Engineer",
            ["Python", "Neo4j"], 2
        )

        # Query top candidates
        results = session.execute_read(top_candidates, "J100", 5)
        for r in results:
            print(r)
