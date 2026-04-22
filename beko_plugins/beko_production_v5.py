# السطر 53 - استبدل:
resp.choices[0].message.content[:40]
# بـ:
content = getattr(resp.choices[0].message, "content", "")
groq_msg = content[:40] + "..." if content else "No response"
