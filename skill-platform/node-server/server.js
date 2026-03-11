const express = require("express");
const cors = require("cors");
const axios = require("axios");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const FormData = require("form-data");
const sqlite3 = require("sqlite3").verbose();

const app = express();

// Get Python backend URL from environment or use localhost
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || "http://localhost:8003";

// ===============================
// Database Setup (SQLite)
// ===============================
const DB_FILE = "resumes.db";
const db = new sqlite3.Database(DB_FILE, (err) => {
  if (err) {
    console.error("❌ Database connection error:", err);
  } else {
    console.log("✅ Connected to SQLite database");
    initializeDatabase();
  }
});

function initializeDatabase() {
  db.run(`
    CREATE TABLE IF NOT EXISTS resumes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      studentName TEXT NOT NULL,
      registerNumber TEXT NOT NULL,
      resumeFile TEXT NOT NULL,
      skillsFound TEXT,
      quizScore INTEGER DEFAULT 0,
      codingScore INTEGER DEFAULT 0,
      totalQuizQuestions INTEGER DEFAULT 0,
      totalCodingQuestions INTEGER DEFAULT 0,
      uploadedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
      completedAt DATETIME
    )
  `, (err) => {
    if (err) {
      console.error("❌ Error creating resumes table:", err);
    } else {
      console.log("✅ Resumes table ready");
    }
  });
}

// ===============================
// CORS (Temporary Open for Debug)
// ===============================
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

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
  res.sendFile(path.join(frontendPath, "login.html"));
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

    // Get student info from request
    const studentName = req.body.studentName || "Unknown";
    const registerNumber = req.body.registerNumber || localStorage?.getItem?.("registerNumber") || "Unknown";

    const absolutePath = path.resolve(req.file.path);
    console.log("✅ File saved at:", absolutePath);

    const stat = fs.statSync(absolutePath);
    console.log("📦 File size:", stat.size);

    // Send file to Python AI server
    const form = new FormData();
    form.append("file", fs.createReadStream(absolutePath));

    console.log("🚀 Sending file to Python AI server...");
    console.log("Python backend URL:", PYTHON_BACKEND_URL);

    const response = await axios.post(
      `${PYTHON_BACKEND_URL}/analyze`,
      form,
      {
        headers: form.getHeaders(),
        maxContentLength: Infinity,
        maxBodyLength: Infinity,
        timeout: 0 // 🔥 IMPORTANT (No timeout limit)
      }
    );

    console.log("✅ Python server response received");

    // Save resume to database
    const skillsFound = response.data.skills_found || [];
    const totalQuizQuestions = response.data.quiz ? response.data.quiz.length : 0;
    const totalCodingQuestions = response.data.coding_challenges ? response.data.coding_challenges.length : 0;

    db.run(
      `INSERT INTO resumes (studentName, registerNumber, resumeFile, skillsFound, totalQuizQuestions, totalCodingQuestions)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [
        studentName,
        registerNumber,
        absolutePath,
        JSON.stringify(skillsFound),
        totalQuizQuestions,
        totalCodingQuestions
      ],
      (err) => {
        if (err) {
          console.error("❌ Error saving resume to database:", err);
        } else {
          console.log("✅ Resume saved to database");
        }
      }
    );

    // Add uploadId to response for tracking
    response.data.uploadId = Date.now().toString();
    response.data.registerNumber = registerNumber;

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
// Teacher API - Get All Resumes
// ===============================
app.get("/api/teacher/resumes", (req, res) => {
  const sortBy = req.query.sortBy || "quizScore"; // or 'codingScore', 'uploadedAt'
  const orderBy = req.query.order || "DESC"; // or 'ASC'

  db.all(
    `SELECT * FROM resumes ORDER BY ${sortBy} ${orderBy}`,
    (err, rows) => {
      if (err) {
        console.error("❌ Error fetching resumes:", err);
        return res.status(500).json({ error: "Failed to fetch resumes" });
      }
      
      // Parse skillsFound JSON back to array
      const resumes = rows.map(row => ({
        ...row,
        skillsFound: Array.isArray(row.skillsFound) ? row.skillsFound : JSON.parse(row.skillsFound || "[]")
      }));

      console.log("✅ Fetched", resumes.length, "resumes");
      res.json(resumes);
    }
  );
});

// ===============================
// Teacher API - Get Resume Details
// ===============================
app.get("/api/teacher/resumes/:id", (req, res) => {
  const { id } = req.params;

  db.get(
    `SELECT * FROM resumes WHERE id = ?`,
    [id],
    (err, row) => {
      if (err) {
        console.error("❌ Error fetching resume:", err);
        return res.status(500).json({ error: "Failed to fetch resume" });
      }
      
      if (!row) {
        return res.status(404).json({ error: "Resume not found" });
      }

      // Parse skillsFound JSON back to array
      row.skillsFound = Array.isArray(row.skillsFound) ? row.skillsFound : JSON.parse(row.skillsFound || "[]");
      
      res.json(row);
    }
  );
});

// ===============================
// Update Quiz & Coding Scores
// ===============================
app.post("/api/update-scores", express.json(), (req, res) => {
  const { registerNumber, quizScore, codingScore, totalQuizQuestions, totalCodingQuestions } = req.body;

  if (!registerNumber) {
    return res.status(400).json({ error: "Register number is required" });
  }

  db.run(
    `UPDATE resumes 
     SET quizScore = ?, codingScore = ?, totalQuizQuestions = ?, totalCodingQuestions = ?, completedAt = CURRENT_TIMESTAMP
     WHERE registerNumber = ?`,
    [quizScore, codingScore, totalQuizQuestions, totalCodingQuestions, registerNumber],
    function(err) {
      if (err) {
        console.error("❌ Error updating scores:", err);
        return res.status(500).json({ error: "Failed to update scores" });
      }

      console.log("✅ Scores updated for:", registerNumber);
      res.json({ success: true, message: "Scores updated" });
    }
  );
});

// ===============================
// Start Server
// ===============================
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});