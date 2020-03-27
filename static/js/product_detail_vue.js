
//##########################################################//
//############### VUE PART STARTS HERE #####################//
//##########################################################//
Vue.use(VueToast);
Vue.component('vue-multiselect', window.VueMultiselect.default);
const vsel = Vue.component('v-select', VueSelect.VueSelect);
let il = {

    template: `<div class="product-main-thumbs">
                <h3>{{ message }}</h3>
                <img style="height: 100px; width: 100px;"
                v-for="prod_img in productImages" :src="prod_img.image" alt="...">
                </div>`,
    // data: function (){
    //     return{
    //         productImages: []
    //     }
    // },
    // methods: {
    //     async getImage(id) {
    //         endpoint = `${ApplicationMainHost}/api/product/images/?product_id=${id}`;
    //         let response = await apiService(endpoint);
    //         this.productImages = response.results;

    //     }
    // }


};

const app = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    components: {
        'image-loader': il
    },
    data: {
        value: [],
        valueEngine: [],
        options: [
            { name: 'Vue.js', language: 'JavaScript' },
            { name: 'Adonis', language: 'JavaScript' },
            { name: 'Rails', language: 'Ruby' },
            { name: 'Sinatra', language: 'Ruby' },
            { name: 'Laravel', language: 'PHP' },
            { name: 'Phoenix', language: 'Elixir' }
        ]
        ,
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
        selectCarModelList: [],
        selectUnitList: [],
        selectBrandList: [],
        selectCarEngineList: [],
        selectedUnitId: null,
        selectedBrandId: null,
        selectedCarModelId: null,
        selectedCarEnginelId: null,
        // Image part of code
        productImages: [],
        selectedFiles: [],
        mainImage: 0, // Later needed to implement selected main image by id,
        // Video part of Code
        productVideos: [],
        productVideoUrl: '',
        imageLoading: false
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
                    return a.id == this.part.car_model.id;
                });
                return result
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
                else if (this.selectCarEngineList) {
                    let result = this.selectCarEngineList.filter(a => {
                        return a.id == this.part.engine;
                    });
                    return result
                }
                else {
                    return '';
                }

            }
        }
    },

    methods: {
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
        popFromArrayById(array, id) {
            let removeIndex = array.map(function (item) { return item.id; }).indexOf(id);
            array.splice(removeIndex, 1);
            return array;
        },
        //Video part of code
        async getVideo(product_id) {
            const endpoint = `${ApplicationMainHost}/api/product/videos/?product_id=${product_id}`;
            let response = await apiService(endpoint);
            this.productVideos = response.results;
        },
        async saveVideo(id) {
            if (id) {
                const endpoint = `${ApplicationMainHost}/api/product/videos/${id}/`;
                let getIndex = this.productVideos.map(function (item) { return item.id; }).indexOf(id);
                const data = {
                    url: this.productVideos[getIndex].url,
                    product: this.part.id
                }
                let response = await apiService(endpoint, 'PUT', data);
            } else {
                this.addVideo();
            }

        },
        async deleteVideo(id) {
            const endpoint = `${ApplicationMainHost}/api/product/videos/${id}/`;
            await apiService(endpoint, 'DELETE');
            this.popFromArrayById(this.productVideos, id);

        },
        async addVideo() {
            const endpoint = `${ApplicationMainHost}/api/product/videos/`;
            data = {
                url: this.productVideoUrl,
                product: this.part.id
            }
            const response = await apiService(endpoint, 'POST', data);
            if (response) {
                this.productVideos.push(response);
                this.productVideoUrl = null;
                this.successToast('Видео сохранено успешно');
            } else {
                this.errorToast('Видео не сохранено!');
            }

        },

        //Image Part Of Code
        onFileSelected(event) {
            this.selectedFiles = event.target.files;
        },
        async getImage(id) {
            const endpoint = `${ApplicationMainHost}/api/product/images/?product_id=${id}`;
            let response = await apiService(endpoint);
            this.productImages = response.results;

        },
        async uploadImage() {
            this.imageLoading = true;
            const endpoint = `${ApplicationMainHost}/api/product/images/`;
            let fd = new FormData();
            for (const element of this.selectedFiles) {
                fd.append('image', element, element.name);
            }

            fd.append('product', this.part.id);
            this.imageLoading = true;
            await axiosUploadImageApi(endpoint, fd)
                .then(response => {
                    if (response) {
                        this.successToast('Фото сохранено успешно');
                        this.imageLoading = false;
                        this.selectedFiles = [];
                    }
                    else {
                        this.errorToast('Фото не сохранилось!');
                        this.imageLoading = false;
                    }
                })
                .catch(error => {
                    this.imageLoading = false;
                })


        },
        async deleteImage(id) {
            const endpoint = `${ApplicationMainHost}/api/product/images/${id}/`;
            const res = await apiService(endpoint, 'DELETE');
            if (!res) {
                this.successToast('Фото удалено успешно');
            } else {
                this.errorToast('Фото не удалилось!');
            }
            let removeIndex = this.productImages.map(function (item) { return item.id; }).indexOf(id);
            this.productImages.splice(removeIndex, 1);
        },
        // Part of product itself
        async editPart() {
            // Отправляем основные данные на сервер
            // Needs to make API and Login in Vue -- Here
            const endpoint = `${ApplicationMainHost}/api/product/detail/${this.part.id}/`;

            //Логика: Если есть выбранный бренд или ед изм то отправляем их
            //или дефолтовые значения
            if (!this.selectedUnitId) {
                unitId = this.part.unit;
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
                carId = this.part.car_model.id;
            } else {
                carId = this.selectedCarModelId.id;
            }
            //car engine
            if (!this.selectedCarEnginelId) {
                engineId = this.part.engine;
            } else {
                engineId = this.selectedCarEnginelId.id;
            }
            let car_mod = this.value.map(obj => {
                return obj.id;
            });
            //Lgic of car engine values comprihansion list
            let engine = [];
            if (this.valueEngine.lenght == 0) {
                engine = [];
            }
            engine = this.valueEngine.map(obj => {
                return obj.id;
            });

            const data = {
                one_c_id: Number(this.part.one_c_id),
                name: this.part.name,
                cat_number: this.part.cat_number,
                brand: brandId,
                car_model: car_mod,
                unit: unitId,
                active: this.part.active,
                engine: engine
            }
            //console.log(JSON.stringify(data));
            let response = await apiService(endpoint, 'PUT', data);
            console.log(response)
            if (response) {
                this.successToast('Товар сохранен!');
            }
            else {
                this.errorToast('Ошибка сохранения товара!');
            }
            //window.location.href = `${ApplicationMainHost}/product/`
        },
        async getPartCarModel(id_list) { //Gettin car model list for specific car part
            const endpoint = `${ApplicationMainHost}/api/product/selectpartcarmodel/?pk=${id_list}`;
            const data = await apiService(endpoint);
            this.value = data;
        },
        async getPartCarEngine(id_list) {
            let endpoint;
            if (id_list.lenght == 0) {
                endpoint = `${ApplicationMainHost}/api/product/selectpartcarengine/?pk=0`;
            }
            endpoint = `${ApplicationMainHost}/api/product/selectpartcarengine/?pk=${id_list}`;
            const data = await apiService(endpoint);
            this.valueEngine = data;
            return data;
        },
        async getPart(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            const data = await apiService(endpoint);
            this.part = data;
            this.getPartCarModel(this.part.car_model);
            this.getPartCarEngine(this.part.engine);
            await this.getSelectCarModelList(1); // Here need to implement selecting models by carmake
            // await this.getSelectCarEnginelList(this.part.car_model.id);
            await this.getImage(this.part.id);
            console.log(data)
        },
        async getSelectCarModelList(id) {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistcarmodel/${id}/`;
            const data = await apiService(endpoint);
            this.selectCarModelList = data;
        },
        async getSelectCarEnginelList(id) {
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
    // beforeMount() {
    //     this.part.id = document.getElementById('mainId').getAttribute('token') || '';
    // },
    created() {
        this.getSelectUnitList();
        this.getSelectBrandsList();
        const id = document.getElementById('mainId').getAttribute('token') || '';
        this.getSelectCarEnginelList();
        this.getPart(id);

        this.getVideo(id);


    },
    mounted() {
    }
});
