// Have to collect settings in separate file later
settings = {
    defaultUnitId: 1,
    defaultUnitName: 'шт'
}

// File for creating new product

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
            name: null,
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
        selectCarModelList: [],
        selectUnitList: [],
        selectBrandList: [],
        selectCarEngineList: [],
        selectedUnitId: null,
        selectedBrandId: null,
        selectedCarModelId: null,
        selectedCarEnginelId: null,
        sessionCountry: null,
        sessionCarMake: null
    },
    computed: {

        selectedUnit: {
            get() {
                if (this.selectedUnitId) {
                    let s = this.selectedUnitId;
                    return s;
                } else {
                    let result = this.selectUnitList.filter(a => {
                        return a.id == settings.defaultUnitId;
                    });
                    return result;
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
                return result;
            }
        },
        selectedCarModel: {
            set(val) {
                this.selectedCarModelId = val;
            },
            get() {
                if (this.selectedCarModelId) {
                    return this.selectedCarModelId;
                }
                let result = this.selectCarModelList.filter(a => {
                    return a.id == selectedSession.car_engine;
                });
                return '';
            }
        },
        selectedCarEngine: {
            set(val) {
                this.selectedCarEnginelId = val;
            },
            get() {
                if (this.selectedCarEnginelId) {
                    return this.selectedCarEnginelId;
                }
                let result = this.selectCarEngineList.filter(a => {
                    return a.id == selectedSession.car_engine;
                });
                return '';
            }
        }
    },
    methods: {
        async createPart() {
            // Отправляем основные данные на сервер
            // Needs to make API and Login in Vue -- Here
            endpoint = `${ApplicationMainHost}/api/product/detailcreate/`;

            //Логика: Если есть выбранный бренд или ед изм то отправляем их
            //или дефолтовые значения
            if (!this.selectedUnitId) {
                unitId = settings.defaultUnitId;
            } else {
                unitId = this.selectedUnitId.id;
            }
            //brand
            if (!this.selectedBrandId) {
                brandId = this.part.brand;
            } else {
                brandId = this.selectedBrandId.id;
            }
            //car model
            if (!this.selectedCarModelId) {
                carId = selectedSession.car_model;
            } else {
                carId = this.selectedCarModelId.id;
            }
            //car engine
            if (!this.selectedCarEnginelId) {
                engineId = selectedSession.car_engine;
            } else {
                engineId = this.selectedCarEnginelId.id;
            }

            const data = {
                name: this.part.name,
                cat_number: this.part.cat_number,
                brand: brandId,
                car_model: {
                    id: carId
                },
                unit: unitId,
                one_c_id: this.part.one_c_id,
                active: this.part.active,
                engine: engineId
            }
            //console.log(JSON.stringify(data));
            const response = await apiService(endpoint, 'POST', data);
            window.location.href = `${ApplicationMainHost}/product/`
            // if(response.car_model.name == "Это поле обязательно.") {
            //     console.log('Works');
            // }
        },
        async getPart(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            const data = await apiService(endpoint);
            this.part = data;

        },
        async getSelectCarModelList() {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistcarmodelnew/`;
            const data = await apiService(endpoint);
            this.selectCarModelList = data;
            // this.sessionCountry = this.selectCarModelList[0].carmake.country.country;
            // this.sessionCarMake = this.selectCarModelList[0].carmake.name;
        },
        async getSelectCarEnginelList() {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistcarengine/`; // Do not forget change api
            const data = await apiService(endpoint);
            this.selectCarEngineList = data;
        },
        async getSelectUnitList() {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistunits/`;
            const data = await apiService(endpoint);
            this.selectUnitList = data;
        },
        async getSelectBrandsList() {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistbrands/`;
            const data = await apiService(endpoint);
            this.selectBrandList = data;
        }
    },
    
    created() {
        this.getSelectUnitList();
        this.getSelectBrandsList();
        this.getSelectCarModelList();
        this.getSelectCarEnginelList();
    },
    mounted() {
    }
});