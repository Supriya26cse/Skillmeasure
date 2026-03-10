const express = require("express");
const cors = require("cors");
const axios = require("axios");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const FormData = require("form-data");

const app = express();

// ===============================
// CORS (Temporary Open for Debug)
// ===============================
app.use(cors());

// ===============================
// Serve Frontend Files
// ===============================
const frontendPath = path.join(__dirname, "..", "frontend");
app.use(express.static(frontendPath));

// ===============================
// Multer Storage (PDF Upload)
// ===============================
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const dir = "uploads";
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir);
    }
    cb(null, dir);
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname).toLowerCase();
    const filename = Date.now() + ext;
    cb(null, filename);
  }
});

const upload = multer({
  storage,
  limits: { fileSize: 20 * 1024 * 1024 }, // 20MB
  fileFilter: (req, file, cb) => {
    if (!file.originalname.toLowerCase().endsWith(".pdf")) {
      return cb(new Error("Only PDF files are allowed"));
    }
    cb(null, true);
  }
});

// ===============================
// Health Check
// ===============================
app.get("/api", (req, res) => {
  res.send("Node Backend Running 🚀");
});

// Default Route
app.get("/", (req, res) => {
  res.sendFile(path.join(frontendPath, "upload.html"));
});

// ===============================
// Resume Upload API
// ===============================
app.post("/upload-resume", upload.single("resume"), async (req, res) => {
  try {
    console.log("📥 Upload request received");

    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const absolutePath = path.resolve(req.file.path);
    console.log("✅ File saved at:", absolutePath);

    const stat = fs.statSync(absolutePath);
    console.log("📦 File size:", stat.size);

    // Send file to Python AI server
    const form = new FormData();
    form.append("file", fs.createReadStream(absolutePath));

    console.log("🚀 Sending file to Python AI server...");

    const response = await axios.post(
      "http://localhost:8003/analyze",
      form,
      {
        headers: form.getHeaders(),
        maxContentLength: Infinity,
        maxBodyLength: Infinity,
        timeout: 0 // 🔥 IMPORTANT (No timeout limit)
      }
    );

    console.log("✅ Python server response received");

    res.json(response.data);

  } catch (error) {
    console.error("❌ FULL ERROR:", error);

    if (error.response) {
      return res.status(error.response.status).json({
        error: error.response.data
      });
    }

    if (error.code === "ECONNREFUSED") {
      return res.status(503).json({
        error: "Python server is not running."
      });
    }

    if (error.code === "ETIMEDOUT") {
      return res.status(504).json({
        error: "Python server took too long to respond."
      });
    }

    res.status(500).json({ error: error.message });
  }
});

// ===============================
// Start Server
// ===============================
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});