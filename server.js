const express = require('express');
const bodyParser = require('body-parser');
const sql = require('mssql');
const bcrypt = require('bcrypt');
const dotenv = require('dotenv');
const nodemailer = require('nodemailer');

dotenv.config();
const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// Database configuration
const dbConfig = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_NAME,
    options: {
        encrypt: true, // For Azure SQL
        trustServerCertificate: true
    }
};

// POST route for signup
app.post('/api/signUp', async (req, res) => {
    const { name, email, password } = req.body;

    // Hash the password before saving it
    const hashedPassword = await bcrypt.hash(password, 10);

    try {
        const pool = await sql.connect(dbConfig);
        const result = await pool.request()
            .input('name', sql.NVarChar, name)
            .input('email', sql.NVarChar, email)
            .input('password', sql.NVarChar, hashedPassword)  // Store the hashed password
            .query(`
                INSERT INTO Users (Name, Email, Password)
                VALUES (@name, @email, @password)
            `);

        res.status(200).json({ message: 'User registered successfully!' });
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Error registering user!' });
    }
});

// POST route for login
app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;

    try {
        const pool = await sql.connect(dbConfig);
        const result = await pool.request()
            .input('email', sql.NVarChar, email)
            .query('SELECT * FROM Users WHERE Email = @email');

        if (result.recordset.length > 0) {
            const user = result.recordset[0];
            // Compare the entered password with the stored hashed password
            const isMatch = await bcrypt.compare(password, user.Password);
            if (isMatch) {
                res.status(200).json({ message: 'Login successful!' });
            } else {
                res.status(401).json({ message: 'Invalid credentials' });
            }
        } else {
            res.status(404).json({ message: 'User not found' });
        }
    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Error logging in user!' });
    }
});

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
    console.log(`Server running at http://localhost:${port}`);
});
