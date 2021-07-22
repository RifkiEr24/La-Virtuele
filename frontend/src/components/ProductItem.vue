<template>
  <div class="product-card" >
    <div class="img-card relative ">
      <div class="content-details fadeIn-top z-10">
        <button @click="$router.push({name: 'details', params: { id: slugProduct },})" class="bg-white text-3xl p-2 rounded-lg mx-2">
          <span class="iconify" data-icon="carbon:zoom-pan" data-inline="false"></span>
        </button>
        <button class="bg-primary text-3xl p-2 rounded-lg mx-2">
          <span class="iconify text-white" data-icon="carbon:shopping-cart-plus"
            data-inline="false"></span>
        </button>
      </div>
      <div class="img-overlay bg-secondary h-full absolute w-full "></div>
              <img :src="`https://la-virtuele.harizmunawar.repl.co${imageProduct}`|| 'default.jpg'" class="w-full img-product" >

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
      slugProduct:{
                type: String,
    required:true
      },
    imageProduct:{
        type: String,
        required:true
    },
    nameProduct:{
        required:true
    },
    priceProduct:{
        type: String,
        required:true
    },
},
methods:{
}
}
</script>
<style scoped lang="postcss">
.img-overlay{
  background: rgba(0,0,0,0.7);
  position: absolute;
  height: 100%;
  width: 100%;
  left: 0;
  top: 0;
  bottom: 0;
  opacity: 0;
  right: 0;
  -webkit-transition: all 0.4s ease-in-out 0s;
  -moz-transition: all 0.4s ease-in-out 0s;
  transition: all 0.4s ease-in-out 0s;
}
.img-card:hover .img-overlay{
  opacity: 0.75;
}
.content-details {
  position: absolute;
  text-align: center;
  padding-left: 1em;
  padding-right: 1em;
  width: 100%;
  left: 50%;
  opacity: 0;
  -webkit-transform: translate(-50%, -50%);
  -moz-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  -webkit-transition: all 0.3s ease-in-out 0s;
  -moz-transition: all 0.3s ease-in-out 0s;
  transition: all 0.3s ease-in-out 0s;
}
.img-card:hover .content-details{
  top: 85%;
  left: 50%;
  opacity: 1;
}
.fadeIn-top{
  top: 100%;
}
.shape-identify{
  transition: margin 1s linear;
    transition: 750ms;
}
.shape-identify#featured-button {
  left: 0;
  /* transform: translateX(-50%); */
}

.shape-identify#new-arrival-button {
  left: 100%;
  transform: translateX(-100%);
}
.img-product{
  height: 400px;
  object-fit: cover;
}
</style>