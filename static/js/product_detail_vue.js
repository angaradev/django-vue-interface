
//##########################################################//
//############### VUE PART STARTS HERE #####################//
//##########################################################//
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
                let result = this.selectCarEngineList.filter(a => {
                    return a.id == this.part.engine;
                });
                return result
            }
        }
    },

    methods: {
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

            //console.log(this.productVideos);
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
            console.log(response);
            this.productVideos.push(response);
            this.productVideoUrl = null;
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
                    this.imageLoading = false;
                    this.selectedFiles = [];
                    this.resetUploadForm();
                })
                .catch(error => {
                    this.imageLoading = false;
                })


        },
        async deleteImage(id) {
            const endpoint = `${ApplicationMainHost}/api/product/images/${id}/`;
            await apiService(endpoint, 'DELETE');
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

            const data = {
                one_c_id: Number(this.part.one_c_id),
                name: this.part.name,
                cat_number: this.part.cat_number,
                brand: brandId,
                car_model: {
                    id: carId
                },
                unit: unitId,
                active: this.part.active,
                engine: engineId
            }
            //console.log(JSON.stringify(data));
            let response = await apiService(endpoint, 'PUT', data);
            //console.log(response)
        },
        async getPart(id) {
            const endpoint = `${ApplicationMainHost}/api/product/detail/${id}/`;
            const data = await apiService(endpoint);
            this.part = data;
            await this.getSelectCarModelList(this.part.car_model.carmake.id);
            await this.getSelectCarEnginelList(this.part.car_model.id);
            await this.getImage(this.part.id);
        },
        async getSelectCarModelList(id) {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistcarmodel/${id}/`;
            const data = await apiService(endpoint);
            this.selectCarModelList = data;
        },
        async getSelectCarEnginelList(id) {
            const endpoint = `${ApplicationMainHost}/api/product/selectlistcarengine/${id}/`; // Do not forget change api
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
        this.getPart(id);

        this.getVideo(id);


    },
    mounted() {
    }
});
