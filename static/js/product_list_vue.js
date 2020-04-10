


let vi = new Vue({
    delimiters: ['{', '}'],
    el: '#app-list',
    data: {
        modelsList: []
    },
    methods: { //Method will update product inline on product list page
        async deleteProduct(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            let result = await apiService(endpoint, 'DELETE');
            location.reload();
        }
    }
});


