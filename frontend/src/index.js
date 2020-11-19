import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Api from "./app/Api";
import {Button, Col, Row, Table} from "react-materialize";
import 'materialize-css/dist/css/materialize.min.css'
import EditCamera from "./components/EditCamera";
import AreaView from "./components/AreaView";


class DeviceList extends Component {
    state = {
        devices: [],
        loading: true,
        error: undefined,
        model: {},
        areaView: undefined
    };

    componentDidMount() {
        this.loadList()
    }

    loadList() {
        fetch(Api.getBaseUrl() + '/devices')
            .then(response => {
                if (this.state.error === undefined) {
                    if (response.status === 200) {
                        response.json()
                            .then(data => {
                                this.setState({
                                    devices: data,
                                    loading: false,
                                    error: undefined
                                });
                            });
                    } else {
                        this.setState({
                            error: response.statusText,
                            loading: false
                        })
                    }
                }
            })
            .catch(err => {
                this.setState({
                    error: err.toString(),
                    loading: false
                })
            });

    }

    render() {
        return (
            <div className="App">
                {this.state.areaView === undefined && (<div className="row">
                    <div className="row">
                        <a className="waves-effect waves-light btn modal-trigger"
                           data-target="edit_camera"
                           onClick={() => {
                               this.setState({
                                   model: {"id": undefined}
                               })
                           }}
                        >Add Camera</a>
                    </div>
                    <EditCamera model={this.state.model} callback={() => {
                        this.loadList()
                    }}/>
                    {!this.state.error && this.state.loading ? (<Row>Fetching data...</Row>) : this.state.error ? (
                        <Row>{this.state.error}</Row>
                    ) : (
                        <Table>
                            <thead>
                            <tr>
                                <th data-field="name">
                                    Name
                                </th>
                                <th data-field="ip">
                                    Ip Address
                                </th>
                                <th>
                                </th>
                            </tr>
                            </thead>
                            <tbody>
                            {(this.state.devices.length > 0 && this.state.devices.map((
                                ({id, name, ip}) => (
                                    <tr>
                                        <td>{name} </td>
                                        <td>{ip} </td>
                                        <td>
                                            <div className="row">
                                                <button className="waves-effect waves-light btn modal-trigger"
                                                        data-target="edit_camera"
                                                        style={{float: 'right', 'background-color':'#48a999'}}
                                                        onClick={() => {
                                                            const device = this.state.devices.find(d => d.id === id);
                                                            this.setState({
                                                                model: device
                                                            })
                                                        }}
                                                >Edit
                                                </button>
                                            </div>
                                            <div className="row">
                                                <button className="waves-effect waves-light btn"
                                                        style={{float: 'right', 'background-color': '#004c40'}}
                                                        onClick={() => {
                                                            this.setState({
                                                                areaView: id
                                                            })
                                                        }}
                                                >Areas
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                )
                            )))}
                            </tbody>
                        </Table>)}
                </div>)}
                {this.state.areaView !== undefined ? (<AreaView/>) : <div/>}
            </div>
        )
    }
}

ReactDOM.render(<DeviceList/>, document.getElementById("root"));