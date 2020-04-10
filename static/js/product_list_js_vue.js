


let vi = new Vue({
    delimiters: ['{', '}'],
    el: '#app-list',
    data: {
        modelsList: [],
        part: []
    },
    methods: { //Method will update product inline on product list page
        async deleteProduct(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            let result = await apiService(endpoint, 'DELETE');
            location.reload();
        },
        async loadProducts(category) {
            const endpoint = `${ApplicationMainHost}/api/product/list/?category=${category}`;
            let result = await apiService(endpoint);
            this.part = result;
            console.log(this.part);
        },
    },
    
    created() {
        this.loadProducts([2002,2003,2004,2005])
    }
});


