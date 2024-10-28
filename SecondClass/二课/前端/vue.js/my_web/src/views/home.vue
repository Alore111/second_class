<template>
  <div class="loginbody">
    <div class="centered-box">  
        <div class="common-layout" >
          <el-container>
                <el-header height='65px' class="yuanjiao1" >
                  <el-container>
                    <el-aside width="100px">
                      <div class="flex-center">
                          <el-avatar
                                :size="55"
                                :src="imageUrl"
                                @click="dialogTableVisible = true"
                          />
                      </div>
                    </el-aside>
                    <el-main>{{ this.basin_data }}同学，{{ this.time }}</el-main>
                  </el-container>
                </el-header>
            <el-container>
                <el-aside  style="width:180px;background-color:rgb(255, 255, 255); height:85vh;" class="yuanjiao2">
                    <el-menu
                        default-active="1"
                        :default-active="$route.path" 
                        router
                    >
                        <el-menu-item index="/choose">
                        <el-icon><document /></el-icon>
                        <span>选课目录</span>
                        </el-menu-item>

                        <el-menu-item index="/my_sc">
                        <el-icon><Promotion /></el-icon>
                        <span>我的二课</span>
                        </el-menu-item>
                        
                        <el-menu-item index="/personal">
                        <el-icon><ElementPlus /></el-icon>
                        <span>个人信息</span>
                        </el-menu-item>

                        <el-menu-item index="/more">
                        <el-icon><More /></el-icon>
                        <span>更多功能</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main style="background-color: rgb(255, 255, 255);height:90vh;" class="yuanjiao3" >
                  <router-view />
                </el-main>
            </el-container>
            </el-container>
        </div>
    </div>
  </div> 
  <el-dialog class="avatarDialog" :showClose="false" center v-model="dialogTableVisible" title="更换头像" :lock-scroll="false">
      <el-upload ref="upload" class="avatar-uploader" :before-upload="beforeAvatarUpload" action="#"
               :http-request="uploadFile" :auto-upload="false" multiple list-type="picture-card" :file-list="fileList"
               :on-change="fileChange">
           <el-icon>
               <Plus />
           </el-icon>
           <template #file="{ file }">
               <img :src="file.url" alt="" />
           </template>
       </el-upload>
       <template #footer>
           <span class="dialog-footer">
               <el-button type="primary" @click="handleUpdateAvatar">
                   更换头像
               </el-button>
               <el-button @click="cancel">取消</el-button>
           </span>
       </template>
    </el-dialog>
</template>

