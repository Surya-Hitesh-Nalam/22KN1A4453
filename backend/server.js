import dotenv from 'dotenv';
import express from 'express';
import mongoose from 'mongoose';
dotenv.config();
import { Log } from '../Logging_Middleware/src/index.js';
const PORT = 3000

const app = express();
app.use(express.json());

mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(()=>{
    Log('backend', 'info', 'db', 'MongoDB connected successfully');
    console.log('MongoDB connected successfully');
    app.listen(PORT, () => {
        Log('backend', 'info', 'server', `Server is running on port ${PORT}`);
        console.log(`Server is running on port ${PORT}`);
    });
}).catch(error=>{
    Log('backend', 'error', 'db', `MongoDB connection failed: ${error.message}`);
    console.error(`MongoDB connection failed: ${error.message}`);
})


