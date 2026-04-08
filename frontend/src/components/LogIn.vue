<script lang="ts" setup>
import { reactive } from 'vue';
import { ElMessage } from 'element-plus';

const isLogin = defineModel<boolean>({default: false})
const loginInfo = reactive({username: '', password: ''})

const inputStyle = {
  width: '10em',
}
const handleLogin = async ()=> {
  if (isLogin.value) {return}
  fetch('/api/login', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(loginInfo)
  }).then((response)=>{
    return response.json()
  }).then((data)=>{
    if (data.success) {
      isLogin.value = true
      ElMessage({
        message: data.message ?? "登录成功",
        type: "success",
      })
    } else {
      ElMessage({
        message: data.message ?? "登录失败",
        type: "error",
      })
    }
  })
}
</script>

<template>
  <div class="login-outer">
    <div class="title">湖师信工远程签到器</div>
    <el-input :style="inputStyle" placeholder="账号" v-model="loginInfo.username" />
    <el-input :style="inputStyle" placeholder="密码" v-model="loginInfo.password" type="password" clearable />
    <el-button round type="primary" @click="handleLogin">登录</el-button>
  </div>
</template>

<style>
  .login-outer {
    margin: 1em;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    justify-content: space-between;
  }
  .title {
    font-weight: bold;
    font-size: large;
  }
</style>