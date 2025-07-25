SYSTEM_PROMPT = """You are VennAI, an insightful life-balance coach.
You MUST output ONLY valid JSON that matches the provided schema.
No extra prose, no markdown, no HTML.

Scoring bands:
1.0–1.5 = MIRAGE
2.0–2.5 = SWAMP
3.0–3.5 = FORGE
4.0      = RADIANT

Domains (exact strings):
- Career/Achievement
- Love/Primary Relationship
- Health/Vitality
- Inner Peace/Purpose
- Money/Financial Confidence
- Friendship/Community
- Parenting/Family Legacy
- Sexuality/Intimacy
- Spirituality/Faith
- Creativity/Play

Classify each domain into one of: "mirage" | "swamp" | "forge" | "radiant".
Then fill all other fields per schema."""

USER_PROMPT = """Below is how the user feels in each life domain, and how important each domain is to them.

User ratings:"""

JSON_SCHEMA = {
  "name": "VennDiagnostic",
  "schema": {
    "type": "object",
    "properties": {
      "scores": {
        "type": "object",
        "additionalProperties": {"type": "number"}
      },
      "quadrants": {
        "type": "object",
        "properties": {
          "mirage":  {"type": "array", "items": {"type": "string"}},
          "swamp":   {"type": "array", "items": {"type": "string"}},
          "forge":   {"type": "array", "items": {"type": "string"}},
          "radiant": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["mirage","swamp","forge","radiant"]
      },
      "dominant_pattern": {
        "type": "object",
        "properties": {
          "name":    {"type": "string"},
          "summary": {"type": "string"}
        },
        "required": ["name","summary"]
      },
      "actions_this_week": {
        "type": "array", "items": {"type": "string"}, "minItems": 3, "maxItems": 5
      },
      "hidden_patterns": {
        "type": "array",
        "items": {
          "type":"object",
          "properties":{
            "areas":     {"type":"array","items":{"type":"string"}},
            "insight":   {"type":"string"},
            "risk":      {"type":"string"},
            "pathway":   {"type":"string"}
          },
          "required":["areas","insight","risk","pathway"]
        }
      },
      "future_projections": {
        "type":"object",
        "properties":{
          "six_months":   {"type":"string"},
          "twelve_months":{"type":"string"}
        },
        "required":["six_months","twelve_months"]
      },
      "strategic_recommendations": {
        "type":"object",
        "properties":{
          "immediate":      {"type":"array","items":{"type":"string"}},
          "forge_focus":    {"type":"array","items":{"type":"string"}},
          "leverage":       {"type":"array","items":{"type":"string"}},
          "transformation": {"type":"array","items":{"type":"string"}}
        },
        "required":["immediate","forge_focus","leverage","transformation"]
      },
      "bottom_line": {
        "type":"object",
        "properties":{
          "summary_scores": {
            "type":"object",
            "properties":{
              "mirage":{"type":"integer"},
              "swamp":{"type":"integer"},
              "forge":{"type":"integer"},
              "radiant":{"type":"integer"}
            },
            "required":["mirage","swamp","forge","radiant"]
          },
          "next_30_days_focus":{"type":"string"}
        },
        "required":["summary_scores","next_30_days_focus"]
      }
    },
    "required": [
      "scores","quadrants","dominant_pattern","actions_this_week",
      "hidden_patterns","future_projections","strategic_recommendations","bottom_line"
    ],
    "additionalProperties": False
  }
}