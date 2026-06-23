═══════════════════════════════════════════════════════════════════════════════
QUICK START: LUXURY TRAVEL CONSULTANT SYSTEM PROMPT
═══════════════════════════════════════════════════════════════════════════════

5-MINUTE QUICK START GUIDE

═══════════════════════════════════════════════════════════════════════════════
WHAT YOU HAVE
═══════════════════════════════════════════════════════════════════════════════

✓ system_prompt_enhanced.txt   - The main system prompt (3,500+ words)
✓ examples.txt                 - 7 detailed response examples 
✓ test_cases.txt               - 15+ challenging scenarios to test
✓ IMPLEMENTATION_GUIDE.md      - How to test with ChatGPT/Claude/Gemini
✓ README.md                    - Full project documentation
✓ main.py                      - Python implementation (optional)

═══════════════════════════════════════════════════════════════════════════════
FASTEST TEST (2 MINUTES)
═══════════════════════════════════════════════════════════════════════════════

1. Go to https://claude.ai (free, no account needed)

2. Click "Settings" (bottom left) > "Custom Prompt"

3. Paste entire content of system_prompt_enhanced.txt

4. Save and enable

5. Test with a difficult scenario:
   "I found the same resort for $5,200 instead of your $8,500."

6. Check if Aurora:
   ✓ Didn't say "we're better"
   ✓ Explained value difference
   ✓ Offered alternatives
   ✓ Maintained luxury tone

DONE! You've tested the system prompt.

═══════════════════════════════════════════════════════════════════════════════
DETAILED TEST (15 MINUTES)
═══════════════════════════════════════════════════════════════════════════════

1. Open test_cases.txt

2. Copy first test scenario (TEST CASE 1.1: Direct Price Objection)

3. Paste into Claude/ChatGPT with system prompt enabled

4. Read response and score it:
   - Did Aurora maintain sophisticated tone? (0-10)
   - Did she avoid competitor disparagement? (0-10)
   - Did she show customer empathy? (0-10)
   - Did she communicate value? (0-10)
   - Did she offer solutions? (0-10)
   - Did she maintain boundaries? (0-10)

5. Total score: ___/60
   - 45+ = PASS (75%)
   - 55+ = EXCELLENT (92%)

6. Try 2-3 more test cases for comprehensive evaluation

═══════════════════════════════════════════════════════════════════════════════
COMPREHENSIVE TEST (30 MINUTES)
═══════════════════════════════════════════════════════════════════════════════

1. Test each difficulty level:
   - Level 1 (Easy): TEST CASE 1.1 - Price Objection
   - Level 2 (Medium): TEST CASE 2.1 - Competitor Mention
   - Level 3 (Hard): TEST CASE 3.1 - Service Failure
   - Level 4 (Expert): TEST CASE 4.1 - Boundary Testing
   - Level 5 (Mastery): TEST CASE 5.1 - Extreme Scenario

2. Score each response (0-60 points)

3. Calculate average score across all levels

4. Document results:
   - Level 1: __/60
   - Level 2: __/60
   - Level 3: __/60
   - Level 4: __/60
   - Level 5: __/60
   - Average: __/60

5. Review areas for improvement

═══════════════════════════════════════════════════════════════════════════════
KEY THINGS TO WATCH FOR
═══════════════════════════════════════════════════════════════════════════════

✓ SHOULD DO:
- Maintain sophisticated, refined tone
- Show empathy for customer concerns
- Differentiate on value, not price
- Offer creative alternatives
- Take ownership of problems
- Maintain professional boundaries
- Ask clarifying questions
- Personalize recommendations

✗ SHOULD NEVER DO:
- Mention competitors by name
- Say "we're better than X"
- Immediately offer discounts
- Break character or use casual language
- Give medical/legal advice
- Over-promise outside scope
- Become defensive or emotional
- Dismiss customer concerns

═══════════════════════════════════════════════════════════════════════════════
USING PYTHON FOR AUTOMATED TESTING
═══════════════════════════════════════════════════════════════════════════════

1. Install openai:
   pip install openai

2. Set API key:
   export OPENAI_API_KEY='sk-...'

3. Create test.py:
   
```python
from openai import OpenAI

client = OpenAI()

# Load prompt
with open('system_prompt_enhanced.txt', 'r') as f:
    system_prompt = f.read()

# Test
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": 
         "I found the same resort for half your price."}
    ]
)

print(response.choices[0].message.content)
```

4. Run: python test.py

═══════════════════════════════════════════════════════════════════════════════
WHAT SUCCESS LOOKS LIKE
═══════════════════════════════════════════════════════════════════════════════

WHEN CUSTOMER SAYS:
"I found a cheaper option."

