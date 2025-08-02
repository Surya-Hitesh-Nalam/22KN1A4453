import mongoose from "mongoose";

const clickDetailSchema = new mongoose.Schema({
    timestamp: {
        type: Date,
        default: Date.now
    },
    ip:String,
    userAgent: String,
    referrer: String,
    location:String,
});

const urlSchema = new mongoose.Schema({
    originalUrl: {
        type: String,
        required: true
    },
    shortUrl: {
        type: String,
        required: true,
    },
    shortCode: {
        type: String,
        required: true,
        unique: true,
        index:true,
    },
    validityPeriod:{
        type:Number,
        default: 30,
    },
    expiresAt: {
        type: Date,
        required:true,
        index:true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    analytics:{
        totalClicks: {
            type: Number,
            default: 0
        },
        clickDetails:[clickDetailSchema]
    }
})

urlSchame.index({expiresAt:1},{expiresAfterSeconds:0});

export default mongoose.model('Url', urlSchema);