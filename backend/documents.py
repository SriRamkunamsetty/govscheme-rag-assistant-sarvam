"""
Knowledge base for Scheme Sahayak (Government Scheme RAG Assistant).

Contains curated, high-fidelity write-ups of major Indian central government
welfare schemes across Agriculture, Healthcare, Housing, Rural Employment,
Clean Energy, Child Welfare, Social Security, and Micro-Finance.
"""

SCHEME_DOCS = [
    {
        "id": "pm-kisan",
        "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "short_name": "PM-KISAN",
        "category": "Agriculture & Farmers",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "eligibility": "All landholding farmer families having cultivable land in their names, subject to certain exclusion criteria (institutional landholders, high-income taxpayers).",
        "benefits": "Financial benefit of Rs. 6,000 per year per family, payable in three equal installments of Rs. 2,000 every four months via Direct Benefit Transfer (DBT).",
        "application_process": "Farmers can register online at pmkisan.gov.in (Farmer Corner) or visit their nearest Common Service Centre (CSC) or State Nodal Officer with land records, Aadhaar, and bank account details.",
        "content": (
            "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) is a central sector scheme that provides "
            "income support to all landholding farmer families across India. Under this scheme, an income "
            "support of Rs. 6,000 per year is provided to eligible farmer families in three equal installments "
            "of Rs. 2,000 each every four months. The funds are transferred directly into the bank accounts of the "
            "beneficiaries through Direct Benefit Transfer (DBT) linked with Aadhaar. The scheme supplements the financial "
            "needs of farmers for procuring agricultural inputs like seeds, fertilizers, and equipment, as well as domestic "
            "household needs. Eligible farmers can enroll through the official PM-KISAN portal (pmkisan.gov.in), village nodal officers, "
            "or local Common Service Centres (CSCs). Exclusions apply to institutional landholders, individuals holding constitutional posts, "
            "and income tax payers."
        ),
    },
    {
        "id": "pm-jay",
        "title": "Ayushman Bharat (PM-JAY - Pradhan Mantri Jan Arogya Yojana)",
        "short_name": "PM-JAY",
        "category": "Healthcare",
        "ministry": "Ministry of Health and Family Welfare / National Health Authority (NHA)",
        "eligibility": "Economically vulnerable rural and urban families identified based on deprivation and occupational criteria of Socio-Economic Caste Census 2011 (SECC 2011), plus senior citizens aged 70+.",
        "benefits": "Cashless health insurance coverage of up to Rs. 5,00,000 per family per year for secondary and tertiary care hospitalisation across India.",
        "application_process": "Check eligibility online at beneficiary.nha.gov.in or visit any empanelled public or private hospital or CSC to generate an Ayushman Card using Aadhaar and Ration Card.",
        "content": (
            "Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (PM-JAY) is the world's largest government-funded health assurance scheme. "
            "It provides a health cover of Rs. 5 Lakh per family per year for secondary and tertiary care hospitalisation to over 12 crore "
            "vulnerable and poor families (covering roughly 55 crore beneficiaries). Beneficiaries are identified through the Socio-Economic "
            "Caste Census (SECC 2011) database. Treatment is entirely cashless and paperless at all empanelled public and private hospitals across "
            "the country. There is no restriction on family size, age, or gender, and pre-existing medical conditions are covered from day one. "
            "Benefits cover medical examination, treatment, consultation, pre- and post-hospitalisation expenses, diagnostics, medicines, "
            "and intensive care services. Senior citizens aged 70 and above are also entitled to a distinct 5 Lakh annual top-up cover."
        ),
    },
    {
        "id": "pmay",
        "title": "Pradhan Mantri Awas Yojana (PMAY - Urban & Gramin)",
        "short_name": "PMAY",
        "category": "Housing",
        "ministry": "Ministry of Housing and Urban Affairs (MoHUA) & Ministry of Rural Development (MoRD)",
        "eligibility": "Homeless families or households living in kutcha or dilapidated houses. Priority for Economically Weaker Sections (EWS), Low Income Groups (LIG), women, SC/ST, and minority households.",
        "benefits": "Direct financial assistance of Rs. 1.20 Lakh in plains and Rs. 1.30 Lakh in hilly/difficult areas (Gramin), plus home loan interest subsidy under Credit Linked Subsidy Scheme (CLSS) up to Rs. 2.67 Lakh (Urban).",
        "application_process": "Rural applicants are selected from SECC/Awaas+ verified lists. Urban applicants can apply online at pmaymis.gov.in or through registered Common Service Centres.",
        "content": (
            "Pradhan Mantri Awas Yojana (PMAY) is the flagship central housing program aimed at providing 'Housing for All' through pucca houses "
            "equipped with basic amenities like water, sanitation, and electricity. In rural areas (PMAY-Gramin), beneficiaries receive direct "
            "financial grant assistance of Rs. 1,20,000 in plain areas and Rs. 1,30,000 in hilly, difficult, and tribal areas, supplemented with "
            "90 to 95 days of unskilled labor wages under MGNREGA and Rs. 12,000 for toilet construction under Swachh Bharat Mission. In urban areas "
            "(PMAY-Urban), the scheme offers interest subsidies on home loans up to Rs. 2.67 Lakh under the Credit Linked Subsidy Scheme (CLSS) "
            "for Economically Weaker Sections (EWS) and Low-Income Groups (LIG), alongside Affordable Housing in Partnership (AHP) and in-situ slum "
            "redevelopment. Houses must be registered either in the name of the female head of the family or jointly."
        ),
    },
    {
        "id": "mgnrega",
        "title": "MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act)",
        "short_name": "MGNREGA",
        "category": "Employment & Livelihood",
        "ministry": "Ministry of Rural Development",
        "eligibility": "Any adult member of a rural household who volunteers to do unskilled manual work.",
        "benefits": "Legal guarantee of at least 100 days of wage employment per financial year per household. Unemployment allowance if work is not provided within 15 days of demand.",
        "application_process": "Apply for a Job Card at the local Gram Panchayat office with photograph, Aadhaar, and family details. Work is demanded by submitting a written application to the Gram Panchayat.",
        "content": (
            "The Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) is a demand-driven statutory social security scheme guaranteeing "
            "at least 100 days of guaranteed wage employment in every financial year to every rural household whose adult members volunteer to do "
            "unskilled manual work. If employment is not provided within 15 days of applying, the applicant is legally entitled to a daily unemployment "
            "allowance paid by the state government. Wages are statutory, notified annually for each state, and disbursed directly into workers' "
            "bank or post office accounts through the National Electronic Fund Management System (NeFMS) with Aadhaar-Based Payment Systems (ABPS). "
            "Permissible works focus on sustainable rural development including water conservation, watershed management, renovation of traditional "
            "water bodies, drought proofing, afforestation, rural roads, and land development."
        ),
    },
    {
        "id": "pmuy",
        "title": "Pradhan Mantri Ujjwala Yojana (PMUY - Ujjwala 2.0)",
        "short_name": "PM Ujjwala Yojana",
        "category": "Clean Energy & Women Welfare",
        "ministry": "Ministry of Petroleum and Natural Gas",
        "eligibility": "Adult woman belonging to poor/deprived households (SECC list, SC/ST, PMAY beneficiaries, Antyodaya Anna Yojana, forest dwellers, most backward classes) without an existing LPG connection in the household.",
        "benefits": "Free deposit-free LPG connection including security deposit for cylinder and regulator, safety hose, domestic gas consumer card, plus first cylinder refill and stove free of cost.",
        "application_process": "Submit application to nearest LPG distributor or apply online at pmuy.gov.in with Aadhaar, ration card, bank passbook, and 14-point self-declaration.",
        "content": (
            "Pradhan Mantri Ujjwala Yojana (PMUY) provides clean cooking fuel (LPG) connections to women from below-poverty-line and economically "
            "disadvantaged households, protecting rural families from indoor air pollution and respiratory hazards caused by traditional cooking "
            "fuels like firewood, dry dung, and coal. Under Ujjwala 2.0, beneficiaries receive a completely deposit-free LPG connection where the "
            "central government covers the security deposit of the cylinder and pressure regulator, installation charges, and inspection fees. "
            "In addition, beneficiaries receive the first LPG refill cylinder and a hotplate (two-burner stove) free of cost. Connections are released "
            "exclusively in the name of an adult female member of the family to promote women empowerment. Beneficiaries also receive targeted annual "
            "subsidies credited directly to their bank accounts per cylinder refill."
        ),
    },
    {
        "id": "ssy",
        "title": "Sukanya Samriddhi Yojana (SSY)",
        "short_name": "Sukanya Samriddhi",
        "category": "Women & Child Development",
        "ministry": "Ministry of Finance",
        "eligibility": "Parent or legal guardian of a girl child can open an account from the child's birth up to the age of 10 years. Maximum two accounts per family (three in case of twins/triplets).",
        "benefits": "Attractive government-guaranteed interest rate (currently 8.2% p.a.), compounding annually. Complete triple tax exemption (EEE: exemption on deposit, interest earned, and maturity proceeds under Section 80C).",
        "application_process": "Open account at any post office or authorised commercial bank branch by submitting the girl child's birth certificate, guardian's identity proof, and address proof.",
        "content": (
            "Sukanya Samriddhi Yojana (SSY) is a government-backed small savings savings scheme launched under the 'Beti Bachao Beti Padhao' campaign "
            "to secure the financial future of girl children in India, specifically catering to higher education and marriage expenses. An account "
            "can be opened by natural parents or legal guardians for a girl child from her birth until she reaches 10 years of age. A minimum deposit "
            "of Rs. 250 and a maximum of Rs. 1,50,000 can be deposited in a financial year. Deposits can be made for a maximum period of 15 years from "
            "the date of opening. The account matures 21 years from account opening or upon the girl's marriage after attaining 18 years. Partial withdrawal "
            "of up to 50% of the balance is permitted after the girl turns 18 or passes Class 10 to fund higher education. The scheme provides triple tax "
            "exemption under Section 80C of the Income Tax Act."
        ),
    },
    {
        "id": "pm-svanidhi",
        "title": "PM SVANidhi (PM Street Vendor's AtmaNirbhar Nidhi)",
        "short_name": "PM SVANidhi",
        "category": "Micro-Enterprise & Artisans",
        "ministry": "Ministry of Housing and Urban Affairs (MoHUA)",
        "eligibility": "Urban, peri-urban, and rural street vendors vending in urban areas possessing a Certificate of Vending / Identity Card issued by Urban Local Bodies (ULBs).",
        "benefits": "Collateral-free working capital micro-loans: 1st tranche up to Rs. 10,000 (1 year), 2nd tranche up to Rs. 20,000, 3rd tranche up to Rs. 50,000. Interest subsidy of 7% per annum on timely repayment and cashback up to Rs. 1,200/year on digital transactions.",
        "application_process": "Apply through pmsvanidhi.mohua.gov.in portal, mobile app, or via local Urban Local Body (ULB) / Common Service Centre.",
        "content": (
            "PM SVANidhi is a central micro-credit scheme aimed at empowering street vendors and hawkers by providing them with formal, affordable "
            "working capital loans to restart and expand their livelihood businesses. The scheme offers collateral-free loans starting with a first "
            "tranche of up to Rs. 10,000 with a repayment tenure of 1 year. Upon timely or early repayment, vendors become eligible for a second loan "
            "tranche of up to Rs. 20,000, and subsequent loans up to Rs. 50,000. Beneficiaries receive an interest subsidy of 7% per annum credited "
            "directly to their bank accounts on quarterly basis for timely repayments. There is no penalty for early repayment. The scheme also actively "
            "incentivizes digital payments by giving monthly cashback rewards up to Rs. 100 per month (Rs. 1,200 annually), effectively building "
            "a formal credit profile for previously unbanked street entrepreneurs."
        ),
    },
    {
        "id": "apy",
        "title": "Atal Pension Yojana (APY)",
        "short_name": "Atal Pension Yojana",
        "category": "Financial Inclusion & Social Security",
        "ministry": "Ministry of Finance / Pension Fund Regulatory and Development Authority (PFRDA)",
        "eligibility": "All Indian citizens between 18 and 40 years of age with a savings bank account or post office account. Individuals who are income tax payers are not eligible.",
        "benefits": "Guaranteed minimum monthly pension of Rs. 1,000, Rs. 2,000, Rs. 3,000, Rs. 4,000, or Rs. 5,000 per month from age 60 until death, depending on chosen contribution.",
        "application_process": "Submit application form at the bank branch or post office where you maintain your savings account, or enroll via net banking.",
        "content": (
            "Atal Pension Yojana (APY) is a government-backed periodic pension scheme focused on providing universal social security and old-age "
            "protection to workers in the unorganized sector. Any Indian citizen between the ages of 18 and 40 years holding a savings bank or "
            "post office account can subscribe to APY. Subscribers choose a guaranteed minimum monthly pension of Rs. 1,000, Rs. 2,000, Rs. 3,000, "
            "Rs. 4,000, or Rs. 5,000, which becomes payable once they reach 60 years of age. Monthly contributions are determined based on the age of "
            "joining and chosen pension amount (e.g., an 18-year-old contributes just Rs. 210 per month for a Rs. 5,000 monthly pension). The pension "
            "is guaranteed for the subscriber's entire lifetime; after death, the exact same monthly pension continues to the surviving spouse. "
            "Upon demise of both subscriber and spouse, the entire accumulated pension corpus is returned to the designated nominee."
        ),
    },
    {
        "id": "pm-vishwakarma",
        "title": "PM Vishwakarma Scheme",
        "short_name": "PM Vishwakarma",
        "category": "Micro-Enterprise & Artisans",
        "ministry": "Ministry of Micro, Small and Medium Enterprises (MoMSME)",
        "eligibility": "Traditional artisans and craftspeople working with hands and tools across 18 specified trades (carpenters, blacksmiths, potters, sculptors, cobblers, weavers, etc.), aged 18+.",
        "benefits": "PM Vishwakarma Certificate & ID Card, 5-7 days basic skill training with Rs. 500/day stipend, modern toolkit incentive of Rs. 15,000, and collateral-free enterprise credit up to Rs. 3 Lakh at 5% concessional interest rate.",
        "application_process": "Enroll online at pmvishwakarma.gov.in through Common Service Centres (CSCs) with three-step verification (Gram Panchayat / Urban Local Body, District Implementation Committee, Screening Committee).",
        "content": (
            "PM Vishwakarma is a comprehensive central initiative launched to provide holistic end-to-end support to traditional artisans and "
            "craftspeople (Vishwakarmas) who produce goods and services using their hands and traditional tools across 18 designated family-based trades. "
            "The scheme provides formal recognition through a PM Vishwakarma Certificate and ID Card. Beneficiaries receive 5-7 days of basic skill training "
            "and 15 days of advanced training, with a daily stipend of Rs. 500 during training. Upon completion of skill verification, artisans receive a "
            "financial grant of Rs. 15,000 in their e-RUPI/bank account to purchase modern toolkits. The scheme also provides collateral-free enterprise loans "
            "up to Rs. 1,00,000 in the first tranche (18 months tenure) and up to Rs. 2,00,000 in the second tranche (30 months tenure) at a concessional "
            "interest rate of only 5%, with interest subvention provided by the Government of India."
        ),
    },
    {
        "id": "pmmy",
        "title": "Pradhan Mantri Mudra Yojana (PMMY)",
        "short_name": "Mudra Yojana",
        "category": "Financial Inclusion & Social Security",
        "ministry": "Ministry of Finance",
        "eligibility": "Any Indian citizen with a business plan for a non-farm income-generating activity such as manufacturing, processing, trading, or service sector.",
        "benefits": "Collateral-free institutional loans up to Rs. 20 Lakh divided into categories: Shishu (up to Rs. 50,000), Kishore (Rs. 50,000 to Rs. 5 Lakh), Tarun (Rs. 5 Lakh to Rs. 10 Lakh), and Tarun Plus (up to Rs. 20 Lakh).",
        "application_process": "Apply at any commercial bank, Regional Rural Bank (RRB), Small Finance Bank (SFB), NBFC, or online through the Udyamimitra portal (udyamimitra.in).",
        "content": (
            "Pradhan Mantri Mudra Yojana (PMMY) facilitates formal, collateral-free credit to micro and small business enterprises engaged in "
            "manufacturing, trading, services, and allied agricultural activities. Under the scheme, commercial banks, RRBs, Micro Finance Institutions (MFIs), "
            "and NBFCs provide institutional loans categorized into four progressive tiers based on business lifecycle: 'Shishu' covers loans up to Rs. 50,000 "
            "for startups and tiny ventures; 'Kishore' covers loans from Rs. 50,001 to Rs. 5,00,000 for purchasing equipment; 'Tarun' covers loans from "
            "Rs. 5,00,001 to Rs. 10,00,000 for expansion; and 'Tarun Plus' extends financing up to Rs. 20 Lakh for entrepreneurs who have successfully repaid "
            "prior loans. No collateral or third-party guarantee is required, and borrowers receive a Mudra Card (debit card) for convenient working "
            "capital withdrawals."
        ),
    },
    {
        "id": "jsy",
        "title": "Janani Suraksha Yojana (JSY)",
        "short_name": "Janani Suraksha",
        "category": "Healthcare",
        "ministry": "Ministry of Health and Family Welfare",
        "eligibility": "Pregnant women belonging to BPL/SC/ST households, with special focus on Low Performing States (LPS) where all women delivering in public institutions are eligible regardless of age or number of children.",
        "benefits": "Direct cash assistance: In rural areas of Low Performing States, Rs. 1,400 for the mother plus Rs. 600 for the ASHA worker; in urban areas, Rs. 1,000 for the mother plus Rs. 400 for ASHA.",
        "application_process": "Register pregnancy with the local Village Health Guide, ANM, or ASHA worker at the nearest primary health sub-centre or government hospital during antenatal checkups.",
        "content": (
            "Janani Suraksha Yojana (JSY) is a safe motherhood intervention under the National Health Mission (NHM) aimed at reducing maternal and neonatal "
            "mortality by promoting institutional delivery among poor pregnant women. The scheme links cash assistance with delivery in government healthcare "
            "facilities or accredited private hospitals. In Low Performing States (LPS: Bihar, UP, MP, Rajasthan, Odisha, Jharkhand, Chhattisgarh, "
            "Uttarakhand, Assam, J&K), all pregnant women delivering in public or accredited health centers receive cash assistance of Rs. 1,400 in rural areas "
            "and Rs. 1,000 in urban areas. In High Performing States (HPS), BPL/SC/ST women receive Rs. 700 in rural areas and Rs. 600 in urban areas. "
            "The Accredited Social Health Activist (ASHA) worker receives an incentive (Rs. 600 in rural LPS) for escorting and facilitating the delivery. "
            "Cash is disbursed directly to the mother's bank account before hospital discharge."
        ),
    },
    {
        "id": "nsap",
        "title": "National Social Assistance Programme (NSAP - Old Age, Widow & Disability Pensions)",
        "short_name": "NSAP Pension",
        "category": "Financial Inclusion & Social Security",
        "ministry": "Ministry of Rural Development",
        "eligibility": "BPL elderly persons aged 60+ (IGNOAPS), BPL widows aged 40-79 (IGNWPS), and BPL persons aged 18+ with severe or multiple disabilities >= 80% (IGNDPS).",
        "benefits": "Monthly central pension contribution directly to bank/post office account, supplemented by state governments (total pensions often range from Rs. 1,000 to Rs. 3,000/month depending on the state).",
        "application_process": "Submit application form to Gram Panchayat / Block Development Officer (rural) or Municipality / District Social Welfare Officer (urban) along with age proof, disability certificate, and BPL card.",
        "content": (
            "The National Social Assistance Programme (NSAP) represents a significant step towards fulfilling the Directive Principles of State Policy "
            "in the Constitution of India by providing social security assistance to vulnerable citizens living below the poverty line (BPL). "
            "NSAP comprises three core pension components: (1) Indira Gandhi National Old Age Pension Scheme (IGNOAPS), providing monthly pensions "
            "to BPL senior citizens aged 60 years and above; (2) Indira Gandhi National Widow Pension Scheme (IGNWPS), providing monthly pensions to BPL "
            "widows aged 40 to 79 years; and (3) Indira Gandhi National Disability Pension Scheme (IGNDPS), providing monthly pension support to BPL "
            "individuals aged 18 years and above having severe or multiple disabilities of 80% or greater. Pensions are disbursed directly into the "
            "beneficiaries' post office or bank accounts through Direct Benefit Transfer (DBT)."
        ),
    },
]
