const express = require('express');
const { createServer } = require('node:http');
const { join } = require('node:path');
const { Server } = require('socket.io');
const session = require("express-session");
const port = process.env.PORT || 3000;
const app = express();
const server = createServer(app);
const io = new Server(server);

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
  
    socket.on('chat message', (msg) => {
      io.to(sessionId).emit('chat message', msg);
    });
  
    socket.on('disconnect', () => {
      console.log('User disconnected:', sessionId);
    });
  });
  
  server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });