import React, {Component} from 'react';
import "materialize-css/dist/css/materialize.min.css";
import PropTypes from 'prop-types'
import ApiService from "../app/Api";
import {Button} from "react-materialize";

class EditCamera extends Component {
    state = {
        x: "",
        y: "",
        width: "",
        height: "",
        coverage: "0",
        id: undefined,
        img: undefined
    };

    componentDidMount() {
        const url = ApiService.getBaseUrl() + '/devices/' + this.props.camera_id + '/image';
        fetch(url).then(response => {
            response.blob().then(blob => {
                const outside = URL.createObjectURL(blob);
                console.log(outside);
                this.setState({
                    img: blob
                })
            })
        })
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
                <div className="row">
                    <h4 style={{
                        display: 'inline-block',
                        float: 'left'
                    }}>{this.props.id && this.props.id > 0 ? "Edit Area" : "New Area"}</h4>
                    {this.props.id && (
                        <Button className="modal-close waves-effect waves-red"
                                style={{float: 'right', 'backgroundColor': 'red'}}
                                onClick={() => {
                                    this.deleteArea()
                                }}>Delete</Button>
                    )}
                </div>
                <div className="row">
                    <div className="input-field col s6">
                        <input placeholder="Starting horizontal position" id="x" type="text" className="validate"
                               onChange={e => {
                                   this.setState({
                                       x: e.target.value
                                   })
                               }} value={this.state.x}/>
                        <label htmlFor="x">x</label>
                    </div>
                    <div className="input-field col s6">
                        <input placeholder="Starting horizontal position" id="y" type="text" className="validate"
                               onChange={e => {
                                   this.setState({
                                       y: e.target.value
                                   })
                               }} value={this.state.y}/>
                        <label htmlFor="y">y</label>
                    </div>
                    <div className="input-field col s6">
                        <input placeholder="Starting horizontal position" id="width" type="text"
                               className="validate"
                               onChange={e => {
                                   this.setState({
                                       width: e.target.value
                                   })
                               }} value={this.state.width}/>
                        <label htmlFor="width">width</label>
                    </div>
                    <div className="input-field col s6">
                        <input placeholder="Area height" id="height" type="text" className="validate"
                               onChange={e => {
                                   this.setState({
                                       height: e.target.value
                                   })
                               }} value={this.state.height}/>
                        <label htmlFor="height">height</label>
                    </div>
                    <div className="input-field col s6">
                        <input placeholder="Area coverage" id="coverage" type="text" className="validate"
                               onChange={e => {
                                   this.setState({
                                       coverage: e.target.value
                                   })
                               }} value={this.state.coverage}/>
                        <label htmlFor="coverage">coverage</label>
                    </div>
                </div>
                {/*<img className="materialboxed" width="650" src={this.state.model.img}/>*/}
                <div className="row">
                    <a href="#" className=" waves-effect waves-red btn-flat" onClick={() => {
                        this.props.dismiss()
                    }}>
                        Cancel
                    </a>
                    <a href="#" className=" waves-effect waves-green btn-flat" onClick={() => {
                        this.postArea();
                        this.props.dismiss()
                    }}>
                        Save
                    </a>
                </div>
            </div>
        );
    }
}

EditCamera.propTypes = {
    model: PropTypes.object.isRequired,
    callback: PropTypes.func.isRequired,
    dismiss: PropTypes.func.isRequired,
    camera_id: PropTypes.number.isRequired
};

export default EditCamera;