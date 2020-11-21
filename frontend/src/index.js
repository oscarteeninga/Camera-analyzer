import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import Api from "./app/Api";
import {Row, Table} from "react-materialize";
import 'materialize-css/dist/css/materialize.min.css'
import EditCamera from "./components/EditCamera";
import AreaView from "./components/AreaView";
import M from 'materialize-css';

class DeviceList extends Component {
    state = {
        devices: [],
        loading: true,
        error: undefined,
        model: {},
        areaView: undefined
    };

    componentDidMount() {
        this.loadList();
        M.FloatingActionButton.init(this.FAB, {})
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
            <div className="container">
                <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
                      rel="stylesheet"/>
                {this.state.areaView === undefined && (<div className="row">
                    <div className="row">
                        <h4 className="col s6">Cameras</h4>
                        <a ref={FAB => {
                            this.FAB = FAB;
                        }} onClick={() => {
                            this.setState({
                                model: {"id": undefined}
                            })
                        }}
                           data-target="edit_camera"
                           className="modal-trigger btn-floating btn-large waves-effect waves-light "
                           style={{'float': 'right', 'margin-top': '16px', 'margin-right': '16px'}}>
                            <i className="material-icons">add</i></a>
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
                                            <div className="row" style={{'margin-right': '16px'}}>
                                                <button className="waves-effect waves-light btn modal-trigger"
                                                        data-target="edit_camera"
                                                        style={{float: 'right', 'backgroundColor': '#48a999'}}
                                                        onClick={() => {
                                                            const device = this.state.devices.find(d => d.id === id);
                                                            this.setState({
                                                                model: device
                                                            })
                                                        }}
                                                >Edit
                                                </button>
                                            </div>
                                            <div className="row" style={{'margin-right': '16px'}}>
                                                <button className="waves-effect waves-light btn"
                                                        style={{float: 'right', 'backgroundColor': '#004c40'}}
                                                        onClick={() => {
                                                            this.setState({
                                                                areaView: {
                                                                    id: id,
                                                                    name: name
                                                                }
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
                {this.state.areaView !== undefined ? (<AreaView device={this.state.areaView}/>) : <div/>}
            </div>
        )
    }
}

ReactDOM.render(<DeviceList/>, document.getElementById("root"));