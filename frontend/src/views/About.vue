<template>
  <div class="container mx-auto">
    <div class="flex -mx-2">
      <div class="w-3/12">
        <h2 class="header text-2xl">Filter</h2>
        <bordered-heading class="mt-5" :headingText="'Categories'"/>
        <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
           <bordered-heading class="mt-5" :headingText="'Categories'"/>
        <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
           <bordered-heading class="mt-5" :headingText="'Categories'"/>
        <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
             <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
      </div>
         <div class="w-9/12 flex px-2 -mx-2">
     <div class="w-6/12 md:w-4/12  px-2" v-for="item in productlist" :key="item.id">
              <product-item :slug-product="item.slug" :image-product="item.model[0].image || 'a'" :name-product="item.name"
                :price-product="`Rp ${item.price}`" />
            </div>
      </div>
    </div>
  </div>
</template>
<script>
import BorderedHeading from '../components/BorderedHeading.vue'
import ProductItem from '../components/ProductItem.vue'

export default {
  components: {
    BorderedHeading,
    ProductItem
 
  },
   data(){
    return{
      productlist:[],
    }
   },
     created(){
      this.axios.get('https://la-virtuele.harizmunawar.repl.co/api/v1/products/').then((response) => {
        this.productlist=response.data;
        console.log(this.productlist[0].slug);
        this.productlist.forEach(element => {
          if(element.model[0] == undefined ){
            element.model.push(element.gallery[0]);
          }
        });
      })
  }
}
</script>
<style scoped lang="postcss">
.container {
  display: block;
  position: relative;
  padding-left: 35px;
  font-size: 18px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default checkbox */
.container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  border: 2px solid black;
  background-color: transparent;
}

/* On mouse-over, add a grey background color */
.container:hover input ~ .checkmark {
}

/* When the checkbox is checked, add a blue background */
.container input:checked ~ .checkmark {
  @apply bg-primary;
  @apply border-primary;  
}

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.container input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}
</style>