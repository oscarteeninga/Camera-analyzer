class Api {

    static baseUrl = 'http://192.168.1.46:5000';

    static getCameras() {
        return fetch(this.baseUrl + '/devices')
    }

    static putCamera(id, body) {
        const url = this.baseUrl + "/devices/" + id;
        return fetch(url, {
            body: JSON.stringify(body),
            method: "PUT",
            headers: {
                'content-type': 'application/json'
            }
        })
    }

    static postCamera(body) {
        const url = this.baseUrl + '/devices';
        return fetch(url, {
            body: JSON.stringify(body),
            method: "POST",
            headers: {
                'content-type': 'application/json'
            }
        })
    }


    static deleteCamera(id) {
        const url = this.baseUrl + "/devices/" + id;
        return fetch(url, {
            method: "DELETE"
        })
    }

    static getPreview(id) {
        return this.baseUrl + '/devices/' + id + '/img';
    }

    static getAreas(deviceId) {
        return fetch(this.baseUrl + '/devices/' + deviceId + '/areas')
    }

    static postArea(deviceId, body) {
        return fetch(this.baseUrl + '/devices/' + deviceId + '/areas', {
            body: JSON.stringify(body),
            method: "POST",
            headers: {
                'content-type': 'application/json'
            }
        });
    }

    static putArea(id, body) {
        return fetch(this.baseUrl + '/areas/' + id, {
            body: JSON.stringify(body),
            method: "PUT",
            headers: {
                'content-type': 'application/json'
            }
        });
    }

    static deleteArea(id) {
        const url = this.baseUrl + '/areas/' + id;
        return fetch(url, {
            method: "DELETE"
        })
    }
}

export default Api;