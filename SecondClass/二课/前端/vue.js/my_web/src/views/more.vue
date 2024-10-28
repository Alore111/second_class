<template>  
    
    <el-container>
        <el-aside width="250px"></el-aside>
        <el-main>
            <p>更多功能还在开发中。。。。</p>
            <el-button type="primary" plain @click="click">友情链接：学校的二课平台</el-button>
        </el-main>
        <el-aside width="300px"></el-aside>
    </el-container>
</template> 
    
<script>  
export default{
    methods:{
        click(){
            window.location.href = 'https://ywtb.cuit.edu.cn/#/login';
        }
    }
}
</script>  
    
<style scoped>  
  
</style>