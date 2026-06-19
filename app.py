# -*- coding: utf-8 -*-
"""
TomatoAI - Complete Farmer App
Home -> Language -> How to Use -> Login/Signup -> Dashboard
"""
import gradio as gr
import numpy as np
import tensorflow as tf
from PIL import Image
import json, os, urllib.parse, hashlib, datetime

from leaf_checker import is_leaf
from disease_info import DISEASE_INFO, LANG_LABELS, get_disease_info

BASE_DIR   = r"C:\Users\gakil\Desktop\TomatoAI"
MODEL_PATH = os.path.join(BASE_DIR, "model", "tomato_disease_model.h5")
INDEX_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")

print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
with open(INDEX_PATH) as f:
    class_indices = json.load(f)
idx_to_class = {v: k for k, v in class_indices.items()}
print("Model loaded:", idx_to_class)

USERS = {}
SCAN_HISTORY = {}

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

LANGUAGES = ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"]

LANG_MAP = {
    "English":  "English",
    "Telugu":   "తెలుగు",
    "Hindi":    "हिंदी",
    "Tamil":    "தமிழ்",
    "Kannada":  "ಕನ್ನಡ",
    "Malayalam":"മലയാളം",
}

# Complete translation dictionary
UI = {
    "app_name":         {"English":"TomatoAI","Telugu":"టమాటో AI","Hindi":"टमाटो AI","Tamil":"தக்காளி AI","Kannada":"ಟೊಮೇಟೊ AI","Malayalam":"ടൊമേറ്റോ AI"},
    "tagline":          {"English":"AI-Powered Tomato Disease Detection","Telugu":"AI ఆధారిత టమాటా వ్యాధి గుర్తింపు","Hindi":"AI-संचालित टमाटर रोग पहचान","Tamil":"AI-இயக்கும் தக்காளி நோய் கண்டறிதல்","Kannada":"AI-ಚಾಲಿತ ಟೊಮೇಟೊ ರೋಗ ಪತ್ತೆ","Malayalam":"AI-ശക്തിയുള്ള തക്കാളി രോഗ കണ്ടെത്തൽ"},
    "select_lang":      {"English":"Choose Your Language","Telugu":"మీ భాష ఎంచుకోండి","Hindi":"अपनी भाषा चुनें","Tamil":"உங்கள் மொழியை தேர்ந்தெடுக்கவும்","Kannada":"ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ","Malayalam":"നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക"},
    "continue_btn":     {"English":"Continue","Telugu":"కొనసాగించు","Hindi":"जारी रखें","Tamil":"தொடர","Kannada":"ಮುಂದುವರಿಯಿರಿ","Malayalam":"തുടരുക"},
    "get_started":      {"English":"Get Started","Telugu":"ప్రారంభించండి","Hindi":"शुरू करें","Tamil":"தொடங்குங்கள்","Kannada":"ಪ್ರಾರಂಭಿಸಿ","Malayalam":"ആരംഭിക്കുക"},
    "login_tab":        {"English":"Login","Telugu":"లాగిన్","Hindi":"लॉगिन","Tamil":"உள்நுழை","Kannada":"ಲಾಗಿನ್","Malayalam":"ലോഗിൻ"},
    "signup_tab":       {"English":"Sign Up","Telugu":"నమోదు చేయండి","Hindi":"साइन अप","Tamil":"பதிவு செய்யுங்கள்","Kannada":"ಸೈನ್ ಅಪ್","Malayalam":"സൈൻ അപ്"},
    "username":         {"English":"Username","Telugu":"వినియోగదారు పేరు","Hindi":"उपयोगकर्ता नाम","Tamil":"பயனர்பெயர்","Kannada":"ಬಳಕೆದಾರ ಹೆಸರು","Malayalam":"ഉപയോക്തൃ നാമം"},
    "password":         {"English":"Password","Telugu":"పాస్వర్డ్","Hindi":"पासवर्ड","Tamil":"கடவுச்சொல்","Kannada":"ಪಾಸ್ವರ್ಡ್","Malayalam":"പാസ്വേഡ്"},
    "login_btn":        {"English":"Login to TomatoAI","Telugu":"TomatoAI లోకి లాగిన్","Hindi":"TomatoAI में लॉगिन","Tamil":"TomatoAI உள்நுழையவும்","Kannada":"TomatoAI ಗೆ ಲಾಗಿನ್","Malayalam":"TomatoAI ൽ ലോഗിൻ"},
    "signup_btn":       {"English":"Create Account","Telugu":"ఖాతా సృష్టించండి","Hindi":"खाता बनाएं","Tamil":"கணக்கு உருவாக்கு","Kannada":"ಖಾತೆ ರಚಿಸಿ","Malayalam":"അക്കൗണ്ട് ഉണ്ടാക്കുക"},
    "welcome":          {"English":"Welcome","Telugu":"స్వాగతం","Hindi":"स्वागत है","Tamil":"வரவேற்பு","Kannada":"ಸ್ವಾಗತ","Malayalam":"സ്വാഗതം"},
    "farmer":           {"English":"Farmer","Telugu":"రైతు","Hindi":"किसान","Tamil":"விவசாயி","Kannada":"ರೈತ","Malayalam":"കർഷകൻ"},
    "total_scans":      {"English":"Total Scans","Telugu":"మొత్తం స్కాన్లు","Hindi":"कुल स्कैन","Tamil":"மொத்த ஸ்கேன்","Kannada":"ಒಟ್ಟು ಸ್ಕ್ಯಾನ್","Malayalam":"മൊത്തം സ്കാൻ"},
    "healthy_lbl":      {"English":"Healthy","Telugu":"ఆరోగ్యం","Hindi":"स्वस्थ","Tamil":"ஆரோக்கியம்","Kannada":"ಆರೋಗ್ಯ","Malayalam":"ആരോഗ്യം"},
    "disease_lbl":      {"English":"Diseases","Telugu":"వ్యాధులు","Hindi":"बीमारियाँ","Tamil":"நோய்கள்","Kannada":"ರೋಗಗಳು","Malayalam":"രോഗങ്ങൾ"},
    "recent_scans":     {"English":"Recent Scans","Telugu":"ఇటీవలి స్కాన్లు","Hindi":"हाल के स्कैन","Tamil":"சமீபத்திய ஸ்கேன்கள்","Kannada":"ಇತ್ತೀಚಿನ ಸ್ಕ್ಯಾನ್‌ಗಳು","Malayalam":"സമീപകാല സ്കാനുകൾ"},
    "no_scans":         {"English":"No scans yet — upload a leaf to start!","Telugu":"స్కాన్లు లేవు — ఒక ఆకు అప్‌లోడ్ చేయండి!","Hindi":"कोई स्कैन नहीं — पत्ती अपलोड करें!","Tamil":"ஸ்கேன் இல்லை — ஒரு இலை பதிவேற்றவும்!","Kannada":"ಸ್ಕ್ಯಾನ್ ಇಲ್ಲ — ಎಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ!","Malayalam":"സ്കാൻ ഇല്ല — ഒരു ഇല അപ്‌ലോഡ് ചെയ്യുക!"},
    "upload_tab":       {"English":"Upload Image","Telugu":"చిత్రం అప్‌లోడ్","Hindi":"छवि अपलोड","Tamil":"படம் பதிவேற்றம்","Kannada":"ಚಿತ್ರ ಅಪ್‌ಲೋಡ್","Malayalam":"ചിത്രം അപ്‌ലോഡ്"},
    "webcam_tab":       {"English":"Live Webcam","Telugu":"లైవ్ వెబ్‌కామ్","Hindi":"लाइव वेबकैम","Tamil":"நேரலை வெப்கேம்","Kannada":"ಲೈವ್ ವೆಬ್‌ಕ್ಯಾಮ್","Malayalam":"ലൈവ് വെബ്ക്യാം"},
    "analyze_btn":      {"English":"Analyze Leaf","Telugu":"ఆకు విశ్లేషించు","Hindi":"पत्ती विश्लेषण करें","Tamil":"இலை பகுப்பாய்வு","Kannada":"ಎಲೆ ವಿಶ್ಲೇಷಿಸಿ","Malayalam":"ഇല വിശകലനം"},
    "capture_btn":      {"English":"Capture & Analyze","Telugu":"తీసి విశ్లేషించు","Hindi":"कैप्चर करें","Tamil":"படம் எடுத்து பகுப்பாய்","Kannada":"ತೆಗೆದು ವಿಶ್ಲೇಷಿಸಿ","Malayalam":"പകർത്തി വിശകലനം"},
    "logout":           {"English":"Logout","Telugu":"లాగ్అవుట్","Hindi":"लॉगआउट","Tamil":"வெளியேறு","Kannada":"ಲಾಗ್‌ಔಟ್","Malayalam":"ലോഗ്ഔട്ട്"},
    "upload_lbl":       {"English":"Upload Tomato Leaf Photo","Telugu":"టమాటా ఆకు ఫోటో అప్‌లోడ్ చేయండి","Hindi":"टमाटर की पत्ती की फोटो अपलोड करें","Tamil":"தக்காளி இலை புகைப்படம் பதிவேற்றவும்","Kannada":"ಟೊಮೇಟೊ ಎಲೆ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ","Malayalam":"തക്കാളി ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക"},
    "result_placeholder":{"English":"Upload a leaf to see results here","Telugu":"ఫలితాలు చూడటానికి ఆకు అప్‌లోడ్ చేయండి","Hindi":"परिणाम देखने के लिए पत्ती अपलोड करें","Tamil":"முடிவுகளைக் காண இலையை பதிவேற்றவும்","Kannada":"ಫಲಿತಾಂಶ ನೋಡಲು ಎಲೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ","Malayalam":"ഫലങ്ങൾ കാണാൻ ഇല അപ്‌ലോഡ് ചെയ്യുക"},
    "not_leaf":         {"English":"Not a Tomato Leaf — Please upload a clear leaf photo","Telugu":"ఇది టమాటా ఆకు కాదు — స్పష్టమైన ఆకు ఫోటో అప్‌లోడ్ చేయండి","Hindi":"यह टमाटर की पत्ती नहीं — स्पष्ट पत्ती की फोटो अपलोड करें","Tamil":"இது தக்காளி இலை அல்ல — தெளிவான இலை படம் பதிவேற்றவும்","Kannada":"ಇದು ಟೊಮೇಟೊ ಎಲೆ ಅಲ್ಲ — ಸ್ಪಷ್ಟ ಎಲೆ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ","Malayalam":"ഇത് തക്കാളി ഇലയല്ല — വ്യക്തമായ ഇലയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക"},
    "confidence":       {"English":"Confidence","Telugu":"నిర్ధారణ స్థాయి","Hindi":"विश्वास स्तर","Tamil":"நம்பகத்தன்மை","Kannada":"ವಿಶ್ವಾಸ ಮಟ್ಟ","Malayalam":"ആത്മവിശ്വാസം"},
    "description":      {"English":"Description","Telugu":"వివరణ","Hindi":"विवरण","Tamil":"விளக்கம்","Kannada":"ವಿವರಣೆ","Malayalam":"വിവരണം"},
    "symptoms":         {"English":"Symptoms","Telugu":"లక్షణాలు","Hindi":"लक्षण","Tamil":"அறிகுறிகள்","Kannada":"ಲಕ್ಷಣಗಳು","Malayalam":"ലക്ഷണങ്ങൾ"},
    "remedy":           {"English":"Organic Remedy","Telugu":"సేంద్రీయ నివారణ","Hindi":"जैविक उपाय","Tamil":"இயற்கை தீர்வு","Kannada":"ಸಾವಯವ ಪರಿಹಾರ","Malayalam":"ജൈവ പ്രതിവിധി"},
    "pesticide_lbl":    {"English":"Recommended Pesticides","Telugu":"పురుగుమందుల సూచన","Hindi":"कीटनाशक सुझाव","Tamil":"பூச்சிக்கொல்லி பரிந்துரை","Kannada":"ಕೀಟನಾಶಕ ಶಿಫಾರಸು","Malayalam":"കീടനാശിനി ശുപാർശ"},
    "shop_lbl":         {"English":"Find Nearest Agri Shop","Telugu":"దగ్గర వ్యవసాయ దుకాణం","Hindi":"निकटतम कृषि दुकान","Tamil":"அருகிலுள்ள விவசாய கடை","Kannada":"ಹತ್ತಿರದ ಕೃಷಿ ಅಂಗಡಿ","Malayalam":"അടുത്തുള്ള കൃഷി കട"},
    "find_shop":        {"English":"Find Shop","Telugu":"దుకాణం కనుగొనండి","Hindi":"दुकान खोजें","Tamil":"கடை கண்டறி","Kannada":"ಅಂಗಡಿ ಹುಡುಕಿ","Malayalam":"കട കണ്ടെത്തുക"},
    "soil_title":       {"English":"Soil & Farm Guide","Telugu":"నేల & వ్యవసాయ మార్గదర్శి","Hindi":"मिट्टी और खेत गाइड","Tamil":"மண் மற்றும் பண்ணை வழிகாட்டி","Kannada":"ಮಣ್ಣು ಮತ್ತು ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ","Malayalam":"മണ്ണ് & കൃഷി ഗൈഡ്"},
    "soil_ph":          {"English":"Soil pH","Telugu":"నేల pH","Hindi":"मिट्टी pH","Tamil":"மண் pH","Kannada":"ಮಣ್ಣಿನ pH","Malayalam":"മണ്ണ് pH"},
    "spacing":          {"English":"Plant Spacing","Telugu":"మొక్కల దూరం","Hindi":"पौध दूरी","Tamil":"செடி இடைவெளி","Kannada":"ಗಿಡ ಅಂತರ","Malayalam":"ചെടി അകലം"},
    "soil_type":        {"English":"Soil Type","Telugu":"నేల రకం","Hindi":"मिट्टी का प्रकार","Tamil":"மண் வகை","Kannada":"ಮಣ್ಣಿನ ಪ್ರಕಾರ","Malayalam":"മണ്ണ് തരം"},
    "irrigation":       {"English":"Irrigation","Telugu":"నీటిపారుదల","Hindi":"सिंचाई","Tamil":"நீர்ப்பாசனம்","Kannada":"ನೀರಾವರಿ","Malayalam":"ജലസേചനം"},
    "fertilizer":       {"English":"Fertilizer Schedule","Telugu":"ఎరువు షెడ్యూల్","Hindi":"उर्वरक कार्यक्रम","Tamil":"உர அட்டவணை","Kannada":"ಗೊಬ್ಬರ ವೇಳಾಪಟ್ಟಿ","Malayalam":"വളം ഷെഡ്യൂൾ"},
    "farmer_tip":       {"English":"Farmer Tip","Telugu":"రైతు చిట్కా","Hindi":"किसान सुझाव","Tamil":"விவசாயி குறிப்பு","Kannada":"ರೈತ ಸಲಹೆ","Malayalam":"കർഷക നുറുങ്ങ്"},
    "pest_h_product":   {"English":"Product","Telugu":"ఉత్పత్తి","Hindi":"उत्पाद","Tamil":"தயாரிப்பு","Kannada":"ಉತ್ಪನ್ನ","Malayalam":"ഉൽപ്പന്നം"},
    "pest_h_brand":     {"English":"Brand","Telugu":"బ్రాండ్","Hindi":"ब्रांड","Tamil":"பிராண்ட்","Kannada":"ಬ್ರಾಂಡ್","Malayalam":"ബ്രാൻഡ്"},
    "pest_h_dose":      {"English":"Dose","Telugu":"మోతాదు","Hindi":"मात्रा","Tamil":"அளவு","Kannada":"ಪ್ರಮಾಣ","Malayalam":"അളവ്"},
    "pest_h_price":     {"English":"Price","Telugu":"ధర","Hindi":"कीमत","Tamil":"விலை","Kannada":"ಬೆಲೆ","Malayalam":"വില"},
    "pest_h_when":      {"English":"When to Use","Telugu":"ఎప్పుడు వాడాలి","Hindi":"कब उपयोग करें","Tamil":"எப்போது பயன்படுத்தவும்","Kannada":"ಯಾವಾಗ ಬಳಸಬೇಕು","Malayalam":"എപ്പോൾ ഉപയോഗിക്കണം"},
    "maps_sub":         {"English":"Click to open Google Maps","Telugu":"గూగుల్ మ్యాప్స్ తెరవడానికి క్లిక్ చేయండి","Hindi":"Google Maps खोलने के लिए क्लिक करें","Tamil":"Google Maps திறக்க கிளிக் செய்யவும்","Kannada":"Google Maps ತೆರೆಯಲು ಕ್ಲಿಕ್ ಮಾಡಿ","Malayalam":"Google Maps തുറക്കാൻ ക്ലിക്ക് ചെയ്യുക"},
    "ai_footer":        {"English":"AI Detection","Telugu":"AI గుర్తింపు","Hindi":"AI पहचान","Tamil":"AI கண்டறிதல்","Kannada":"AI ಪತ್ತೆ","Malayalam":"AI കണ്ടെത്തൽ"},
    "expert_note":      {"English":"Always consult a local agricultural expert","Telugu":"స్థానిక వ్యవసాయ నిపుణుడిని సంప్రదించండి","Hindi":"हमेशा स्थानीय कृषि विशेषज्ञ से सलाह लें","Tamil":"எப்போதும் உள்ளூர் வேளாண் நிபுணரை அணுகவும்","Kannada":"ಯಾವಾಗಲೂ ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ","Malayalam":"എപ്പോഴും പ്രാദേശിക കൃഷി വിദഗ്ദ്ധനെ സമീപിക്കുക"},
    "how_step1_title":  {"English":"Step 1 — Upload or Capture","Telugu":"దశ 1 — అప్‌లోడ్ లేదా తీయండి","Hindi":"चरण 1 — अपलोड या कैप्चर करें","Tamil":"படி 1 — பதிவேற்றம் அல்லது படம் எடுக்கவும்","Kannada":"ಹಂತ 1 — ಅಪ್‌ಲೋಡ್ ಅಥವಾ ತೆಗೆಯಿರಿ","Malayalam":"ഘട്ടം 1 — അപ്‌ലോഡ് ചെയ്യുക അല്ലെങ്കിൽ ക്യാപ്ചർ ചെയ്യുക"},
    "how_step1_desc":   {"English":"Take a clear photo of the tomato leaf. Make sure the leaf fills the frame with good lighting.","Telugu":"టమాటా ఆకు యొక్క స్పష్టమైన ఫోటో తీయండి. మంచి కాంతితో ఆకు మొత్తం ఫ్రేమ్‌లో ఉండాలి.","Hindi":"टमाटर की पत्ती की स्पष्ट फोटो लें। सुनिश्चित करें कि पत्ती पूरे फ्रेम में अच्छी रोशनी में हो।","Tamil":"தக்காளி இலையின் தெளிவான புகைப்படம் எடுக்கவும். இலை நல்ல ஒளியில் சட்டகத்தை நிரப்ப வேண்டும்.","Kannada":"ಟೊಮೇಟೊ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ತೆಗೆಯಿರಿ. ಎಲೆ ಉತ್ತಮ ಬೆಳಕಿನೊಂದಿಗೆ ಫ್ರೇಮ್ ತುಂಬಬೇಕು.","Malayalam":"തക്കാളി ഇലയുടെ വ്യക്തമായ ഫോട്ടോ എടുക്കുക. നല്ല വെളിച്ചത്തിൽ ഇല ഫ്രെയിം നിറയ്ക്കണം."},
    "how_step2_title":  {"English":"Step 2 — Click Analyze","Telugu":"దశ 2 — విశ్లేషించు క్లిక్ చేయండి","Hindi":"चरण 2 — विश्लेषण करें क्लिक करें","Tamil":"படி 2 — பகுப்பாய்வு கிளிக் செய்யவும்","Kannada":"ಹಂತ 2 — ವಿಶ್ಲೇಷಿಸಿ ಕ್ಲಿಕ್ ಮಾಡಿ","Malayalam":"ഘട്ടം 2 — വിശകലനം ക്ലിക്ക് ചെയ്യുക"},
    "how_step2_desc":   {"English":"Our AI model analyzes the leaf in seconds and identifies the disease with 95.7% accuracy.","Telugu":"మా AI మోడల్ సెకన్లలో ఆకును విశ్లేషించి 95.7% ఖచ్చితత్వంతో వ్యాధిని గుర్తిస్తుంది.","Hindi":"हमारा AI मॉडल सेकंड में पत्ती का विश्लेषण करता है और 95.7% सटीकता से रोग की पहचान करता है।","Tamil":"எங்கள் AI மாதிரி இலைகளை நொடிகளில் பகுப்பாய்வு செய்து 95.7% துல்லியத்துடன் நோயை அடையாளம் காட்டுகிறது.","Kannada":"ನಮ್ಮ AI ಮಾದರಿ ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಎಲೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ 95.7% ನಿಖರತೆಯಿಂದ ರೋಗ ಗುರುತಿಸುತ್ತದೆ.","Malayalam":"ഞങ്ങളുടെ AI മോഡൽ ഇലകൾ നിമിഷങ്ങളിൽ വിശകലനം ചെയ്ത് 95.7% കൃത്യതയോടെ രോഗം തിരിച്ചറിയുന്നു."},
    "how_step3_title":  {"English":"Step 3 — Get Full Report","Telugu":"దశ 3 — పూర్తి నివేదిక పొందండి","Hindi":"चरण 3 — पूरी रिपोर्ट पाएं","Tamil":"படி 3 — முழு அறிக்கை பெறுங்கள்","Kannada":"ಹಂತ 3 — ಪೂರ್ಣ ವರದಿ ಪಡೆಯಿರಿ","Malayalam":"ഘട്ടം 3 — പൂർണ്ണ റിപ്പോർട്ട് നേടുക"},
    "how_step3_desc":   {"English":"Get disease name, symptoms, organic remedies, pesticide recommendations with prices, soil guide and nearest shop.","Telugu":"వ్యాధి పేరు, లక్షణాలు, సేంద్రీయ నివారణలు, ధరలతో పురుగుమందుల సిఫారసులు, నేల మార్గదర్శి మరియు సమీప దుకాణం పొందండి.","Hindi":"रोग का नाम, लक्षण, जैविक उपाय, कीमतों के साथ कीटनाशक सुझाव, मिट्टी गाइड और नजदीकी दुकान पाएं।","Tamil":"நோய் பெயர், அறிகுறிகள், இயற்கை தீர்வுகள், விலைகளுடன் பூச்சிக்கொல்லி பரிந்துரைகள், மண் வழிகாட்டி மற்றும் அருகிலுள்ள கடை பெறுங்கள்.","Kannada":"ರೋಗದ ಹೆಸರು, ಲಕ್ಷಣಗಳು, ಸಾವಯವ ಪರಿಹಾರಗಳು, ಬೆಲೆಗಳೊಂದಿಗೆ ಕೀಟನಾಶಕ ಶಿಫಾರಸುಗಳು, ಮಣ್ಣಿನ ಮಾರ್ಗದರ್ಶಿ ಮತ್ತು ಹತ್ತಿರದ ಅಂಗಡಿ ಪಡೆಯಿರಿ.","Malayalam":"രോഗം, ലക്ഷണങ്ങൾ, ജൈവ പ്രതിവിധികൾ, വിലകൾ സഹിതം കീടനാശിനി ശുപാർശകൾ, മണ്ണ് ഗൈഡ്, സമീപത്തുള്ള കട നേടുക."},
    "diseases_detected":{"English":"Diseases We Detect","Telugu":"మేము గుర్తించే వ్యాధులు","Hindi":"हम जो रोग पहचानते हैं","Tamil":"நாங்கள் கண்டறியும் நோய்கள்","Kannada":"ನಾವು ಪತ್ತೆ ಮಾಡುವ ರೋಗಗಳು","Malayalam":"ഞങ്ങൾ കണ്ടെത്തുന്ന രോഗങ്ങൾ"},
}

