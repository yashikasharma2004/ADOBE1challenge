import os
import json
import time
from utils import extract_heading_paragraphs, rank_relevance_on_sections

def process_documents():
    input_dir = "INPUT"
    output_dir = "OUTPUT"
    persona_path = "persona.json"

    # Validate inputs
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    if not os.path.exists(persona_path):
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    # Load persona
    try:
        with open(persona_path) as f:
            persona = json.load(f)
        job_text = persona.get("job_to_be_done", "")
        if not job_text:
            raise ValueError("No job_to_be_done found in persona.json")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in persona file")

    # Initialize results
    results = {
        "metadata": {
            "input_documents": [],
            "persona": persona.get("persona", ""),
            "job_to_be_done": job_text,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Collect all sections from all PDFs
    all_sections = []
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {input_dir}")

    for file in pdf_files:
        pdf_path = os.path.join(input_dir, file)
        results["metadata"]["input_documents"].append(file)

        try:
            sections = extract_heading_paragraphs(pdf_path)
            if not sections:
                print(f"Warning: No sections extracted from {file}")
                continue
                
            for section in sections:
                if not section.get("paragraph", "").strip():
                    continue  # Skip empty sections
                section["document"] = file
                all_sections.append(section)
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
            continue

    if not all_sections:
        raise ValueError("No sections were extracted from any documents")

    # Rank globally
    try:
        top_sections = rank_relevance_on_sections(all_sections, job_text, top_k=5)
    except Exception as e:
        raise ValueError(f"Error in ranking sections: {str(e)}")

    # Format output
    for idx, section in enumerate(top_sections):
        results["extracted_sections"].append({
            "document": section.get("document", "unknown"),
            "section_title": section.get("heading", ""),
            "importance_rank": idx + 1,
            "page_number": section.get("page_number", 0)
        })
        results["subsection_analysis"].append({
            "document": section.get("document", "unknown"),
            "refined_text": section.get("paragraph", ""),
            "page_number": section.get("page_number", 0)
        })

    # Save results
    output_path = os.path.join(output_dir, "output.json")
    try:
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Successfully saved results to {output_path}")
    except Exception as e:
        raise IOError(f"Failed to save results: {str(e)}")

    return results

if _name_ == "_main_":
    try:
        results = process_documents()
        print("Processing completed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")