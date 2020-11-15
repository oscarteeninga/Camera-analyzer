import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './assets/style.css'
import Api from "./app/Api";


class DeviceList extends Component {
    state = {
        devices: []
    };

    getDevices = () => {
        fetch(Api.getBaseUrl() + '/devices')
            .then(result => {
                if (result.status === 200) {
                    this.setState({
                        devices: result.json()
                    })
                } else {

                }
            });
    };

    componentDidMount() {
        this.getDevices();
    }

    render() {
        return (
            <div className="container">
                <div className="title">Camera Analyzer Configuration</div>
            </div>
        );
    }
}

ReactDOM.render(<DeviceList/>, document.getElementById("root"));