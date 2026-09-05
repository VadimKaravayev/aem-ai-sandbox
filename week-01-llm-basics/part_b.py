from openai import OpenAI

client = OpenAI()

QUESTION = "Explain what an OSGi Declarative Services component is in AEM and give one realistic example."

BASE = (
    "You are an assistant that helps developers working with "
    "Adobe Experience Manager (AEM). Answer accurately and concisely. "
    "When you explain a concept, include a concrete, realistic example."
)

AUDIENCES = {
    "junior Java developer": (
        "Write for a junior Java developer who is new to AEM. "
        "Do not assume they know OSGi terminology — define terms such as "
        "bundle, service, and component as you introduce them. "
        "Favor a step-by-step explanation over density."
    ),
    "senior AEM developer": (
        "Write for a senior AEM developer who already knows OSGi and Sling. "
        "Skip the basics and be precise about details that matter in practice: "
        "annotation choices, service ranking, references and their cardinality, "
        "and activation lifecycle."
    ),
    "non-technical project manager": (
        "Write for a non-technical project manager. Avoid code and avoid Java or "
        "OSGi jargon. Make the example a business scenario — what the team is able "
        "to build or change — rather than a technical one."
    ),
}

for audience, line in AUDIENCES.items():
    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=BASE + " " + line,
        input=QUESTION
    )
    print(f"=== {audience} ===")
    print(response.output_text)
