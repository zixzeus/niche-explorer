import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest) {
  try {
    const { topic } = await req.json();

    if (!topic) {
      return NextResponse.json({ error: 'Topic is required' }, { status: 400 });
    }

    // Path to the Python executable - uses env var for Docker compatibility
    const pythonPath = process.env.PYTHON_PATH || '/Users/ericzeus/anaconda3/envs/dev_agent/bin/python';
    // Path to our JSON-ready entry point
    const scriptPath = path.join(process.cwd(), '..', 'run_json.py');

    return new Promise((resolve) => {
      console.log(`Executing Python agent for topic: ${topic}`);
      const child = spawn(pythonPath, [scriptPath, topic], {
        cwd: path.join(process.cwd(), '..'),
      });

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        if (code !== 0) {
          console.error(`Python script failed with code ${code}`);
          console.error(`Stderr: ${stderr}`);
          resolve(NextResponse.json({ error: 'Agent execution failed', details: stderr }, { status: 500 }));
          return;
        }

        try {
          // Find the last line that is valid JSON (in case there are warnings/logs)
          const lines = stdout.trim().split('\n');
          const lastLine = lines[lines.length - 1];
          const data = JSON.parse(lastLine);
          resolve(NextResponse.json({ status: 'success', data }));
        } catch (e) {
          console.error('Failed to parse Python output as JSON');
          console.error('Raw Output:', stdout);
          resolve(NextResponse.json({ error: 'Failed to process agent results' }, { status: 500 }));
        }
      });
    });
  } catch (error) {
    console.error('API Route Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
