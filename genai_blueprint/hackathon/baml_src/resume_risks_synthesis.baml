

function ResumeRisk(document: string) -> string {
  client "GptOss120" 
  prompt #"
    Generate a easy to understand summerize of the following structured document, 
    that follows a given schema.
  - Be concise and well-structured with sections (Title, Key Facts, Highlights, Anomalies).
  - Preserve important numeric values, entities, and dates.
  - Identify common patterns and notable outliers.
  - Generate output format in Markdown.

    Document:
    {{ document }}
    ---- 
    Schema:

    {{ ctx.output_format }}

    Markdown:
  "#
}
