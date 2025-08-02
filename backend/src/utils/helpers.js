import validator from 'validator';;

export function generateShortCode(custom){
    if(custom){
        if(!/^[a-zA-Z0-9_-]{3,10}$/.test(custom)){
            throw new Error('short code invalid');
        }
        return custom;
    }

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let Code = '';
    for (let i = 0; i < 6; i++) {
        Code += chars[Math.floor(Math.random() * chars.length)];
    }
    return Code;
}

export function validateUrl(url){
    return validator.isURL(url,{protocols:['http','https'],require_protocol:true})
}
export function Expiry(minutes=30){
    return new Date(Date.now() + minutes*60000);
}
