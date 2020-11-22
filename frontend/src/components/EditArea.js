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
        id: undefined
    };

    componentDidMount() {
        M.updateTextFields();
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
        if (this.state.id !== this.props.model.id)
            this.setState({
                x: this.props.model.x,
                y: this.props.model.y,
                width: this.props.model.width,
                height: this.props.model.height,
                id: this.props.model.id,
                coverage: this.props.model.coverage_required
            });
        return (
            <div>
                <div className="row" style={{'margin-top': '16px'}}>
                    <a ref={FAB => {
                        this.FAB = FAB;
                    }} onClick={() => {
                        this.postArea();
                        this.props.dismiss()
                    }}
                       className="btn-floating btn-large waves-effect waves-light "
                    >
                        <i className="material-icons">done</i></a>
                    <div className="right">
                        {this.state.id && (<i className="material-icons waves-effect btn-flat"
                                              style={{'font-size': '36px'}}
                                              onClick={() => {
                                                  this.deleteArea()
                                              }}>delete</i>
                        )}
                        <i className="material-icons btn-flat waves-effect " onClick={() => {
                            this.props.dismiss()
                        }} style={{'font-size': '36px'}}>clear</i>
                    </div>
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