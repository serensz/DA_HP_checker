import { svelte } from '@sveltejs/vite-plugin-svelte'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [svelte()],
  base: '/DA_HP_checker/',   // 👈 ชื่อ repo ต้องตรงเป๊ะ
})
