import express from 'express';
import mongoose from 'mongoose';
import urlRoutes from './routes/urlRoutes.js';
import { requestLogger } from './middleware/requestLogger.js';

const app = express();

app.use(express.json());
app.use(requestLogger);
app.use('/', urlRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ success: false, error: 'Endpoint not found' });
});

export default app;