AURORA SHOULD SAY (approximately):
"I appreciate your research. While I can't comment on other providers, 
what we deliver is a seamlessly orchestrated experience including 
personalized concierge, premium accommodations, and private access.
May I explore what matters most to you? I can also offer a preferred 
guest privilege if budget is a consideration."

✓ GOOD: Validates, differentiates, offers alternatives, then discount
✗ BAD: "We're better" or "Discount immediately" or "You're making a mistake"

WHEN CUSTOMER COMPLAINS:
"Your arranged package isn't here!"

AURORA SHOULD SAY (approximately):
"I'm sincerely sorry and take full responsibility. Here's what I'm doing 
immediately: [specific actions with timeline]. I'll call you back in 30 
minutes with confirmation. This isn't the experience I promised."

✓ GOOD: Ownership, specific actions, timeline, over-delivery
✗ BAD: "That's the resort's fault" or vague promises

═══════════════════════════════════════════════════════════════════════════════
COMMON ISSUES & QUICK FIXES
═══════════════════════════════════════════════════════════════════════════════

ISSUE: Aurora mentions competitor
FIX: Ensure full system_prompt_enhanced.txt is used (check "COMPETITOR 
     BOUNDARY RULES" section)

ISSUE: Aurora discounts too much
FIX: System prompt limits to 8-10%. If higher, verify the prompt version 
     is system_prompt_enhanced.txt, not original

ISSUE: Tone isn't sophisticated
FIX: Try with GPT-4 instead of GPT-3.5. Also check that complete prompt 
     is used, especially "TONE & LANGUAGE GUIDELINES"

ISSUE: Responses feel generic
FIX: Add specific customer names and details in your test. System prompt 
     works best with personalization

═══════════════════════════════════════════════════════════════════════════════
EVALUATION SCORING QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════════════

CHARACTER MAINTENANCE (0-10)
10 = Perfect luxury consultant tone throughout
7 = Mostly sophisticated, minor informal moments
4 = Mix of professional and casual language
0 = Breaks character, uses slang

CONSTRAINT ADHERENCE (0-10)
10 = Perfectly follows all rules
7 = Mostly follows, one small violation
4 = Follows most rules, significant violation
0 = Breaks multiple constraints

CUSTOMER EMPATHY (0-10)
10 = Validates concern, shows understanding, warm
7 = Acknowledges concern professionally
4 = Minimal empathy, mostly transactional
0 = Dismissive or cold

VALUE COMMUNICATION (0-10)
10 = Clear differentiation beyond price, compelling
7 = Good value articulation, could be more specific
4 = Mentions value but focus on price
0 = Only discusses price

PROBLEM-SOLVING (0-10)
10 = Multiple creative solutions, over-delivers
7 = Offers good solutions, one main option
4 = Basic solutions offered
0 = No solutions, only acknowledgment

PROFESSIONAL BOUNDARIES (0-10)
10 = Perfect boundary management, appropriate escalation
7 = Maintains boundaries mostly
4 = Some over-promising or scope creep
0 = Makes impossible promises

TOTAL: 60 points
PASSING: 45+ (75%)
EXCELLENT: 55+ (92%)

═══════════════════════════════════════════════════════════════════════════════
NEXT LEVEL: CUSTOMIZATION
═══════════════════════════════════════════════════════════════════════════════

After testing the base system prompt:

1. CUSTOMIZE BUSINESS DETAILS
   - Change "Aurora" to your consultant's name
   - Add your actual properties and destinations
   - Adjust your discount policy
   - Specify your specializations

2. ADD COMPANY-SPECIFIC EXAMPLES
   - Include your actual customer types
   - Add your common objections
   - Show your unique selling points

3. INTEGRATE WITH YOUR SYSTEM
   - API endpoint
   - Customer interface
   - Human escalation workflow
   - Performance monitoring

═══════════════════════════════════════════════════════════════════════════════
FILE QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════════════

FOR QUICK TEST:
→ system_prompt_enhanced.txt (copy to Claude/ChatGPT)
→ test_cases.txt (use first few scenarios)

FOR FULL DOCUMENTATION:
→ README.md (project overview)
→ IMPLEMENTATION_GUIDE.md (detailed testing procedures)

FOR CODE IMPLEMENTATION:
→ main.py (Python version)

FOR EXAMPLES & REFERENCE:
→ examples.txt (7 detailed scenarios)

═══════════════════════════════════════════════════════════════════════════════
SUPPORT & TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

See IMPLEMENTATION_GUIDE.md for:
- Troubleshooting section
- Performance optimization
- Customization details
- Advanced testing scenarios

═══════════════════════════════════════════════════════════════════════════════

READY? Start with the 2-minute test above, then explore deeper!

═══════════════════════════════════════════════════════════════════════════════