def u(key, lang):
    return UI.get(key, {}).get(lang) or UI.get(key, {}).get("English", "")

SOIL_INFO = {
    "Bacterial Spot":{"ph":"6.0-6.8","soil_key":"Well-drained loamy soil","fertilizer_en":"Reduce nitrogen. Apply potassium (MOP 25kg/acre).","irrigation_en":"Drip only. Never wet leaves.","spacing":"60x45 cm","tip_en":"Never work in field when plants are wet.",
        "fertilizer":{"Telugu":"నత్రజని తగ్గించండి. పొటాషియం (MOP 25కి/ఎకరా) వేయండి.","Hindi":"नाइट्रोजन कम करें। पोटेशियम (MOP 25kg/एकड़) डालें।","Tamil":"நைட்ரஜனை குறைக்கவும். பொட்டாசியம் (MOP 25கி/ஏக்கர்) சேர்க்கவும்.","Kannada":"ಸಾರಜನಕ ಕಡಿಮೆ ಮಾಡಿ. ಪೊಟ್ಯಾಸಿಯಂ (MOP 25kg/ಎಕರೆ) ಹಾಕಿ.","Malayalam":"നൈട്രജൻ കുറയ്ക്കുക. പൊട്ടാസ്യം (MOP 25kg/ഏക്കർ) ചേർക്കുക."},
        "tip":{"Telugu":"తడి మొక్కలపై పని చేయకండి.","Hindi":"गीले पौधों पर काम न करें।","Tamil":"தாவரங்கள் நனைவாக இருக்கும்போது வேலை செய்யாதீர்கள்.","Kannada":"ಒದ್ದೆ ಸಸ್ಯಗಳ ಮೇಲೆ ಕೆಲಸ ಮಾಡಬೇಡಿ.","Malayalam":"ചെടികൾ നനഞ്ഞിരിക്കുമ്പോൾ ജോലി ചെയ്യരുത്."}},
    "Early Blight":{"ph":"6.0-7.0","soil_key":"Sandy loam, good drainage","fertilizer_en":"NPK 19:19:19 monthly. Calcium+Boron foliar spray.","irrigation_en":"Morning only. Keep leaves dry.","spacing":"75x60 cm","tip_en":"Mulch with paddy straw to prevent soil splash.",
        "fertilizer":{"Telugu":"NPK 19:19:19 నెలకోసారి. కాల్షియం+బోరాన్ పిచికారీ.","Hindi":"NPK 19:19:19 मासिक। कैल्शियम+बोरॉन का छिड़काव।","Tamil":"NPK 19:19:19 மாதந்தோறும். கால்சியம்+போரான் தெளிக்கவும்.","Kannada":"NPK 19:19:19 ತಿಂಗಳಿಗೊಮ್ಮೆ. ಕ್ಯಾಲ್ಸಿಯಂ+ಬೋರಾನ್ ಸಿಂಪಡಿಸಿ.","Malayalam":"NPK 19:19:19 മാസം ഒരിക്കൽ. കാൽസ്യം+ബോറോൺ തളിക്കുക."},
        "tip":{"Telugu":"పాకెట్ తడికె వేయండి.","Hindi":"धान की पुआल से मल्चिंग करें।","Tamil":"நெல் வைக்கோல் மல்ச்சிங் செய்யுங்கள்.","Kannada":"ಭತ್ತದ ಹುಲ್ಲಿನಿಂದ ಮಲ್ಚಿಂಗ್ ಮಾಡಿ.","Malayalam":"നെൽ വൈക்கോൽ കൊണ്ട് മൾച്ചിംഗ് ചെയ്യുക."}},
    "Late Blight":{"ph":"6.0-6.5","soil_key":"Raised bed, well-drained","fertilizer_en":"DAP (phosphorus-rich). Avoid excess nitrogen.","irrigation_en":"Drip only. Stop during outbreak.","spacing":"90x60 cm","tip_en":"URGENT: Remove infected plants immediately!",
        "fertilizer":{"Telugu":"DAP (ఫాస్ఫరస్) వేయండి. నత్రజని తగ్గించండి.","Hindi":"DAP (फास्फोरस) डालें। नाइट्रोजन कम करें।","Tamil":"DAP (பாஸ்பரஸ்) கொடுக்கவும். நைட்ரஜனை குறைக்கவும்.","Kannada":"DAP (ಫಾಸ್ಫರಸ್) ಹಾಕಿ. ಸಾರಜನಕ ಕಡಿಮೆ ಮಾಡಿ.","Malayalam":"DAP (ഫോസ്ഫറസ്) കൊടുക്കുക. നൈട്രജൻ കുറയ്ക്കുക."},
        "tip":{"Telugu":"అత్యవസరం: సోకిన మొక్కలు వెంటనే తొలగించండి!","Hindi":"तुरंत: संक्रमित पौधों को हटाएं!","Tamil":"அவசரம்: பாதிக்கப்பட்ட செடிகளை உடனே அகற்றவும்!","Kannada":"ತುರ್ತು: ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ತಕ್ಷಣ ತೆಗೆದು ಹಾಕಿ!","Malayalam":"അടിയന്തരം: ബാധിച്ച ചെടികൾ ഉടൻ നീക്കം ചെയ്യുക!"}},
    "Healthy":{"ph":"6.0-6.8","soil_key":"Loamy, good organic matter","fertilizer_en":"NPK 12:32:16 at planting. Urea at 30 days. Potash at flowering.","irrigation_en":"Drip 4-5L/plant/day. Reduce at fruiting.","spacing":"60x45 cm","tip_en":"Add vermicompost 2 tonnes/acre before planting.",
        "fertilizer":{"Telugu":"NPK 12:32:16 నాటేటప్పుడు. యూరియా 30 రోజులకు. పొటాష్ పూత దశలో.","Hindi":"NPK 12:32:16 रोपाई पर। यूरिया 30 दिन बाद। पोटाश फूल पर।","Tamil":"NPK 12:32:16 நடும்போது. யூரியா 30 நாளில். பொட்டாஷ் பூக்கும்போது.","Kannada":"NPK 12:32:16 ನಾಟಿ ಸಮಯ. ಯೂರಿಯಾ 30 ದಿನಕ್ಕೆ. ಪೊಟ್ಯಾಶ್ ಹೂ ಬಿಡುವಾಗ.","Malayalam":"NPK 12:32:16 നടുമ്പോൾ. യൂറിയ 30 ദിവസത്തിൽ. പൊട്ടാഷ് പൂക്കുമ്പോൾ."},
        "tip":{"Telugu":"వేర్మీకంపోస్ట్ 2 టన్నులు/ఎకరా వేయండి.","Hindi":"वर्मीकम्पोस्ट 2 टन/एकड़ डालें।","Tamil":"மண்புழு உரம் 2 டன்/ஏக்கர் சேர்க்கவும்.","Kannada":"ಎರೆಹುಳ ಗೊಬ್ಬರ 2 ಟನ್/ಎಕರೆ ಹಾಕಿ.","Malayalam":"മണ്ണിര കമ്പോസ്റ്റ് 2 ടൺ/ഏക്കർ ചേർക്കുക."}},
    "Septoria Leaf Spot":{"ph":"6.2-6.8","soil_key":"Well-drained loamy soil","fertilizer_en":"Balanced NPK. Gypsum 200kg/acre. Reduce nitrogen.","irrigation_en":"Base watering only. 60cm row spacing.","spacing":"60x45 cm","tip_en":"Crop rotation - do not plant tomato same field for 2 years.",
        "fertilizer":{"Telugu":"సమతుల్య NPK. జిప్సమ్ 200కి/ఎకరా.","Hindi":"संतुलित NPK। जिप्सम 200kg/एकड़।","Tamil":"சமச்சீர் NPK. ஜிப்சம் 200கி/ஏக்கர்.","Kannada":"ಸಮತೋಲಿತ NPK. ಜಿಪ್ಸಂ 200kg/ಎಕರೆ.","Malayalam":"സമതുലിത NPK. ജിപ്സം 200kg/ഏക്കർ."},
        "tip":{"Telugu":"పంట మార్పిడి — 2 సంవత్సరాలు అదే పొలంలో వేయకండి.","Hindi":"फसल चक्र — 2 साल तक उसी खेत में न लगाएं।","Tamil":"பயிர் சுழற்சி — 2 ஆண்டுகள் அதே நிலத்தில் நடாதீர்கள்.","Kannada":"ಬೆಳೆ ಬದಲಾವಣೆ — 2 ವರ್ಷ ಅದೇ ಹೊಲದಲ್ಲಿ ಹಾಕಬೇಡಿ.","Malayalam":"വിള മാറ്റം — 2 വർഷം അതേ പാടത്ത് നടരുത്."}},
    "Yellow Leaf Curl Virus":{"ph":"6.0-6.5","soil_key":"Sandy loam, well-drained","fertilizer_en":"Reduce nitrogen. Zinc sulfate foliar spray.","irrigation_en":"Regular drip. Avoid plant stress.","spacing":"75x60 cm + silver mulch","tip_en":"Install 40 yellow sticky traps/acre. Plant marigold border.",
        "fertilizer":{"Telugu":"నత్రజని తగ్గించండి. జింక్ సల్ఫేట్ పిచికారీ చేయండి.","Hindi":"नाइट्रोजन कम करें। जिंक सल्फेट का छिड़काव।","Tamil":"நைட்ரஜனை குறைக்கவும். ஜிங்க் சல்பேட் தெளிக்கவும்.","Kannada":"ಸಾರಜನಕ ಕಡಿಮೆ ಮಾಡಿ. ಸತು ಸಲ್ಫೇಟ್ ಸಿಂಪಡಿಸಿ.","Malayalam":"നൈട്രജൻ കുറയ്ക്കുക. സിങ്ക് സൾഫേറ്റ് തളിക്കുക."},
        "tip":{"Telugu":"40 పసుపు అంటే ఉచ్చులు/ఎకరా పెట్టండి. బంతిపూలు నాటండి.","Hindi":"40 पीले जाल/एकड़ लगाएं। गेंदे का बॉर्डर लगाएं।","Tamil":"40 மஞ்சள் பொறிகள்/ஏக்கர் வையுங்கள். மேரிகோல்ட் நடுங்கள்.","Kannada":"40 ಹಳದಿ ಅಂಟು ಬಲೆ/ಎಕರೆ ಇಡಿ. ಮೇರಿಗೋಲ್ಡ್ ಅಂಚು ನೆಡಿ.","Malayalam":"40 മഞ്ഞ കെണികൾ/ഏക്കർ. മേരിഗോൾഡ് അതിർത്തി നടുക."}},
}

