<template>  
  <ul v-infinite-scroll="submitData" class="infinite-list" style="overflow: auto; height: 500px;">  
    <li v-for="item,index in items"  class="infinite-list-item">  
      <el-card style="width: 100%;height: 88px;" shadow="hover" class="card" :body-style="{ display: 'flex', padding: '7px ' }" @click="Click(clickdata(item,index))">  
        <div class="common-layout">
          <el-container>
            <el-container>
              <el-aside width="100px" style="min-height:10vh;border-radius: 10px;border-bottom-right-radius: 10px;">
                <img  
                  :src="item.ShowImges"
                  style="width: 100%;  height: 70px; "  
                  class="img"  
                /> </el-aside>
              <el-container>
                <el-main style="width:700px;">
                  <el-container >
                    <el-header height="25px" class="activity-header">{{ item.ActivityName }}</el-header>
                    <el-footer height="27px" class="code">{{ item.ActScore }}分</el-footer>
                  </el-container>
                </el-main>
                <el-aside width="100px"></el-aside>
              </el-container>
            </el-container>
          </el-container>
        </div> 
      </el-card>  
    </li>  
  </ul>
  <el-dialog v-model="dialogTableVisible" title="活动详情" width="800" :lock-scroll="false" style="overflow: hidden !important;">
    <div class="common-layout">
    <el-container>
      <el-aside style="width: 430px;">
        <el-table :data="showdata" style="width: 100%">  
          <el-table-column prop="key" width="110"></el-table-column>  
          <el-table-column prop="value" width="315"></el-table-column>  
        </el-table> 
      </el-aside>
      <el-main style= "width:100px; height:350px;" >
        <img  
            :src="this.image"
            style="width: 75%;  height: 98%; margin-left: 40px;"
                />
      </el-main>
    </el-container>
    <el-container>
        <el-footer style="height: 30px; display: flex; align-items: center; justify-content: center;">
          <el-button :type="choose1()"  @click="post(choose2())">{{ choose2() }}</el-button>
        </el-footer>
      </el-container>
  </div>
    
    
  </el-dialog>  
</template> 

<script>  

import axios from 'axios';
export default {  
  data() {  
    return {  
      items: [],  
      serverItems: [],
      showdata:[],
      id:null,
      image:null,
      index:null,
      page:1,
      dialogTableVisible: false,  
      carddata: null,
      StatusName:null,
    };  
  },  
  methods: {
    async submitData() {
      try {
        var storedData = localStorage.getItem('userData');  
        var data = JSON.parse(storedData).data.data
        const response = await axios.post('/api/choose/sc_data',{page:this.page,data:data});  
        this.load(response.data)
        this.page += 1;
      } catch (error) {  
        console.error("报错", error);
        
      }
    },

  Click(data) {
    this.showdata = this.show(data)
    this.dialogTableVisible = true; 
  },

  clickdata(item,index){
    this.image = item.ShowImges
    this.id = item.Id
    this.StatusName = item.StatusName
    this.index = index
    const data = {    
      '活动名称：': item.ActivityName,
      '活动类型：': item.ActivityType,
      '活动时间：': item.ActivityTime,
      '承办单位：': item.SponsorNames,
      '所属模块：': item.ModuleCode,
      '活动地点：': item.ActivityAddress,
      '人数限制：': item.LimitStuNumber,
      '报名时间：': item.StuTime,
  }
  return data
  },
  show(data) {  
    return Object.entries(data).map(([key, value]) => ({  
      key: key,  
      value: value  
    }));  
  }, 

  load(data) {  
      if (!data) {  
        console.error('No data provided to load method.');  
        return; 
    }  
    if (!data.info) {  
        console.error('Data does not contain an info property.');  
        return; 
      }
    const list = data.info.List;  
    if (!list) {  
        console.error('Data.info does not contain a List property.');  
        return; 
    }  
    const serverItems = list.Items;  
    if (!serverItems) {  
        console.error('Data.info.List does not contain an Items property.');  
        return; 
    }  
        const newitems = serverItems.map((serverItem) => ({  
            Id: serverItem.Id, 
            ShowImges: serverItem.ShowImges,  
            ActivityName: serverItem.ActivityName,
            ActivityTime: serverItem.ActivityTime, 
            ActivityType:serverItem.ActivityType,
            SponsorNames:serverItem.SponsorNames,
            ResponsiblePerson:serverItem.ResponsiblePerson,
            ActScore:serverItem.ActScore,
            StuTime:serverItem.StuTime,
            LimitStuNumber:serverItem.LimitStuNumber,
            ActivityAddress:serverItem.ActivityAddress,
            ModuleCode:serverItem.ModuleCode,
            StatusName:serverItem.StatusName
          }));
          this.items = this.items.concat(newitems);  
      ;  
  }, 
  choose1(){
    if(this.StatusName=="已报名"||this.StatusName=="不可报名"){
      return "info"
    }
    return "primary"
  },
  choose2(){
    if(this.StatusName=="已报名"){
      return "已报名"
    }
    if(this.StatusName=="不可报名"){
      return "不可报名"
    }
    return "点击申报"
  },
  async post(pd){
    if(pd=="已报名"){
      this.$message({
                  message: "你已经报过名啦",
                  type: "error",
                  showClose: true,
                });
    }
    if(pd=="不可报名"){
      this.$message({
                  message: "此活动不可报名",
                  type: "error",
                  showClose: true,
                });
    }
    else{
      var storedData = localStorage.getItem('userData');  
      var data = JSON.parse(storedData).data.data;
      const response = await axios.post('/api/choose/choose',{id:this.id,data:data},{  
    headers: {  
        'Content-Type': 'application/json'  
    }  
});
      console.log(response)
      if(response.data.return_data == '{"errcode":0,"errmsg":"操作成功!"}'){
        this.$message({
                  message: "报名成功",
                  type: "success",
                  showClose: true,
                });
        this.StatusName = "已报名"; 
        this.items[this.index].StatusName = '已报名'
      }
      else{
        this.$message({
                  message: "报名失败，请联系开发人员",
                  type: "error",
                  showClose: true,
                });
      }
    }
  }
  }  
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

.activity-header {  
  font-family: Arial, sans-serif;  
  font-size: 17px;  
  color: #3a3939;
}  

.code {  
  font-family: 	SimHei, Arial, sans-serif;  
  font-size: 18px;  
  color: #fe882d;
  font-weight: 900;
}  

::v-deep .img {
padding: 3px 7px;
border-radius: 10px;
}
</style>