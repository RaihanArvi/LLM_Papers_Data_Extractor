"""
Script to extract structured data from a set of markdown-converted papers
using the OpenAI API, based on a protocol spreadsheet, and output a CSV.
"""
import os
import glob
import argparse
import time
import json
import pandas as pd
from openai import OpenAI

protocol_path = "protocol.xlsx"
markdown_path = "markdown_file"

# Load API key
with open("api.txt", "r") as f:
    apikey = f.read()

os.environ['OPENAI_API_KEY'] = apikey
client = OpenAI(api_key=apikey)

def load_protocol(protocol_path):
    """
    Load the protocol Excel file and build a list of variables and their definitions.
    """
    df = pd.read_excel(protocol_path)
    variables = df['Variable'].tolist()
    definitions = df['Definition'].tolist()
    # Build markdown-formatted definitions for the prompt
    var_defs = []
    for var, defn in zip(variables, definitions):
        var_defs.append(f"- **{var}**: {defn.strip()}")
    var_defs_text = "\n".join(var_defs)
    return variables, var_defs_text

def extract_data(markdown_text, var_defs_text, model="gpt-4", temperature=0.0):
    """
    Call OpenAI ChatCompletion to extract data from markdown text.
    Returns a dict mapping variable names to extracted values.
    """
    system_msg = "You extract structured data from scientific papers provided in markdown format."
    user_prompt = (
        "Extract the following variables from the paper markdown and output a JSON object "
        "where keys are variable names and values are the extracted data. "
        "If a value is missing, use null.\n\n"
        f"{var_defs_text}\n\n"
        "---Paper Markdown---\n"
        f"{markdown_text}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature,
    )
    content = response.choices[0].message.content
    # Try parsing the entire content as JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: extract first JSON object substring
        import re
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
        else:
            raise ValueError(f"Failed to parse JSON from model response: {content}")
    return data

def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from markdown papers using OpenAI API."
    )
    parser.add_argument(
        "-p", "--protocol", default=protocol_path,
        help="Path to the protocol Excel file"
    )
    parser.add_argument(
        "-i", "--input_dir", default=markdown_path,
        help="Directory containing markdown files to process"
    )
    parser.add_argument(
        "-o", "--output", default="extracted_data.csv",
        help="Path for the output CSV file"
    )
    parser.add_argument(
        "-m", "--model", default="gpt-4.1",
        help="OpenAI model to use (e.g., gpt-4.1)"
    )
    parser.add_argument(
        "-r", "--rate_limit_wait", type=float, default=1.0,
        help="Seconds to wait between API calls"
    )
    args = parser.parse_args()

    # Ensure API key is set
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    if not OpenAI.api_key:
        raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

    # Load protocol definitions
    variables, var_defs_text = load_protocol(args.protocol)

    # Find markdown files
    md_files = glob.glob(os.path.join(args.input_dir, "*.md"))
    if not md_files:
        print(f"No markdown files found in {args.input_dir}")
        return

    records = []
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            markdown = f.read()
        try:
            record = extract_data(markdown, var_defs_text, model=args.model)
            # Optionally add filename for reference
            record['filename'] = os.path.basename(md_file)
            records.append(record)
            print(f"Extracted data from {md_file}")
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
        time.sleep(args.rate_limit_wait)

    # Save results to CSV
    df_out = pd.DataFrame(records)
    # Reorder columns: protocol variables first, then filename
    cols = variables + ['filename'] if 'filename' in df_out.columns else variables
    df_out = df_out.reindex(columns=cols)
    df_out.to_csv(args.output, index=False)
    print(f"Extraction complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()