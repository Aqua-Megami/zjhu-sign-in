<script setup lang="ts">
import LogIn from './components/LogIn.vue';
import SignIn from './components/SignIn.vue';
import { ref } from 'vue';
import { ElMessage } from 'element-plus';

const isLogin = ref<boolean>(false)
fetch('/api/hasLogin', {method:'POST'}).then(
    (response)=>(response.json())
  ).then((data)=>{
    if (data.hasLogin) {
      ElMessage({
        message: "成功读取登录信息",
        type: "success",
      })
      isLogin.value = true
    } else {
      ElMessage({
        message: data.message ?? "未登录，请登录",
        type: "error",
      })
    }
  }
)


</script>

<template>
  <LogIn v-if="!isLogin" v-model="isLogin" />
  <SignIn v-else />
</template>

