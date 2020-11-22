import React, {Component} from 'react';
import "materialize-css/dist/css/materialize.min.css";
import PropTypes from 'prop-types'
import ApiService from "../app/Api";
import M from "materialize-css";
import {fabric} from 'fabric'


class CameraPreview extends Component {

    constructor(props) {
        super(props);
        this.state = {
            x: props.x,
            y: props.y,
            width: props.width,
            height: props.height
        }
    }

    componentDidMount() {
        const updateCallback = this.props.updateCallback;
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
        if (M.MBox) {
            M.MBox.init(this.MBox, options);
        }
        M.updateTextFields();
        var canvas = new fabric.Canvas('canvas', {selection: false});

        var rect, isDown, origX, origY, height, width;

        const drawRect = this.drawRect;

        canvas.on('mouse:down', function (o) {
            isDown = true;
            var pointer = canvas.getPointer(o.e);
            origX = pointer.x;
            origY = pointer.y;
            width = pointer.x - origX;
            height = pointer.y - origY;
            canvas.clear();
            rect = drawRect(canvas, origX, origY, width, height);
        });

        const updateFunction = this.updateRect;

        canvas.on('mouse:move', function (o) {
            if (!isDown) return;
            var pointer = canvas.getPointer(o.e);

            if (origX > pointer.x) {
                rect.set({left: Math.abs(pointer.x)});
            }
            if (origY > pointer.y) {
                rect.set({top: Math.abs(pointer.y)});
            }

            height = Math.abs(origY - pointer.y);
            width = Math.abs(origX - pointer.x);
            rect.set({width: width});
            rect.set({height: height});

            updateFunction(origX, origY, width, height, updateCallback);

            canvas.renderAll();
        });

        canvas.on('mouse:up', function (o) {
            isDown = false;
        });
        if (this.state.width > 0 && this.state.height > 0) {
            this.drawRectWithCameraCoords(
                canvas,
                this.state.x,
                this.state.y,
                this.state.width,
                this.state.height
            );
        }
        const img = document.querySelector("#img");
        const existingOnLoad = img.onload;
        img.onload = () => {
            canvas.setHeight(img.clientHeight);
            canvas.setWidth(img.clientWidth);
            if (existingOnLoad)
                existingOnLoad();
        };
        window.onresize = function (event) {
            canvas.setHeight(img.clientHeight);
            canvas.setWidth(img.clientWidth);
        }
    }

    drawRectWithCameraCoords(canvas, x, y, w, h) {
        const img = document.querySelector("#img");
        img.onload = () => {
            const realWidth = img.naturalWidth;
            const displayedWidth = img.clientWidth;
            const realHeight = img.naturalHeight;
            const displayedHeight = img.clientHeight;
            const multiplierX = displayedWidth / realWidth;
            const multiplierY = displayedHeight / realHeight;
            this.drawRect(
                canvas,
                x * multiplierX,
                y * multiplierY,
                w * multiplierX,
                h * multiplierY
            )
        };
    }

    drawRect(canvas, x, y, w, h) {
        const rect = new fabric.Rect({
            left: x,
            top: y,
            originX: 'left',
            originY: 'top',
            width: w,
            height: h,
            angle: 0,
            fill: 'rgba(173,216,230,0.2)',
            transparentCorners: false,
            objectCaching: false
        });
        canvas.add(rect);
        return rect;
    }

    updateRect(x, y, w, h, updateFunction) {
        const img = document.querySelector("#img");
        const realWidth = img.naturalWidth;
        const displayedWidth = img.clientWidth;
        const realHeight = img.naturalHeight;
        const displayedHeight = img.clientHeight;
        const multiplierX = realWidth / displayedWidth;
        const multiplierY = realHeight / displayedHeight;
        updateFunction(
            Math.floor(x * multiplierX),
            Math.floor(y * multiplierY),
            Math.floor(w * multiplierX),
            Math.floor(h * multiplierY)
        )
    }

    render() {
        return (
            <div className="col s12" style={{
                'display': 'inline-block',
                'margin': '0 auto',
                'position': 'relative'
            }}>
                <img className="materialboxed col s12" alt="Camera Preview" id="img"
                     src={ApiService.getPreview(this.props.camera_id)}
                     style={{
                         "position": "absolute",
                         "z-index": 1
                     }}
                />
                <canvas className="col s12" id="canvas" style={{'position': 'relative', 'z-index': 20}}/>
            </div>
        );
    }
}

CameraPreview.propTypes = {
    camera_id: PropTypes.number.isRequired,
    x: PropTypes.number.isRequired,
    y: PropTypes.number.isRequired,
    width: PropTypes.number.isRequired,
    height: PropTypes.number.isRequired,
    updateCallback: PropTypes.func.isRequired
};

export default CameraPreview;