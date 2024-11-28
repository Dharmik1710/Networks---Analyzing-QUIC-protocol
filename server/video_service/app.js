const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const port = 9000;

// Route for serving video content (optional)
app.get("/video", (req, res) => {
  res.send("Video service is running!");
});

// Route for serving a video file
app.get("/video/:filename", (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, "public", filename);

  // Security check for path traversal
  if (!filePath.startsWith(path.join(__dirname, "public"))) {
    return res.status(400).send("Invalid file path.");
  }

  // Serve the video file (default response)
  res.sendFile(filePath, (err) => {
    if (err) {
      res.status(404).send("Video not found!");
    }
  });
});

// Route for streaming video content
app.get("/video/stream/:filename", (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, "public", filename);

  // Check file exists
  fs.stat(filePath, (err, stats) => {
    if (err) {
      return res.status(404).send("Video not found!");
    }

    const fileSize = stats.size;
    const range = req.headers.range;

    if (!range) {
      return res.status(416).send("Range header is required");
    }

    // Parse the range to get the start and end bytes
    const [start, end] = range.replace(/bytes=/, "").split("-").map(Number);

    const chunkStart = start || 0;
    const chunkEnd = end || Math.min(fileSize - 1, chunkStart + 1024 * 1024 - 1); // Send 1MB chunk if no end is provided

    const fileStream = fs.createReadStream(filePath, { start: chunkStart, end: chunkEnd });
    res.writeHead(206, { // 206 status code for partial content
      "Content-Range": `bytes ${chunkStart}-${chunkEnd}/${fileSize}`,
      "Accept-Ranges": "bytes",
      "Content-Length": chunkEnd - chunkStart + 1,
      "Content-Type": "video/mp4",
    });

    fileStream.pipe(res);
  });
});

app.listen(port, () => {
  console.log(`Video service listening on port ${port}`);
});
