import re
from typing import List, Tuple

def extract_insights(docs):
    """
    Extract key insights from legal documents
    """
    risks = []
    dates = []
    stakeholders = []

    # Enhanced keywords for legal documents
    risk_keywords = [
        "risk", "liability", "indemnif", "breach", "default", "termination",
        "damage", "loss", "claim", "dispute", "arbitration", "litigation",
        "penalty", "fine", "violation", "non-compliance", "warrant",
        "guarantee", "obligation", "responsibility", "duty"
    ]

    stakeholder_keywords = [
        "party", "parties", "company", "corporation", "client", "vendor",
        "supplier", "partner", "contractor", "employee", "director",
        "officer", "shareholder", "investor", "lessor", "lessee",
        "landlord", "tenant", "buyer", "seller", "lender", "borrower"
    ]

    # Date patterns
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY-MM-DD
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b'
    ]

    for doc in docs:
        text = doc.page_content.lower()
        original_text = doc.page_content

        # Extract risks
        for keyword in risk_keywords:
            if keyword in text:
                # Get context around the keyword
                start = max(0, text.find(keyword) - 100)
                end = min(len(original_text), text.find(keyword) + 200)
                context = original_text[start:end].strip()
                if context not in risks and len(risks) < 10:
                    risks.append(context)

        # Extract dates
        for pattern in date_patterns:
            matches = re.findall(pattern, original_text, re.IGNORECASE)
            for match in matches:
                if match not in dates and len(dates) < 10:
                    # Get context around date
                    start = max(0, original_text.find(match) - 50)
                    end = min(len(original_text), original_text.find(match) + 100)
                    context = original_text[start:end].strip()
                    dates.append(context)

        # Extract stakeholders
        for keyword in stakeholder_keywords:
            if keyword in text:
                # Get sentence containing stakeholder
                sentences = original_text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        clean_sentence = sentence.strip()
                        if clean_sentence not in stakeholders and len(stakeholders) < 10:
                            stakeholders.append(clean_sentence)
                        break

    # Remove duplicates while preserving order
    risks = list(dict.fromkeys(risks))[:5]
    dates = list(dict.fromkeys(dates))[:5]
    stakeholders = list(dict.fromkeys(stakeholders))[:5]

    return risks, dates, stakeholders

def format_response(text):
    """
    Format the response for better readability
    """
    if not text:
        return "No response generated."

    # Clean up the response
    response = text.strip()

    # Add formatting for legal terms
    legal_terms = [
        "clause", "section", "article", "paragraph", "subsection",
        "agreement", "contract", "party", "parties", "obligation"
    ]

    for term in legal_terms:
        response = re.sub(
            rf'\b{term}\b',
            f'**{term}**',
            response,
            flags=re.IGNORECASE
        )

    return response