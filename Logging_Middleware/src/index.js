import fetch from "node-fetch";


const ALLOWED_VALUES = {
    stack:['backend','frontend'],
    level:['debug','info','warn','error','factal'],
    package:['cache','controller','cron_job','db','handler','repository','route','services','server']
}

function validate(field,value){
    if(!ALLOWED_VALUES[field].includes(value)){
        throw new Error(`Invalid ${field}: ${value}`)
    }
}

export async function Log(stack,level,pkg,message) {
    validate('stack', stack);
    validate('level', level);
    validate('package', pkg);
    const payload = { stack, level, package: pkg, message };

    //const token = await fetch(process.env.LOGGING_URL,{
       // method: 'POST',
        //headers: {
            //'Content-Type': 'application/json',
            //'Authorization': `Bearer ${process.env.TOKEN}`
    //},
//body:JSON.stringify(payload)}
    
// if(!res.ok){
//     console.error('Log API error');
// }

}

