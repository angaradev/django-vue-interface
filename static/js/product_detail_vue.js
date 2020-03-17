function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var CSRF_TOKEN = getCookie('csrftoken');
//import { CSRF_TOKEN } from './api.token';
async function getJSON(response) {
    if (response.status === 204) return '';
    return response.json()
}
function apiService(endpoint, method, data) {
    const config = {
        method: method || 'GET',
        body: data !== undefined ? JSON.stringify(data) : null,
        headers: {
            'content-type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        }
    }
    return fetch(endpoint, config)
        .then(getJSON)
        .catch(error => console.log(error));
}
//##########################################################//
//############### VUE PART STARTS HERE #####################//
//##########################################################//
const vsel = Vue.component('v-select', VueSelect.VueSelect);
const app = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    data: {
        part: {
            id: null,
            one_c_id: 0,
            name: 'Part Name From Vue',
            cat_number: '',
            category: '',
            brand: 1,
            car_model: {
                name: '',
                carmake: {
                    country: {}
                }
            },
            unit: null,
            engine: '',
            active: true,
            engine: {}
        },
        selectUnitList: [],
        selectBrandList: [],
        selectedUnitId: null,
        selectedBrandId: null,
        selectedWhatchUnit: null
    },
    computed: {
        selectedUnit: {
            get() {
                if (this.selectedUnitId) {
                    let s = this.selectedUnitId;
                    return s;
                } else {
                    let result = this.selectUnitList.filter(a => {
                        return a.id == this.part.unit
                    });
                    return result
                }
            },
            set(val) {
                this.selectedUnitId = val;
            },
        },
        selectedBrand: {
            set(val) {
                this.selectedBrandId = val;
            },
            get() {
                if (this.selectedBrandId) {
                    return this.selectedBrandId;
                }
                let result = this.selectBrandList.filter(a => {
                    return a.id == this.part.brand
                });
                return result
            }
        }
    },
    methods: {
        async editPart() {
            // Отправляем основные данные на сервер
            // Needs to make API and Login in Vue -- Here
            endpoint = `http://localhost:8000/api/product/detail/${this.part.id}/`;

            //Логика: Если есть выбранный бренд или ед изм то отправляем их
            //или дефолтовые значения
            if(!this.selectedUnitId){
                unitId = this.part.unit;
            }else{
                unitId = this.selectedUnitId.id;
            }
            if(!this.selectedBrandId){
                brandId = this.part.brand;
            }else{
                brandId = this.selectedBrandId.id;
            }

            const data = {
                one_c_id: Number(this.part.one_c_id),
                name: this.part.name,
                cat_number: this.part.cat_number,
                brand: brandId,
                car_model: {
                    name: this.part.car_model.name
                },
                unit: unitId,
                active: this.part.active,
                engine: {
                    name: this.part.engine.name
                }
            }
            //console.log(JSON.stringify(data));
            const response = await apiService(endpoint, 'PUT', data);
            console.log(response)
        },
        async getPart(id) {
            endpoint = `http://localhost:8000/api/product/detail/${id}/`;
            const data = await apiService(endpoint);
            this.part = data;
        },
        async getSelectUnitList() {
            endpoint = `http://localhost:8000/api/product/selectlistunits/`;
            const data = await apiService(endpoint);
            this.selectUnitList = data;
        },
        async getSelectBrandsList() {
            endpoint = `http://localhost:8000/api/product/selectlistbrands/`;
            const data = await apiService(endpoint);
            this.selectBrandList = data;
        }
    },
    // beforeMount() {
    //     this.part.id = document.getElementById('mainId').getAttribute('token') || '';
    // },
    async created() {
        this.getSelectUnitList();
        this.getSelectBrandsList();
        const id = document.getElementById('mainId').getAttribute('token') || '';
        await this.getPart(15);
    },
    mounted() {
    }
});
