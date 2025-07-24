system_prompt = """# Venn Diagnostic Report Template Package

## FRAMEWORK OVERVIEW ###
Scoring System
- **1.0-1.5 = MIRAGE** (performance without substance, looks good but feels disconnected)
- **2.0-2.5 = SWAMP** (stuck, stagnant, painful patterns)
- **3.0-3.5 = FORGE** (active building, conscious growth work)
- **4.0 = RADIANT** (authentic flow, aligned presence)

### 10 Life Domains
1. Career/Achievement
2. Love/Primary Relationship
3. Health/Vitality
4. Inner Peace/Purpose
5. Money/Financial Confidence
6. Friendship/Community
7. Parenting/Family Legacy
8. Sexuality/Intimacy
9. Spirituality/Faith
10. Creativity/Play

--- ## REPORT STRUCTURE ###
1. Radar Chart (HTML/Chart.js)
<!DOCTYPE html>
<html>
    <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
        <!-- Styling here -->
    </head>

    <body>
        <canvas id="radarChart"></canvas>
        <script>
            // Chart data: [career, love, health, purpose, money, friendship, parenting, sexuality, spirituality, creativity]
            const data = [3.5, 4.0, 2.5, 3.0, 3.0, 3.5, 3.0, 1.0, 3.5, 3.5];
            // Chart configuration with color-coded points
        </script>
    </body>
</html>

### 2. Report Sections (Order)
1. **Quadrant Map** - List domains by quadrant
2. **Dominant Pattern** - Overall theme and opportunity
3. **This Week's Actions** - 3 immediate action items
4. **Hidden Patterns** - 3-4 deeper insights with 🔍 emoji
5. **Future Projections** - 6-month outlook, 12-month scenarios
6. **Strategic Recommendations** - 🚨 Immediate, 🔥 Forge Focus, 🌟 Leverage, 🌫️ Transformation
7. **Bottom Line** - Summary scores and next 30 days focus

--- ## PATTERN LIBRARY
### Pattern Recognition Framework
Each pattern includes:
- **Areas:** Which domains show this pattern
- **Insight:** What this reveals about the person
- **Strategic Opportunity/Hidden Risk/Recovery Pathway:** Action implications

### Common Patterns We've Identified
1. **The High-Achiever's Paradox** - Success without soul fuel
2. **The Conscious Builder in Transition** - Active growth work
3. **The Performance Fatigue** - Mirage areas creating exhaustion
4. **The Foundation-First Success** - Radiant areas enabling growth
5. **The Sacred vs Secular Split** - Authentic in some areas, performing in others

--- ## SAMPLE REPORTS
### Example 1: Chris (Integrated Builder)
**Pattern:** 4 Radiant + 6 Forge = Strong foundation with active transformation
**Key Insight:** Conscious work across all domains with no dysfunction
**Recommendations:** Focus on 2 areas for Radiant breakthrough

### Example 2: Victoria (Crisis Pattern)
**Pattern:** 0 Radiant + 3 Forge + 5 Swamp + 2 Mirage = Perfect storm
**Key Insight:** Importance-satisfaction gap creating unsustainable pressure
**Recommendations:** Emergency intervention needed

### Example 3: Doug O. (Optimal Growth)
**Pattern:** 2 Radiant + 5 Forge + 3 Swamp = Foundation enabling breakthrough
**Key Insight:** Purpose + Money foundation supporting transformation everywhere
**Recommendations:** Systematic breakthrough in interconnected areas

--- ## QUICK INSTRUCTIONS FOR NEW THREAD
### What to Upload:
1. This template package
2. Client's raw diagnostic data
3. Survey questionnaire (for .5 score interpretation)

### Prompt Template: Generate a complete Venn Diagnostic report using this framework and template structure.
Client data: [paste scores]
Include:
- HTML radar chart with color-coded points
- Complete report following the section structure
- Pattern recognition from the library
- Specific action recommendations
- Production time should be 3-5 minutes

Use the scoring system: 1-1.5=Mirage, 2-2.5=Swamp, 3-3.5=Forge, 4=Radiant

--- ## PRODUCTION NOTES
### Typical Production Time: 3-5 minutes
### Key Elements for Speed:
- Pre-written pattern descriptions to mix and match
- Standard section templates with client-specific details
- Radar chart template requiring only data array changes

### Quality Checklist:
- [ ] Radar chart matches client scores
- [ ] Quadrant mapping is accurate
- [ ] Patterns reflect actual data
- [ ] Actions are specific and actionable
- [ ] Importance ratings considered in recommendations
- [ ] Client name/date correct throughout

--- ## STYLING NOTES
### Color Coding:
- **Green styling** for high-performing clients (like Kimberly)
- **Blue styling** for building/growth clients (like Doug O.)
- **Amber styling** for healing/recovery clients (like Kevin)
- **Red styling** for crisis clients (like Victoria)

### Visual Impact:
- Radar charts immediately show pattern
- Consistent section structure for easy scanning
- Emoji use for pattern recognition and recommendations
- Action items in highlighted boxes

--- *This package contains everything needed to replicate the Venn diagnostic report system in any new conversation.
Simply upload this template and client data to generate professional-quality reports.*"""

user_prompt = """Below is how the user feels in each life domain.
Choose the ONE domain they most need help with (lowest or most negative).

Return **only** JSON in EXACTLY this shape:
{ "focus_area": "<single domain>", "followup_survey": "<module name>" }

User ratings:"""