def get_soil_html(disease, lang):
    s = SOIL_INFO.get(disease, SOIL_INFO["Healthy"])
    fert = s["fertilizer"].get(lang, s["fertilizer_en"])
    tip  = s["tip"].get(lang, s["tip_en"])
    return f"""<div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:14px;padding:20px;margin-top:14px;">
        <h3 style="color:#15803d;margin:0 0 14px;font-size:15px;font-weight:700;">🌱 {u('soil_title',lang)}</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;">
            <div style="background:white;border:1px solid #dcfce7;border-radius:10px;padding:12px;">
                <div style="color:#86efac;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">🧪 {u('soil_ph',lang)}</div>
                <div style="color:#14532d;font-size:16px;font-weight:700;">{s['ph']}</div>
            </div>
            <div style="background:white;border:1px solid #dcfce7;border-radius:10px;padding:12px;">
                <div style="color:#86efac;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">📏 {u('spacing',lang)}</div>
                <div style="color:#14532d;font-size:14px;font-weight:600;">{s['spacing']}</div>
            </div>
            <div style="background:white;border:1px solid #dcfce7;border-radius:10px;padding:12px;">
                <div style="color:#86efac;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">🌍 {u('soil_type',lang)}</div>
                <div style="color:#166534;font-size:13px;">{s['soil_key']}</div>
            </div>
            <div style="background:white;border:1px solid #dcfce7;border-radius:10px;padding:12px;">
                <div style="color:#86efac;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">💧 {u('irrigation',lang)}</div>
                <div style="color:#166534;font-size:13px;">{s['irrigation_en']}</div>
            </div>
        </div>
        <div style="background:white;border:1px solid #dcfce7;border-radius:10px;padding:12px;margin-bottom:10px;">
            <div style="color:#86efac;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">🌿 {u('fertilizer',lang)}</div>
            <div style="color:#166534;font-size:13px;line-height:1.6;">{fert}</div>
        </div>
        <div style="background:#fefce8;border:1px solid #fde68a;border-radius:10px;padding:12px;">
            <div style="color:#92400e;font-size:13px;font-weight:700;">💡 {u('farmer_tip',lang)}</div>
            <div style="color:#78350f;font-size:13px;margin-top:4px;line-height:1.6;">{tip}</div>
        </div>
    </div>"""

