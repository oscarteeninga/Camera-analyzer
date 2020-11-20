import React, {Component} from 'react';
import 'materialize-css/dist/css/materialize.min.css'
import Api from "../app/Api";
import {Table} from "react-materialize";
import PropTypes from "prop-types";
import EditArea from "./EditArea";

class AreaView extends Component {
    state = {
        areas: [],
        model: undefined
    };

    loadList() {
        const deviceId = this.props.deviceId;
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
    }

    render() {
        const editArea = <EditArea model={this.state.model} camera_id={this.props.deviceId} callback={() => {
            this.loadList()
        }} dismiss={() => {
            this.setState({
                model: undefined
            })
        }}/>;
        const table = <Table>
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
                                    style={{float: 'right', 'backgroundColor': '#48a999'}}
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
        </Table>;
        return (
            <div className="row">
                <div className="row">
                    <a className="waves-effect waves-light btn modal-trigger"
                       data-target="edit_area"
                       onClick={() => {
                           this.setState({
                               model: {"id": undefined}
                           })
                       }}
                    >Add Area</a>
                </div>
                {this.state.model ? editArea : table}

            </div>
        )
    }
}

AreaView.propTypes = {
    deviceId: PropTypes.number.isRequired
};
export default AreaView;