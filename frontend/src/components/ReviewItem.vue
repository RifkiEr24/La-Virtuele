<template>
  <div class="flex -mx-2">
   <img class="profile-img px-2" src="@/assets/img/2.png" alt="">
   <div class=" border-2  border-black w-full">
    <div class="bg-secondary w-full flex justify-between">
        <p class="header text-white text-3xl pl-2 p-1">Ahmad Wahyu</p>
        <p class="text-white p-1">30 June 2021</p>
    </div>
    <div class="review-text p-4">
        <div class="flex gap-1">
            <span class="iconify" data-icon="ant-design:star-filled" data-inline="false"></span>
            <span class="iconify" data-icon="ant-design:star-filled" data-inline="false"></span>
            <span class="iconify" data-icon="ant-design:star-filled" data-inline="false"></span>
            <span class="iconify" data-icon="ant-design:star-filled" data-inline="false"></span>
            <span class="iconify" data-icon="ant-design:star-filled" data-inline="false"></span>
        </div>
        <p class="mt-3">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in</p>
    </div>
   </div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="postcss" scoped>
.profile-img{
    @apply w-20;
    @apply h-20;
    @apply object-cover;
}
</style>
