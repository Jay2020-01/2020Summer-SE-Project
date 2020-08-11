<template>
<div>
<editor v-model="content" ></editor>
</div>
    
</template>

<script>
import editor from './EditorComponent';
export default {
  components: {
    editor
  },
  data() {
      return {
          content: ''
      }
  }
}
</script>