import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(req: NextRequest) {
  try {
    const { topic, userProfile } = await req.json();

    if (!topic) {
      return NextResponse.json({ error: 'Topic is required' }, { status: 400 });
    }

    const pythonPath = process.env.PYTHON_PATH || '/usr/bin/python3';
    const scriptPath = path.join(process.cwd(), '..', 'run_json.py');
    const profile = userProfile || 'Experienced software developer.';

    // Wrap the spawn logic in a typed async function
    const executeAgent = (): Promise<NextResponse> => {
      return new Promise((resolve) => {
        console.log(`Executing Python agent for topic: ${topic}, Profile: ${profile}`);
        const child = spawn(pythonPath, [scriptPath, topic, profile], {
          cwd: path.join(process.cwd(), '..'),
        });

        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (data) => { 
          const chunk = data.toString();
          stdout += chunk;
          console.log(`[Python Stdout]: ${chunk}`);
        });
        child.stderr.on('data', (data) => { 
          const chunk = data.toString();
          stderr += chunk;
          console.error(`[Python Stderr]: ${chunk}`);
        });

        child.on('close', (code) => {
          console.log(`Python agent finished with code ${code}`);
          if (code !== 0) {
            console.error(`Python script failed with code ${code}. Final Stderr: ${stderr}`);
            resolve(NextResponse.json({ error: 'Agent execution failed', details: stderr }, { status: 500 }));
            return;
          }

          try {
            const lines = stdout.trim().split('\n');
            const lastLine = lines[lines.length - 1];
            const data = JSON.parse(lastLine);
            resolve(NextResponse.json({ status: 'success', data }));
          } catch (e) {
            console.error('Failed to parse Python output as JSON', stdout);
            resolve(NextResponse.json({ error: 'Failed to process agent results' }, { status: 500 }));
          }
        });
      });
    };

    return await executeAgent();
  } catch (error) {
    console.error('API Route Error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
