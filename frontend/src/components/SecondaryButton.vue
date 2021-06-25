<template>
       <button
          class="text-white  bg-primary p-2 text-3xl transition duration-500" ref="button">
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