from pydantic import BaseModel, Field
from typing import Literal


class ListeningExerciseSchema(BaseModel):
    speaker_one: str = Field(..., description="Nama pembicara pertama, misalnya: 'Joe'")
    speaker_two: str = Field(..., description="Nama pembicara kedua, misalnya: 'Jane'")
    script: str = Field(
        ...,
        description="Dialog yang dibicarakan oleh TTS (Text-to-speech), format: 'Joe: ... \\nJane: ... ' bergantian",
    )
    questions: list[str] = Field(
        ...,
        description="Daftar pertanyaan untuk menguji pemahaman peserta berdasarkan 'script'",
    )


class EvaluateUserIntentionSchema(BaseModel):
    skill_types: Literal["reading", "speaking", "listening", "writing"] = Field(
        ..., description="pilihan salah satu skill_types yang dibutuhkan peserta"
    )


class EvaluateSpeakingSchema(BaseModel):
    correction: str = Field(
        ..., description="catatan perbaikan pelafalan (pronunciation), fokus pada 1-2 hal utama saja"
    )
    score: str = Field(
        ..., description="nilai pelafalan dalam rentang 0-100 (berupa string, mis. '80')"
    )
    summary: str = Field(
        ..., description="gabungan dari correction dan score, ditulis memotivasi, menyisipkan emoji, dan memberi panduan perbaikan yang praktis"
    )


class LearningSkillTypesSchema(BaseModel):  # item latihan yang dilakukan peserta
    category: str = Field(
        ..., description="salah satu catefory skill_types: reading, speaking, listening, writing"
    )
    title: str = Field(..., description="judul latihan")
    feedback: str = Field(
        ..., description="penilaian objective dengan metode sandwich feedback"
    )
    score: int = Field(..., description="nilai kemampuan dalam rentang 1-10")


class LearningReportSchema(BaseModel):  # Laporan belajar
    start_date: str = Field(..., description="tanggal mulai belajar")
    end_date: str = Field(..., description="tanggal akhir belajar")
    username: str = Field(..., description="username dari peserta")
    global_score: str = Field(..., description="nilai keseluruhan")
    skill_types: list[LearningSkillTypesSchema]  # list of LearningSkillTypesSchema
    markdown_content: str = Field(
        ..., description="seluruh isi laporan dalam format markdown"
    )