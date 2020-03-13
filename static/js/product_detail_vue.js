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
const app = new Vue({
    delimiters: ['{', '}'],
    el: '#app',
    data: {
        part: {
            partName: 'Part Name From Vue',
            partNumber: '',
            partGroup: '',
            partBrand: '',
            partMake: '',
            partModel: '',
            partEngine: '',
            part1CId: null,
            partActive: true
        }
    },
    methods: {
        basesubmit() {
            console.log(this.part);
            apiService('http://localhost:8000/api/list/');
            // Отправляем основные данные на сервер
            // Needs to make API and Login in Vue -- Here 
        }
    }
  });
  //#####################################

 
