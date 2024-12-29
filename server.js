const express = require('express');
const passport = require('passport');
const OIDCStrategy = require('passport-azure-ad').OIDCStrategy;
const session = require('express-session');
const path = require('path');
const nodemailer = require('nodemailer');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

// Middleware to parse JSON and URL-encoded bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Azure AD B2C configuration
const b2cConfig = {
  identityMetadata: `https://${process.env.B2C_TENANT_NAME}.b2clogin.com/${process.env.B2C_TENANT_NAME}.onmicrosoft.com/v2.0/.well-known/openid-configuration?p=${process.env.B2C_USER_FLOW}`,
  clientID: process.env.B2C_CLIENT_ID,
  clientSecret: process.env.B2C_CLIENT_SECRET,
  responseType: 'code',
  responseMode: 'form_post',
  redirectUrl: process.env.B2C_REDIRECT_URI,
  allowHttpForRedirectUrl: false,
  scope: ['openid', 'profile', 'email'],
  loggingLevel: 'debug',
};

// Middleware for sessions
app.use(
  session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
  })
);

// Initialize Passport
app.use(passport.initialize());
app.use(passport.session());

// Configure the Azure AD B2C strategy
passport.use(
  new OIDCStrategy(b2cConfig, (profile, done) => {
    return done(null, profile);
  })
);

// Serialize and deserialize user
passport.serializeUser((user, done) => {
  done(null, user);
});

passport.deserializeUser((user, done) => {
  done(null, user);
});

// Serve static files (including home.html)
app.use(express.static(path.join(__dirname, 'public')));

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/login', passport.authenticate('azuread-openidconnect', { failureRedirect: '/' }));

app.post(
    '/auth/callback',
    passport.authenticate('azuread-openidconnect', {
      failureRedirect: '/',
      failureMessage: true,  // Enable failure messages
    }),
    (req, res) => {
      res.redirect('/home.html'); // Redirect to home.html after successful login
    }
  );

app.get('/logout', (req, res) => {
  req.logout((err) => {
    if (err) {
      console.error(err);
    }
    res.redirect('/');
  });
});

// Email sending route
app.post('/send-email', async (req, res) => {
  const { name, email, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).send('All fields are required.');
  }

  try {
    // Configure nodemailer transporter
    const transporter = nodemailer.createTransport({
      service: 'gmail', // Example: Gmail, or use other email service
      auth: {
        user: process.env.EMAIL, // Your email from .env
        pass: process.env.EMAIL_PASSWORD, // Your email password from .env
      },
    });

    // Email details
    const mailOptions = {
      from: process.env.EMAIL,
      to: process.env.EMAIL, // Replace with a different recipient if needed
      subject: 'Contact Form Submission',
      text: `Name: ${name}\nEmail: ${email}\nMessage: ${message}`,
    };

    // Send email
    await transporter.sendMail(mailOptions);
    res.status(200).send('Email sent successfully.');
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).send('Failed to send email.');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
