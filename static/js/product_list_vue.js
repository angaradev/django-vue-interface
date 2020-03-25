


let vi = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    data: {
        modelsList: []
    },
    methods: {
        async deleteProduct(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`
            let result = await apiService(endpoint, 'DELETE');
            location.reload();
        }
    },
    async getModelsForMenu(id) {
        const endpoint = `${ApplicationMainHost}/api/product/selectlistcarmodel/${id}/`
        let result = await apiService(endpoint, 'DELETE');
        result = this.modelsList;
        console.log(this.modelsList);
    }
});