def make_how_to_html(lang):
    diseases = [
        ("🦠", "Bacterial Spot"), ("🍂", "Early Blight"), ("☠️", "Late Blight"),
        ("✅", "Healthy"), ("🔴", "Septoria Leaf Spot"), ("🟡", "Yellow Leaf Curl Virus")
    ]
    disease_cards = "".join(f"""<div style="background:white;border:1px solid #e5e7eb;border-radius:12px;padding:14px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
        <div style="font-size:28px;margin-bottom:6px;">{icon}</div>
        <div style="font-size:12px;font-weight:700;color:#111827;">{name}</div>
    </div>""" for icon, name in diseases)

    return f"""<div style="background:linear-gradient(160deg,#f0fdf4 0%,#dcfce7 50%,#f0f9ff 100%);min-height:100vh;padding:40px 20px;">
        <div style="max-width:720px;margin:0 auto;">

            <!-- HERO -->
            <div style="text-align:center;margin-bottom:40px;">
                <div style="font-size:72px;margin-bottom:12px;filter:drop-shadow(0 4px 12px rgba(22,163,74,0.2));">🍅</div>
                <h1 style="color:#111827;font-size:36px;font-weight:900;margin:0 0 8px;letter-spacing:-1px;">{u('app_name',lang)}</h1>
                <p style="color:#16a34a;font-size:16px;font-weight:600;margin:0 0 6px;">{u('tagline',lang)}</p>
                <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:16px;">
                    <span style="background:#dcfce7;color:#15803d;border:1px solid #86efac;padding:5px 14px;border-radius:20px;font-size:12px;font-weight:700;">✅ 95.7% Accuracy</span>
                    <span style="background:#dbeafe;color:#1d4ed8;border:1px solid #93c5fd;padding:5px 14px;border-radius:20px;font-size:12px;font-weight:700;">🌐 6 Languages</span>
                    <span style="background:#fce7f3;color:#be185d;border:1px solid #f9a8d4;padding:5px 14px;border-radius:20px;font-size:12px;font-weight:700;">💊 Pesticide Guide</span>
                    <span style="background:#fef9c3;color:#854d0e;border:1px solid #fde68a;padding:5px 14px;border-radius:20px;font-size:12px;font-weight:700;">🌱 Soil Advice</span>
                </div>
            </div>

            <!-- HOW TO USE -->
            <div style="background:white;border-radius:20px;padding:32px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border:1px solid #e5e7eb;">
                <h2 style="color:#111827;font-size:20px;font-weight:800;margin:0 0 24px;text-align:center;">📖 How to Use</h2>
                <div style="display:flex;flex-direction:column;gap:16px;">
                    <div style="display:flex;gap:16px;align-items:flex-start;">
                        <div style="background:linear-gradient(135deg,#16a34a,#22c55e);color:white;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;flex-shrink:0;">1</div>
                        <div>
                            <div style="font-weight:700;color:#111827;font-size:15px;margin-bottom:4px;">{u('how_step1_title',lang)}</div>
                            <div style="color:#6b7280;font-size:13px;line-height:1.6;">{u('how_step1_desc',lang)}</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:16px;align-items:flex-start;">
                        <div style="background:linear-gradient(135deg,#2563eb,#3b82f6);color:white;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;flex-shrink:0;">2</div>
                        <div>
                            <div style="font-weight:700;color:#111827;font-size:15px;margin-bottom:4px;">{u('how_step2_title',lang)}</div>
                            <div style="color:#6b7280;font-size:13px;line-height:1.6;">{u('how_step2_desc',lang)}</div>
                        </div>
                    </div>
                    <div style="display:flex;gap:16px;align-items:flex-start;">
                        <div style="background:linear-gradient(135deg,#7c3aed,#8b5cf6);color:white;border-radius:50%;width:40px;height:40px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;flex-shrink:0;">3</div>
                        <div>
                            <div style="font-weight:700;color:#111827;font-size:15px;margin-bottom:4px;">{u('how_step3_title',lang)}</div>
                            <div style="color:#6b7280;font-size:13px;line-height:1.6;">{u('how_step3_desc',lang)}</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- DISEASES -->
            <div style="background:white;border-radius:20px;padding:28px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border:1px solid #e5e7eb;">
                <h2 style="color:#111827;font-size:18px;font-weight:800;margin:0 0 16px;text-align:center;">🔬 {u('diseases_detected',lang)}</h2>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">{disease_cards}</div>
            </div>

        </div>
    </div>"""

