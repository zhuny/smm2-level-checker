<template lang="pug">
div.w-full.relative.input-box
  .horizontal-line
  div.value-wrapper
    div.value-container(:style="{right: `${gap}px`}")
      div.left-value(:style="{left: `${ratioLeft}%`}")
        .range-left-arrow(@click="moveStartLeft" v-if="isStartInner") &#x25C0;
        .value {{ thisRangeStart }}
        .range-right-arrow(@click="moveStartRight" v-if="isInterval") &#x25B6;
    div.value-container(:style="{left: `${gap}px`}")
      div.right-value(:style="{right: `${ratioRight}%`}")
        .range-left-arrow(@click="moveEndLeft" v-if="isInterval") &#x25C0;
        .value {{ thisRangeEnd }}
        .range-right-arrow(@click="moveEndRight" v-if="isEndInner" ) &#x25B6;
</template>

<script>
export default {
  name: "NumberRangeInput",
  data() {
    return { gap: 28 };
  },
  props: {
    minValue: {
      type: Number,
      default: 0,
    },
    maxValue: {
      type: Number,
      required: true,
    },
    rangeStart: Number,
    rangeEnd: Number,
  },
  trims: ["update:rangeStart", "update:rangeEnd"],
  computed: {
    thisRangeStart: {
      get() {
        return this.rangeStart ?? this.minValue;
      },
      set(value) {
        this.$emit("update:rangeStart", value);
      },
    },
    thisRangeEnd: {
      get() {
        return this.rangeEnd ?? this.maxValue;
      },
      set(value) {
        this.$emit("update:rangeEnd", value);
      },
    },
    rangeValue() {
      return this.maxValue - this.minValue;
    },
    ratioLeft() {
      return ((this.thisRangeStart - this.minValue) * 100) / this.rangeValue;
    },
    ratioRight() {
      return ((this.maxValue - this.thisRangeEnd) * 100) / this.rangeValue;
    },
    isInterval() {
      return this.thisRangeStart !== this.thisRangeEnd;
    },
    isStartInner() {
      return this.minValue < this.thisRangeStart;
    },
    isEndInner() {
      return this.thisRangeEnd < this.maxValue;
    },
  },
  methods: {
    moveStartLeft() {
      this.thisRangeStart--;
    },
    moveStartRight() {
      this.thisRangeStart++;
    },
    moveEndLeft() {
      this.thisRangeEnd--;
    },
    moveEndRight() {
      this.thisRangeEnd++;
    },
  },
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

  .value-wrapper {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 12px;
    right: 12px;
  }

  .value-container {
    position: absolute;
    top: 50%;
    height: 0;
    left: 0;
    right: 0;
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
    .value,
    .range-left-arrow,
    .range-right-arrow {
      position: absolute;
      top: -12px;
      width: 24px;
      height: 24px;
      text-align: center;
    }

    .value {
      left: -12px;
      text-align: center;
      border: 2px solid yellow;
      box-sizing: border-box;
      border-radius: 4px;
      background-color: lightyellow;
    }

    .range-left-arrow {
      left: -33px;
    }

    .range-right-arrow {
      left: 9px;
    }
  }
}
</style>
