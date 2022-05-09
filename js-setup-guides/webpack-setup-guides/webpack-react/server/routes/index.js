const path = require("path");
const router = require("express").Router();

// serve the index.html from the build folder (dist/)
// in any route
router.get("*", (req, res) => {
  const route = path.join(__dirname, "..", "..", "dist", "index.html");
  res.sendFile(route);
});

module.exports = router;
