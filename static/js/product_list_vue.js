


let vi = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    data: {

    },
    methods: {
        async deleteProduct(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`
            let result = await apiService(endpoint, 'DELETE');
            console.log(result);
            location.reload();
        }
    }
});


