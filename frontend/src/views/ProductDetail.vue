<template>
  <div class="container mx-auto">
      <div class="flex -mx-2">
          <div class="w-4/12 px-2">
                b
          </div>
           <div class="w-4/12 px-2">
                b
          </div>
           <div class="w-4/12 px-2">
                b
          </div>
      </div>
      <h1 class="text-5xl font-bold header text-graysecondary tracking-wide">{{product.product}}</h1>
      <p class="text-primary  text-xl font-semibold">Rp {{product.price}}</p>
  </div>
</template>

<script>
export default {
data(){
    return{
      product:{}
    }
  },
  created(){
      this.axios.get(`http://la-virtuele.harizmunawar.repl.co/api/v1/products/${this.$route.params.id}/`).then((response) => {
        this.product=response.data;
        console.log(this.product.product);
      })
  },
}
</script>

<style>

</style>