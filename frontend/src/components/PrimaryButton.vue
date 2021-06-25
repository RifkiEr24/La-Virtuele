<template>
       <button
          class="border-primary border  p-3 transition duration-500 hover:bg-primary hover:rounded-xl hover:text-white px-16">
          {{btnText}}
          </button>
</template>

<script>
export default {
props: ['btnText']
}
</script>

<style>

</style>