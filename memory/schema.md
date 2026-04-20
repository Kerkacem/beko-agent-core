# Memory Schema

## Item Structure

كل عنصر memory يكون شكل JSON:

```json
{
  "id": "unique_id",
  "type": "fact | note | skill | plugin",
  "content": "النص الرئيسي أو الوصف",
  "facts": ["حقيقة 1", "حقيقة 2"],
  "notes": "ملاحظات إضافية",
  "tags": ["tag1", "tag2", "skill:python"],
  "source": "session_id أو goal_name أو file_path",
  "created_at": "2026-04-20T14:00:00+01:00",
  "skills": ["مهارة 1", "مهارة 2"],
  "skill_creator": "اسم المحرك أو session",
  "plugins": ["plugin_name"]
}
```

## أمثلة

### Fact
```json
{
  "id": "fact_001",
  "type": "fact",
  "content": "pytest مثبت ويعمل مع 15 test ناجح",
  "facts": ["pytest 9.0.3", "15 tests passed"],
  "tags": ["pytest", "tests"],
  "source": "session_2026-04-20_14:00",
  "created_at": "2026-04-20T14:00:00+01:00"
}
```

### Skill
```json
{
  "id": "skill_001",
  "type": "skill",
  "content": "كتابة اختبارات pytest بسيطة",
  "skills": ["pytest", "unit-testing"],
  "skill_creator": "BEKO Agent v1.0",
  "tags": ["skill", "testing"],
  "source": "phase2_tests",
  "created_at": "2026-04-20T14:30:00+01:00"
}
```