<script>  
import { ref } from 'vue';  
import axios from 'axios';
import { ElButton, ElDialog } from 'element-plus';  
import {
      Document,
      Menu as IconMenu,
      Location,
      Setting,
} from '@element-plus/icons-vue'  
export default {  
  created() {  
    const loginData = JSON.parse(localStorage.getItem('userData')); 
    this.basin_data = loginData.data.info.data.userName
  },  
data() {
        return {
            fileList: [],
            basin_data: [],           
            username:null,     
            dialogTableVisible:false,
            imageUrl:'',
            time:[]
        }
    },   
mounted() {  
    this.icol()
    this.gettime()
    },  
methods: {
        async icol(){
            try {  
                const Newresponse = await axios.post('/api/images/get', null, {  
                    responseType: 'arraybuffer'
                    });  
                let byteArray = new Uint8Array(Newresponse.data);  
  
                let blob = new Blob([byteArray], {type: 'image/jpeg'});  

                this.imageUrl = URL.createObjectURL(blob);  

        } catch (error) {  
                console.error('请求失败:', error);  
        }
        },
        async uploadFile(params) {
            const file = params.file;
            var forms = new FormData();
            forms.append("file", file);
            forms.append("uid", this.username);
            const res = await axios.post('/api/personal/img',forms);  
            if (res.status == "200") {
                    this.$message({
                        message: '上传成功',
                        type: 'success'
                    })
                    this.dialogTableVisible = false;
                    this.icol()
                } else {
                    this.$message({
                        message: '上传失败',
                        type: 'error'
                    })
                }
            },
        beforeAvatarUpload(file) {
            const imgType = (file.type === 'image/jpeg') || (file.type === 'image/png') || (file.type === 'image/gif');
            const imgLimit= (file.size / 1024 / 1024) < 5;
            if (!imgType) {
                this.$message.error("只允许jpg、png、gif格式的图片");
                return false;
            }
            if (!imgLimit) {
                this.$message.error("上传的图片大小不能超过5MB");
                return false;
            }
            console.log("检查通过");
            return true;
        },
        fileChange(file, fileList) {
            this.file = file.raw;
            if (fileList.length > 0) {
                this.fileList = [fileList[fileList.length - 1]];
            }
        },
        handleUpdateAvatar() {
            this.$refs['upload'].submit();
            this.dialogTableVisible = false;
            this.$refs['upload'].clearFiles();
        },
        cancel() {
            this.dialogTableVisible = false;
            this.$refs['upload'].clearFiles();
        },   
        gettime(){
          const now = new Date(); 
          const hours = now.getHours(); 
          const morningGreetings = [  
              "清晨的阳光和努力的你，都值得被命运温柔以待。早安！",  
              "来如夏花之绚烂，去如秋叶之静美。早安!",  
              "朝阳真美，新的一天开始了",  
              "今天也要加油哦",  
              "已经起床了,击败全国99%的懒狗",  
              "花自向阳开,人自向前走,早安!",
              " Good day, sir. How may I assist you?",
          ]; 
          const noonGreetings = [  
              "树阴满地日当午，梦觉流莺时一声~~",
              "中午好，吃个午饭放松一下吧",
              "该睡午觉了(￣o￣) . z Z",
              "吃饭去了，(╯▽╰ )好香~~",
              "Good day, What have you been up to? ",
          ]; 
          const afterGreetings = [  
             "下午好，喝杯茶放松一下吧✧(≖ ◡ ≖✿)",
             "今天天气好热啊…………",
             "夏日炎炎正好眠，上课可别打瞌睡哦 (ˉ▽￣～) ",
             "中午睡没睡觉觉啊？|･ω･｀)",
             "下午好！绿树阴浓夏日长，楼台倒影入池塘~~~",
             "下午好！纸屏石枕竹方床，手倦抛书午梦长~~~",
          ]; 
          const nightGreetings = [  
             "夏夜谁知亦自长，幽居渺在水云乡~~",
             "疲惫一天了，出去运动一下吧( ‘-ωก̀ )",
             "太阳落山了哦 _(・ω・｣ ∠)_",
          ]; 
          const Greetings = [  
             "夜深了，早点休息吧。。。"
          ]; 
          if (hours >= 7 && hours < 11) {
              const randomIndex = Math.floor(Math.random() * morningGreetings.length);  
              this.time = morningGreetings[randomIndex];
          } else if (hours >= 11 && hours < 14) {  
              const randomIndex = Math.floor(Math.random() * noonGreetings.length);  
              this.time = noonGreetings[randomIndex]; 
          } else if (hours >= 14 && hours < 18) {  
              const randomIndex = Math.floor(Math.random() * afterGreetings.length);  
              this.time = afterGreetings[randomIndex];  
          } else if (hours >= 18 && hours <= 24) {  
            const randomIndex = Math.floor(Math.random() * nightGreetings.length);  
              this.time = nightGreetings[randomIndex];  
            }
          else {    
              const randomIndex = Math.floor(Math.random() * Greetings.length);  
              this.time = Greetings[randomIndex];
          }  
        }
    }
};  
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
  padding-right:0px!important
}

.centered-box {  
    position: absolute; 
    top: 50%; 
    left: 50%; 
    transform: translate(-50%, -43%);
    width: 1070px; 
    height: 590px; 
    background-color: white; 
    border-radius: 16px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
    padding: 20px; 
}

.yuanjiao1 {  
    border-top-left-radius: 10px; 
    border-top-right-radius: 10px; 
}

.yuanjiao2{
    border-bottom-left-radius: 10px;  
}

.yuanjiao3{
    border-bottom-right-radius: 10px;
}
.headers{
    width: 700px;  
    height: 200px;  
    overflow: hidden;
}
.flex-center {  
  width: 20%; 
  margin-left: 30%;
  
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
}

</style>

