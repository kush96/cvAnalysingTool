from config import config
from pyresparser import ResumeParser
import os
import spacy
import json
from docx import Document
import fitz
from spacy.matcher import PhraseMatcher
import time


class CvParserService:
    def __init__(self):
        self._path_to_cvs = config['cv_folder_path']
        print("""
Pls wait while CVs are being analysed.
The CVs are currently being analysed and parsed; this process may take up to a couple of minutes.
Based on our current benchmarks, parsing 10 CVs takes approximately 30 seconds.
        
        """)
        num_cvs = len([f for f in os.listdir(config['cv_folder_path']) if f.endswith(('.pdf', '.docx'))])
        # Estimate processing time
        approx_time = 3 * num_cvs  # 3 seconds per CV
        print(f"Current number of CVs in path (.pdf or .docx): {num_cvs}")
        print(f"Estimated processing time: {approx_time} seconds")

        self.nlp = spacy.load("en_core_web_sm")
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        self._setup_matcher()
        self._all_cv_data = self._get_all_cv_data()
        self.data_store_path = config['cv_data_store']
        self.persist_data(self._all_cv_data)

    def _setup_matcher(self):
        patterns = [self.nlp.make_doc(title) for title in config['job_titles'].split(",")]
        self.matcher.add("JOB_TITLE", patterns)

    def _setup_ner(self):
        """Sets up the custom NER Entity Ruler with predefined patterns for EDU, ORG."""
        try:
            # In spaCy v2, we must use create_pipe to create a new component
            if "entity_ruler" not in self.nlp.pipe_names:
                ruler = self.nlp.create_pipe("entity_ruler")
            else:
                ruler = self.nlp.get_pipe("entity_ruler")

            # Define patterns for EDU (Education), ORG (Company), and TITLE (Designation)
            patterns = [
                {"label": "EDU", "pattern": [{"LOWER": {"REGEX": ".*(university|college|institute|school).*"}}]},
            ]

            # Add the patterns to the entity ruler
            ruler.add_patterns(patterns)
            if "entity_ruler" not in self.nlp.pipe_names:
                self.nlp.add_pipe(ruler, before="ner")  # Add it before the existing NER
        except Exception as e:
            print(f"Error setting up Entity Ruler: {e}")

    def persist_data(self, all_cv_data):
        """Saves each key-value pair as a separate JSON file and an aggregated JSON file."""
        for key, value in all_cv_data.items():
            file_path = os.path.join(self.data_store_path, f"{key}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(value, f, indent=4)

    def load_all_cv_data(self):
        """Loads all individual JSON files into self._all_cv_data"""
        self._all_cv_data = {}

        for file_name in os.listdir(self.data_store_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.data_store_path, file_name)
                key = file_name.replace(".json", "")
                with open(file_path, "r", encoding="utf-8") as f:
                    self._all_cv_data[key] = json.load(f)

        return self._all_cv_data

    def load_cv_data(self, cv_names):
        """
        Loads and returns CV data for the specified cv_names.

        Args:
            cv_names (list[str]): List of CV names (without the ".json" extension).

        Returns:
            dict: A dictionary with keys as CV names and values as the parsed CV data.
        """
        cv_data = {}

        # Ensure all CV data is loaded
        if not hasattr(self, '_all_cv_data') or not self._all_cv_data:
            self.load_all_cv_data()

        for cv in cv_names:
            if cv in self._all_cv_data:
                cv_data[cv] = self._all_cv_data[cv]
            else:
                # Fallback: Try loading the file individually if it's not in _all_cv_data
                file_name = cv + ".json"
                file_path = os.path.join(self.data_store_path, file_name)
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        cv_data[cv] = json.load(f)
                else:
                    print(f"Warning: File for CV '{cv}' not found.")

        return cv_data

    def _get_education_history(self, text):
        """Extracts educational institutions using spaCy NER."""
        doc = self.nlp(text)
        education_institutions = {ent.text.strip() for ent in doc.ents if ent.label_ == "EDU"}
        return list(education_institutions)

    def _get_company_names(self, text):
        """Extracts company names using spaCy NER and company suffix matching."""
        doc = self.nlp(text)
        companies = {ent.text.strip() for ent in doc.ents if ent.label_ == "ORG"}

        # Additional filtering: Keep only companies that contain known suffixes
        filtered_companies = [
            company for company in companies if
            any(suffix in company.lower() for suffix in config['company_suffix'].split(','))
        ]

        return list(filtered_companies)

    def _get_designations(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        matched_titles = set()  # use a set to avoid duplicates
        for match_id, start, end in matches:
            span = doc[start:end]  # use the Doc, not the raw text string
            matched_titles.add(span.text)
        return list(matched_titles)

    def _get_all_cv_data(self):
        """Processes all CVs in the folder and extracts structured data."""
        all_cv_data = {}
        for file in os.listdir(self._path_to_cvs):
            if file.endswith(".pdf") or file.endswith(".docx"):
                file_path = os.path.join(self._path_to_cvs, file)

                # Parse the resume using pyresparser
                parsed_result = ResumeParser(file_path, skills_file=config['skills_file_path']).get_extracted_data()

                if not parsed_result:
                    continue

                # Get full resume text to perform a full-text search for education
                full_experience_text = "\n".join(parsed_result['experience'])

                # full_text needed for education results as it is not captured in parsed_result properly
                # Get full text based on file type
                if file.endswith(".pdf"):
                    with fitz.open(file_path) as doc:
                        full_text = "\n".join(page.get_text("text") for page in doc)
                elif file.endswith(".docx"):
                    full_text = "\n".join(p.text for p in Document(file_path).paragraphs)

                # Extract structured information
                parsed_result["company_names"] = self._get_company_names(full_text)  # Search full text
                parsed_result["designation"] = self._get_designations(
                    full_text)  # Search full text
                parsed_result["college_name"] = self._get_education_history(
                    full_text)  # Full-text search for education

                # Save parsed data
                all_cv_data[file] = parsed_result

        return all_cv_data
