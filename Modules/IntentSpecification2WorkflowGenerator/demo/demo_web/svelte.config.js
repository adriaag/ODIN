import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'

export default {
  // Consult https://svelte.dev/docs#compile-time-svelte-preprocess
  // for more information about preprocessors
  preprocess: vitePreprocess(),
  server: {
    fs: {
      allow: ['node_modules']
    }
  },
  optimizeDeps: {
    include: ['@smui-extra/autocomplete']  // Include the library in optimized deps
  }
}
