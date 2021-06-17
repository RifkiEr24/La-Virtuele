<template>
  <div >
    <div class="img-card relative ">
      <div class="content-details fadeIn-top z-10">
        <button class="bg-white text-3xl p-2 rounded-lg mx-2">
          <span class="iconify" data-icon="carbon:zoom-pan" data-inline="false"></span>
        </button>
        <button class="bg-primary text-3xl p-2 rounded-lg mx-2">
          <span class="iconify text-white" data-icon="carbon:shopping-cart-plus"
            data-inline="false"></span>
        </button>
      </div>
      <div class="img-overlay bg-secondary h-full absolute w-full "></div>
      <img :src="getImgUrl(imageProduct)" class="w-full" alt="">

    </div>

    <p class="font-light mt-3">{{nameProduct}}</p>
    <p class="font-semibold">{{priceProduct}}</p>
  </div>
</template>

<script>
export default {
    data(){
        return {
    publicPath: process.env.BASE_URL
  }
    },
props:{
    imageProduct:{
        type: String,
        required:true
    },
    nameProduct:{
        type: String,
        required:true
    },
    priceProduct:{
        type: String,
        required:true
    },
},
method:{
    getImgUrl(pic) {
    return require('../assets/img/'+pic)
}
}
}
</script>

<style>

</style>