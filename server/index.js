const express = require("express");
const app = express();
const path = require("path");
const port = 8000;

app.use((req, res, next) => {
  console.log('Request Headers:', req.headers);  // Log all headers
  next();
});

app.get("/", (req, res) => {
  console.log("Recevied request for '/' route \n")
  res.send("Hello World!");
});

app.use(express.static(path.join(__dirname, "public")));

app.get("/files", (req, res) => {
  console.log("Received request for '/files' route \n")
  
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
