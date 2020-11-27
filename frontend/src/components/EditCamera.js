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
        password: "",
        fit_video_to_areas: false
    };

    resetState() {
        document.getElementById("name").classList.remove("invalid");
        document.getElementById("name").classList.add("valid");
        document.getElementById("ip").classList.remove("invalid");
        document.getElementById("ip").classList.add("valid");
        document.getElementById("user").classList.remove("invalid");
        document.getElementById("user").classList.add("valid");
        document.getElementById("password").classList.remove("invalid");
        document.getElementById("password").classList.add("valid");
        this.setState({
            id: undefined,
            name: "",
            ip: "",
            user: "",
            password: "",
            fit_video_to_areas: false
        })
    }

    componentDidMount() {
        const options = {
            onOpenStart: () => {
                this.bindState();
            },
            onOpenEnd: () => {
                M.updateTextFields();
            },
            onCloseStart: () => {
            },
            onCloseEnd: () => {
            },
            inDuration: 250,
            outDuration: 250,
            opacity: 0.5,
            dismissible: false,
            startingTop: "4%",
            endingTop: "20%"
        };
        M.Modal.init(this.Modal, options);

    }

    bindState() {
        this.setState({
            id: this.props.model.id,
            name: this.props.model.name,
            ip: this.props.model.ip,
            user: this.props.model.user,
            password: this.props.model.password,
            fps: this.props.model.fps,
            fit_video_to_areas: this.props.model.fit_video_to_areas
        });
        M.updateTextFields();
    }

    postCamera() {
        const body = {
            name: this.state.name,
            ip: this.state.ip,
            user: this.state.user,
            password: this.state.password,
            fit_video_to_areas: this.state.fit_video_to_areas ? 1 : 0
        };
        const fetch = this.state.id ? ApiService.putCamera(this.state.id, body) : ApiService.postCamera(body);
        fetch.then(response => {
            if (response.status === 200) {
                this.props.callback()
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
        return (
            <>
                <form
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
                                <span className="helper-text" data-error="Name cannot be empty" data-success=""/>
                            </div>
                            <div className="input-field col s6">
                                <input placeholder="192.168.1.15" id="ip" type="text" className="active validate"
                                       required
                                       onChange={e => {
                                           this.setState({
                                               ip: e.target.value
                                           })
                                       }} value={this.state.ip ? this.state.ip : ""}/>
                                <label htmlFor="ip">Ip Address</label>
                                <span className="helper-text" data-error="Ip Address cannot be empty"
                                      data-success=""/>
                            </div>
                        </div>
                        <div className="row">
                            <div className="input-field col s6">
                                <input placeholder="admin" id="user" type="text" className="active validate"
                                       required
                                       onChange={e => {
                                           this.setState({
                                               user: e.target.value
                                           })
                                       }} value={this.state.user ? this.state.user : ""}/>
                                <label htmlFor="user">User</label>
                                <span className="helper-text" data-error="User cannot be empty" data-success=""/>
                            </div>
                            <div className="input-field col s6">
                                <input id="password" type="password" className="active validate" onChange={e => {
                                    this.setState({
                                        password: e.target.value
                                    })

                                }} required value={this.state.password ? this.state.password : ""}/>
                                <label htmlFor="password">Password</label>
                                <span className="helper-text" data-error="Password cannot be empty"
                                      data-success=""/>
                            </div>
                        </div>
                        <div className="row col s6">
                            <label>
                                <input type="checkbox" className="filled-in" onChange={e => {
                                    this.setState({
                                        fit_video_to_areas: e.target.checked
                                    })
                                }} checked={this.state.fit_video_to_areas}/>
                                <span>Fit video to areas for better detection accuracy</span>
                            </label>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button href="#" className="modal-close waves-effect waves-red btn-flat" onClick={() => {
                            this.resetState();
                        }}>
                            Cancel
                        </button>
                        <a name="action" type="submit" href="#" className="waves-effect waves-green btn"
                           onClick={() => {
                               M.updateTextFields();
                               if (this.state.name.length > 0 && this.state.ip.length > 0 && this.state.user.length > 0 && this.state.password.length > 0) {
                                   this.postCamera();
                                   this.Modal.M_Modal.close();
                                   this.resetState();
                               } else {
                                   if (this.state.name.length === 0) {
                                       document.getElementById("name").classList.remove("valid");
                                       document.getElementById("name").classList.add("invalid");
                                   }
                                   if (this.state.ip.length === 0) {
                                       document.getElementById("ip").classList.remove("valid");
                                       document.getElementById("ip").classList.add("invalid");
                                   }
                                   if (this.state.user.length === 0) {
                                       document.getElementById("user").classList.remove("valid");
                                       document.getElementById("user").classList.add("invalid");
                                   }
                                   if (this.state.password.length === 0) {
                                       document.getElementById("password").classList.remove("valid");
                                       document.getElementById("password").classList.add("invalid");
                                   }
                               }
                           }}>
                            Save
                        </a>
                    </div>
                </form>
            </>
        );
    }
}

EditCamera.propTypes = {
    model: PropTypes.object.isRequired,
    callback: PropTypes.func.isRequired
};

export default EditCamera;