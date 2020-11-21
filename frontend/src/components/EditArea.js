import React, {Component} from 'react';
import "materialize-css/dist/css/materialize.min.css";
import PropTypes from 'prop-types'
import ApiService from "../app/Api";
import {Button} from "react-materialize";
import M from "materialize-css";
import CameraPreview from "./CameraPreview";

class EditArea extends Component {
    state = {
        x: "",
        y: "",
        width: "",
        height: "",
        coverage: "",
        id: undefined,
        img: undefined
    };

    componentDidMount() {
        const url = ApiService.getBaseUrl() + '/devices/' + this.props.camera_id + '/img';
        fetch(url).then(response => {
            response.blob().then(blob => {
                const outside = URL.createObjectURL(blob);
                console.log(outside);
                this.setState({
                    img: blob
                })
            })
        });
        M.updateTextFields();
    }

    postArea() {
        const callback = this.props.callback;
        const camera_id = this.props.camera_id;
        const id = this.props.id;
        const url = id ? ApiService.getBaseUrl() + "/devices/" + camera_id + '/areas/' + id : ApiService.getBaseUrl() + '/devices/' + camera_id + '/areas';
        fetch(url, { // optional fetch options
            body: JSON.stringify({
                area_x: this.state.x,
                area_y: this.state.y,
                area_width: this.state.width,
                area_height: this.state.height,
                area_confidence_required: this.coverage
            }),
            method: this.state.id ? "PUT" : "POST",
            headers: {
                'content-type': 'application/json'
            }
        })
            .then(function (response) {
                if (response.status === 200) {
                    callback()
                }
            })
    }

    deleteArea() {
        const callback = this.props.callback;
        const camera_id = this.props.camera_id;
        const id = this.props.id;
        const url = ApiService.getBaseUrl() + "/devices/" + camera_id + '/areas/' + id;
        fetch(url, { // optional fetch options
            method: "DELETE"
        })
            .then(function (response) {
                if (response.status === 200) {
                    callback()
                }
            })
    }


    render() {
        if (this.state.id !== this.props.model.id)
            this.setState({
                x: this.props.model.x,
                y: this.props.model.y,
                width: this.props.model.width,
                height: this.props.model.height,
                id: this.props.model.id,
                coverage: this.props.model.coverage
            });
        return (
            <div>
                <div className="row" style={{'margin-top': '16px'}}>
                    <a className="btn-flat waves-effect waves-green col s1" onClick={() => {
                        this.props.dismiss()
                    }}><i className="material-icons" style={{'font-size': '24px'}}>arrow_back</i></a>

                    <button className="right col s1 waves-effect waves-green btn" onClick={() => {
                        this.postArea();
                        this.props.dismiss()
                    }} style={{'margin-right': '16px'}}>
                        Save
                    </button>
                    {this.props.id && (
                        <Button className="modal-close waves-effect waves-red"
                                style={{float: 'right', 'backgroundColor': 'red'}}
                                onClick={() => {
                                    this.deleteArea()
                                }}>Delete</Button>
                    )}
                </div>
                <div className="row">
                    <div className="input-field col s1">
                        <input required placeholder="Starting horizontal position" id="x" type="text"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       x: e.target.value
                                   })
                               }} value={this.state.x}/>
                        <label htmlFor="x">x</label>
                    </div>
                    <div className="input-field col s1">
                        <input required placeholder="Starting horizontal position" id="y" type="text"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       y: e.target.value
                                   })
                               }} value={this.state.y}/>
                        <label htmlFor="y">y</label>
                    </div>
                    <div className="input-field col s1">
                        <input required placeholder="Starting horizontal position" id="width" type="text"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       width: e.target.value
                                   })
                               }} value={this.state.width}/>
                        <label htmlFor="width">width</label>
                    </div>
                    <div className="input-field col s1">
                        <input required placeholder="Area height" id="height" type="text" className="active validate"
                               onChange={e => {
                                   this.setState({
                                       height: e.target.value
                                   })
                               }} value={this.state.height}/>
                        <label htmlFor="height">height</label>
                    </div>
                    <div className="input-field col s2">
                        <input required placeholder="Area coverage" id="coverage" type="number" min="0" max="100"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       coverage: e.target.value
                                   })
                               }} value={this.state.coverage}/>
                        <label htmlFor="coverage">coverage</label>
                    </div>
                </div>
                <CameraPreview updateCallback={(x, y, w, h) => {
                    this.setState({
                        x: x.toString(),
                        y: y.toString(),
                        width: w.toString(),
                        height: h.toString()
                    })
                }} camera_id={this.props.camera_id} x={this.state.x} y={this.state.y} width={this.state.width}
                               height={this.state.height}/>
            </div>
        );
    }
}

EditArea.propTypes = {
    model: PropTypes.object,
    callback: PropTypes.func.isRequired,
    dismiss: PropTypes.func.isRequired,
    camera_id: PropTypes.number.isRequired
};

export default EditArea;