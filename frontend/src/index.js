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
        M.FloatingActionButton.init(this.FAB, {});
        document.title = "Camera Analyzer Config"
    }

    loadList() {
        Api.getCameras()
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

    deleteCamera(id) {
        Api.deleteCamera(id).then(r => {
            this.loadList();
        })
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
                                            <div className="right">
                                                <i className="material-icons waves-effect btn-flat modal-trigger"
                                                   data-target="edit_camera"
                                                   title="Edit Camera"
                                                   onClick={() => {
                                                       const device = this.state.devices.find(d => d.id === id);
                                                       this.setState({
                                                           model: device
                                                       })
                                                   }}
                                                >edit</i>
                                                <i className="material-icons waves-effect btn-flat" title="Areas"
                                                   onClick={() => {
                                                       this.setState({
                                                           areaView: {
                                                               id: id,
                                                               name: name
                                                           }
                                                       })
                                                   }}>filter</i>
                                                <i className="material-icons waves-effect btn-flat"
                                                   title="Delete Camera"
                                                   onClick={() => {
                                                       this.deleteCamera(id)
                                                   }}>delete</i>
                                            </div>
                                        </td>
                                    </tr>
                                )
                            )))}
                            </tbody>
                        </Table>)}
                </div>)}
                {this.state.areaView !== undefined ? (<AreaView device={this.state.areaView} dismiss={() => {
                    this.setState({
                        areaView: undefined
                    })
                }}/>) : <div/>}
            </div>
        )
    }
}

ReactDOM.render(<DeviceList/>, document.getElementById("root"));