# --------------------------------------------------
# AutiGuide knowledge base
# --------------------------------------------------

#this file stores the reviewed information used by the chatbot
#the chatbot only retrieves answers from this file

#store the date when the knowledge base was last reviewed
REVIEW_DATE = "2026-06-30"


#store the names and links of the main information sources
SOURCES = {
    "WHO": (
        "WHO autism fact sheet",
        "https://www.who.int/news-room/fact-sheets/detail/autism-spectrum-disorders",
    ),
    "WHO_CST": (
        "WHO Caregiver Skills Training",
        "https://www.who.int/teams/mental-health-and-substance-use/treatment-care/"
        "who-caregivers-skills-training-for-families-of-children-with-developmental-delays-and-disorders",
    ),
    "MOH": (
        "Malaysia Ministry of Health ASD quick reference",
        "https://hq.moh.gov.my/bpkk/images/Kesihatan_Orang_Kurang_Upaya/PDF/Garis_Panduan/"
        "9_Quick_Reference_for_Healthcare_Providers_-_Management_Of_Autism_Spectrum_Disorder_"
        "In_Children___Adolescents.pdf",
    ),
    "JKM": (
        "Jabatan Kebajikan Masyarakat OKU registration guidance",
        "https://www.jkm.gov.my/main/article/pendaftaran-orang-kurang-upaya-oku",
    ),
    "MERS": (
        "Malaysia Emergency Response Services 999",
        "https://www.malaysia.gov.my/en/my-initiative/cyber-security-and-disaster-response-and-recovery/"
        "tindak-balas-serta-pemulihan-bencana/malaysia-emergency-response-services-mers-999",
    ),
    "YAACOB": (
        "Yaacob et al. (2021), Malaysian caregiver experiences",
        "https://doi.org/10.3390/ijerph18168532",
    ),
    "ONO": (
        "Oono et al. (2013), parent-mediated early intervention review",
        "https://doi.org/10.1002/14651858.CD009774.pub2",
    ),
    "VIRUES": (
        "Virues-Ortega (2010), behavioural intervention review",
        "https://doi.org/10.1016/j.cpr.2010.01.006",
    ),
}


#this function creates one topic in a clear dictionary format
def create_topic(
    topic_id,
    category,
    questions,
    keywords,
    answer,
    steps=None,
    suggestions=None,
    risk="low",
    source="WHO",
):
    #use empty lists when a topic has no steps or suggestions
    if steps is None:
        steps = []

    if suggestions is None:
        suggestions = []

    #return all information belonging to one topic
    return {
        "topic_id": topic_id,
        "category": category,
        "questions": questions,
        "keywords": keywords,
        "answer": answer,
        "steps": steps,
        "suggestions": suggestions,
        "risk_level": risk,
        "source": source,
    }


