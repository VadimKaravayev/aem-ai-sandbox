from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    instructions=(
        "You are an assistant that helps developers working with "
        "Adobe Experience Manager (AEM). Answer accurately and concisely. "
        "When you explain a concept, include a concrete, realistic example. "
        "If you are unsure or the answer depends on the specific AEM version "
        "or environment, say so rather than guessing."
    ),
    input="Explain what an OSGI Declarative Service component is in AEM and give one realistic example."
)

print(response.output_text)
