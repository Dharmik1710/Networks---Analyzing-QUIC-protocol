const express = require("express");
const app = express();
const path = require("path");
const port = 8000;

// Middleware to log request headers
app.use((req, res, next) => {
  console.log("Request Headers:", req.headers);
  next();
});

// Serve static files from the public directory and its subdirectories
app.use(express.static(path.join(__dirname, "public")));

// Dynamic route to serve files from nested directories within public
app.get('/web/*', (req, res) => {
  const requestedPath = req.params[0];  // Capture everything after /web/
  const filePath = path.normalize(path.join(__dirname, 'public', requestedPath));

  // Security check to ensure the filePath stays within the public directory
  if (!filePath.startsWith(path.join(__dirname, 'public'))) {
    return res.status(400).send('Invalid file path.');
  }

  res.sendFile(filePath, (err) => {
    if (err) {
      res.status(404).send('File not found!');
    }
  });
});

// Fallback to serve index.html at /files route
app.get("/files", (req, res) => {
  console.log("Received request for '/files' route \n");
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

// Start the server
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
