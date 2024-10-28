<template>
    <el-container @submit.prevent="submitData">
      <el-aside style="width:350px" @submit.prevent="icol">
        
        <el-loading :visible="isLoading"></el-loading>
            <el-table :data="showdata" style="width: 100%" v-if="showdata.length > 0">  
                    <el-table-column prop="key" width="100"></el-table-column>  
                    <el-table-column prop="value" width="200"></el-table-column>  
            </el-table>
        
        </el-aside>
        <el-main>
             <p>这里是二课成绩单</p>
            （学校的服务器接口出错了，此功能暂时用不了T^T）
        </el-main>
    </el-container>
    
</template>

<script>
import { ref } from 'vue'
import axios from 'axios';
import { ElLoading } from 'element-plus';
export default{
    data() {
        return {
            fileList: [],
            basin_data: [],           
            username:null,     
            dialogTableVisible:false,
            imageUrl:'',
            showdata:[],
            isLoading: false,
            tableing: false,
        }
    },
    mounted() {  
    this.submitData();
    this.icol()
    },  
    methods: {
        async submitData(){
            try {  
                this.isLoading = true;
                var storedData = localStorage.getItem('userData');  
                var data = JSON.parse(storedData).data.data;
                const response = await axios.post('/api/personal/basin_data',{data:data});  
                this.basin_data = response.data; 
                this.username = response.data.info.StudentId;
                this.showdata = this.newdata(response.data.info)
                this.isLoading = false;
        } catch (error) {  
                console.error('请求失败:', error);  
        }  
        },
        async icol(){
            try {  
                const Newresponse = await axios.post('/api/images/get', null, {  
                    responseType: 'arraybuffer'
                    });  
                console.log(Newresponse)
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
        newdata(data){
            const newdata ={
                '姓名：':data.Name,
                '学号：':data.StudentId,
                '专业：':data.SpecialtyName,
                '年级：':data.SpeGradeText,
                '学院：':data.CollegeName,
                '手机号：':data.MoveTel,
                '邮箱：':data.Email,
                'QQ号：':data.QQCard,
                } 
                return this.show(newdata)
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
        show(data) {  
            return Object.entries(data).map(([key, value]) => ({  
            key: key,  
            value: value  
        }));},
        cancel() {
            this.dialogTableVisible = false;
            this.$refs['upload'].clearFiles();
        },
        
    }
}
</script>

<style scoped>
.flex-center {  
  width: 10%; 
  margin-left: 37%;
}  
</style>