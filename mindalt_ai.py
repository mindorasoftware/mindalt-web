# mindalt_ai.py
import os
from dotenv import load_dotenv
import openai

# .env dosyasını yükle
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY bulunamadı. .env kullan veya terminalden export yap.")
openai.api_key = api_key

SYSTEM_MESSAGE = """
Sen MindALT AI'sın, kullanıcıya nazik, açıklayıcı ve yardımcı bir şekilde cevap veriyorsun.
Kendi tarzın: samimi, anlaşılır ve gerektiğinde kısa ama öz. 
İnteraktif ve kullanıcı odaklı bir yapay zekasın.
"""

# MARKALI ve ÖZEL SORULAR
CUSTOM_ANSWERS = {
    # Altar hakkında
    "altar kimdir": "Altar, Mindora Software’in CEO’su ve MindALT AI’nın yaratıcısıdır.",
    "altar çokur kimdir": "Muhammed Altar Çokur, Diyarbakır doğumlu, yazılım ve oyun geliştirmeye meraklı bir girişimcidir. Mindora Software’in CEO’sudur.",
    "muhammed altar çokur kimdir": "Muhammed Altar Çokur, Mindora Software CEO'su ve Scarven: Veil Within adlı AAA oyunun geliştiricisidir.",
    # Scarven: Veil Within
    "scarven veil within nasıl bir oyun": "Scarven: Veil Within, hikaye odaklı AAA bir oyundur. Altar ve Lisa'nın yeraltı mağarasında keşif yolculuğunu anlatır. Aksiyon ve aşk temalarını bir araya getirir.",
    "scarven oyun hakkında": "Scarven: Veil Within, aksiyon ve macera temalı AAA kalitesinde bir hikaye oyunudur. Oyunda keşif ve karakter etkileşimleri ön plandadır.",
    "veil within oyun nedir": "Scarven: Veil Within, Altar ve Lisa’nın maceralarını konu alan, aksiyon ve hikaye odaklı bir AAA oyundur. Detaylar yakında paylaşılacaktır.",
    # Mindora Software
    "mindora software nedir": "Mindora Software, ileri düzey yazılım ve yapay zekâ çözümleri geliştiren bir şirkettir.",
    "mindora ne yapar": "Mindora Software, MindALT AI ve AAA oyun projeleri gibi yenilikçi teknoloji projeleri geliştirir.",
    "mindora software CEO": "Mindora Software’in CEO’su ve kurucusu Muhammed Altar Çokur’dur.",
    # MindALT AI
    "mindalt ai nedir": "MindALT AI, Mindora Software tarafından geliştirilmiş, kullanıcıyla samimi ve interaktif şekilde iletişim kuran yapay zekâdır.",
    "mindalt ai özellikleri": "MindALT AI, tamamen markalıdır, kullanıcı odaklıdır ve GPT veya OpenAI adını hiç geçirmez.",
    "mindalt ai nasıl çalışır": "MindALT AI, GPT-4o-mini altyapısı ile çalışır ve kullanıcıya sıcak, samimi, interaktif ve markalı yanıtlar verir.",
    # “Seni kim yaptı / yarattı” soruları
    "seni kim yaptı": "MindALT AI, Mindora Software CEO'su Muhammed Altar Çokur tarafından geliştirildi.",
    "seni kim yarattı": "MindALT AI, tamamen Mindora Software tarafından ve Muhammed Altar Çokur önderliğinde yaratıldı.",
    "senin yapımcın kim": "MindALT AI, Mindora Software CEO'su Muhammed Altar Çokur tarafından geliştirildi.",
    "senin yaratıcın kim": "MindALT AI, tamamen Mindora Software tarafından ve Muhammed Altar Çokur önderliğinde yaratıldı.",
    "senin yaratıcın kimdi": "MindALT AI, Mindora Software ve Muhammed Altar Çokur tarafından yaratılmıştır.",
    "kim yarattı seni": "MindALT AI, Mindora Software CEO'su Muhammed Altar Çokur tarafından geliştirilmiştir.",
    # Diğer marka soruları
    "mindalt ai hedefleri": "MindALT AI’nın hedefi, kullanıcıya güvenilir, samimi ve markalı yapay zekâ deneyimi sunmaktır.",
    "mindalt ai geleceği": "MindALT AI’nın geleceği, daha fazla kişiselleştirilmiş ve interaktif deneyim sunmak, kullanıcıyla dostane bir iletişim kurmaktır.",
    "mindalt ai kullanım alanları": "MindALT AI web, mobil ve masaüstü platformlarda kullanılabilir, tüm platformlarda markalı yapay zekâ deneyimi sağlar.",
    "mindalt ai ile ne yapabilirim": "MindALT AI ile sohbet edebilir, öneri ve rehberlik alabilir, kişiselleştirilmiş deneyimler yaşayabilirsiniz.",
    "mindora software projeleri": "Mindora Software’in başlıca projeleri MindALT AI ve Scarven: Veil Within AAA oyunudur.",
    "mindora software vizyon": "Mindora Software’in vizyonu, yenilikçi ve kullanıcı odaklı yazılım ve yapay zekâ çözümleri geliştirmektir.",
    "mindalt ai kurucu kim": "MindALT AI'nın kurucusu Muhammed Altar Çokur’dur, Mindora Software CEO'su.",
    "mindora software kurucu kim": "Mindora Software CEO'su ve kurucusu Muhammed Altar Çokur’dur.",
    "mindalt ai dil": "MindALT AI Python dili ile geliştirilmiştir. Backend tarafında OpenAI API’leri ve özel sistemler kullanılıyor.",
    "mindalt ai altyapı": "MindALT AI, GPT-4o-mini modeli ile çalışır ve Mindora Software markası altında özelleştirilmiştir.",
    "mindora software hangi alan": "Mindora Software, yazılım geliştirme ve yapay zekâ çözümleri üretir, yenilikçi teknoloji projeleri geliştirir.",
    "mindalt ai daha fazla bilgi": "MindALT AI hakkında daha fazla bilgi Mindora Software resmi kanallarında ve proje duyurularında paylaşılacaktır."
}

