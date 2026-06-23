═══════════════════════════════════════════════════════════════════════════════
IMPLEMENTATION GUIDE: TESTING AURORA WITH CHATGPT/CLAUDE/GEMINI
═══════════════════════════════════════════════════════════════════════════════

This guide shows how to test the Aurora luxury travel consultant system prompt
with various AI models and services.

═══════════════════════════════════════════════════════════════════════════════
OPTION 1: CHATGPT (GPT-4) IMPLEMENTATION
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Copy the System Prompt
──────────────────────────────
1. Open system_prompt_enhanced.txt
2. Select and copy ALL content (Ctrl+A, Ctrl+C)
3. This is your system prompt

STEP 2: Access ChatGPT
──────────────────────
1. Go to https://chat.openai.com
2. Click "Create New Chat"
3. Click the three dots ⋯ in top left > Settings
4. NOT available in web UI - use API instead

STEP 3: Using ChatGPT API (Recommended)
───────────────────────────────────────
```bash
# 1. Install openai SDK
pip install openai

# 2. Set your API key
export OPENAI_API_KEY='sk-...'

# 3. Create a test script
```

```python
from openai import OpenAI

client = OpenAI()

# Load system prompt
with open('system_prompt_enhanced.txt', 'r') as f:
    system_prompt = f.read()

# Test conversation
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": "I found a cheaper option elsewhere for the same resort."
        }
    ]
)

print(response.choices[0].message.content)
```

STEP 4: Evaluate Response
─────────────────────────
Using criteria from test_cases.txt:
✓ Did Aurora avoid mentioning the competitor?
✓ Did she differentiate on value?
✓ Did she maintain luxury tone?
✓ Did she offer alternatives?
✓ Did she maintain professional boundaries?

═══════════════════════════════════════════════════════════════════════════════
OPTION 2: CLAUDE (ANTHROPIC) IMPLEMENTATION
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Get API Access
──────────────────────
1. Go to https://console.anthropic.com
2. Sign up or log in
3. Create an API key
4. Set environment variable: export ANTHROPIC_API_KEY='sk-ant-...'

STEP 2: Install SDK
───────────────────
```bash
pip install anthropic
```

STEP 3: Test Script
───────────────────
```python
from anthropic import Anthropic

client = Anthropic()

# Load system prompt
with open('system_prompt_enhanced.txt', 'r') as f:
    system_prompt = f.read()

# Test conversation
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": "This is too expensive. Can you match their price?"
        }
    ]
)

print(response.content[0].text)
```

STEP 4: Multi-Turn Conversation
────────────────────────────────
```python
conversation_history = []

def chat_with_aurora(user_message):
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system=system_prompt,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    return assistant_message

# Test multiple interactions
print("Aurora:", chat_with_aurora("Hello, I'm interested in Maldives"))
print("Aurora:", chat_with_aurora("How much does it cost?"))
print("Aurora:", chat_with_aurora("That's more than I expected"))
```

═══════════════════════════════════════════════════════════════════════════════
OPTION 3: GOOGLE GEMINI IMPLEMENTATION
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Get API Access
──────────────────────
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create new API key
4. Set: export GOOGLE_API_KEY='...'

STEP 2: Install SDK
───────────────────
```bash
pip install google-generativeai
```

STEP 3: Test Script
───────────────────
```python
import google.generativeai as genai

# Configure API
genai.configure(api_key="YOUR_API_KEY")

# Load system prompt
with open('system_prompt_enhanced.txt', 'r') as f:
    system_prompt = f.read()

# Create model
model = genai.GenerativeModel('gemini-1.5-pro', 
                             system_instruction=system_prompt)

# Test conversation
response = model.generate_content(
    "Your Maldives package is way too expensive."
)

print(response.text)
```

═══════════════════════════════════════════════════════════════════════════════
OPTION 4: MANUAL TESTING (No Code Required)
═══════════════════════════════════════════════════════════════════════════════

STEP 1: Choose a Platform
─────────────────────────
- ChatGPT: https://chat.openai.com (requires Plus subscription for GPT-4)
- Claude: https://claude.ai (free)
- Gemini: https://gemini.google.com (free)

STEP 2: Access Custom Instructions
──────────────────────────────────
On Claude:
1. Click "Settings" (bottom left)
2. Scroll to "Custom Prompt"
3. Paste system_prompt_enhanced.txt content
4. Check "Enable for all conversations"
5. Save

On Gemini:
1. Settings ⚙️ > Personalization
2. Add custom instructions
3. Paste system prompt
4. Save

STEP 3: Test with Difficult Scenarios
──────────────────────────────────────
Copy customer messages from test_cases.txt:

FROM TEST CASE 1.1:
"Your quoted price for Maldives is $12,000. Expedia has the same resort for $7,500.
Why would I pay $4,500 more for the same room?"

FROM TEST CASE 2.1:
"I've been using [Luxury Travel Concierge] for three years. They know me,
they understand my preferences, and I'm very happy with them. 
Why should I even consider switching to you?"

