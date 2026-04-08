<script lang="ts" setup>
import { ref, watch, h } from 'vue';
import Map from './MapSign.vue';
import { ElMessage, ElMessageBox } from 'element-plus';

const inputStyle = {
  width: '20em',
}

const coordinate = ref([120.128543,30.876596])
const placeholder = '点击地图选择坐标'
const display = ref(placeholder)
const buttonEnable = ref(false)

watch(coordinate, (newVal)=>{
  if (display.value===placeholder) {
    buttonEnable.value = true
  }
  display.value = transformC(newVal)
})

const transformC = (coordinate:number[]) => {
  return `${coordinate[0]},${coordinate[1]}`
}

const handleSignIn = async () => {
  buttonEnable.value = false
  const data = {
    latitude: coordinate.value[1],
    longitude: coordinate.value[0],
  }
  fetch('/api/signin', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data)
  }).then((response)=>{
    buttonEnable.value = true
    return response.json()
  }).then((data)=>{
    if (data.success) {
      ElMessage({
        message: data.message ?? "签到成功",
        type: "success",
      })
      if (data.data) {
        const info = data.data
        ElMessageBox({
          title: data.message ?? "签到成功",
          message: h('div', null, [
            h('div', null, `用户：${info.username}`),
            h('div', null, `课程：${info.courseName} 第${info.period}节`),
            h('div', null, `时间：${new Date(info.checkinTime).toLocaleString()}`),
          ])
        })
      }
    } else {
      ElMessage({
        message: data.message ?? "签到失败",
        type: "error",
      })
    }
  })
}

</script>

<template>
  <div class="signin-outer">
    <Map v-model="coordinate" />
    <div class="coordinate-line">
      <el-icon><Location /></el-icon>
      <el-input placeholder="坐标" v-model="display" :style="inputStyle" disabled />
    </div>
    <el-button type="primary" :disabled="!buttonEnable" @click="handleSignIn">签到</el-button>
  </div>
</template>

<style>
  .signin-outer {
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    justify-content: space-between;
  }
  .coordinate-line {
    display: flex;
    align-items: center;
    gap: 8px;
    justify-content: space-between;
  }
</style>