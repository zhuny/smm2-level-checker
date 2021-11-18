<template lang="pug">
div.w-full.relative.input-box
  .horizontal-line
  div.left-value
    .value 3
  div.right-value
    .value 5
</template>

<script>
export default {
  name: "NumberRangeInput",
};
</script>

<style scoped lang="scss">
.input-box {
  height: 32px;
  position: relative;

  .horizontal-line {
    position: absolute;
    top: 12px;
    bottom: 12px;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.2);
  }

  .left-value {
    position: absolute;
    left: 10%;
    top: 50%;
  }

  .right-value {
    position: absolute;
    right: 30%;
    top: 50%;
  }

  .left-value,
  .right-value {
    .value {
      width: 24px;
      height: 24px;
      text-align: center;
      border: 2px solid yellow;
      box-sizing: border-box;
      border-radius: 4px;
      transform: translate(-50%, -50%);
      background-color: lightyellow;
    }
  }
}
</style>