FROM TEST CASE 3.1:
"Aurora, I don't know what to do. The resort says they have no record of the
$5,000 spa package you told me was arranged."

STEP 4: Evaluate
────────────────
Score each response on the 6-point rubric:
- Character Maintenance: 0-10
- Constraint Adherence: 0-10
- Customer Empathy: 0-10
- Value Communication: 0-10
- Problem-Solving: 0-10
- Professional Boundaries: 0-10

Minimum passing: 45/60 (75%)
Excellence: 55/60 (92%)

═══════════════════════════════════════════════════════════════════════════════
QUICK TEST CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Test Case: Price Objection
Customer: "Why pay $12k when Expedia has it for $7.5k?"

WHAT TO LOOK FOR:
□ Aurora did NOT say "we're better"
□ Aurora did NOT disparage the competitor
□ Aurora acknowledged the price difference
□ Aurora explained value-add beyond booking
□ Aurora offered solutions (alternatives, timing, etc.)
□ Aurora maintained sophisticated tone
□ No defensive or dismissive language
□ Empathy shown for budget considerations

SCORE FACTORS:
✓ All 8 points = 80%+, likely passing

Test Case: Competitor with Loyalty
Customer: "I love my current agency, why switch?"

WHAT TO LOOK FOR:
□ Aurora didn't try to steal the customer
□ Aurora acknowledged value of existing relationship
□ Aurora positioned as addition/alternative
□ Aurora offered something unique
□ Aurora respected their choice
□ No arrogance or competitiveness
□ Warm, professional tone
□ Left door open for future

SCORE FACTORS:
✓ All 8 points = 80%+, likely passing

Test Case: Service Failure During Trip
Customer: "The spa package you arranged isn't in their system!"

WHAT TO LOOK FOR:
□ Aurora took immediate ownership
□ Aurora provided specific action steps
□ Aurora didn't blame the resort
□ Aurora specified timeline
□ Aurora offered compensation/correction
□ Aurora committed to follow-up
□ No defensiveness
□ Genuine accountability

SCORE FACTORS:
✓ All 8 points = 80%+, likely passing

═══════════════════════════════════════════════════════════════════════════════
ADVANCED TESTING SCENARIOS
═══════════════════════════════════════════════════════════════════════════════

STRESS TEST 1: Multi-Turn Conversation
───────────────────────────────────────
Try this sequence:

1. Customer: "Hi, I'm interested in planning a honeymoon."
   Expected: Aurora asks clarifying questions, shows enthusiasm

2. Customer: "What's the cost?"
   Expected: Aurora asks about preferences before quoting

3. Customer: "Your quote is double what I expected."
   Expected: Aurora doesn't immediately discount

4. Customer: "I found a cheaper option with another agency."
   Expected: Aurora doesn't disparage competitor

5. Customer: "Can you match their price?"
   Expected: Aurora offers creative alternatives

QUALITY CHECK: Does Aurora's personality remain consistent across turns?

STRESS TEST 2: Boundary Testing
──────────────────────────────
Try asking things outside scope:

"Can you recommend anxiety medication for flying?"
Expected: Aurora politely declines, redirects to physician, offers what she CAN help

"Is this place safe for someone with [medical condition]?"
Expected: Aurora respects boundary, recommends consulting healthcare provider, 
         offers resort coordination support

"Can you book this Airbnb I found?"
Expected: Aurora asks about vetting, explains risk, recommends verified properties

QUALITY CHECK: Does Aurora maintain professional boundaries?

STRESS TEST 3: Emotional Challenge
──────────────────────────────────
Try testing with emotional scenarios:

"I'm going through a divorce. This trip is my last hope. Surely you can help me?"
Expected: Aurora shows genuine empathy without being manipulated, finds solutions
         that honor their situation while maintaining boundaries

"Your service ruined my anniversary trip. I'm devastated."
Expected: Aurora takes ownership, shows genuine regret, over-delivers on correction,
         offers meaningful compensation

QUALITY CHECK: Does Aurora maintain professionalism while showing humanity?

═══════════════════════════════════════════════════════════════════════════════
BATCH TESTING SCRIPT (For Multiple Scenarios)
═══════════════════════════════════════════════════════════════════════════════

```python
import json
from datetime import datetime

# Load test cases
test_scenarios = [
    {
        "name": "Price Objection",
        "prompt": "Your Maldives quote is $12k, but I found $7.5k elsewhere.",
        "success_criteria": [
            "No competitor disparagement",
            "Value-based differentiation",
            "Maintains luxury tone",
            "Offers alternatives"
        ]
    },
    {
        "name": "Competitor Loyalty",
        "prompt": "I love my current travel agency. Why should I switch?",
        "success_criteria": [
            "Respects existing relationship",
            "Doesn't criticize competitor",
            "Positions as addition",
            "Offers unique value"
        ]
    },
    # ... more test cases from test_cases.txt
]

# Run tests
results = []
for test in test_scenarios:
    response = call_aurora(test["prompt"])
    
    # Evaluate response
    evaluation = {
        "test_name": test["name"],
        "timestamp": datetime.now().isoformat(),
        "passed_criteria": evaluate(response, test["success_criteria"]),
        "response": response,
        "score": score_response(response)
    }
    
    results.append(evaluation)

# Save results
with open('test_results.json', 'w') as f:
    json.dump(results, f, indent=2)

# Print summary
print(f"Tests run: {len(results)}")
print(f"Average score: {sum(r['score'] for r in results) / len(results):.1f}%")
```

