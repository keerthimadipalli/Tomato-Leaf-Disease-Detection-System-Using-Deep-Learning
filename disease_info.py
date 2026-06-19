"""
=============================================================
  DISEASE INFO DATABASE
  Contains: disease details, remedies, pesticides, prices,
  and translations in 6 Indian languages
=============================================================
"""

# ─────────────────────────────────────────────────────────────
# LANGUAGE LABELS (UI strings)
# ─────────────────────────────────────────────────────────────
LANG_LABELS = {
    "English": {
        "title": "🍅 Tomato Leaf Disease Detector",
        "upload_tab": "📁 Upload Image",
        "webcam_tab": "📷 Webcam",
        "result_header": "🔬 Detection Result",
        "disease_label": "Disease",
        "confidence_label": "Confidence",
        "description_label": "Description",
        "symptoms_label": "Symptoms",
        "remedy_label": "Organic Remedy",
        "pesticide_label": "Recommended Pesticides",
        "shop_label": "Find Nearest Agri Shop",
        "not_leaf_label": "⚠️ Not a Leaf",
        "healthy_msg": "✅ Your tomato plant looks healthy!",
        "upload_prompt": "Upload a clear tomato leaf image",
        "webcam_prompt": "Capture a tomato leaf from webcam",
        "analyze_btn": "🔍 Analyze",
        "capture_btn": "📷 Capture & Analyze",
    },
    "తెలుగు": {
        "title": "🍅 టమాటా ఆకు వ్యాధి గుర్తింపు",
        "upload_tab": "📁 చిత్రం అప్‌లోడ్",
        "webcam_tab": "📷 వెబ్‌కామ్",
        "result_header": "🔬 ఫలితం",
        "disease_label": "వ్యాధి",
        "confidence_label": "నిర్ధారణ స్థాయి",
        "description_label": "వివరణ",
        "symptoms_label": "లక్షణాలు",
        "remedy_label": "సేంద్రీయ నివారణ",
        "pesticide_label": "పురుగుమందుల సూచన",
        "shop_label": "దగ్గర వ్యవసాయ దుకాణం",
        "not_leaf_label": "⚠️ ఇది ఆకు కాదు",
        "healthy_msg": "✅ మీ టమాటా మొక్క ఆరోగ్యంగా ఉంది!",
        "upload_prompt": "స్పష్టమైన టమాటా ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "webcam_prompt": "వెబ్‌కామ్ ద్వారా ఆకు చిత్రాన్ని తీయండి",
        "analyze_btn": "🔍 విశ్లేషించు",
        "capture_btn": "📷 తీసి విశ్లేషించు",
    },
    "हिंदी": {
        "title": "🍅 टमाटर पत्ती रोग पहचानकर्ता",
        "upload_tab": "📁 छवि अपलोड करें",
        "webcam_tab": "📷 वेबकैम",
        "result_header": "🔬 परिणाम",
        "disease_label": "बीमारी",
        "confidence_label": "विश्वास स्तर",
        "description_label": "विवरण",
        "symptoms_label": "लक्षण",
        "remedy_label": "जैविक उपाय",
        "pesticide_label": "कीटनाशक सुझाव",
        "shop_label": "निकटतम कृषि दुकान",
        "not_leaf_label": "⚠️ यह पत्ती नहीं है",
        "healthy_msg": "✅ आपका टमाटर का पौधा स्वस्थ है!",
        "upload_prompt": "एक स्पष्ट टमाटर की पत्ती की छवि अपलोड करें",
        "webcam_prompt": "वेबकैम से पत्ती की छवि कैप्चर करें",
        "analyze_btn": "🔍 विश्लेषण करें",
        "capture_btn": "📷 कैप्चर करें और विश्लेषण करें",
    },
    "தமிழ்": {
        "title": "🍅 தக்காளி இலை நோய் கண்டறிவு",
        "upload_tab": "📁 படம் பதிவேற்றம்",
        "webcam_tab": "📷 வெப்கேம்",
        "result_header": "🔬 முடிவு",
        "disease_label": "நோய்",
        "confidence_label": "நம்பகத்தன்மை",
        "description_label": "விளக்கம்",
        "symptoms_label": "அறிகுறிகள்",
        "remedy_label": "இயற்கை தீர்வு",
        "pesticide_label": "பூச்சிக்கொல்லி பரிந்துரை",
        "shop_label": "அருகிலுள்ள விவசாய கடை",
        "not_leaf_label": "⚠️ இது இலை அல்ல",
        "healthy_msg": "✅ உங்கள் தக்காளி செடி ஆரோக்கியமாக உள்ளது!",
        "upload_prompt": "தெளிவான தக்காளி இலை படத்தை பதிவேற்றவும்",
        "webcam_prompt": "வெப்கேம் மூலம் இலை படம் எடுக்கவும்",
        "analyze_btn": "🔍 பகுப்பாய்வு",
        "capture_btn": "📷 படம் எடுத்து பகுப்பாய்வு",
    },
    "ಕನ್ನಡ": {
        "title": "🍅 ಟೊಮೇಟೊ ಎಲೆ ರೋಗ ಪತ್ತೆ",
        "upload_tab": "📁 ಚಿತ್ರ ಅಪ್‌ಲೋಡ್",
        "webcam_tab": "📷 ವೆಬ್‌ಕ್ಯಾಮ್",
        "result_header": "🔬 ಫಲಿತಾಂಶ",
        "disease_label": "ರೋಗ",
        "confidence_label": "ವಿಶ್ವಾಸ ಮಟ್ಟ",
        "description_label": "ವಿವರಣೆ",
        "symptoms_label": "ಲಕ್ಷಣಗಳು",
        "remedy_label": "ಸಾವಯವ ಪರಿಹಾರ",
        "pesticide_label": "ಕೀಟನಾಶಕ ಶಿಫಾರಸು",
        "shop_label": "ಹತ್ತಿರದ ಕೃಷಿ ಅಂಗಡಿ",
        "not_leaf_label": "⚠️ ಇದು ಎಲೆ ಅಲ್ಲ",
        "healthy_msg": "✅ ನಿಮ್ಮ ಟೊಮೇಟೊ ಗಿಡ ಆರೋಗ್ಯಕರವಾಗಿದೆ!",
        "upload_prompt": "ಸ್ಪಷ್ಟ ಟೊಮೇಟೊ ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "webcam_prompt": "ವೆಬ್‌ಕ್ಯಾಮ್‌ನಿಂದ ಎಲೆ ಚಿತ್ರ ತೆಗೆಯಿರಿ",
        "analyze_btn": "🔍 ವಿಶ್ಲೇಷಿಸಿ",
        "capture_btn": "📷 ತೆಗೆದು ವಿಶ್ಲೇಷಿಸಿ",
    },
    "മലയാളം": {
        "title": "🍅 തക്കാളി ഇല രോഗ കണ്ടെത്തൽ",
        "upload_tab": "📁 ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "webcam_tab": "📷 വെബ്ക്യാം",
        "result_header": "🔬 ഫലം",
        "disease_label": "രോഗം",
        "confidence_label": "ആത്മവിശ്വാസ നിലവാരം",
        "description_label": "വിവരണം",
        "symptoms_label": "ലക്ഷണങ്ങൾ",
        "remedy_label": "ജൈവ പ്രതിവിധി",
        "pesticide_label": "കീടനാശിനി ശുപാർശ",
        "shop_label": "അടുത്തുള്ള കൃഷി കട",
        "not_leaf_label": "⚠️ ഇത് ഒരു ഇലയല്ല",
        "healthy_msg": "✅ നിങ്ങളുടെ തക്കാളി ചെടി ആരോഗ്യകരമാണ്!",
        "upload_prompt": "വ്യക്തമായ ഒരു തക്കാളി ഇലയുടെ ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
        "webcam_prompt": "വെബ്ക്യാമിൽ നിന്ന് ഇലയുടെ ചിത്രം എടുക്കുക",
        "analyze_btn": "🔍 വിശകലനം",
        "capture_btn": "📷 പകർത്തി വിശകലനം ചെയ്യുക",
    },
}

