import { createRouter, createWebHistory } from 'vue-router';   
import login from '@/views/login.vue';
import choose from '@/views/choose.vue';
import personal from '@/views/personal.vue'
import my_sc from '@/views/my_sc.vue'
import more from "@/views/more.vue"
import home from "@/views/home.vue"
import main from "@/views/main.vue"

const routers=   
   [ 
    {  
      path: '/',  
      name: 'login',   
      component: login
    },
    {  
      path: '/home',  
      name: 'home',   
      component: home,
      children: [
        {  
          path: '/choose',  
          name: 'choose',   
          component: choose
        },
        {  
          path: '/my_sc',  
          name: 'my_sc',   
          component: my_sc
        },
        {  
          path: '/personal',  
          name: 'personal',   
          component: personal
        },
        {  
          path: '/more',  
          name: 'more',   
          component: more
        },    
        {  
          path: '/main',  
          name: 'main',   
          component: main
        },
      ]
    },   
    
    
  ]  
   
const router = createRouter({  
  history: createWebHistory(process.env.BASE_URL),   
  routes:routers  
});  


router.beforeEach((to, from, next) => {

  const oldServerHost = '39.102.213.237'; 
  const newServerUrl = 'http://1.94.144.75'; 

  if (window.location.host === oldServerHost) {

    const fullPath = to.fullPath ? to.fullPath : '/';
    window.location.href = newServerUrl + (newServerUrl.endsWith('/') ? '' : '/') + fullPath;
  } else {
    next(); 
  }
});

export default router;