═══════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING & TIPS
═══════════════════════════════════════════════════════════════════════════════

PROBLEM: Aurora doesn't maintain character
SOLUTIONS:
- Ensure full system prompt is copied (not truncated)
- For API calls, verify system parameter is set correctly
- Try rephrasing prompt with emphasis on persona maintenance
- Test with simpler scenario first, then escalate

PROBLEM: Aurora mentions competitors by name
SOLUTIONS:
- Add explicit rule: "Never mention competitor names"
- Use few-shot examples showing competitor handling
- Test with specific competitor names to reinforce boundary

PROBLEM: Aurora discounts too easily
SOLUTIONS:
- Verify discount policy section is in system prompt
- Add example showing wrong way (discounting immediately)
- Add example showing right way (alternatives first)
- Use "preferred guest offer" language instead of "discount"

PROBLEM: Aurora loses luxury tone
SOLUTIONS:
- Check for slang or casual language in responses
- Add tone examples with before/after comparisons
- Reinforce vocabulary (curated, exclusive, bespoke vs. cheap, sale, etc.)
- Test with GPT-4 rather than GPT-3.5 (better consistency)

PROBLEM: Response seems generic
SOLUTIONS:
- Add more specific few-shot examples
- Include customer names and personalization
- Show how to ask clarifying questions
- Demonstrate proactive value-add thinking

═══════════════════════════════════════════════════════════════════════════════
PERFORMANCE OPTIMIZATION
═══════════════════════════════════════════════════════════════════════════════

FOR FASTER RESPONSES:
- Use GPT-3.5 for quick testing, GPT-4 for final evaluation
- Reduce max_tokens if responses are too long
- Use temperature=0.7 for balance between creativity and consistency
- Cache system prompt if making multiple API calls

FOR BETTER RESPONSES:
- Use GPT-4 or Claude for production (more consistent)
- Increase max_tokens to allow detailed responses
- Use temperature=0.7-0.8 for personality while maintaining boundaries
- Provide examples specific to your customer base

FOR COST EFFICIENCY:
- Batch test scenarios together
- Use Claude (more affordable per token than GPT-4)
- Cache the system prompt across multiple conversations
- Use Claude Instant for brainstorming, Claude 3 for production

═══════════════════════════════════════════════════════════════════════════════
NEXT STEPS AFTER TESTING
═══════════════════════════════════════════════════════════════════════════════

1. DOCUMENT RESULTS
   - Record which test cases passed/failed
   - Note any improvements needed
   - Capture surprising or excellent responses

2. REFINE SYSTEM PROMPT
   - Based on failed tests, strengthen weak areas
   - Add more examples for challenging scenarios
   - Clarify ambiguous rules

3. A/B TEST VARIATIONS
   - Try different persona approaches
   - Test different discount policies
   - Experiment with tone variations

4. INTEGRATE INTO PRODUCTION
   - Set up API endpoint with final prompt
   - Create user interface for customer interactions
   - Set up logging and monitoring
   - Train human team on supporting Aurora

5. MEASURE REAL-WORLD PERFORMANCE
   - Track conversion rates
   - Monitor customer satisfaction
   - Collect feedback from agents
   - Continuously improve based on real interactions

═══════════════════════════════════════════════════════════════════════════════
PROMPT CUSTOMIZATION FOR YOUR BUSINESS
═══════════════════════════════════════════════════════════════════════════════

To customize Aurora for your specific business:

1. CHANGE AGENCY DETAILS
   Replace:
   - "Aurora" → Your consultant's name
   - "premium high-end travel agency" → Your company name
   - Luxury properties → Your actual offerings

2. ADJUST DISCOUNT POLICY
   Current: 8-10% maximum discount
   Modify: your_discount_percentage in system prompt

3. ADD SPECIFIC DESTINATIONS
   Current: General luxury destinations
   Add: Your specialty regions/properties

4. CUSTOMIZE SPECIALIZATIONS
   Current: Honeymoons, islands, etc.
   Add: Your unique specialties

5. MODIFY TONE IF NEEDED
   Current: Sophisticated, refined
   Options: More casual (boutique), more formal (luxury), etc.

6. ADD YOUR COMPETITORS' NAMES TO BLOCKLIST
   Add their specific names to constraints to ensure never mentioned

═══════════════════════════════════════════════════════════════════════════════

For detailed evaluation rubrics and more test cases, see test_cases.txt
For example conversations, see examples.txt
For complete system prompt details, see system_prompt_enhanced.txt

═══════════════════════════════════════════════════════════════════════════════
