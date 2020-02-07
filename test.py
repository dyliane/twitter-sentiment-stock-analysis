from google.cloud import translate_v2 as translate

client = translate.Client.from_service_account_json('credential.json')

print(client.translate("Olá, sou um text", target_language="en")['translatedText'])