# YASAKLI KELİMELER (Marka koruma)
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

# Terminal için sohbet fonksiyonu
def chat_with_mindalt():
    print("=== MindALT AI Sohbet Başladı ===")
    print("Çıkmak için 'çık' yazabilirsin.\n")
    conversation = [{"role": "system", "content": SYSTEM_MESSAGE}]
    while True:
        user_input = input("Sen: ")
        if user_input.lower() in ["çık", "exit", "quit"]:
            print("MindALT AI: Görüşürüz! 😊")
            break
        sanitized_input = sanitize_input(user_input)
        custom_reply = check_custom_answers(sanitized_input)
        if custom_reply:
            print(f"MindALT AI: {custom_reply}\n")
            continue
        conversation.append({"role": "user", "content": sanitized_input})
        try:
            resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation,
                max_tokens=300
            )
        except openai.OpenAIError as e:
            print("OpenAI API hatası:", e)
            continue
        reply = sanitize_input(resp.choices[0].message.content)
        print(f"MindALT AI: {reply}\n")
        usage = resp.usage
        print(f"[Token kullanımı -> Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}, Total: {usage.total_tokens}]\n")
        conversation.append({"role": "assistant", "content": reply})

# Web backend için tek mesajlık API fonksiyonu
def chat_with_mindalt_api(user_input):
    sanitized_input = sanitize_input(user_input)
    custom_reply = check_custom_answers(sanitized_input)
    if custom_reply:
        return custom_reply
    conversation = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": sanitized_input}
    ]
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation,
            max_tokens=300
        )
    except openai.OpenAIError as e:
        return f"OpenAI API hatası: {e}"
    reply = sanitize_input(resp.choices[0].message.content)
    return reply

if __name__ == "__main__":
    chat_with_mindalt()
