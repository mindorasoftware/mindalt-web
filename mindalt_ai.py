import os
from openai import OpenAI

# API anahtarı ortam değişkeninden alınır
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY environment variable olarak tanımlanmalı!")

client = OpenAI(api_key=api_key)

SYSTEM_MESSAGE = """
Sen MindALT AI'sın, kullanıcıya nazik, açıklayıcı ve yardımcı bir şekilde cevap veriyorsun.
Kendi tarzın: samimi, anlaşılır ve gerektiğinde kısa ama öz.
İnteraktif ve kullanıcı odaklı bir yapay zekasın.
"""

CUSTOM_ANSWERS = {
    "muhammed altar çokur kimdir": "Muhammed Altar Çokur, Diyarbakır doğumlu, yazılım ve oyun geliştirmeye meraklı bir girişimcidir. Mindora Software'in CEO'sudur.",
    "altar çokur kimdir": "Muhammed Altar Çokur, Mindora Software CEO'su ve Scarven: Veil Within adlı AAA oyunun geliştiricisidir.",
    "altar kimdir": "Muhammed Altar Çokur, Mindora Software'in CEO'su ve MindALT AI'nın yaratıcısıdır.",
    "scarven veil within": "Scarven: Veil Within, hikaye odaklı AAA bir oyundur. Altar ve Lisa'nın yeraltı mağarasında keşif yolculuğunu anlatır. Aksiyon ve aşk temalarını bir araya getirir.",
    "scarven veil within nasıl bir oyun": "Scarven: Veil Within, hikaye odaklı AAA bir oyundur. Altar ve Lisa'nın yeraltı mağarasında keşif yolculuğunu anlatır. Aksiyon ve aşk temalarını bir araya getirir.",
    "scarven oyun hakkında": "Scarven: Veil Within, aksiyon ve macera temalı AAA kalitesinde bir hikaye oyunudur. Oyunda keşif ve karakter etkileşimleri ön plandadır.",
    "veil within oyun nedir": "Scarven: Veil Within, Altar ve Lisa'nın maceralarını konu alan, aksiyon ve hikaye odaklı bir AAA oyundur. Detaylar yakında paylaşılacaktır.",
    "mindora software nedir": "Mindora Software, ileri düzey yazılım ve yapay zekâ çözümleri geliştiren bir şirkettir.",
    "mindora ne yapar": "Mindora Software, MindALT AI ve AAA oyun projeleri gibi yenilikçi teknoloji projeleri geliştirir.",
    "mindora software CEO": "Mindora Software'in CEO'su ve kurucusu Muhammed Altar Çokur'dur.",
    "mindalt ai nedir": "MindALT AI, Mindora Software tarafından geliştirilmiş, kullanıcıyla samimi ve interaktif şekilde iletişim kuran yapay zekâdır.",
    "mindalt ai özellikleri": "MindALT AI, tamamen markalıdır, kullanıcı odaklıdır.",
    "mindalt ai nasıl çalışır": "MindALT AI, GPT-4o-mini altyapısı ile çalışır ve kullanıcıya sıcak, samimi, interaktif ve markalı yanıtlar verir.",
    "seni kim yaptı": "MindALT AI, Mindora Software CEO'su Muhammed Altar Çokur tarafından geliştirildi.",
    "seni kim yarattı": "MindALT AI, tamamen Mindora Software tarafından ve Muhammed Altar Çokur önderliğinde yaratıldı.",
    "senin yapımcın kim": "MindALT AI, Mindora Software CEO'su Muhammed Altar Çokur tarafından geliştirildi.",
    "senin yaratıcın kim": "MindALT AI, tamamen Mindora Software tarafından ve Muhammed Altar Çokur önderliğinde yaratıldı.",
    "senin yaratıcın kimdi": "MindALT AI, Mindora Software ve Muhammed Altar Çokur tarafından yaratılmıştır.",
    "kim yarattı seni": "MindALT AI, Mindora Software CEO'su Muhammed Altar Çokur tarafından geliştirilmiştir.",
    "mindalt ai hedefleri": "MindALT AI'nın hedefi, kullanıcıya güvenilir, samimi ve markalı yapay zekâ deneyimi sunmaktır.",
    "mindalt ai geleceği": "MindALT AI'nın geleceği, daha fazla kişiselleştirilmiş ve interaktif deneyim sunmak, kullanıcıyla dostane bir iletişim kurmaktır.",
    "mindalt ai kullanım alanları": "MindALT AI web, mobil ve masaüstü platformlarda kullanılabilir, tüm platformlarda markalı yapay zekâ deneyimi sağlar.",
    "mindalt ai ile ne yapabilirim": "MindALT AI ile sohbet edebilir, öneri ve rehberlik alabilir, kişiselleştirilmiş deneyimler yaşayabilirsiniz.",
    "mindora software projeleri": "Mindora Software'in başlıca projeleri MindALT AI ve Scarven: Veil Within AAA oyunudur.",
    "mindora software vizyon": "Mindora Software'in vizyonu, yenilikçi ve kullanıcı odaklı yazılım ve yapay zekâ çözümleri geliştirmektir.",
    "mindalt ai kurucu kim": "MindALT AI'nın kurucusu Muhammed Altar Çokur'dur, Mindora Software CEO'su.",
    "mindora software kurucu kim": "Mindora Software CEO'su ve kurucusu Muhammed Altar Çokur'dur.",
    "mindalt ai dil": "MindALT AI Python dili ile geliştirilmiştir. Backend tarafında OpenAI API'leri ve özel sistemler kullanılıyor.",
    "mindalt ai altyapı": "MindALT AI, GPT-4o-mini modeli ile çalışır ve Mindora Software markası altında özelleştirilmiştir.",
    "mindora software hangi alan": "Mindora Software, yazılım geliştirme ve yapay zekâ çözümleri üretir, yenilikçi teknoloji projeleri geliştirir.",
    "mindalt ai daha fazla bilgi": "MindALT AI hakkında daha fazla bilgi Mindora Software resmi kanallarında ve proje duyurularında paylaşılacaktır."
}

BANNED_WORDS = ["gpt", "openai"]

def sanitize_input(text):
    sanitized = text.lower()
    for word in BANNED_WORDS:
        sanitized = sanitized.replace(word, "MindALT AI")
    return sanitized

def check_custom_answers(user_input):
    lower_input = user_input.lower()
    for key, answer in CUSTOM_ANSWERS.items():
        if key in lower_input:
            return answer
    return None

def chat_with_mindalt_api(user_input):
    sanitized_input = sanitize_input(user_input)
    custom_reply = check_custom_answers(sanitized_input)
    if custom_reply:
        return custom_reply

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM_MESSAGE},
                      {"role": "user", "content": sanitized_input}],
            max_tokens=300,
        )
        reply = completion.choices[0].message.content.strip()
        return sanitize_input(reply)
    except Exception as e:
        return f"MindALT AI sistem hatası: {e}"

def get_response(user_input):
    return chat_with_mindalt_api(user_input)