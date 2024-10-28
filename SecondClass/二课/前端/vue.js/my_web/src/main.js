import { createApp } from 'vue';  
import App from './App.vue';  
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'  
import router from './router';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'



const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  } 
app.use(ElementPlus); 
app.use(router);
app.mount('#app');


const debounce = (fn, delay) => {
  let timer
   return (...args) => {
     if (timer) {
       clearTimeout(timer)
     }
     timer = setTimeout(() => {
       fn(...args)
     }, delay)
   }
}
  
const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver{
   constructor(callback) {
     callback = debounce(callback, 200);
     super(callback);
   }}

   router.beforeEach((to, from, next) => {  
    let token = localStorage.getItem("userData");  
    if (token) {  
      next();
    } else {  
      if (to.path !== '/') {   
        alert("请先登录");  
        next({ path: '/' });  
      } else {  
        next(); 
      }  
    }  
  });
  
   
