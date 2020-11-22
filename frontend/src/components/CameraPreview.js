import React, {Component} from 'react';
import "materialize-css/dist/css/materialize.min.css";
import PropTypes from 'prop-types'
import ApiService from "../app/Api";
import M from "materialize-css";
import {fabric} from 'fabric'


class CameraPreview extends Component {
    state = {};

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
        var canvas = new fabric.Canvas('c', {selection: false});

        var rect, isDown, origX, origY, height, width;

        canvas.on('mouse:down', function (o) {
            isDown = true;
            var pointer = canvas.getPointer(o.e);
            origX = pointer.x;
            origY = pointer.y;
            width = pointer.x - origX;
            height = pointer.y - origY;
            rect = new fabric.Rect({
                left: origX,
                top: origY,
                originX: 'left',
                originY: 'top',
                width: width,
                height: height,
                angle: 0,
                fill: 'rgba(173,216,230,0.2)',
                transparentCorners: false
            });
            canvas.clear();
            canvas.add(rect);
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
            <div style={{
                'display': 'inline-block',
                'width': '1280px',
                'height': '720px',
                'margin': '0 auto',
                'position': 'relative'
            }}>
                <img className="materialboxed" alt="" id="img"
                     width="1280" height="720" style={{"position": "absolute", "z-index": 1}}
                     src={ApiService.getPreview(this.props.camera_id)}/>
                <canvas id="c" width="1280" height="720" style={{'position': 'relative', 'z-index': 20}}>
                </canvas>
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