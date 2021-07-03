<template>
       <button
          class="text-white  d-flex bg-primary p-2 header text-3xl transition duration-500" ref="button">
          </button>
</template>

<script>
export default {
props: ['btnText'],
mounted(){
    this.$refs.button.innerHTML=this.btnText;
}
}
</script>

<style>

</style>