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

    loadList(deviceId) {
        Api.getAreas(deviceId)
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
        const deviceId = this.props.device.id;
        this.loadList(deviceId);
        M.FloatingActionButton.init(this.FAB, {})
    }

    deleteArea(id) {
        const deviceId = this.props.device.id;
        Api.deleteArea(id).then(function (response) {
        });
        this.loadList(deviceId);
    }

    render() {
        const editArea = <EditArea model={this.state.model} camera_id={this.props.device.id} callback={() => {
            this.setState({
                model: undefined
            });
            this.loadList(this.props.device.id);
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
                        ({id, name, x, y, width, height, coverage_required}) => (
                            <tr>
                                <td>{name} </td>
                                <td>{'x: ' + x + ' y: ' + y + ' width: ' + width + ' height: ' + height + ' coverage: ' + coverage_required + '%'} </td>
                                <td>
                                    <div className="right">
                                        <i className="material-icons waves-effect btn-flat" title="Edit Area"
                                           onClick={() => {
                                               const area = this.state.areas.find(d => d.id === id);
                                               this.setState({
                                                   model: area
                                               })
                                           }}>edit</i>
                                        <i className="material-icons right waves-effect btn-flat" title="Delete Area"
                                           onClick={() => {
                                               this.deleteArea(id)
                                           }}>delete</i>
                                    </div>
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