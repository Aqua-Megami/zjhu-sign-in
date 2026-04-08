<script lang="ts" setup>
import { Map, View } from "ol";
import * as olProj from "ol/proj";
import TileLayer from "ol/layer/Tile";
import XYZ from "ol/source/XYZ";
import { ref, onMounted, nextTick } from "vue"
import { wgs84togcj02, gcj02towgs84 } from '../tools/coordinates'

import { ElIcon } from 'element-plus'
import { LocationFilled } from '@element-plus/icons-vue'
import Overlay from 'ol/Overlay'

const mapContainer = ref<HTMLDivElement | null>(null)
const markerContainer = ref<HTMLDivElement | null>(null)
const coordinate = defineModel<number[]>({required: true})
let map: Map | null = null
let markerOverlay: Overlay | null = null

onMounted(() => {
  nextTick(() => {
    if (mapContainer.value) {
      map = new Map({
        target: mapContainer.value,
        layers: [
          new TileLayer({
            source: new XYZ({
              url: 'https://webst01.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'
            })
          }),
        ],
        view: new View({
          center: olProj.fromLonLat(wgs84togcj02(coordinate.value[0], coordinate.value[1])),
          zoom: 18,
        }),
        controls: []
      });

      // 创建 Overlay 用于显示图标
      if (markerContainer.value) {
        // 设置 markerContainer 的 transform 以保证居中
        markerContainer.value.style.transform = 'translate(-50%, -50%)';
        markerOverlay = new Overlay({
          element: markerContainer.value,
          positioning: 'bottom-center',
          stopEvent: false,
        });
        map.addOverlay(markerOverlay);
        markerContainer.value.style.display = 'none'; // 初始不显示
      }

      map.on('click', function (evt) {
        if (!markerOverlay || !markerContainer.value) {return}
        const coord_gcj = olProj.toLonLat(evt.coordinate);
        const coord_wgs = gcj02towgs84(coord_gcj[0], coord_gcj[1]);
        coordinate.value = [parseFloat(coord_wgs[0].toFixed(7)), parseFloat(coord_wgs[1].toFixed(7))];
        markerOverlay.setPosition(evt.coordinate);
        markerContainer.value.style.display = ''
      });
    }
  });
});
</script>

<template>
  <div class="map-outer">
    <div ref="mapContainer" class="map-home"></div>
    <!-- marker overlay -->
    <div ref="markerContainer" style="position:absolute;z-index:10;pointer-events:none;">
      <el-icon style="font-size:32px;color:#f56c6c;">
        <LocationFilled />
      </el-icon>
    </div>
  </div>
</template>

<style>
.map-home {
  width: 100vw;
  height: 80vh;
}
</style>