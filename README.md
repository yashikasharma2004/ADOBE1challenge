Challenge 1a: PDF Processing Solution
Overview
This repository contains my solution for Challenge 1a of the Adobe India Hackathon 2025.

I built a PDF processing system that extracts structured information from PDF files and generates JSON outputs conforming to a predefined schema.
The solution is containerized with Docker and optimized to meet performance and resource constraints.

Our Approach
Designed a Python-based pipeline to automatically process all PDFs from the /app/input directory.

Created JSON outputs for each PDF using a schema defined in sample_dataset/schema/output_schema.json.

Used Docker for containerization to ensure cross-platform compatibility and easy deployment.

Current Status:
This is a working baseline solution. At present, it generates dummy JSON outputs for testing.
My next step will be to integrate real PDF parsing using libraries like pdfminer.six or PyMuPDF to extract text, structure, and hierarchy.

Key Features
Automatic Processing: Scans and processes all PDFs from the input directory.

Schema-Compliant Output: Generates a JSON file for each PDF that matches the required schema.

Dockerized Solution: Fully containerized, runs on amd64 without external dependencies.

Performance-Oriented: Designed to process 50-page PDFs in under 10 seconds within a 16GB RAM limit.

Project Structure

Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON output files
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker configuration
├── process_pdfs.py      # PDF processing script
└── README.md            # Project documentation
Output Schema
Each processed PDF generates a JSON file with this structure:

json

{
  "title": "string",
  "outline": [
    {
      "level": "string",    // e.g., H1, H2, H3
      "text": "string",     // Section heading text
      "page": "integer"     // Page number
    }
  ]
}
How to Build & Run
Build the Docker Image

docker build --platform=linux/amd64 -t pdf-processor .


docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  pdf-processor
Validation Checklist
 All PDFs in /app/input are processed.

 JSON outputs are generated for each PDF.

 Output matches the schema in sample_dataset/schema/output_schema.json.

 Designed for sub-10-second execution on 50-page PDFs.

 Runs without internet access.

 Works on amd64 architecture with 8 CPUs and 16GB RAM.

Next Steps
Implement full PDF parsing for text, headings, and layout extraction.

Optimize performance for large and complex PDFs.

Add unit tests for better validation.

This solution reflects my approach to solving Challenge 1a within the given constraints.
