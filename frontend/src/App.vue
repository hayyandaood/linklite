<template>
  <Toaster position="bottom-right" />
  <div>
    <router-view />
  </div>
</template>


<script setup>
import { Toaster, toast } from 'vue-sonner';
import 'vue-sonner/style.css'
</script>