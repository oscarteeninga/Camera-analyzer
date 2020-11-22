import React, {Component} from "react";
import M from "materialize-css";
import "materialize-css/dist/css/materialize.min.css";
import PropTypes from 'prop-types'
import ApiService from "../app/Api";

class EditCamera extends Component {
    state = {
        id: undefined,
        name: "",
        ip: "",
        user: "",
        password: ""
    };

    componentDidMount() {
        const options = {
            onOpenStart: () => {
                console.log("Open Start");
            },
            onOpenEnd: () => {
                console.log("Open End");
                M.updateTextFields();
            },
            onCloseStart: () => {
                console.log("Close Start");
            },
            onCloseEnd: () => {
                console.log("Close End");
            },
            inDuration: 250,
            outDuration: 250,
            opacity: 0.5,
            dismissible: false,
            startingTop: "4%",
            endingTop: "20%"
        };
        M.Modal.init(this.Modal, options);

        // If you want to work on instance of the Modal then you can use the below code snippet
        // let instance = M.Modal.getInstance(this.Modal);
        // instance.open();
        // instance.close();
        // instance.destroy();
    }

    postCamera() {
        const callback = this.props.callback;
        const body = {
            name: this.state.name,
            ip: this.state.ip,
            user: this.state.user,
            password: this.state.password
        };
        const fetch = this.state.id ? ApiService.putCamera(this.state.id, body) : ApiService.postCamera(body);
        fetch.then(function (response) {
            if (response.status === 200) {
                callback()
            }
        })
    }

    deleteCamera() {
        const callback = this.props.callback;
        ApiService.deleteCamera(this.state.id).then(function (response) {
            if (response.status === 200) {
                callback()
            }
        })
    }

    render() {
        if (this.state.id !== this.props.model.id) {
            this.setState({
                id: this.props.model.id,
                name: this.props.model.name,
                ip: this.props.model.ip,
                user: this.props.model.user,
                password: this.props.model.password,
                fps: this.props.model.fps
            });
            M.updateTextFields();
        }
        return (
            <>
                <div
                    ref={Modal => {
                        this.Modal = Modal;
                    }}
                    id="edit_camera"
                    className="modal"
                >
                    <div className="modal-content">
                        <div className="row">
                            <h4 style={{
                                display: 'inline-block',
                                float: 'left'
                            }}>{this.state.id && this.state.id > 0 ? "Edit Camera" : "New Camera"}</h4>
                            {this.state.id && (
                                <a className="right modal-close waves-effect waves-red btn red"
                                   onClick={() => {
                                       this.deleteCamera()
                                   }}>Delete<i className="material-icons right">delete</i></a>
                            )}
                        </div>
                        <div className="row">
                            <div className="input-field col s6">
                                <input placeholder="Outside House Camera" id="name" type="text"
                                       className="active validate"
                                       onChange={e => {
                                           this.setState({
                                               name: e.target.value
                                           })
                                       }} value={this.state.name ? this.state.name : ""}/>
                                <label htmlFor="name">Name</label>
                            </div>
                            <div className="input-field col s6">
                                <input placeholder="192.168.1.15" id="ip" type="text" className="active validate"
                                       onChange={e => {
                                           this.setState({
                                               ip: e.target.value
                                           })
                                       }} value={this.state.ip ? this.state.ip : ""}/>
                                <label htmlFor="ip">Ip Address</label>
                            </div>
                        </div>
                        <div className="row">
                            <div className="input-field col s6">
                                <input placeholder="admin" id="first_name" type="text" className="active validate"
                                       onChange={e => {
                                           this.setState({
                                               user: e.target.value
                                           })
                                       }} value={this.state.user ? this.state.user : ""}/>
                                <label htmlFor="user">User</label>
                            </div>
                            <div className="input-field col s6">
                                <input id="password" type="password" className="active validate" onChange={e => {
                                    this.setState({
                                        password: e.target.value
                                    })
                                }} value={this.state.password ? this.state.password : ""}/>
                                <label htmlFor="password">Password</label>
                            </div>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <a href="#" className="modal-close waves-effect waves-red btn-flat">
                            Cancel
                        </a>
                        <a href="#" className="modal-close waves-effect waves-green btn" onClick={() => {
                            this.postCamera()
                        }}>
                            Save
                        </a>
                    </div>
                </div>
            </>
        );
    }
}

EditCamera.propTypes = {
    model: PropTypes.object.isRequired,
    callback: PropTypes.func.isRequired
};

export default EditCamera;