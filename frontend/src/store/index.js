import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';
import data from './../api/api-endpoint.js'
Vue.use(Vuex, axios)

export default new Vuex.Store({
  state: {
    allProduct:[],
    featuredProduct:[],
    category:[],
    detailProduct:{},
  },
  mutations: {
    SET_FEATURED_PRODUCT(state, product){
      state.featuredProduct = product;
    },
    SET_DETAILED_PRODUCT(state, product){
      state.detailProduct = product;
    },
    SET_CATEGORY_LIST(state, category){
      state.categoryList = category;
    }
  },
  actions: {
    fetchFeaturedProduct({commit},) {
      axios
          .get(data.featured)
          .then(response => {
              let product = response.data;
              product.forEach(element => {
                if (element.model[0] == undefined) {
                  element.model.push(element.gallery[0]);
                }
              });
              console.log(product);
              commit('SET_FEATURED_PRODUCT', product);
          })
          .catch(error => {
              console.log(error)
          })
  },
  fetchDetailedProduct({commit}, slug) {
    axios
        .get(data.detail(slug))
        .then(response => {
            let product = response.data;
            commit('SET_DETAILED_PRODUCT', product);
        })
        .catch(error => {
            console.log(error)
        })
  },
  fetchCategoryList({commit}) {
    axios
        .get(data.categoryList)
        .then(response => {
            let category = response.data;
            commit('SET_CATEGORY_LIST', category);
        })
        .catch(error => {
            console.log(error)
        })
  },
  },
  modules: {
  }
})