def predict(image):
    img = image.convert("RGB").resize((224, 224))
    arr = np.expand_dims(np.array(img) / 255.0, 0).astype(np.float32)
    preds = model.predict(arr, verbose=0)[0]
    idx = int(np.argmax(preds))
    return idx_to_class.get(idx, "Unknown"), float(np.max(preds)) * 100

def analyze(image, lang, username):
    if image is None:
        return f"<div style='text-align:center;padding:40px;color:#ef4444;'>❌ {u('result_placeholder',lang)}</div>"
    if not isinstance(image, Image.Image):
        image = Image.fromarray(image)
    lbl_map = LANG_LABELS.get(LANG_MAP.get(lang, lang), LANG_LABELS["English"])
    leaf_ok, leaf_score, _ = is_leaf(image)
    if not leaf_ok:
        return f"""<div style="background:#fef2f2;border:2px solid #fecaca;border-radius:16px;padding:32px;text-align:center;">
            <div style="font-size:56px;margin-bottom:12px;">🚫</div>
            <h2 style="color:#dc2626;margin:0 0 10px;font-size:18px;">⚠️ {u('not_leaf',lang)}</h2>
            <p style="color:#6b7280;font-size:13px;">Score: {leaf_score:.2f}</p>
        </div>"""
    disease, conf = predict(image)
    info = get_disease_info(disease, LANG_MAP.get(lang, lang))
    if username and username in SCAN_HISTORY:
        SCAN_HISTORY[username].append({"disease": disease, "confidence": conf, "time": datetime.datetime.now().strftime("%d %b %H:%M")})
    bar = "#16a34a" if conf >= 85 else "#f59e0b" if conf >= 65 else "#ef4444"
    sev_bg  = "#dcfce7" if disease == "Healthy" else "#fef9c3" if "Moderate" in info["severity"] else "#fee2e2"
    sev_col = "#15803d" if disease == "Healthy" else "#854d0e" if "Moderate" in info["severity"] else "#dc2626"
    symptoms = info.get("symptoms", [])
    symp_html = "".join(f"<li style='margin-bottom:5px;color:#374151;'>{s}</li>" for s in (symptoms if isinstance(symptoms, list) else [symptoms]))
    remedy = info.get("organic_remedy", [])
    rem_html = "".join(f"<li style='margin-bottom:5px;color:#374151;'>{r}</li>" for r in (remedy if isinstance(remedy, list) else [remedy]))
    h1 = u("pest_h_product", lang); h2 = u("pest_h_brand", lang)
    h3 = u("pest_h_dose", lang);    h4 = u("pest_h_price", lang); h5 = u("pest_h_when", lang)
    pest_html = ""
    if info.get("pesticides"):
        rows = "".join(f"""<tr style="border-bottom:1px solid #f3f4f6;">
            <td style="padding:10px;font-weight:600;color:#111827;font-size:13px;">{p['name']}</td>
            <td style="padding:10px;color:#6b7280;font-size:13px;">{p['brand']}</td>
            <td style="padding:10px;color:#374151;font-size:13px;">{p['dose']}</td>
            <td style="padding:10px;color:#16a34a;font-weight:700;font-size:13px;">{p['price_range']}</td>
            <td style="padding:10px;color:#6b7280;font-size:12px;">{p['when']}</td>
        </tr>""" for p in info["pesticides"])
        pest_html = f"""<div style="margin-top:14px;">
            <h3 style="color:#7c3aed;font-size:14px;font-weight:700;margin:0 0 8px;">💊 {u('pesticide_lbl',lang)}</h3>
            <div style="border:1px solid #ede9fe;border-radius:12px;overflow:hidden;overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;min-width:480px;">
                <thead><tr style="background:#f5f3ff;">
                    <th style="padding:10px;text-align:left;color:#7c3aed;font-size:12px;font-weight:700;">{h1}</th>
                    <th style="padding:10px;text-align:left;color:#7c3aed;font-size:12px;font-weight:700;">{h2}</th>
                    <th style="padding:10px;text-align:left;color:#7c3aed;font-size:12px;font-weight:700;">{h3}</th>
                    <th style="padding:10px;text-align:left;color:#7c3aed;font-size:12px;font-weight:700;">{h4}</th>
                    <th style="padding:10px;text-align:left;color:#7c3aed;font-size:12px;font-weight:700;">{h5}</th>
                </tr></thead><tbody>{rows}</tbody>
            </table></div></div>"""
    shop_q = urllib.parse.quote("agricultural pesticide shop near me")
    soil_html = get_soil_html(disease, lang)
    return f"""<div style="background:white;border:1px solid #e5e7eb;border-radius:20px;padding:24px;box-shadow:0 4px 24px rgba(0,0,0,0.06);">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;padding-bottom:18px;border-bottom:1px solid #f3f4f6;">
            <span style="font-size:48px;">{info['icon']}</span>
            <div>
                <h2 style="margin:0 0 6px;color:#111827;font-size:22px;font-weight:800;">{info['name']}</h2>
                <span style="background:{sev_bg};color:{sev_col};padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;">⚡ {info['severity']}</span>
            </div>
        </div>
        <div style="margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                <span style="color:#6b7280;font-size:12px;font-weight:600;text-transform:uppercase;">{u('confidence',lang)}</span>
                <span style="color:{bar};font-weight:700;font-size:13px;">{conf:.1f}%</span>
            </div>
            <div style="background:#f3f4f6;border-radius:8px;height:8px;">
                <div style="background:{bar};width:{min(conf,100):.0f}%;height:100%;border-radius:8px;"></div>
            </div>
        </div>
        <div style="background:#f8fafc;border-radius:12px;padding:14px;margin-bottom:12px;border:1px solid #e2e8f0;">
            <h3 style="margin:0 0 6px;color:#0369a1;font-size:13px;font-weight:700;text-transform:uppercase;">📋 {u('description',lang)}</h3>
            <p style="margin:0;color:#374151;line-height:1.7;font-size:13px;">{info['description']}</p>
        </div>
        <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:12px;padding:14px;margin-bottom:12px;">
            <h3 style="margin:0 0 6px;color:#c2410c;font-size:13px;font-weight:700;text-transform:uppercase;">🔍 {u('symptoms',lang)}</h3>
            <ul style="margin:0;padding-left:18px;font-size:13px;line-height:1.8;">{symp_html}</ul>
        </div>
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px;margin-bottom:12px;">
            <h3 style="margin:0 0 6px;color:#15803d;font-size:13px;font-weight:700;text-transform:uppercase;">🌿 {u('remedy',lang)}</h3>
            <ul style="margin:0;padding-left:18px;font-size:13px;line-height:1.8;">{rem_html}</ul>
        </div>
        {pest_html}
        {soil_html}
        <div style="margin-top:14px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:14px;display:flex;align-items:center;gap:14px;">
            <span style="font-size:28px;">🏪</span>
            <div style="flex:1;">
                <div style="color:#1e40af;font-weight:700;font-size:13px;">{u('shop_lbl',lang)}</div>
                <div style="color:#93c5fd;font-size:12px;">{u('maps_sub',lang)}</div>
            </div>
            <a href="https://www.google.com/maps/search/{shop_q}" target="_blank" style="background:#2563eb;color:white;padding:9px 16px;border-radius:10px;text-decoration:none;font-weight:700;font-size:13px;white-space:nowrap;">📍 {u('find_shop',lang)}</a>
        </div>
        <p style="text-align:center;font-size:11px;color:#d1d5db;margin:12px 0 0;">{u('ai_footer',lang)} | Leaf:{leaf_score:.2f} | {u('expert_note',lang)}</p>
    </div>"""

