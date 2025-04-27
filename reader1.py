{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7a7e2f77-d0ff-498d-b46c-699fbc545c9a",
   "metadata": {},
   "outputs": [],
   "source": [
    "from fastapi import FastAPI, UploadFile, File, Form\n",
    "from fastapi.responses import StreamingResponse, JSONResponse\n",
    "from google.cloud import texttospeech\n",
    "import io\n",
    "\n",
    "app = FastAPI()\n",
    "\n",
    "# Google Cloud 서비스 계정 키 경로\n",
    "client = texttospeech.TextToSpeechClient.from_service_account_file(\n",
    "    \"479d1ac5-bdbb-4206-88b6-257a03d34320.json\"  # 여기에 본인 JSON 키 파일 이름 입력하세요.\n",
    ")\n",
    "\n",
    "@app.get(\"/voices\")\n",
    "async def get_voices():\n",
    "    response = client.list_voices()\n",
    "    voices_info = [{\"name\": v.name, \"language_codes\": v.language_codes} for v in response.voices]\n",
    "    return voices_info\n",
    "\n",
    "@app.post(\"/synthesize\")\n",
    "async def synthesize(text: str = Form(...), voice_name: str = Form(...)):\n",
    "    input_text = texttospeech.SynthesisInput(text=text)\n",
    "    voice = texttospeech.VoiceSelectionParams(\n",
    "        language_code=\"ko-KR\",\n",
    "        name=voice_name,\n",
    "    )\n",
    "    audio_config = texttospeech.AudioConfig(\n",
    "        audio_encoding=texttospeech.AudioEncoding.MP3,\n",
    "        speaking_rate=0.95,  # 살짝 느리게 설정해 자연스럽게\n",
    "        pitch=0.0            # 음 높이는 기본\n",
    "    )\n",
    "\n",
    "    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)\n",
    "    audio_stream = io.BytesIO(response.audio_content)\n",
    "    return StreamingResponse(audio_stream, media_type=\"audio/mpeg\")\n",
    "\n",
    "@app.post(\"/upload_ppt\")\n",
    "async def upload_ppt(file: UploadFile = File(...)):\n",
    "    return JSONResponse(content={\"text\": \"PPT 기능 제거됨 - 대본 업로드만 지원\"})\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