# ─────────────────────────────────────────────────────────────
# DISEASE DATABASE
# ─────────────────────────────────────────────────────────────
DISEASE_INFO = {

    "Bacterial Spot": {
        "en_name": "Bacterial Spot",
        "icon": "🦠",
        "severity": "Moderate",
        "description": "Bacterial Spot is caused by Xanthomonas species. It affects leaves, stems and fruits, causing significant yield losses in warm, wet conditions.",
        "symptoms": [
            "Small, water-soaked spots on leaves (1–3 mm)",
            "Spots turn brown/black with yellow halos",
            "Irregular lesions on fruits",
            "Leaves turn yellow and drop prematurely",
        ],
        "organic_remedy": [
            "Spray copper-based bactericide (Bordeaux mixture 1%) every 7–10 days",
            "Apply Neem oil spray (2%) to reduce bacterial spread",
            "Remove and destroy infected plant parts immediately",
            "Avoid overhead irrigation — use drip irrigation",
            "Rotate crops with non-solanaceous plants for 2–3 years",
            "Apply Trichoderma viride to soil before planting",
        ],
        "pesticides": [
            {
                "name": "Blitox 50 WP (Copper Oxychloride)",
                "brand": "Bayer India",
                "dose": "3g per litre of water",
                "price_range": "₹180–₹220 / 250g",
                "when": "At first sign of disease, repeat every 7 days",
            },
            {
                "name": "Kocide 3000 (Copper Hydroxide)",
                "brand": "FMC India",
                "dose": "2g per litre of water",
                "price_range": "₹350–₹420 / 250g",
                "when": "Preventive spray before rainy season",
            },
            {
                "name": "Streptomycin Sulphate 9% + Tetracycline 1%",
                "brand": "Various (Plantomycin)",
                "dose": "0.5g per litre of water",
                "price_range": "₹120–₹160 / 50g",
                "when": "Only when disease severity is high",
            },
        ],
        "translations": {
            "తెలుగు": {
                "name": "బ్యాక్టీరియల్ స్పాట్",
                "description": "జాంథోమోనాస్ బ్యాక్టీరియా వల్ల వచ్చే వ్యాధి, తేమతో కూడిన వాతావరణంలో వ్యాపిస్తుంది.",
                "symptoms": "ఆకులపై చిన్న నీటి మరకలు, పసుపు అంచులతో నల్లని మచ్చలు, ఆకులు రాలిపోవడం.",
                "remedy": "బోర్డో మిశ్రమం (1%) పిచికారీ చేయండి. వేప నూనె వాడండి. నీటి పారుదల మెరుగుపరచండి.",
            },
            "हिंदी": {
                "name": "बैक्टीरियल स्पॉट",
                "description": "ज़ैंथोमोनास बैक्टीरिया के कारण होने वाली बीमारी, गर्म और आर्द्र मौसम में फैलती है।",
                "symptoms": "पत्तियों पर छोटे काले धब्बे, पीले घेरे, पत्तियों का झड़ना।",
                "remedy": "बोर्डो मिश्रण (1%) का छिड़काव करें। नीम के तेल का उपयोग करें।",
            },
            "தமிழ்": {
                "name": "பாக்டீரியா புள்ளி",
                "description": "Xanthomonas பாக்டீரியாவால் ஏற்படும் நோய், வெப்பமான மற்றும் ஈரமான சூழலில் பரவுகிறது.",
                "symptoms": "இலைகளில் சிறிய கருப்பு புள்ளிகள், மஞ்சள் வளையங்கள், இலை உதிர்வு.",
                "remedy": "போர்டோ கலவை (1%) தெளிக்கவும். வேப்ப எண்ணெய் பயன்படுத்தவும்.",
            },
            "ಕನ್ನಡ": {
                "name": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಸ್ಪಾಟ್",
                "description": "ಜಾಂಥೋಮೋನಾಸ್ ಬ್ಯಾಕ್ಟೀರಿಯಾದಿಂದ ಉಂಟಾಗುವ ರೋಗ.",
                "symptoms": "ಎಲೆಗಳ ಮೇಲೆ ಸಣ್ಣ ಕಪ್ಪು ಚುಕ್ಕೆಗಳು, ಹಳದಿ ವಲಯಗಳು.",
                "remedy": "ಬೋರ್ಡೋ ಮಿಶ್ರಣ (1%) ಸಿಂಪಡಿಸಿ. ಬೇವಿನ ಎಣ್ಣೆ ಬಳಸಿ.",
            },
            "മലയാളം": {
                "name": "ബാക്ടീരിയൽ സ്പോട്ട്",
                "description": "Xanthomonas ബാക്ടീരിയ മൂലം ഉണ്ടാകുന്ന രോഗം.",
                "symptoms": "ഇലകളിൽ ചെറിയ കറുത്ത പൊട്ടുകൾ, മഞ്ഞ വളയങ്ങൾ, ഇല കൊഴിയൽ.",
                "remedy": "ബോർഡോ മിശ്രിതം (1%) തളിക്കുക. വേപ്പ് എണ്ണ ഉപയോഗിക്കുക.",
            },
        },
    },

    "Early Blight": {
        "en_name": "Early Blight",
        "icon": "🍂",
        "severity": "Moderate to High",
        "description": "Early Blight is caused by the fungus Alternaria solani. It first attacks older leaves and can cause complete defoliation if untreated.",
        "symptoms": [
            "Concentric ring (target board) brown spots on older leaves",
            "Yellow halos around the brown spots",
            "Dark brown spots on stems and fruits",
            "Lower leaves affected first",
            "Severe defoliation leading to sunscald on fruits",
        ],
        "organic_remedy": [
            "Apply Mancozeb 75 WP spray (2.5g/L) every 10 days",
            "Use Trichoderma-based bio-fungicide",
            "Mulch around plants to prevent soil splashing",
            "Avoid wetting foliage during irrigation",
            "Remove infected leaves and burn them",
            "Spray baking soda solution (5g/L) as early preventive",
        ],
        "pesticides": [
            {
                "name": "Dithane M-45 (Mancozeb 75% WP)",
                "brand": "Dow AgroSciences India",
                "dose": "2.5g per litre of water",
                "price_range": "₹280–₹320 / 500g",
                "when": "Start spraying at first sign, continue weekly",
            },
            {
                "name": "Ridomil Gold MZ (Metalaxyl + Mancozeb)",
                "brand": "Syngenta India",
                "dose": "2g per litre of water",
                "price_range": "₹550–₹650 / 500g",
                "when": "During high humidity / pre-monsoon",
            },
            {
                "name": "Amistar Top (Azoxystrobin + Difenoconazole)",
                "brand": "Syngenta India",
                "dose": "1ml per litre of water",
                "price_range": "₹800–₹950 / 200ml",
                "when": "Severe infection, systemic action needed",
            },
        ],
        "translations": {
            "తెలుగు": {
                "name": "ఎర్లీ బ్లైట్",
                "description": "ఆల్టర్నేరియా సోలాని అనే శిలీంధ్రం వల్ల వచ్చే వ్యాధి. పాత ఆకులపై మొదటగా దాడి చేస్తుంది.",
                "symptoms": "గోల రింగులతో గోధుమ రంగు మచ్చలు, పసుపు అంచులు, ఆకులు రాలిపోవడం.",
                "remedy": "మాంకోజెబ్ పిచికారీ చేయండి. ట్రైకోడెర్మా వాడండి. ఆకులకు నీరు పడకుండా చూడండి.",
            },
            "हिंदी": {
                "name": "अर्ली ब्लाइट",
                "description": "अल्टरनेरिया सोलानी कवक के कारण होने वाला रोग।",
                "symptoms": "लक्ष्य बोर्ड जैसे भूरे धब्बे, पीले घेरे, पत्तियों का झड़ना।",
                "remedy": "मैनकोजेब का छिड़काव करें। ट्राइकोडर्मा का उपयोग करें।",
            },
            "தமிழ்": {
                "name": "எர்லி ப்லைட்",
                "description": "Alternaria solani என்ற பூஞ்சையால் ஏற்படும் நோய்.",
                "symptoms": "இலைகளில் இலக்கு வட்ட வடிவ பழுப்பு புள்ளிகள், மஞ்சள் வளையங்கள்.",
                "remedy": "மான்கோஜெப் தெளிக்கவும். டிரைக்கோடெர்மா உரம் பயன்படுத்தவும்.",
            },
            "ಕನ್ನಡ": {
                "name": "ಅರ್ಲಿ ಬ್ಲೈಟ್",
                "description": "Alternaria solani ಶಿಲೀಂಧ್ರದಿಂದ ಉಂಟಾಗುವ ರೋಗ.",
                "symptoms": "ಎಲೆಗಳ ಮೇಲೆ ಗುರಿ ಆಕಾರದ ಕಂದು ಚುಕ್ಕೆಗಳು.",
                "remedy": "ಮ್ಯಾಂಕೋಜೆಬ್ ಸಿಂಪಡಿಸಿ. ಟ್ರೈಕೋಡರ್ಮಾ ಬಳಸಿ.",
            },
            "മലയാളം": {
                "name": "എർലി ബ്ലൈറ്റ്",
                "description": "Alternaria solani ഫംഗസ് മൂലം ഉണ്ടാകുന്ന രോഗം.",
                "symptoms": "ഇലകളിൽ ടാർഗറ്റ് ബോർഡ് ആകൃതിയിലുള്ള തവിട്ടു പൊട്ടുകൾ.",
                "remedy": "മാൻകോസെബ് തളിക്കുക. ട്രൈക്കോഡർമ ഉപയോഗിക്കുക.",
            },
        },
    },

    "Late Blight": {
        "en_name": "Late Blight",
        "icon": "☠️",
        "severity": "Very High (can destroy entire crop)",
        "description": "Late Blight caused by Phytophthora infestans is one of the most devastating tomato diseases. It caused the Irish Potato Famine. Acts very fast in cool, wet conditions.",
        "symptoms": [
            "Water-soaked, pale green to brown lesions on leaves",
            "White fungal growth (mold) on underside of leaves",
            "Brown-black lesions on stems",
            "Fruit shows firm, brown rot",
            "Entire plant can collapse within days",
        ],
        "organic_remedy": [
            "Spray copper hydroxide (3g/L) immediately at first sign",
            "Remove and bag all infected plant material — do not compost",
            "Improve air circulation by pruning lower leaves",
            "Avoid overhead watering, especially in evenings",
            "Apply phosphorous acid (Fosetyl-Al) for systemic protection",
            "Resistant varieties: Arka Rakshak, Pusa Hybrid-8",
        ],
        "pesticides": [
            {
                "name": "Infinito (Fluopicolide + Propamocarb)",
                "brand": "Bayer CropScience India",
                "dose": "1.6ml per litre of water",
                "price_range": "₹1100–₹1300 / 200ml",
                "when": "URGENT — apply immediately at first sign",
            },
            {
                "name": "Revus (Mandipropamid)",
                "brand": "Syngenta India",
                "dose": "0.6ml per litre",
                "price_range": "₹900–₹1100 / 200ml",
                "when": "Preventive + curative, excellent for late blight",
            },
            {
                "name": "Kocide 3000 (Copper Hydroxide)",
                "brand": "FMC India",
                "dose": "2–3g per litre",
                "price_range": "₹350–₹420 / 250g",
                "when": "Early preventive, alternate with systemic fungicide",
            },
        ],
        "translations": {
            "తెలుగు": {
                "name": "లేట్ బ్లైట్",
                "description": "ఫైటోఫ్తోరా ఇన్ఫెస్టాన్స్ వల్ల వచ్చే అత్యంత ప్రమాదకరమైన వ్యాధి. వేగంగా మొత్తం పంటను నాశనం చేయగలదు.",
                "symptoms": "నీటి మరకల్లాంటి పాలిపోయిన ఆకు మచ్చలు, ఆకు కింద తెల్లని పూత, కాండం మీద నల్లని మచ్చలు.",
                "remedy": "తక్షణమే రాగి హైడ్రాక్సైడ్ పిచికారీ చేయండి. సోకిన మొక్కలను తొలగించండి. వాతావరణ ప్రసరణ మెరుగుపరచండి.",
            },
            "हिंदी": {
                "name": "लेट ब्लाइट",
                "description": "फाइटोफ्थोरा इन्फेस्टान्स के कारण होने वाली सबसे खतरनाक बीमारी।",
                "symptoms": "पानी भीगे जैसे धब्बे, पत्तियों के नीचे सफेद फफूंद, पूरा पौधा खराब हो सकता है।",
                "remedy": "तुरंत कॉपर हाइड्रॉक्साइड का छिड़काव करें। संक्रमित पत्तियों को हटाएं।",
            },
            "தமிழ்": {
                "name": "லேட் ப்லைட்",
                "description": "Phytophthora infestans மூலம் ஏற்படும் மிகவும் ஆபத்தான நோய்.",
                "symptoms": "நீரில் ஊறிய பச்சை-பழுப்பு புண்கள், இலை அடியில் வெள்ளை பூஞ்சை.",
                "remedy": "உடனடியாக காப்பர் ஹைட்ராக்சைடு தெளிக்கவும். பாதிக்கப்பட்ட பகுதிகளை நீக்கவும்.",
            },
            "ಕನ್ನಡ": {
                "name": "ಲೇಟ್ ಬ್ಲೈಟ್",
                "description": "Phytophthora infestans ನಿಂದ ಉಂಟಾಗುವ ಅತ್ಯಂತ ಅಪಾಯಕಾರಿ ರೋಗ.",
                "symptoms": "ನೀರು ಹಿಡಿದಂತಹ ಹಸಿರು-ಕಂದು ಗಾಯಗಳು, ಎಲೆಗಳ ಕೆಳಗೆ ಬಿಳಿ ಶಿಲೀಂಧ್ರ.",
                "remedy": "ತಕ್ಷಣ ಕಾಪರ್ ಹೈಡ್ರಾಕ್ಸೈಡ್ ಸಿಂಪಡಿಸಿ.",
            },
            "മലയാളം": {
                "name": "ലേറ്റ് ബ്ലൈറ്റ്",
                "description": "Phytophthora infestans മൂലം ഉണ്ടാകുന്ന ഏറ്റവും ഭീകരമായ രോഗം.",
                "symptoms": "വെള്ളത്തിൽ കുതിർന്ന ഇളം പച്ച-തവിട്ടു ക്ഷതങ്ങൾ, ഇലയുടെ അടിഭാഗത്ത് വെള്ള പൂപ്പൽ.",
                "remedy": "ഉടൻ കോപ്പർ ഹൈഡ്രോക്സൈഡ് തളിക്കുക.",
            },
        },
    },

    "Healthy": {
        "en_name": "Healthy",
        "icon": "✅",
        "severity": "None",
        "description": "Your tomato plant leaf is healthy! No disease detected. Continue good farming practices to maintain plant health.",
        "symptoms": [
            "Bright green color throughout the leaf",
            "No spots, lesions, or discoloration",
            "Firm leaf texture",
            "No curling or wilting",
        ],
        "organic_remedy": [
            "Continue regular watering (avoid overwatering)",
            "Apply balanced NPK fertilizer monthly",
            "Use neem-based pesticide as preventive measure",
            "Ensure proper spacing for good air circulation",
            "Monitor weekly for early signs of disease",
        ],
        "pesticides": [],
        "translations": {
            "తెలుగు": {
                "name": "ఆరోగ్యకరం",
                "description": "మీ టమాటా ఆకు పూర్తిగా ఆరోగ్యంగా ఉంది! వ్యాధి లేదు.",
                "symptoms": "పచ్చని రంగు, మచ్చలు లేవు, ఆకు గట్టిగా ఉంది.",
                "remedy": "సరైన నీటి పారుదల కొనసాగించండి. NPK ఎరువులు వాడండి.",
            },
            "हिंदी": {
                "name": "स्वस्थ",
                "description": "आपकी टमाटर की पत्ती पूरी तरह स्वस्थ है!",
                "symptoms": "हरा रंग, कोई धब्बा नहीं, पत्ती मजबूत है।",
                "remedy": "नियमित सिंचाई जारी रखें। NPK खाद का उपयोग करें।",
            },
            "தமிழ்": {
                "name": "ஆரோக்கியம்",
                "description": "உங்கள் தக்காளி இலை முழுமையாக ஆரோக்கியமாக உள்ளது!",
                "symptoms": "பச்சை நிறம், புள்ளிகள் இல்லை, இலை உறுதியாக உள்ளது.",
                "remedy": "சரியான நீர்ப்பாசனம் தொடரவும். NPK உரம் பயன்படுத்தவும்.",
            },
            "ಕನ್ನಡ": {
                "name": "ಆರೋಗ್ಯಕರ",
                "description": "ನಿಮ್ಮ ಟೊಮೇಟೊ ಎಲೆ ಸಂಪೂರ್ಣ ಆರೋಗ್ಯಕರವಾಗಿದೆ!",
                "symptoms": "ಹಸಿರು ಬಣ್ಣ, ಚುಕ್ಕೆಗಳಿಲ್ಲ, ಎಲೆ ಗಟ್ಟಿಯಾಗಿದೆ.",
                "remedy": "ನಿಯಮಿತ ನೀರಾವರಿ ಮುಂದುವರಿಸಿ. NPK ಗೊಬ್ಬರ ಬಳಸಿ.",
            },
            "മലയാളം": {
                "name": "ആരോഗ്യകരം",
                "description": "നിങ്ങളുടെ തക്കാളി ഇല പൂർണ്ണ ആരോഗ്യത്തിൽ ഉണ്ട്!",
                "symptoms": "പച്ച നിറം, പൊട്ടുകൾ ഇല്ല, ഇല ഉറപ്പുള്ളതാണ്.",
                "remedy": "പതിവ് നനയ്ക്കൽ തുടരുക. NPK വളം ഉപയോഗിക്കുക.",
            },
        },
    },

    "Septoria Leaf Spot": {
        "en_name": "Septoria Leaf Spot",
        "icon": "🔴",
        "severity": "Moderate",
        "description": "Caused by Septoria lycopersici fungus. One of the most destructive foliar diseases of tomato. Starts on lower leaves and moves upward.",
        "symptoms": [
            "Numerous small (2–4 mm) circular spots with white/gray centers",
            "Dark brown borders around each spot",
            "Tiny black specks (pycnidia) visible in spot centers",
            "Leaves turn yellow then brown and drop",
            "Disease progresses from bottom to top of plant",
        ],
        "organic_remedy": [
            "Apply Chlorothalonil (Kavach) every 7–10 days",
            "Remove infected lower leaves regularly",
            "Water at base, not overhead",
            "Apply compost tea spray as preventive",
            "Maintain 45–60cm spacing between plants",
        ],
        "pesticides": [
            {
                "name": "Kavach (Chlorothalonil 75% WP)",
                "brand": "Syngenta India",
                "dose": "2g per litre of water",
                "price_range": "₹200–₹250 / 250g",
                "when": "Every 7–10 days from disease onset",
            },
            {
                "name": "Contaf (Hexaconazole 5% EC)",
                "brand": "BASF India",
                "dose": "2ml per litre of water",
                "price_range": "₹150–₹200 / 250ml",
                "when": "Systemic treatment when infection is moderate",
            },
        ],
        "translations": {
            "తెలుగు": {
                "name": "సెప్టోరియా ఆకు మచ్చ",
                "description": "సెప్టోరియా లైకోపెర్సిసి శిలీంధ్రం వల్ల వచ్చే వ్యాధి.",
                "symptoms": "చిన్న గుండ్రటి మచ్చలు (తెలుపు/బూడిద కేంద్రం), ముదురు అంచులు.",
                "remedy": "క్లోరోతలోనిల్ పిచికారీ చేయండి. దిగువ ఆకులు తొలగించండి.",
            },
            "हिंदी": {
                "name": "सेप्टोरिया पत्ती धब्बा",
                "description": "सेप्टोरिया लाइकोपर्सिसी कवक के कारण होने वाला रोग।",
                "symptoms": "छोटे गोल धब्बे (सफेद/भूरे केंद्र), गहरे भूरे किनारे।",
                "remedy": "क्लोरोथेलोनिल का छिड़काव करें। निचली पत्तियों को हटाएं।",
            },
            "தமிழ்": {
                "name": "செப்டோரியா இலைப் புள்ளி",
                "description": "Septoria lycopersici பூஞ்சையால் ஏற்படும் நோய்.",
                "symptoms": "சிறிய வட்ட புள்ளிகள் (வெள்ளை/சாம்பல் மையம்), அடர் பழுப்பு விளிம்புகள்.",
                "remedy": "குளோரோத்தலோனில் தெளிக்கவும். கீழ் இலைகளை அகற்றவும்.",
            },
            "ಕನ್ನಡ": {
                "name": "ಸೆಪ್ಟೋರಿಯಾ ಎಲೆ ಚುಕ್ಕೆ",
                "description": "Septoria lycopersici ಶಿಲೀಂಧ್ರದಿಂದ ಉಂಟಾಗುವ ರೋಗ.",
                "symptoms": "ಸಣ್ಣ ಸುತ್ತಾಕಾರದ ಚುಕ್ಕೆಗಳು (ಬಿಳಿ/ಬೂದು ಕೇಂದ್ರ).",
                "remedy": "ಕ್ಲೋರೋಥಾಲೋನಿಲ್ ಸಿಂಪಡಿಸಿ.",
            },
            "മലയാളം": {
                "name": "സെപ്റ്റോറിയ ഇലപ്പൊട്ടൽ",
                "description": "Septoria lycopersici ഫംഗസ് മൂലം ഉണ്ടാകുന്ന രോഗം.",
                "symptoms": "ചെറിയ വൃത്താകൃതിയിലുള്ള പൊട്ടുകൾ (വെള്ള/ചാര കേന്ദ്രം).",
                "remedy": "ക്ലോറോതലോണിൽ തളിക്കുക.",
            },
        },
    },

    "Yellow Leaf Curl Virus": {
        "en_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "icon": "🟡",
        "severity": "Very High",
        "description": "TYLCV is transmitted by the silverleaf whitefly (Bemisia tabaci). There is no chemical cure — management focuses on controlling the whitefly vector and using resistant varieties.",
        "symptoms": [
            "Upward curling and cupping of leaves",
            "Severe yellowing (chlorosis) of leaf margins",
            "Stunted plant growth",
            "Flower drop, very few fruits",
            "New leaves remain small and deformed",
        ],
        "organic_remedy": [
            "Install yellow sticky traps to catch whiteflies (40 traps/acre)",
            "Spray Imidacloprid (0.3ml/L) to control whitefly vector",
            "Use reflective silver mulch to repel whiteflies",
            "Plant resistant varieties: Arka Ananya, NS 7552, COTH-3",
            "Remove and destroy infected plants early to prevent spread",
            "Spray Neem oil (3%) + soap solution to repel whiteflies",
        ],
        "pesticides": [
            {
                "name": "Confidor (Imidacloprid 17.8% SL)",
                "brand": "Bayer CropScience India",
                "dose": "0.3ml per litre (drench) or 0.5ml/L (spray)",
                "price_range": "₹230–₹280 / 100ml",
                "when": "To kill whitefly vector — does NOT cure the virus",
            },
            {
                "name": "Actara (Thiamethoxam 25% WG)",
                "brand": "Syngenta India",
                "dose": "0.3g per litre of water",
                "price_range": "₹280–₹350 / 100g",
                "when": "Alternate with Imidacloprid to prevent resistance",
            },
            {
                "name": "Pegasus (Diafenthiuron 50% WP)",
                "brand": "Novartis India",
                "dose": "1g per litre of water",
                "price_range": "₹400–₹480 / 250g",
                "when": "For resistant whitefly populations",
            },
        ],
        "translations": {
            "తెలుగు": {
                "name": "టమాటా పసుపు ఆకు మెలిక వైరస్",
                "description": "వైట్‌ఫ్లై ద్వారా వ్యాపించే వైరస్ వ్యాధి. నేరుగా రసాయన నివారణ లేదు.",
                "symptoms": "ఆకులు పైకి మెలిత పడటం, పసుపు రంగు మారడం, మొక్క పెరుగుదల ఆగిపోవడం.",
                "remedy": "వైట్‌ఫ్లై నియంత్రణకు ఇమిడాక్లోప్రిడ్ పిచికారీ చేయండి. తట్టుకునే రకాలు వాడండి.",
            },
            "हिंदी": {
                "name": "टमाटर पीला पत्ता कर्ल वायरस",
                "description": "सफेद मक्खी द्वारा फैलने वाला वायरस रोग।",
                "symptoms": "पत्तियों का ऊपर की ओर मुड़ना, पीलापन, पौधे का रुका विकास।",
                "remedy": "सफेद मक्खी नियंत्रण के लिए इमिडाक्लोप्रिड का छिड़काव करें।",
            },
            "தமிழ்": {
                "name": "தக்காளி மஞ்சள் இலை சுருள் வைரஸ்",
                "description": "வெள்ளை ஈ மூலம் பரவும் வைரஸ் நோய்.",
                "symptoms": "இலைகள் மேல்நோக்கி சுருளுகின்றன, மஞ்சள் நிறம், வளர்ச்சி தடை.",
                "remedy": "வெள்ளை ஈ கட்டுப்பாட்டிற்கு இமிடாக்லோபிரிட் தெளிக்கவும்.",
            },
            "ಕನ್ನಡ": {
                "name": "ಟೊಮೇಟೊ ಹಳದಿ ಎಲೆ ಸುರುಳಿ ವೈರಸ್",
                "description": "ಬಿಳಿ ನೊಣದಿಂದ ಹರಡುವ ವೈರಸ್ ರೋಗ.",
                "symptoms": "ಎಲೆಗಳು ಮೇಲಕ್ಕೆ ಸುರುಳಿಯಾಗುವವು, ಹಳದಿ ಬಣ್ಣ, ಬೆಳವಣಿಗೆ ನಿಂತುಹೋಗುವುದು.",
                "remedy": "ಬಿಳಿ ನೊಣ ನಿಯಂತ್ರಣಕ್ಕೆ ಇಮಿಡಾಕ್ಲೋಪ್ರಿಡ್ ಸಿಂಪಡಿಸಿ.",
            },
            "മലയാളം": {
                "name": "തക്കാളി മഞ്ഞ ഇല ചുരുൾ വൈറസ്",
                "description": "വെള്ളീച്ച വഴി പടരുന്ന വൈറസ് രോഗം.",
                "symptoms": "ഇലകൾ മുകളിലേക്ക് ചുരുളുന്നു, മഞ്ഞ നിറം, വളർച്ച നിലയ്ക്കുന്നു.",
                "remedy": "വെള്ളീച്ച നിയന്ത്രണത്തിന് ഇമിഡാക്ലോപ്രിഡ് തളിക്കുക.",
            },
        },
    },
}


def get_disease_info(disease_name: str, language: str = "English") -> dict:
    """
    Get disease information in the requested language.
    Falls back to English if translation not available.
    """
    info = DISEASE_INFO.get(disease_name, DISEASE_INFO["Healthy"])

    if language == "English" or language not in info.get("translations", {}):
        return {
            "name": info["en_name"],
            "icon": info["icon"],
            "severity": info["severity"],
            "description": info["description"],
            "symptoms": info["symptoms"],
            "organic_remedy": info["organic_remedy"],
            "pesticides": info["pesticides"],
        }
    else:
        t = info["translations"][language]
        return {
            "name": t["name"],
            "icon": info["icon"],
            "severity": info["severity"],
            "description": t["description"],
            "symptoms": t.get("symptoms", info["symptoms"]),
            "organic_remedy": t.get("remedy", ""),
            "pesticides": info["pesticides"],
        }
