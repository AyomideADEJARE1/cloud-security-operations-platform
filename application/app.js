const express = require("express");
const mysql = require("mysql2/promise");
const morgan = require("morgan");

const app = express();

app.use(morgan("combined"));

const PORT = process.env.PORT || 3000;

const dbConfig = {
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT || 3306),
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
};

function securityLog(event, details = {}) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    event,
    ...details
  }));
}

app.get("/", (req, res) => {
  res.json({
    application: "Cloud Security Operations Platform",
    status: "running",
    environment: process.env.NODE_ENV || "development"
  });
});

app.get("/health", async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    await connection.query("SELECT 1");
    await connection.end();

    res.json({
      status: "healthy",
      database: "connected"
    });
  } catch (error) {
    securityLog("database_connection_failed", {
      endpoint: "/health",
      error: error.message
    });

    res.status(503).json({
      status: "unhealthy",
      database: "disconnected"
    });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Application listening on port ${PORT}`);
});