topics = [
    # ------------------------------------------------------------------
    # Autism information: 6 topics × 3 questions
    # ------------------------------------------------------------------
    create_topic(
        "autism_basic", "Autism Information",
        ["What is autism?", "What is ASD?", "Explain Autism Spectrum Disorder"],
        "autism asd spectrum neurodevelopment communication social behaviour sensory",
        "Autism Spectrum Disorder (ASD) is a lifelong neurodevelopmental condition. "
        "It can affect communication, social interaction, behaviour, interests and sensory "
        "responses. Every autistic child is different and support should be based on the "
        "individual child's needs.",
        suggestions=["Why is autism called a spectrum?", "What are common signs of autism?",
                     "Why is early support important?"],
    ),

    # ------------------------------------------------------------------
    # Behavioural management: 10 topics × 3 questions
    # ------------------------------------------------------------------
    create_topic(
        "beh_meltdown", "Behavioural Management",
        ["What should I do during a meltdown?", "My child is screaming and overwhelmed",
         "How do I calm an autistic child during a meltdown?"],
        "meltdown overwhelmed screaming crying calm safety reduce stimulation",
        "During a meltdown, focus first on safety and reducing demands and stimulation. "
        "A meltdown is usually a sign that the child is overwhelmed, not deliberate bad behaviour.",
        [
            "Stay calm and use a quiet, simple voice.",
            "Reduce noise, light, crowds and unnecessary talking when possible.",
            "Give safe space and avoid punishment, arguing or forced eye contact.",
            "After the child is calm, note possible triggers and what helped.",
        ],
        ["Start meltdown guide", "How can I prevent meltdowns?",
         "What is sensory overload?"],
        "medium", "WHO_CST",
    ),

    # ------------------------------------------------------------------
    # Therapy and intervention: 5 topics × 3 questions
    # ------------------------------------------------------------------
    create_topic(
        "therapy_aba", "Therapy and Intervention",
        ["What is ABA therapy?", "How does Applied Behaviour Analysis work?",
         "Is ABA suitable for every autistic child?"],
        "aba applied behaviour analysis reinforcement skills therapy goals dignity",
        "Applied Behaviour Analysis (ABA) uses observation and learning principles to teach skills "
        "and understand behaviour. Quality varies. Goals should be meaningful, measurable, "
        "individualised and respectful of the child's dignity, communication and comfort.",
        [
            "Ask who sets the goals and how the child and family are involved.",
            "Ask how progress and distress are monitored.",
            "Avoid programmes that rely on fear, humiliation or suppress harmless traits.",
            "Review benefits and concerns with qualified professionals.",
        ],
        ["How should therapy goals be chosen?", "Can parents support therapy at home?",
         "How do I choose a therapist?"],
        source="VIRUES",
    ),

    # ------------------------------------------------------------------
    # Dietary guidance: 5 topics × 3 questions
    # ------------------------------------------------------------------
    create_topic(
        "diet_picky", "Dietary Guidance",
        ["My child is a picky eater", "How can I introduce new foods?",
         "My child eats only a few foods"],
        "picky eating selective few foods new food nutrition texture smell colour",
        "Selective eating can be connected with texture, smell, appearance, routine, anxiety or "
        "oral-motor difficulty. Pressure and punishment often increase distress.",
        [
            "Keep at least one accepted food available.",
            "Place a tiny amount of a new food nearby without forcing it.",
            "Change one feature at a time, such as shape, brand or texture.",
            "Keep meals predictable and calm.",
            "Consult a doctor or dietitian if variety is very limited or growth is affected.",
        ],
        ["Start picky eating guide", "My child refuses all food",
         "Does a special diet cure autism?"],
        "medium", "MOH",
    ),

    # ------------------------------------------------------------------
    # School and social support: 5 topics × 3 questions
    # ------------------------------------------------------------------
    create_topic(
        "school_teacher", "School and Social Support",
        ["How can I talk to my child's teacher?", "How do I create a school support plan?",
         "What information should I share with school?"],
        "teacher school support plan meeting strengths triggers communication accommodations",
        "A useful school conversation is specific, collaborative and focused on the child's "
        "strengths, needs, triggers and successful supports.",
        [
            "Prepare a short summary of strengths, communication and sensory needs.",
            "Describe what happens before difficult situations and what helps.",
            "Agree on a few practical strategies and who will use them.",
            "Choose a simple way to share updates between home and school.",
            "Set a date to review whether the plan is helping.",
        ],
        ["Start school support guide", "How can school reduce sensory stress?",
         "My child hurts classmates at school"],
        "medium", "YAACOB",
    ),

    # ------------------------------------------------------------------
    # Malaysia resources and boundaries: 5 topics × 3 questions
    # ------------------------------------------------------------------
    create_topic(
        "resource_start", "Available Resources",
        ["Where can I get autism support in Malaysia?", "Where should I start if I suspect autism?",
         "How can I find an autism assessment in Malaysia?"],
        "malaysia support assessment clinic hospital paediatrician child development referral",
        "In Malaysia, a practical starting point is a government or private clinic, paediatric "
        "service or child development service. Bring notes about development and behaviour and "
        "ask about assessment and suitable referrals. Availability and referral processes differ "
        "by location, so confirm details directly with the service.",
        [
            "Record your main concerns and examples.",
            "Contact a Klinik Kesihatan, doctor, paediatric service or hospital.",
            "Ask what documents, referral and appointment are required.",
            "Keep copies of assessment and therapy reports.",
        ],
        ["What is JKM OKU registration?", "What if services are far away?",
         "How do I choose a therapist?"],
        "low", "MOH",
    )
]


# --------------------------------------------------
# Build the final question and answer list
# --------------------------------------------------

#this function changes every topic into three searchable question records
def build_knowledge_base():
    #create an empty list for the final records
    records = []

    #go through every reviewed topic
    for topic in topics:
        #get the full source name and source link
        source_name, source_url = SOURCES[topic["source"]]

        #join the three question forms so they can also be used as keywords
        all_question_forms = " ".join(topic["questions"])

        #create one searchable record for every question form
        for question_number, question in enumerate(topic["questions"], start=1):
            #combine the topic keywords with all question forms
            search_keywords = topic["keywords"] + " " + all_question_forms

            #add the completed record to the final list
            records.append({
                "id": topic["topic_id"] + "_" + str(question_number),
                "topic_id": topic["topic_id"],
                "category": topic["category"],
                "question": question,
                "keywords": search_keywords.split(),
                "answer": topic["answer"],
                "steps": topic["steps"],
                "suggestions": topic["suggestions"],
                "risk_level": topic["risk_level"],
                "source_type": source_name,
                "source_url": source_url,
                "last_reviewed": REVIEW_DATE,
            })

    #return the complete list of records
    return records


#create the knowledge base when this file is imported by app.py
knowledge_base = build_knowledge_base()
