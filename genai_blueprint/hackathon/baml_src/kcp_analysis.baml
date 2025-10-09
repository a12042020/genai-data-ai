function KcpAnalysis(document: string, kcp: string) -> string {
  client "GptOss120" 
  prompt #"
    Analyse the contact provided according to the Contract Principles Checklist (KCP). 
    The contrat is provided in a structured way, with its associated schema.

    Assess each points of the checklist, and for each of them write a line in a table 
    with a Ok/NotOk symbol, and a concise text explaining the reason of the discrepency.
    Create sections for the different parts of the Contract Principles Checklist.
  - Generate output format in Markdown.
    ---- 
    Contract):
    {{ document }}
    ---- 
    Schema:

    {{ ctx.output_format }}

    ---- 
    Contract Principles Checklist 
    {{ kcp }}

    Markdown:
  "#
}