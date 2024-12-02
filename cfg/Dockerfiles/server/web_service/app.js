const express = require("express");
const app = express();
const path = require("path");
const port = 8000;

app.use((req, res, next) => {
  console.log('Request Headers:', req.headers);  // Log all headers
  next();
});

// Route for serving video content (optional)
app.get("/web", (req, res) => {
  res.send("Web service is running!");
});

app.use(express.static(path.join(__dirname, "public")));

app.get('/web/:filename', (req, res) => {
  const fileName = req.params.filename;
  const filePath = path.join(__dirname, 'public', fileName);

  // Security check for path traversal
  if (!filePath.startsWith(path.join(__dirname, 'public'))) {
    return res.status(400).send('Invalid file path.');
  }

  res.sendFile(filePath, (err) => {
    if (err) {
      return res.status(404).send('File not found!');
    }
  });
});

app.get("/files", (req, res) => {
  console.log("Received request for '/files' route \n")
  
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
