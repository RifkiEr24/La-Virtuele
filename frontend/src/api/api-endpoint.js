
const baseUrl = `http://la-virtuele.harizmunawar.repl.co/api/v1`;
const API_ENDPOINT = {
    productlist :  `${baseUrl}/products/`,
    detail: (slug) => `${baseUrl}/product/${slug}`,
    featured : `${baseUrl}/products?featured=true`,
    category : (category) => `${baseUrl}/products?category=${category}`,
    categoryList: `${baseUrl}/categories/`,
  };
  
  export default API_ENDPOINT;