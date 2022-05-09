const RateLimit = require('express-rate-limit');
// important if behind a proxy to ensure client IP is passed to req.ip
// app.enable('trust proxy');

export default (apiLimiter = new RateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
}));

// only apply to requests that begin with /user/
// app.use('/user/', apiLimiter);
