import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import './assets/style.css'
import Api from "./app/Api";
import DeviceListItem from "./components/DeviceListItem";


class DeviceList extends Component {
    state = {
        devices: [],
        loading: true,
        error: undefined
    };

    async componentDidMount() {
        const response = await fetch(Api.getBaseUrl() + '/devices')
            .catch(err => {
                this.setState({
                    error: err.toString(),
                    loading: false
                })
            });
        if (this.state.error === undefined) {
            if (response.status === 200) {
                const data = await response.json();
                this.setState({
                    devices: data,
                    loading: false,
                    error: undefined
                });
            } else {
                this.setState({
                    error: response.statusText,
                    loading: false
                })
            }
        }
    }

    render() {
        return (
            <div className="container">
                <div className="title">Camera Analyzer Configuration</div>
                {!this.state.error && this.state.loading ? (<div>Pobieranie danych...</div>) : this.state.error ? (
                    <div>{this.state.error}</div>
                ) : (
                    this.state.devices.length > 0 && this.state.devices.map((
                        ({id, name, ip}) => (
                            <DeviceListItem id={id} name={name} ip={ip} key={id}/>
                        )
                    ))
                )}
            </div>
        );
    }
}

ReactDOM.render(<DeviceList/>, document.getElementById("root"));