def get_stats_html(username, lang):
    history  = SCAN_HISTORY.get(username, [])
    total    = len(history)
    healthy  = sum(1 for s in history if s["disease"] == "Healthy")
    diseased = total - healthy
    rows = "".join(f"""<tr style="border-bottom:1px solid #f3f4f6;">
        <td style="padding:8px 12px;font-size:13px;color:#374151;">{'🟢' if s['disease']=='Healthy' else '🔴'} {s['disease']}</td>
        <td style="padding:8px 12px;font-size:13px;color:#16a34a;font-weight:700;">{s['confidence']:.1f}%</td>
        <td style="padding:8px 12px;font-size:12px;color:#9ca3af;">{s['time']}</td>
    </tr>""" for s in reversed(history[-5:]))
    recent = f"""<div style="margin-top:12px;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;">
        <div style="background:#f9fafb;padding:10px 14px;border-bottom:1px solid #e5e7eb;">
            <span style="color:#374151;font-size:13px;font-weight:700;">🕐 {u('recent_scans',lang)}</span>
        </div>
        <table style="width:100%;border-collapse:collapse;">
            <tbody>{rows if rows else f'<tr><td colspan="3" style="padding:16px;text-align:center;color:#d1d5db;font-size:13px;">{u("no_scans",lang)}</td></tr>'}</tbody>
        </table>
    </div>""" if total > 0 else f'<div style="padding:16px;text-align:center;color:#d1d5db;font-size:13px;">{u("no_scans",lang)}</div>'
    return f"""<div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:4px;">
            <div style="background:linear-gradient(135deg,#dcfce7,#bbf7d0);border-radius:12px;padding:14px;text-align:center;border:1px solid #86efac;">
                <div style="font-size:26px;font-weight:800;color:#15803d;">{total}</div>
                <div style="font-size:10px;color:#166534;font-weight:600;margin-top:2px;">{u('total_scans',lang)}</div>
            </div>
            <div style="background:linear-gradient(135deg,#dbeafe,#bfdbfe);border-radius:12px;padding:14px;text-align:center;border:1px solid #93c5fd;">
                <div style="font-size:26px;font-weight:800;color:#1d4ed8;">{healthy}</div>
                <div style="font-size:10px;color:#1e40af;font-weight:600;margin-top:2px;">{u('healthy_lbl',lang)}</div>
            </div>
            <div style="background:linear-gradient(135deg,#fee2e2,#fecaca);border-radius:12px;padding:14px;text-align:center;border:1px solid #fca5a5;">
                <div style="font-size:26px;font-weight:800;color:#dc2626;">{diseased}</div>
                <div style="font-size:10px;color:#b91c1c;font-weight:600;margin-top:2px;">{u('disease_lbl',lang)}</div>
            </div>
        </div>
        {recent}
    </div>"""

