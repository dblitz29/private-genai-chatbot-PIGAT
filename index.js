const express = require('express');
const { createServer } = require('node:http');
const { join } = require('node:path');
const { Server } = require('socket.io');
const session = require("express-session");
const port = process.env.PORT || 3000;
const app = express();
const server = createServer(app);
const io = new Server(server);
const fetch = require('node-fetch-commonjs'); 
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path')

const knowledgeDir = './knowledge';

if (!fs.existsSync(knowledgeDir)) {
  fs.mkdirSync(knowledgeDir);
}

const sessionMiddleware = session({
    secret: "changeit",
    resave: true,
    saveUninitialized: true,
});

app.use(sessionMiddleware);
app.use(express.json());
io.engine.use(sessionMiddleware);

app.get('/', (req, res) => {
    res.sendFile(join(__dirname, 'index.html'));
});

app.post('/message', (req, res) => {
  res.status(200).end('OK');

  io.to(req.body.sessionid).emit('chat message', {
    message: req.body.message,
    source: "api"
  });
});
  
io.on('connection', (socket) => {
  const sessionId = socket.request.session.id;
    console.log('User connected:', sessionId);
    socket.join(sessionId);

    socket.on('chat message', async (msg) => {
        io.to(sessionId).emit('chat message', msg);
        
        // Spawn the Python script as a child process
        const pythonProcess = spawn('python', ['add_time.py', msg],{
          env: { ...process.env, SESSION_ID: sessionId }
        });

        pythonProcess.stdout.on('data', async (data) => {
            const processedMessage = data.toString().trim(); 

            // Dynamically import node-fetch
            const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args)); 

            // Send the processed message to /message via POST
            try {
                const response = await fetch('http://localhost:3000/message', { 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sessionid: sessionId, // Use Socket.IO's session ID
                        message: processedMessage 
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                } 
            } catch (error) {
                console.error('Error posting message:', error); 
            }
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Error from Python script: ${data}`);
        });
    });
  
    socket.on('save-knowledge', (customKnowledge) => {
      const filename = path.join(knowledgeDir, `knowledge_${sessionId}.txt`);
  
      fs.writeFile(filename, customKnowledge, (err) => {
        if (err) {
          console.error('Error saving custom knowledge:', err);
        } else {
          console.log('Custom knowledge saved:', filename);
        }
      });
    });

    socket.on('disconnect', () => {
      const filename = path.join(knowledgeDir, `knowledge_${sessionId}.txt`);
  
      fs.unlink(filename, (err) => {
        if (err && err.code !== 'ENOENT') {
          console.error('Error deleting custom knowledge:', err);
        } else {
          console.log('Custom knowledge deleted:', filename);
        }
      });
    });
});

app.post('/process_message', (req, res) => {
  const { message } = req.body;

  const pythonProcess = spawn('python', ['chatbot.py', message]);

  pythonProcess.stdout.on('data', (data) => {
    const processedMessage = data.toString().trim(); 

    fetch('/message', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sessionid: req.session.id,
            message: processedMessage
        })
    })
    .then(response => { /* Handle response as needed */ })
    .catch(error => { /* Handle error as needed */ });

    res.sendStatus(200); // Acknowledge the request
});

  pythonProcess.stderr.on('data', (data) => {
      console.error(`Error from Python script: ${data}`);
      res.sendStatus(500); // Internal Server Error
  });
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});