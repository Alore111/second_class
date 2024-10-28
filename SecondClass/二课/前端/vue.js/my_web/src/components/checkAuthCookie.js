export function checkAuthCookie() {  
    const cookies = document.cookie.split('; ');  
    for (let i = 0; i < cookies.length; i++) {  
        const cookie = cookies[i].split('=');  
        if (cookie[0].trim() === 'your_auth_cookie_name') {  
            return true;  
        }  
    }  
    return false;  
}