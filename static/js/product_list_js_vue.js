

Vue.use(VueToast);
Vue.component('vue-multiselect', window.VueMultiselect.default);

let vi = new Vue({
    delimiters: ['{', '}'],
    el: '#app-list',
    data: {
        value: [],
        selectCarModelList: [],
        formBrand: [],
        modelsList: [],
        part: [],
        product: null,
        value: '',
        options: [
            { name: 'Vue.js', language: 'JavaScript' },
            { name: 'Rails', language: 'Ruby' },
            { name: 'Sinatra', language: 'Ruby' },
            { name: 'Laravel', language: 'PHP' },
            { name: 'Phoenix', language: 'Elixir' }
        ]
    },
    filters: {
        capitalize: function (value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        }
    },
    methods: { //Method will update product inline on product list page

        async getSelectCarModelList(id=1) {

            const endpoint = `${ApplicationMainHost}/api/product/selectlistcarmodel/${id}/`;
            const data = await apiService(endpoint);
            this.selectCarModelList = data;
        },

        
        async getSelectBrandsList() {
            let localstor;
            let dif = 0;
            let newTimestamp = new Date().getTime();
            if (localStorage.getItem('key') != null) {
                localstor = JSON.parse(localStorage.getItem("key"));
                dif = (newTimestamp - localstor.timestamp) / 1000 / 60;
            }
            console.log(dif)
            if (dif > 30) {
                const endpoint = `${ApplicationMainHost}/api/product/selectlistbrands/`;
                const data = await apiService(endpoint);
                this.selectBrandList = data;
                this.options = data;
                localstor = {
                    options: this.options,
                    timestamp: new Date().getTime()
                }
                localStorage.setItem("key", JSON.stringify(localstor));
            } else {
                this.options = JSON.parse(localStorage.getItem("key")).options;
            }


        },
        errorToast(message) {
            this.$toast.open({
                message: message,
                type: 'error',
                position: 'top-right'
            })
        },
        successToast(message) {
            this.$toast.open({
                message: message,
                type: 'success',
                position: 'top-right'
            })
        },
        async deleteProduct(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            let result = await apiService(endpoint, 'DELETE');
            location.reload();
        },
        async getPartCarModel(id_list, i) { //Gettin car model list for specific car part
            const endpoint = `${ApplicationMainHost}/api/product/selectpartcarmodel/?pk=${id_list}`;
            const data = await apiService(endpoint);
            this.part[i].car_model = [{'id': data.id, 'name': data.name }];
            
        },
        async loadProducts(category) {
            const endpoint = `${ApplicationMainHost}/api/product/list/?category=${category}`;
            let result = await apiService(endpoint);
            this.part = result;

            this.part.forEach((element, index) => {
                brand = this.options.filter(obj => {
                    return obj.id === element.brand;
                })
                this.part[index].brand = brand;
            });
            // Adding car models to v-model
            this.part.forEach((element, index) => {
                let c_l = []
                element.car_model.forEach((e,i) => {
                    let v = this.selectCarModelList.find(obj=> obj.id === e);
                    c_l.push(v);
                })
                this.part[index].car_model = c_l;
            });

        },
        async saveProduct(id, i) {
            // Отправляем основные данные на сервер
            // Needs to make API and Login in Vue -- Here
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            let cl = [];
            this.part[i].car_model.forEach(e=>{
                cl.push(e.id);
            });
            const data = {
                name: this.part[i].name,
                name2: this.part[i].name2,
                cat_number: this.part[i].cat_number,
                brand: this.part[i].brand.id,
                car_model: cl,
                unit: this.part[i].unit,
                engine: this.part[i].engine
            }
            //console.log(JSON.stringify(data));
            let response = await apiService(endpoint, 'PUT', data);
            if (response) {
                this.successToast('Товар сохранен!');
            }
            else {
                this.errorToast('Ошибка сохранения товара!');
            }
            //window.location.href = `${ApplicationMainHost}/product/`
        },






    },

    created() {
        this.loadProducts([2002, 2003, 2004, 2005]);
        this.getSelectBrandsList();
        this.getSelectCarModelList(1);

    },
    mounted() {

    }
});


