<template>
  <ul v-infinite-scroll="submitData" class="infinite-list" style="overflow: auto; height: 500px;">  
  <li v-for="item,index in items"  class="infinite-list-item">  
    <el-card style="width: 100%;height: 88px;" shadow="hover" class="card" :body-style="{ display: 'flex', padding: '7px ' }" >  
      <div class="common-layout">
        <el-container>
          <el-aside width="700px">
              <el-container>
                <el-header height="30px" class="activity-header">{{ item.ActivityName }}</el-header>
                <el-footer class="ziti">签到时间：{{ item.ActivityTime }}</el-footer>
              </el-container>
          </el-aside>
          <el-main style="width:100px">
            <el-button type="primary" v-if="ShowButton(item)" @click="click(item,index)">签到</el-button>
          </el-main>
        </el-container>
      </div> 
    </el-card>  
  </li>  
</ul>
</template>

<script>
import axios from 'axios';
export default {  

data() {  
  return {  
    items: [],  
    serverItems: [],
    showdata:[],
    i:null,
    id:null,
    image:null,
    index:null,
    page:0,
    dialogTableVisible: false,  
  };  
},  
methods: {
  async submitData() {
    try {
      if(this.i==null){this.page += 1;   
      const storedData = localStorage.getItem('userData');  
      var data = JSON.parse(storedData).data.data;
      const response = await axios.post('/api/my_sc/register_data',{page:this.page,data:data});    
      if (response.data.info.PageList.TotalItems<10){
        this.i=0
      }
      this.load(response)
      }} catch (error) {  
      console.error("Error fetching data:", error);  
      this.$message({
                  message: "加载失败T^T",
                  type: "error",
                  showClose: true,
                });
    }
  },
  load(response) {  
  const serverItems = response.data.info.PageList.Items;  
  const newitems = serverItems.map((serverItem) => ({  
    ActivityName:serverItem.ActivityName,
    ActivityId:serverItem.ActivityId,
    ActivityTime:serverItem.ActivityTime,
    SignD:serverItem.SignD,
    }));
    this.items = this.items.concat(newitems);  
    ;  
  }, 
  convertStr(Time) {  
  const date = new Date(Time);  
  return date.getTime(); 
  },
  ShowButton(item){
    const timeStrings = item.ActivityTime.split('至');  
    const startTime = timeStrings[0].trim(); 
    const endTime = timeStrings[1].trim();   
    const startTimeStamp = this.convertStr(startTime);
    const endTimeStamp = this.convertStr(endTime);
    const Timestamp= Date.now();  
    if(item.SignD=='未签到'&&Timestamp>=startTimeStamp&&Timestamp<=endTimeStamp){
      return true
    }
    else{
      return false
    }
  },
  async click(item,index){
    this.id = item.ActivityId
    this.index = index
    const storedData = localStorage.getItem('userData');  
    var data = JSON.parse(storedData).data.data;
    const response = await axios.post('/api/my_sc/register',{id:this.id,data:data}); 
    console.log(response)
    if(response.data.msg == '签到成功'){
        this.$message({
                  message: "签到成功",
                  type: "success",
                  showClose: true,
                });
        this.items[this.index].SignD = '已签到'
      }
      else{
        this.$message({
                  message: "签到失败T^T" + "  " + JSON.parse(response.data.msg2).errmsg,
                  type: "error",
                  showClose: true,
                });
  }
    

  },
},
}
</script>




<style scoped>
.infinite-list {
height: 300px;
padding: 0;
margin: 0;
list-style: none;
}

.infinite-list .infinite-list-item {
display: flex;
align-items: center;
justify-content: center;
height: 87px;
background: var(--el-color-primary-light-9);
margin: 10px;
color: var(--el-color-primary);
}

.infinite-list .infinite-list-item + .list-item {
margin-top: 10px;
}

.el-button {  
transition: none !important; 
animation: none !important; 
}

.ziti{
  font-family: 	SimHei, Arial, sans-serif;  
  font-size: 15px;  
  color: #fba563;
  font-weight: 900;
}

.activity-header {  
  font-family: Arial, sans-serif;  
  font-size: 17px;  
  color: #3a3939;
}  

::v-deep .img {
padding: 3px 7px;
border-radius: 10px;
}
</style>