CSS = """
* { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important; box-sizing: border-box; }
.gradio-container { background: #f8fafc !important; max-width:100% !important; padding:0 !important; }
footer { display:none !important; }
.gr-button-primary { background: linear-gradient(135deg,#16a34a,#22c55e) !important; border:none !important; border-radius:12px !important; font-weight:700 !important; font-size:15px !important; color:white !important; box-shadow:0 4px 12px rgba(22,163,74,0.3) !important; }
.gr-button-secondary { background:white !important; border:1.5px solid #e5e7eb !important; color:#374151 !important; border-radius:10px !important; font-weight:600 !important; }
input, textarea { background:white !important; border:1.5px solid #e5e7eb !important; color:#111827 !important; border-radius:10px !important; }
label span { color:#374151 !important; font-size:13px !important; font-weight:600 !important; }
.tab-nav button { color:#9ca3af !important; font-weight:600 !important; }
.tab-nav button.selected { color:#16a34a !important; border-bottom:2px solid #16a34a !important; }
"""

with gr.Blocks(title="TomatoAI", css=CSS, theme=gr.themes.Base()) as demo:
    cur_user = gr.State("")
    cur_lang = gr.State("English")

    # SCREEN 1: LANGUAGE
    with gr.Group(visible=True) as lang_screen:
        gr.HTML("""<div style="min-height:100vh;background:linear-gradient(160deg,#f0fdf4 0%,#dcfce7 50%,#f0f9ff 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;">
            <div style="background:white;border-radius:28px;padding:48px 40px;max-width:480px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,0.08);text-align:center;border:1px solid #dcfce7;">
                <div style="font-size:72px;margin-bottom:12px;">🍅</div>
                <h1 style="color:#111827;font-size:34px;font-weight:900;margin:0 0 6px;letter-spacing:-1px;">TomatoAI</h1>
                <p style="color:#16a34a;font-size:14px;font-weight:600;margin:0 0 28px;">AI-Powered Tomato Leaf Disease Detection</p>
            </div>
        </div>""")
        with gr.Column(scale=1, min_width=360):
            lang_dd  = gr.Dropdown(choices=LANGUAGES, value="English", label="Select Language / भाषा / భాష")
            lang_btn = gr.Button("Continue", variant="primary", size="lg")

    # SCREEN 2: HOW TO USE
    with gr.Group(visible=False) as how_screen:
        how_html = gr.HTML("")
        how_next_btn = gr.Button("Get Started", variant="primary", size="lg")

    # SCREEN 3: AUTH
    with gr.Group(visible=False) as auth_screen:
        auth_header = gr.HTML("")
        with gr.Tabs():
            with gr.TabItem("Login"):
                lu = gr.Textbox(label="Username", placeholder="Enter username")
                lp = gr.Textbox(label="Password", type="password", placeholder="Enter password")
                lb = gr.Button("Login", variant="primary", size="lg")
                lm = gr.HTML("")
            with gr.TabItem("Sign Up"):
                su = gr.Textbox(label="Username", placeholder="Choose a username")
                sp = gr.Textbox(label="Password", type="password", placeholder="Min 4 characters")
                sb = gr.Button("Create Account", variant="primary", size="lg")
                sm = gr.HTML("")

    # SCREEN 4: DASHBOARD
    with gr.Group(visible=False) as main_screen:
        hdr_html = gr.HTML("")
        with gr.Row(equal_height=False):
            with gr.Column(scale=1, min_width=300):
                stats_html = gr.HTML("")
                gr.HTML("<div style='height:10px;'></div>")
                with gr.Tabs():
                    with gr.TabItem("Upload"):
                        up_img = gr.Image(type="pil", label="Upload Tomato Leaf", source="upload", height=220)
                        up_btn = gr.Button("Analyze Leaf", variant="primary", size="lg")
                    with gr.TabItem("Webcam"):
                        wc_img = gr.Image(type="pil", label="Webcam", source="webcam", height=220)
                        wc_btn = gr.Button("Capture & Analyze", variant="primary", size="lg")
                logout_btn = gr.Button("Logout", variant="secondary", size="sm")
            with gr.Column(scale=2):
                result_html = gr.HTML("""<div style="min-height:480px;background:white;border:2px dashed #e5e7eb;border-radius:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.03);">
                    <div style="font-size:56px;margin-bottom:12px;">🍃</div>
                    <p style="color:#9ca3af;font-size:15px;font-weight:500;text-align:center;margin:0;">Upload a leaf to detect disease</p>
                </div>""")

    # HANDLERS
    def do_lang(lang):
        how = make_how_to_html(lang)
        return gr.update(visible=False), gr.update(visible=True), how, lang

    def do_how_next(lang):
        hdr = f"""<div style="background:linear-gradient(160deg,#f0fdf4,#dcfce7);padding:32px 20px 20px;text-align:center;">
            <div style="font-size:44px;margin-bottom:8px;">🍅</div>
            <h1 style="color:#111827;font-size:22px;font-weight:800;margin:0 0 4px;">TomatoAI</h1>
            <p style="color:#16a34a;font-size:13px;font-weight:600;margin:0;">{u('tagline',lang)}</p>
        </div>"""
        return gr.update(visible=False), gr.update(visible=True), hdr

    def do_login(user, pw, lang):
        if not user or not pw:
            return "", gr.update(visible=True), gr.update(visible=False), "<p style='color:#ef4444;font-size:13px;padding:6px;'>Fill all fields.</p>", "", ""
        if user not in USERS:
            return "", gr.update(visible=True), gr.update(visible=False), "<p style='color:#ef4444;font-size:13px;padding:6px;'>User not found. Please Sign Up first.</p>", "", ""
        if USERS[user] != hash_pw(pw):
            return "", gr.update(visible=True), gr.update(visible=False), "<p style='color:#ef4444;font-size:13px;padding:6px;'>Wrong password.</p>", "", ""
        hdr = f"""<div style="background:white;border-bottom:1px solid #e5e7eb;padding:12px 24px;display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:26px;">🍅</span>
                <span style="color:#111827;font-weight:800;font-size:17px;">TomatoAI</span>
                <span style="background:#dcfce7;color:#15803d;font-size:10px;padding:2px 8px;border-radius:20px;font-weight:700;border:1px solid #86efac;">LIVE</span>
            </div>
            <div style="color:#6b7280;font-size:13px;">{u('welcome',lang)}, <span style="color:#16a34a;font-weight:700;">{user}</span> 👨‍🌾</div>
        </div>"""
        stats = get_stats_html(user, lang)
        return user, gr.update(visible=False), gr.update(visible=True), "", hdr, stats

    def do_signup(user, pw):
        if not user or not pw: return "<p style='color:#ef4444;font-size:13px;'>Fill all fields.</p>"
        if len(pw) < 4: return "<p style='color:#ef4444;font-size:13px;'>Password must be 4+ characters.</p>"
        if user in USERS: return "<p style='color:#ef4444;font-size:13px;'>Username taken.</p>"
        USERS[user] = hash_pw(pw)
        SCAN_HISTORY[user] = []
        return "<p style='color:#16a34a;font-size:13px;background:#f0fdf4;padding:8px;border-radius:8px;border:1px solid #bbf7d0;'>Account created! Go to Login tab.</p>"

    def do_logout():
        return gr.update(visible=True), gr.update(visible=False), ""

    def do_analyze(img, lang, user):
        res   = analyze(img, lang, user)
        stats = get_stats_html(user, lang)
        return res, stats

    lang_btn.click(do_lang, [lang_dd], [lang_screen, how_screen, how_html, cur_lang])
    how_next_btn.click(do_how_next, [cur_lang], [how_screen, auth_screen, auth_header])
    lb.click(do_login, [lu, lp, cur_lang], [cur_user, auth_screen, main_screen, lm, hdr_html, stats_html])
    sb.click(do_signup, [su, sp], [sm])
    logout_btn.click(do_logout, [], [auth_screen, main_screen, cur_user])
    up_btn.click(do_analyze, [up_img, cur_lang, cur_user], [result_html, stats_html])
    wc_btn.click(do_analyze, [wc_img, cur_lang, cur_user], [result_html, stats_html])

if __name__ == "__main__":
    print("\nTomatoAI starting at http://localhost:7860\n")
    demo.launch(server_name="0.0.0.0", server_port=7860, inbrowser=True, share=False)
