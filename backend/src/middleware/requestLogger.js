import { Log } from "../Logging_Middleware/src/index.js" ;

export function requestLogger(req,res,next){
    req.requestId = Math.random().toString(36).slice(2);
    Log('backend', 'info', 'middleware', `Request received`);
    const send = res.send.bind(res);
    res.send = (body)=>{
        Log('backend', 'info', 'middleware', `Response sent `);
        return send(body);
    }
    next();
}