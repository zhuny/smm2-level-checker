<template lang="pug">
div
  button.bg-purple-300.px-4.py-2.text-white.rounded-3xl(@click="getRandomLevel") 랜덤 맵 가져오기
</template>

<script>
export default {
  name: "Home",
  methods: {
    getRandomLevel() {
      console.log("HI");
    },
  },
};
</script>
