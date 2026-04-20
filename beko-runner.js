const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

// مجلد واحد مسموح للعب داخله: D:/beko-agent-core
const ALLOWED_BASE_DIR = 'D:/beko-agent-core';

// قائمة الأوامر المسموحة لـ run_command فقط
const ALLOWED_COMMANDS = ['python', 'pytest', 'node', 'npm', 'git'];

// دالة تتأكد أن أي مسار داخل هذا المجلد فقط
function resolveSafePath(p) {
  const normalized = path.normalize(p).replace(/\\/g, '/');
  const full = path.resolve(normalized);
  const baseNorm = path.resolve(ALLOWED_BASE_DIR.replace(/\\/g, '/'));
  if (!full.startsWith(baseNorm)) {
    throw new Error('Path not allowed: ' + full);
  }
  return full;
}

const app = express();
app.use(cors());
app.use(express.json({ limit: '2mb' }));

// endpoint رئيسي: يستقبل steps وينفذها
app.post('/execute', async (req, res) => {
  const steps = req.body?.steps || [];
  const results = [];

  for (const [i, step] of steps.entries()) {
    const { action } = step;
    try {
      if (action === 'read_file') {
        const safePath = resolveSafePath(step.path);
        try {
          const content = fs.readFileSync(safePath, 'utf8');
          results.push({ index: i, ok: true, action, path: safePath, content });
        } catch (err) {
          if (err.code === 'ENOENT') {
            // الملف غير موجود: نرجّع ok مع محتوى فارغ بدل Error
            results.push({ index: i, ok: true, action, path: safePath, content: '' });
          } else {
            results.push({ index: i, ok: false, error: err.message });
          }
        }
      } else if (action === 'write_file') {
        const safePath = resolveSafePath(step.path);

        // نتأكد أن المجلد الأب موجود، وإن لم يكن موجوداً ننشئه
        const dir = path.dirname(safePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true }); // علاج ENOENT قبل الكتابة[web:175][web:176]
        }

        fs.writeFileSync(safePath, step.content ?? '', 'utf8');
        results.push({ index: i, ok: true, action, path: safePath });
      } else if (action === 'run_command') {
        const command = String(step.command || '').trim();
        const args = Array.isArray(step.args)
          ? step.args.map(a => String(a))
          : [];

        if (!ALLOWED_COMMANDS.includes(command)) {
          results.push({
            index: i,
            ok: false,
            action,
            error: `Command not allowed: ${command}`,
          });
          continue;
        }

        // نجبر الـ cwd أن يكون داخل الـ sandbox فقط
        const cwd = ALLOWED_BASE_DIR;

        const proc = spawnSync(command, args, {
          cwd,
          encoding: 'utf8',
          shell: false,
        });

        const stdout = proc.stdout || '';
        const stderr = proc.stderr || '';
        const exitCode = proc.status;

        results.push({
          index: i,
          ok: exitCode === 0,
          action,
          command,
          args,
          cwd,
          exitCode,
          stdout,
          stderr,
        });
      } else {
        results.push({ index: i, ok: false, error: 'Unsupported action: ' + action });
      }
    } catch (e) {
      results.push({ index: i, ok: false, error: e.message });
    }
  }

  res.json({ ok: true, results });
});

const PORT = 8002;
app.listen(PORT, () => {
  console.log('beko-runner listening on port ' + PORT);
});