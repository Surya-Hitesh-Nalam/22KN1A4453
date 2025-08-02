import express from "express";
import { UrlController } from "../controllers/urlController";

const router = express.Router();

router.post("/shorturls",(req,res)=>{
    UrlController.createShortUrl(req, res);
})
router.get("/shorturls/:shortId",(req,res)=>{
    UrlController.getUrlStats(req, res);
})

router.get("/:shortId",(req,res)=>{
    UrlController.redirectToOriginalUrl(req, res);
})

export default router;