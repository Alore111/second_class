<template>
  <div class="loginbody">  
    <div class="logindata">  
      <div class="logintext">  
        <h2>auto二课</h2>  
      </div>  
      <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="submitData" label-width="0">  
        <div class="formdata">  
          <el-form-item prop="username">  
            <el-input  
              v-model="form.username"  
              clearable  
              @keydown.enter.native="submitData"  
              placeholder="请输入学号"  
              class="short-input"  
            ></el-input>  
          </el-form-item>  
          <el-form-item prop="password">  
            <el-input  
              v-model="form.password"  
              clearable  
              @keydown.enter.native="submitData"  
              placeholder="请输入密码"  
              class="short-input"  
              show-password  
            ></el-input>  
          </el-form-item>  
        </div>  
        <div class="butt">  
          <el-button type="primary" @click="submitData">登录</el-button>  
        </div>  
      </el-form>  
    </div>  
  </div>

</template>

<script>
import { get_password } from '../../public/password.js';
import { ElLoading } from 'element-plus';  
import { ElForm, ElFormItem, ElInput, ElButton } from 'element-plus';
import spinnerImage from '../assets/a.gif'; 
import axios from 'axios'; 
export default {
  name: "login",
  components: {  
    ElForm,  
    ElFormItem,  
    ElInput,  
    ElButton  
  },  
  data() {
    return {
      form: {
            "username": "",
            "password": "",
            "encrypt":"",
            "user_agent":""
      },
      checked: false,
      rules: {
        username: [
          { required: true, message: "请输入学号", trigger: "blur" },
          { max: 10, message: "不能大于10个字符", trigger: "blur" },
        ],
        password: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { max: 100, message: "密码过长", trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    async submitData() { 
    try {
      this.startLoading();
      const userAgent = navigator.userAgent;

      function isMobileUserAgent(userAgent) {  
          return /Mobile|Android|iPhone|iPad/.test(userAgent);  
      }

      function  External(e) {  
          return get_password(e)
      }

      const isMobile = isMobileUserAgent(userAgent);

      this.form.encrypt = External(this.form.username)
      if (!isMobile) {  
          const headersList = [  
            {  
              'User-Agent': 'Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2679 MicroMessenger/7.0.10.1580(0x27000A59) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            },  
            {  
              'User-Agent': 'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045129 Mobile Safari/537.36 MMWEBID/6735 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/WIFI Language/zh_CN ABI/arm64', 
            },  
            {
              'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.11(0x17000b21) NetType/4G Language/zh_CN',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 9; HLK-AL00 Build/HONORHLK-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/4465 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/WIFI Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 9; MI 9 SE Build/PKQ1.181121.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045129 Mobile Safari/537.36 MMWEBID/1500 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/4G Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 9; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/8968 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/4G Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 9; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/72.0.3626.121 Mobile Safari/537.36 MMWEBID/1247 MicroMessenger/7.0.10.1561(0x27000A41) Process/tools NetType/4G Language/zh_CN ABI/arm64 GPVersion/1',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 10; LIO-AL00 Build/HUAWEILIO-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/6203 MicroMessenger/7.0.10.1580(0x27000AFC) Process/tools NetType/WIFI Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 10; EVR-AL00 Build/HUAWEIEVR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1170 MMWEBSDK/200201 Mobile Safari/537.36 MMWEBID/5192 MicroMessenger/7.0.12.1620(0x27000C36) Process/toolsmp NetType/4G Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 10; MI 9 Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1171 MMWEBSDK/200201 Mobile Safari/537.36 MMWEBID/2568 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/4G Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 7.0; Mi-4c Build/NRD91M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1169 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/2208 MicroMessenger/7.0.10.1580(0x27010AFF) Process/tools NetType/4G Language/zh_CN ABI/arm64',
              
            },
            {
              'User-Agent':'Mozilla/5.0 (Linux; Android 7.1.2; vivo X9Plus Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile',
              
            }
          ];    
            const index = Math.floor(Math.random() * headersList.length);  
            var headers = headersList[index];
            this.form.user_agent = headers  
        } else{

          var headers = {
            'User-Agent': navigator.userAgent,
          };
            this.form.user_agent = headers  
        }
      
      const response = await axios.post('/api/login/login',this.form); 

      const dic = response.data
      localStorage.setItem('userData', JSON.stringify(dic));  
      if (dic['status'] == 'ok') {
          this.endLoading(this.startLoading()); 
          this.$message({
                  message: "登录成功啦",
                  type: "success",
                  showClose: true,
                });
          this.$router.push({path: '/main'});
      } 
      else {   
        this.$message({
                  message: "账户名或密码错误",
                  type: "error",
                  showClose: true,  
                });   
      }} 
    catch (error) {  
        {
              this.endLoading(this.startLoading()); 
              this.$message({
                message: "好像出错了哦,请联系开发人员 T^T",
                type: "error",
                showClose: true,
              });
      }}  
  },
  startLoading() {
    const loading = this.$loading({
       lock: true,
       text: "正在加载中…………",
       
       background: "rgba(250, 250, 250, 0.7)",
       
    });
    return loading;
},
endLoading(loading) {
   loading.close();
},
},
  
}
</script>




<style scoped>

.loginbody {
  display: flex;
  width: 100%;  
  height: 110vh; 
  background-image: url("@/assets/20240313183806.jpg");
  background-position: center center;
  overflow: auto;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}


.logindata {
  width: 400px;
  height: 300px;
  top: 50%; 
  transform: translate(-50%, 10%);
  margin-left: 50%;
  align-items: center;
}

.short-input{
  width: 450px;
  margin-left: auto;   
  margin-right: auto; 
}

.logintext {
  margin-top: 50px;
  margin-bottom: 20px;
  line-height: 90px;
  text-align: center;
  font-size: 30px;
  font-weight: bolder;
  color: white;
  text-shadow: 2px 2px 4px #000000;
}



@media screen and (max-width: 600px) {
  .loginbody {
    display: flex;
    width: 100%;  
    height: 98vh; 
    background-image: url("@/assets/20240313183806.jpg");
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
    background-attachment: fixed;  
    overflow: hidden;
  }    
  .short-input {  
    width: 80%;
    margin-left: auto;   
    margin-right: auto;  
      
  }
  .logintext {
  margin-top: 50px;
  margin-bottom: 20px;
  line-height: 90px;
  font-size: 30px;
  font-weight: bolder;
  color: white;
  text-shadow: 2px 2px 4px #000000;
}  
}


.tool {
  display: flex;
  justify-content: space-between;
  color: #606266;
}

.butt {
  margin-top: 10px;
  text-align: center;
}

.shou {
  cursor: pointer;
  color: #606266;
}


.el-loading-spinner{
  background-image:url('../assets/a.gif');
}
.el-image__placeholder {
  background: url('../assets/a.gif') no-repeat 50% 50% !important;
  background-size: 50% !important;
}
::v-deep .el-loading-mask .el-loading-text {  
    font-family: 'Roboto', sans-serif; 
}
</style>