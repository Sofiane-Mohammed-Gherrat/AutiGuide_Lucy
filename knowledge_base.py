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
    create_topic(
        "autism_spectrum", "Autism Information",
        ["Why is autism called a spectrum?", "Are all autistic children the same?",
         "Why does autism look different in every child?"],
        "spectrum different individual needs support abilities communication",
        "Autism is called a spectrum because characteristics and support needs vary widely. "
        "A child may have strong language but find social situations difficult, while another "
        "may communicate without speech and need more daily support. Labels such as 'mild' "
        "or 'severe' can miss these individual differences.",
        suggestions=["What is ASD?", "What are common signs of autism?",
                     "How can I understand my child's needs?"],
    ),
    create_topic(
        "autism_signs", "Autism Information",
        ["What are common signs of autism?", "How can I recognise possible autism signs?",
         "My child shows autism signs. What should I do?"],
        "signs assessment delayed speech eye contact repetitive routine sensory communication",
        "Possible signs can include differences in communication and social interaction, "
        "repetitive movements or interests, strong preference for routines and unusual sensory "
        "responses. A checklist or chatbot cannot diagnose autism. If you are concerned, record "
        "what you observe and request an assessment from a qualified health professional.",
        [
            "Write down the behaviours, when they happen and how they affect daily life.",
            "Ask teachers or other caregivers what they have observed.",
            "Discuss the concerns with a doctor, paediatrician or child development service.",
        ],
        ["Can AutiGuide diagnose autism?", "Why is early support important?",
         "Where can I seek an assessment in Malaysia?"],
        "medium", "MOH",
    ),
    create_topic(
        "autism_causes", "Autism Information",
        ["What causes autism?", "Did parenting cause my child's autism?",
         "Do vaccines cause autism?"],
        "cause causes parenting blame vaccine vaccines genetics brain development",
        "Autism is related to differences in brain development and is likely influenced by "
        "multiple genetic and biological factors. It is not caused by poor parenting. Reliable "
        "evidence does not show that childhood vaccines cause autism. Speak with a qualified "
        "health professional when you have concerns about vaccination or development.",
        suggestions=["What is ASD?", "Can autism be cured?",
                     "How do I find reliable autism information?"],
    ),
    create_topic(
        "autism_early_support", "Autism Information",
        ["Why is early intervention important?", "Does early support help autistic children?",
         "When should autism support begin?"],
        "early intervention support development communication daily skills parent training",
        "Early, individualised support can help a child develop communication, social and daily "
        "living skills and can help caregivers use useful strategies at home. Support should "
        "focus on the child's goals, comfort, strengths and participation rather than trying to "
        "make the child appear non-autistic.",
        suggestions=["What therapies may help?", "Can parents support therapy at home?",
                     "How should goals be chosen?"],
        source="VIRUES",
    ),
    create_topic(
        "autism_lifelong", "Autism Information",
        ["Can autism be cured?", "Will my child grow out of autism?",
         "Is autism a lifelong condition?"],
        "cure grow out lifelong strengths support development",
        "Autism is lifelong and is not an illness that has a simple cure. Children can learn, "
        "develop and gain independence with suitable support. The aim is to improve safety, "
        "communication, participation and quality of life while respecting the child's identity "
        "and strengths.",
        suggestions=["What support can help?", "What is early intervention?",
                     "How can I build on my child's strengths?"],
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
    create_topic(
        "beh_prevent_meltdown", "Behavioural Management",
        ["How can I prevent meltdowns?", "How do I find meltdown triggers?",
         "My child has frequent meltdowns"],
        "prevent meltdown trigger pattern routine transition tired hunger communication",
        "Meltdowns cannot always be prevented, but patterns can often be reduced. Common factors "
        "include sensory overload, unexpected change, fatigue, hunger, pain and difficulty "
        "communicating.",
        [
            "Keep a brief before-during-after record.",
            "Use predictable routines and warnings before transitions.",
            "Offer breaks or communication choices before distress becomes intense.",
            "Share useful prevention strategies with school and other caregivers.",
            "Seek professional support when episodes are frequent, dangerous or worsening.",
        ],
        ["Start meltdown guide", "How can I prepare for changes?",
         "What is sensory overload?"],
        "medium", "WHO_CST",
    ),
    create_topic(
        "beh_sensory", "Behavioural Management",
        ["What is sensory overload?", "Loud appliances make my child cover their ears",
         "My child is sensitive to noise, light or touch"],
        "sensory overload noise loud blender vacuum light touch smell crowd ears",
        "Sensory overload happens when sights, sounds, touch, smells or other sensations become "
        "more than the child can process comfortably. The child may cover their ears, escape, "
        "cry, become agitated or shut down.",
        [
            "Reduce the strongest sensory trigger when possible.",
            "Move to a quieter or less crowded place.",
            "Offer familiar sensory tools only if the child finds them helpful.",
            "Track triggers and discuss persistent difficulties with a qualified professional.",
        ],
        ["How can I prevent meltdowns?", "What does occupational therapy do?",
         "How can school reduce sensory stress?"],
        "medium", "MOH",
    ),
    create_topic(
        "beh_aggression", "Behavioural Management",
        ["My child hits or bites other people", "What should I do about aggressive behaviour?",
         "My child hurts classmates at school"],
        "aggression aggressive hit hitting bite biting kick hurt classmates safety trigger",
        "Hitting, biting or kicking should be taken seriously, while remembering that behaviour "
        "may communicate pain, fear, overload, frustration or an unmet need. Safety comes first.",
        [
            "Create distance and remove dangerous objects without shouting or physical punishment.",
            "Use few words until everyone is calm.",
            "Record what happened immediately before and after the behaviour.",
            "Agree on a consistent support plan with school and relevant professionals.",
            "Seek urgent help if anyone is in immediate danger or seriously injured.",
        ],
        ["Start aggression guide", "How can I identify behaviour triggers?",
         "How can I talk to the teacher?"],
        "high", "WHO_CST",
    ),
    create_topic(
        "beh_self_injury", "Behavioural Management",
        ["My child hits their head or hurts themselves", "How should I respond to self-injury?",
         "My autistic child bites themselves"],
        "self injury self-injury head banging hurts themselves biting pain danger",
        "Self-injury can have several causes, including pain, communication difficulty, sensory "
        "needs or severe distress. Protect the child from immediate harm and arrange professional "
        "assessment, especially when the behaviour is new, frequent or causes injury.",
        [
            "Move hard or sharp objects away and use the least restrictive safe response.",
            "Check for injury, illness or pain.",
            "Record triggers, duration and what helped.",
            "Contact a doctor or qualified behavioural professional for assessment.",
            "Call emergency services if there is serious injury or immediate danger.",
        ],
        ["How can behaviour triggers be recorded?", "What is sensory overload?",
         "When is a situation an emergency?"],
        "high", "MOH",
    ),
    create_topic(
        "beh_stimming", "Behavioural Management",
        ["What is stimming?", "Should I stop repetitive movements?",
         "My child flaps, rocks or spins repeatedly"],
        "stimming repetitive flapping rocking spinning movement regulate calm",
        "Stimming means repetitive movements, sounds or actions that may help an autistic child "
        "regulate emotion, express excitement or manage sensory input. Safe stimming does not "
        "usually need to be stopped.",
        [
            "Observe what purpose the behaviour may serve.",
            "Allow it when it is safe and not preventing essential activities.",
            "Redirect only when it is harmful, unsafe or seriously disruptive.",
            "Offer a safer alternative that meets a similar need.",
        ],
        ["What is sensory overload?", "How can I support emotional regulation?",
         "What does occupational therapy do?"],
        source="WHO",
    ),
    create_topic(
        "beh_transition", "Behavioural Management",
        ["My child becomes upset when routines change", "How can I prepare my child for transitions?",
         "Unexpected changes cause distress"],
        "routine change transition schedule warning visual predictability upset",
        "Changes can be difficult when a child relies on predictability. Advance warning and a "
        "clear, simple plan can reduce uncertainty.",
        [
            "Use a visual or written schedule suitable for the child.",
            "Give short countdown warnings before a change.",
            "Explain what will stay the same as well as what will change.",
            "Offer a small choice when possible.",
            "Practise common transitions during calm periods.",
        ],
        ["How can I prevent meltdowns?", "How can school support transitions?",
         "How do visual schedules help?"],
        source="WHO_CST",
    ),
    create_topic(
        "beh_sleep", "Behavioural Management",
        ["How can I help my child sleep?", "My autistic child wakes during the night",
         "What can improve an autism bedtime routine?"],
        "sleep bedtime night waking insomnia routine screen room tired",
        "Sleep problems are common and may be linked to routines, anxiety, sensory discomfort or "
        "health conditions. A consistent routine may help, but persistent sleep problems should "
        "be discussed with a doctor.",
        [
            "Keep sleep and wake times as consistent as possible.",
            "Use a short, predictable bedtime routine.",
            "Reduce stimulating screens and activities before bed.",
            "Check noise, light, temperature and bedding comfort.",
            "Keep a sleep record and seek medical advice when problems continue.",
        ],
        ["How do routines help?", "Could sensory issues affect sleep?",
         "When should I contact a doctor?"],
        "medium", "MOH",
    ),
    create_topic(
        "beh_wandering", "Behavioural Management",
        ["How can I prevent my child from wandering?", "My child tries to run away",
         "What safety plan can help with elopement?"],
        "wandering elopement run away escape missing door safety identification",
        "Wandering can create serious danger. Prevention should combine supervision, environmental "
        "safety, teaching and an emergency plan rather than relying on punishment.",
        [
            "Identify common reasons and locations connected with wandering.",
            "Secure exits safely while preserving emergency access.",
            "Teach and practise a simple stop-and-return response.",
            "Prepare identification and a recent photograph for emergencies.",
            "Coordinate a written safety plan with school and caregivers.",
            "Call 999 immediately if the child is missing or in immediate danger in Malaysia.",
        ],
        ["How can I create a safety plan?", "How do I identify triggers?",
         "When should I call emergency services?"],
        "high", "MERS",
    ),
    create_topic(
        "beh_communication_frustration", "Behavioural Management",
        ["My child becomes upset because they cannot communicate", "How can I reduce communication frustration?",
         "My non-speaking child becomes angry"],
        "communication frustration non speaking nonverbal angry request choice visual aac",
        "Behaviour can become more intense when a child cannot express pain, refusal, a request "
        "or the need for a break. Giving a simple, reliable way to communicate can reduce frustration.",
        [
            "Offer clear choices using words, pictures, gestures or an AAC system.",
            "Teach useful requests such as help, stop, break, toilet and pain.",
            "Allow enough processing time before repeating the question.",
            "Ask a speech-language professional about suitable communication supports.",
        ],
        ["What is AAC?", "What does speech therapy do?",
         "How can I understand behaviour triggers?"],
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
    create_topic(
        "therapy_speech_aac", "Therapy and Intervention",
        ["What is speech therapy?", "What is AAC communication?",
         "Can a non-speaking child use pictures or a device?"],
        "speech language communication aac pictures device gestures non speaking",
        "Speech and language therapy can support understanding, expression and social communication. "
        "Communication may use speech, gestures, pictures, signs or augmentative and alternative "
        "communication (AAC). AAC supports communication and does not require a child to stop "
        "trying to speak.",
        suggestions=["What does occupational therapy do?", "How can I reduce communication frustration?",
                     "Can parents practise communication at home?"],
        source="MOH",
    ),
    create_topic(
        "therapy_ot", "Therapy and Intervention",
        ["What is occupational therapy?", "Can occupational therapy help sensory needs?",
         "Which therapy supports daily living skills?"],
        "occupational therapy ot sensory motor dressing handwriting eating daily living",
        "Occupational therapy can support daily living, motor, play, school and sensory regulation "
        "skills. A qualified occupational therapist should assess the child's actual needs and "
        "choose practical goals connected with daily participation.",
        suggestions=["What is sensory overload?", "How can school reduce sensory stress?",
                     "How do I choose a therapist?"],
        source="MOH",
    ),
    create_topic(
        "therapy_choose", "Therapy and Intervention",
        ["How do I choose a therapist?", "How can I tell whether a therapy is trustworthy?",
         "What questions should I ask a therapy centre?"],
        "choose therapist qualified evidence goals progress consent cost centre trustworthy",
        "A trustworthy provider should explain qualifications, goals, methods, expected benefits, "
        "possible harms, costs and how progress will be reviewed. Be cautious of guaranteed cures "
        "or pressure to buy an expensive programme immediately.",
        [
            "Verify professional qualifications and relevant experience.",
            "Ask for written, individual goals and a progress-review schedule.",
            "Ask how the child's assent, distress and privacy are handled.",
            "Request explanations in clear language and seek a second opinion when unsure.",
        ],
        ["What is ABA therapy?", "How should therapy goals be measured?",
         "Can parents support therapy at home?"],
        "medium", "MOH",
    ),
    create_topic(
        "therapy_parent", "Therapy and Intervention",
        ["Can parents support therapy at home?", "What is parent-mediated intervention?",
         "How can I practise skills during daily routines?"],
        "parent caregiver home practice routine play communication parent-mediated",
        "Caregivers can reinforce useful skills during ordinary play, meals, dressing and community "
        "activities. Home practice should be simple, realistic and based on guidance that fits "
        "the child and family.",
        [
            "Choose one useful skill at a time.",
            "Practise briefly during a familiar routine.",
            "Notice and encourage successful attempts.",
            "Share observations with the professional and adjust the plan.",
            "Protect time for rest and normal family life.",
        ],
        ["What is early intervention?", "How can I support communication?",
         "How should goals be chosen?"],
        source="ONO",
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
    create_topic(
        "diet_refusal", "Dietary Guidance",
        ["My child refuses to eat", "When is food refusal serious?",
         "My child has stopped eating usual foods"],
        "food refusal not eating stopped eating dehydration weakness weight loss",
        "Food refusal may be related to illness, pain, anxiety, sensory sensitivity or a change in "
        "routine. It needs prompt professional attention when the child has dehydration, weakness, "
        "weight loss, choking, persistent vomiting or very little intake.",
        [
            "Do not force-feed or punish the child.",
            "Offer familiar fluids and foods when it is safe to do so.",
            "Record intake and symptoms.",
            "Contact a doctor or dietitian when refusal persists or health is affected.",
            "Use emergency services for choking, breathing difficulty or loss of consciousness.",
        ],
        ["Start picky eating guide", "Could texture cause food refusal?",
         "When is a situation an emergency?"],
        "high", "MOH",
    ),
    create_topic(
        "diet_cure", "Dietary Guidance",
        ["Does diet cure autism?", "Should my child follow a gluten-free diet for autism?",
         "Can food changes remove autism symptoms?"],
        "diet cure gluten free casein autism evidence restriction",
        "No diet cures autism. A restricted diet should not be started only because of an autism "
        "claim, because it may reduce nutrition and increase cost or stress. Dietary changes may "
        "be appropriate for a diagnosed allergy, intolerance or other health need under qualified "
        "medical or dietetic guidance.",
        suggestions=["My child is a picky eater", "Are supplements safe?",
                     "How do I choose reliable advice?"],
        risk="medium", source="WHO",
    ),
    create_topic(
        "diet_mealtime", "Dietary Guidance",
        ["How can I make mealtimes easier?", "Food textures upset my child",
         "My child will only eat one texture or colour"],
        "mealtime texture colour smell temperature sensory routine calm",
        "Mealtime difficulty may reflect genuine sensory discomfort. The goal is gradual, safe "
        "expansion of foods while keeping accepted foods and avoiding battles.",
        [
            "Use a regular meal place and routine.",
            "Describe foods without demanding that the child eat them.",
            "Allow gradual steps such as tolerating, touching, smelling and tasting.",
            "Avoid hiding foods when it may damage trust.",
            "Seek feeding or dietetic support when needs are complex.",
        ],
        ["My child is a picky eater", "What is sensory overload?",
         "When should I contact a dietitian?"],
        "medium", "MOH",
    ),
    create_topic(
        "diet_supplements", "Dietary Guidance",
        ["Are autism supplements safe?", "Should I give vitamins or herbal products for autism?",
         "My child has allergy or stomach symptoms"],
        "supplement vitamins herbal allergy stomach constipation diarrhoea medicine interaction",
        "Supplements and herbal products can have side effects, interact with medicines or provide "
        "unsafe doses. They should not be used as an autism cure. Allergy, pain, constipation, "
        "diarrhoea or other persistent symptoms should be assessed by a qualified health professional.",
        suggestions=["Does diet cure autism?", "When is food refusal serious?",
                     "Who should advise on nutrition?"],
        risk="high", source="MOH",
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
    create_topic(
        "school_sensory", "School and Social Support",
        ["How can school reduce sensory stress?", "The classroom is too noisy for my child",
         "What classroom accommodations may help?"],
        "school classroom noise sensory accommodation quiet break visual schedule seating",
        "Small classroom adjustments may reduce stress and improve participation. Supports should "
        "be based on the child's observed needs rather than applied automatically.",
        [
            "Identify the most difficult times, places and sensory triggers.",
            "Consider a quieter seat, planned breaks or reduced crowding.",
            "Use clear instructions and visual schedules.",
            "Prepare the child before alarms, assemblies or transitions.",
            "Review the adjustments with the child, family and school team.",
        ],
        ["How can I talk to the teacher?", "What is sensory overload?",
         "How can I prepare for transitions?"],
        "medium", "MOH",
    ),
    create_topic(
        "school_friends", "School and Social Support",
        ["How can I help my child make friends?", "My child struggles with social interaction",
         "How can I support play with classmates?"],
        "friends friendship social play classmates turn taking interest pressure",
        "Friendship support should respect the child's preferences and should not force long or "
        "uncomfortable interaction. Shared interests and short, structured activities can make "
        "interaction easier.",
        [
            "Start with one supportive peer and a familiar activity.",
            "Explain the activity and expected steps clearly.",
            "Practise useful phrases, gestures or AAC messages.",
            "Allow breaks and accept that some children prefer limited social contact.",
            "Praise effort without demanding eye contact or masking.",
        ],
        ["How can school support my child?", "What is AAC?",
         "What should I do about bullying?"],
        source="WHO_CST",
    ),
    create_topic(
        "school_bullying", "School and Social Support",
        ["My autistic child is being bullied", "What should I do about bullying at school?",
         "My child is excluded or teased by classmates"],
        "bullying bullied teased excluded school safety report teacher evidence",
        "Bullying should not be treated as the autistic child's fault or as a social-skills problem "
        "alone. The school should protect the child and investigate what is happening.",
        [
            "Listen calmly and record dates, places, people and messages.",
            "Report the concern in writing to the teacher or school leadership.",
            "Ask for a safety plan and named contact person.",
            "Monitor changes in sleep, mood, school attendance or self-injury.",
            "Seek professional or safeguarding help when there is serious harm or threat.",
        ],
        ["How can I talk to the teacher?", "My child refuses school",
         "When is a situation an emergency?"],
        "high", "YAACOB",
    ),
    create_topic(
        "school_refusal", "School and Social Support",
        ["My child refuses to go to school", "School transitions cause severe anxiety",
         "Homework and school routines cause meltdowns"],
        "school refusal anxiety transition homework routine pain bullying sensory",
        "School refusal can be linked to anxiety, bullying, learning difficulty, sensory overload, "
        "pain or an unsuitable support plan. Treat it as information about a problem, not simple defiance.",
        [
            "Ask what part of the day feels hardest and observe patterns.",
            "Check for bullying, illness, sleep problems and sensory triggers.",
            "Meet the school to agree on gradual, practical adjustments.",
            "Use a predictable morning and transition plan.",
            "Seek professional support when distress is severe or persistent.",
        ],
        ["Start school support guide", "What should I do about bullying?",
         "How can I prepare for transitions?"],
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
    ),
    create_topic(
        "resource_jkm", "Available Resources",
        ["What is JKM OKU registration?", "How do I apply for an OKU card?",
         "Can JKM support an autistic child?"],
        "jkm oku card registration welfare malaysia district office medical confirmation",
        "Jabatan Kebajikan Masyarakat (JKM) manages voluntary OKU registration. Registration may "
        "help a person access relevant services or programmes. The official process requires the "
        "appropriate form and medical confirmation, followed by submission through the relevant "
        "JKM channel or district welfare office. Check the current official requirements before applying.",
        [
            "Read the current instructions on the official JKM website.",
            "Prepare the required identity and medical documents.",
            "Obtain medical confirmation where required.",
            "Contact the nearest Pejabat Kebajikan Masyarakat Daerah for help.",
        ],
        ["Where can I get support in Malaysia?", "What documents should I keep?",
         "What if I live far from services?"],
        source="JKM",
    ),
    create_topic(
        "resource_access", "Available Resources",
        ["What if autism services are far away?", "How can rural families access support?",
         "Therapy is too expensive or has a long waiting list"],
        "rural distance cost waiting list access telehealth school clinic caregiver training",
        "When specialist services are difficult to access, ask local health and school services "
        "about referral pathways, caregiver training, community programmes and remote follow-up "
        "where available. Do not pay for an unverified cure because it promises immediate results.",
        [
            "Ask the nearest clinic what public referral options exist.",
            "Request practical strategies that can be used safely at home.",
            "Ask school which supports can begin without waiting for a diagnosis.",
            "Keep a list of waiting times, costs and questions for each provider.",
            "Use only providers whose qualifications and methods can be explained.",
        ],
        ["Can parents support therapy at home?", "How do I choose a therapist?",
         "What is JKM registration?"],
        "medium", "YAACOB",
    ),
    create_topic(
        "resource_caregiver", "Available Resources",
        ["Where can caregivers get emotional support?", "I feel overwhelmed caring for my child",
         "How can I find a parent support group or respite?"],
        "caregiver parent stress overwhelmed support group respite family mental health",
        "Caregiver stress is common and deserves support. Consider a trusted family member, parent "
        "group, social worker, counsellor or health professional. A useful support group respects "
        "privacy and does not promote blame or unproven cures.",
        [
            "Tell a trusted person specifically what help would be useful.",
            "Ask health, school or JKM services about local caregiver support.",
            "Schedule small, realistic periods of rest when possible.",
            "Seek professional mental-health support when distress is persistent or affects safety.",
        ],
        ["Where can I get support in Malaysia?", "How do I check reliable information?",
         "What should I do in an emergency?"],
        "medium", "YAACOB",
    ),
    create_topic(
        "resource_boundary", "Available Resources",
        ["Can AutiGuide diagnose or prescribe treatment?", "When should I call emergency services?",
         "What can and cannot AutiGuide do?"],
        "autiguide diagnose prescription emergency boundary doctor 999 malaysia",
        "AutiGuide provides general educational information from a prepared knowledge base. It "
        "cannot diagnose autism, prescribe medicine, choose a treatment plan or replace a doctor "
        "or therapist. In Malaysia, call 999 for immediate danger, severe injury, breathing "
        "difficulty, loss of consciousness or a missing child in danger.",
        suggestions=["What are common signs of autism?", "Where can I seek assessment in Malaysia?",
                     "What should I do during a meltdown?"],
        risk="high", source="MERS",
    ),
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
