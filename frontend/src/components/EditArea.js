import React, {Component} from 'react';
import "materialize-css/dist/css/materialize.min.css";
import PropTypes from 'prop-types'
import ApiService from "../app/Api";
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
        name: ""
    };

    resetValidation() {
        document.getElementById("x").classList.remove("invalid");
        document.getElementById("x").classList.add("valid");
        document.getElementById("y").classList.remove("invalid");
        document.getElementById("y").classList.add("valid");
        document.getElementById("height").classList.remove("invalid");
        document.getElementById("height").classList.add("valid");
        document.getElementById("width").classList.remove("invalid");
        document.getElementById("width").classList.add("valid");
        document.getElementById("coverage").classList.remove("invalid");
        document.getElementById("coverage").classList.add("valid");
    }

    resetState() {
        this.resetValidation();
        this.setState({
            x: "",
            y: "",
            width: "",
            height: "",
            coverage: "",
            id: undefined,
            name: ""
        })
    }

    componentDidMount() {
        M.updateTextFields();
        if (this.state.id !== this.props.model.id) {
            this.setState({
                x: this.props.model.x.toString(),
                y: this.props.model.y.toString(),
                width: this.props.model.width.toString(),
                height: this.props.model.height.toString(),
                id: this.props.model.id,
                name: this.props.model.name,
                coverage: this.props.model.coverage_required.toString()
            });
            M.updateTextFields();
        }
        M.FloatingActionButton.init(this.FAB, {});
    }

    deleteArea() {
        const callback = this.props.callback;
        ApiService.deleteArea(this.state.id).then(r => callback());
    }

    postArea() {
        const callback = this.props.callback;
        const camera_id = this.props.camera_id;
        const id = this.state.id;
        const body = {
            x: this.state.x,
            y: this.state.y,
            width: this.state.width,
            height: this.state.height,
            coverage_required: this.state.coverage
        };
        const fetch = id ? ApiService.putArea(id, body) : ApiService.postArea(camera_id, body);
        fetch.then(function (response) {
            if (response.status === 200) {
                callback()
            }
        })
    }


    render() {
        return (
            <div>
                <div className="row" style={{'margin-top': '16px'}}>
                    <a ref={FAB => {
                        this.FAB = FAB;
                    }} onClick={() => {
                        if (this.state.x.length > 0 && this.state.y.length > 0 && this.state.width.length > 0 && this.state.height.length > 0 && this.state.coverage.length > 0) {
                            this.postArea();
                            this.resetState();
                            this.props.dismiss();
                        } else {
                            this.resetValidation();
                            if (this.state.x.length === 0) {
                                document.getElementById("x").classList.remove("valid");
                                document.getElementById("x").classList.add("invalid");
                            }
                            if (this.state.y.length === 0) {
                                document.getElementById("y").classList.remove("valid");
                                document.getElementById("y").classList.add("invalid");
                            }
                            if (this.state.width.length === 0) {
                                document.getElementById("width").classList.remove("valid");
                                document.getElementById("width").classList.add("invalid");
                            }
                            if (this.state.height.length === 0) {
                                document.getElementById("height").classList.remove("valid");
                                document.getElementById("height").classList.add("invalid");
                            }
                            if (this.state.coverage.length === 0) {
                                document.getElementById("coverage").classList.remove("valid");
                                document.getElementById("coverage").classList.add("invalid");
                            }
                        }

                    }}
                       className="btn-floating btn-large waves-effect waves-light "
                    >
                        <i className="material-icons">done</i></a>
                    <b style={{
                        'margin-left': '16px',
                        'font-size': '24px'
                    }}>{this.state.name ? "Area " + this.state.name : "New Area"}</b>
                    <div className="right">
                        {this.state.id && this.props.canBeDeleted && (
                            <i className="material-icons waves-effect btn-flat"
                               style={{'font-size': '36px'}}
                               onClick={() => {
                                   this.deleteArea()
                               }}>delete</i>
                        )}
                        <i className="material-icons btn-flat waves-effect " onClick={() => {
                            this.resetState();
                            this.props.dismiss()
                        }} style={{'font-size': '36px'}}>clear</i>
                    </div>
                </div>
                <div className="row">
                    <div className="input-field col s1">
                        <input id="x" type="number"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       x: e.target.value
                                   })
                               }} value={this.state.x}/>
                        <label htmlFor="x">x</label>
                        <span className="helper-text" data-error="x cannot be empty"
                              data-success=""/>
                    </div>
                    <div className="input-field col s1">
                        <input required id="y" type="number"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       y: e.target.value
                                   })
                               }} value={this.state.y}/>
                        <label htmlFor="y">y</label>
                        <span className="helper-text" data-error="y cannot be empty"
                              data-success=""/>
                    </div>
                    <div className="input-field col s1">
                        <input required id="width" type="number"
                               className="active validate"
                               onChange={e => {
                                   this.setState({
                                       width: e.target.value
                                   })
                               }} value={this.state.width}/>
                        <label htmlFor="width">width</label>
                        <span className="helper-text" data-error="width cannot be empty"
                              data-success=""/>
                    </div>
                    <div className="input-field col s1">
                        <input required id="height" type="number" className="active validate"
                               onChange={e => {
                                   this.setState({
                                       height: e.target.value
                                   })
                               }} value={this.state.height}/>
                        <label htmlFor="height">height</label>
                        <span className="helper-text" data-error="height cannot be empty"
                              data-success=""/>
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
                        <span className="helper-text" data-error="Coverage cannot be empty"
                              data-success=""/>
                    </div>
                </div>
                {this.state.name || !this.props.model.id ? (<CameraPreview updateCallback={(x, y, w, h) => {
                    this.setState({
                        x: x.toString(),
                        y: y.toString(),
                        width: w.toString(),
                        height: h.toString(),
                    });
                    M.updateTextFields();
                }} camera_id={this.props.camera_id} x={this.state.x} y={this.state.y} width={this.state.width}
                                                                           height={this.state.height}/>) : (<></>)}
            </div>
        );
    }
}

EditArea.propTypes = {
    model: PropTypes.object,
    callback: PropTypes.func.isRequired,
    dismiss: PropTypes.func.isRequired,
    camera_id: PropTypes.number.isRequired,
    canBeDeleted: PropTypes.bool.isRequired
};

export default EditArea;