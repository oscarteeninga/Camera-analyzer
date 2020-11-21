import React, {Component} from 'react';
import 'materialize-css/dist/css/materialize.min.css'
import Api from "../app/Api";
import {Table} from "react-materialize";
import PropTypes from "prop-types";
import EditArea from "./EditArea";
import M from 'materialize-css'

class AreaView extends Component {
    state = {
        areas: [],
        model: undefined
    };

    loadList() {
        const deviceId = this.props.device.id;
        fetch(Api.getBaseUrl() + '/devices/' + deviceId + '/areas')
            .then(response => {
                if (response.status === 200) {
                    response.json()
                        .then(data => {
                            this.setState({
                                areas: data,
                            });
                        });
                }
            });
    }

    componentDidMount() {
        this.loadList();
        M.FloatingActionButton.init(this.FAB, {})
    }

    render() {
        const editArea = <EditArea model={this.state.model} camera_id={this.props.device.id} callback={() => {
            this.loadList()
        }} dismiss={() => {
            this.setState({
                model: undefined
            })
        }}/>;
        const table =
            <div>
                <div className="row">
                    <h4 className="col s6">{this.props.device.name} areas</h4>
                    <a ref={FAB => {
                        this.FAB = FAB;
                    }} onClick={() => {
                        this.setState({
                            model: {"id": undefined}
                        })
                    }}
                       className="btn-floating btn-large waves-effect waves-light "
                       style={{'float': 'right', 'margin-top': '16px', 'margin-right': '16px'}}>
                        <i className="material-icons">add</i></a>
                </div>
                <Table>
                    <thead>
                    <tr>
                        <th data-field="name">
                            Name
                        </th>
                        <th data-field="ip">
                            Properties
                        </th>
                        <th>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {(this.state.areas.length > 0 && this.state.areas.map((
                        ({id, name, x, y, width, height, camera_id}) => (
                            <tr>
                                <td>{name} </td>
                                <td>{'x: ' + x + ' y: ' + y + ' width: ' + width + ' height: ' + height} </td>
                                <td>
                                    <button className="waves-effect waves-light btn modal-trigger"
                                            data-target="edit_camera"
                                            style={{
                                                float: 'right',
                                                'backgroundColor': '#48a999',
                                                'margin-right': '16px'
                                            }}
                                            onClick={() => {
                                                const area = this.state.areas.find(d => d.id === id);
                                                this.setState({
                                                    model: area
                                                })
                                            }}
                                    >Edit
                                    </button>
                                </td>
                            </tr>
                        )
                    )))}
                    </tbody>
                </Table>
            </div>;
        return (
            <div className="row">
                {this.state.model ? editArea : table}

            </div>
        )
    }
}

AreaView.propTypes = {
    device: PropTypes.object.isRequired,
};
export default AreaView;